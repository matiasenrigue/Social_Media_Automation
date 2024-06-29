import httplib2
import os
import random
import sys
import time
import json

from argparse import Namespace

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

"""
This script is designed to authenticate and upload videos to YouTube using the YouTube Data API v3.
It includes functions to authenticate the user, upload videos, and handle errors efficiently.

WARNING! Script is a bit complicated and I didn't know (or wanted to invest the time in) how to simplify it.
I took the one from Google's official documentation and adapted it to my use.
"""

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

# CLIENT_SECRETS_FILE = os.path.join("..", "..", "..", "Posting_APIs", "client_secrets.json") # "Posting_APIs/client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")




def get_authenticated_service(args: Namespace, client_secrets_path: str, oauth_storage_path: str) -> object:
    """
    Authenticates and returns an authorized YouTube service.
        Creates an instance that allows connecting to a YouTube account.
        
    Function defined like this to be able to send the paths of these files when calling.
    And in this way, be able to use this workflow for multiple accounts.

    Parameters:
    args (Namespace): Necessary arguments for authentication.
    client_secrets_path (str): Path to the client_secrets.json file that contains the OAuth 2.0 information.
    oauth_storage_path (str): Path to the OAuth 2.0 storage file.

    Return:
    Authenticated YouTube service object.
    """
    flow = flow_from_clientsecrets(client_secrets_path,  
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(oauth_storage_path)  
    # Previous code: # storage = Storage(os.path.join(os.path.dirname(__file__),"Youtube_API.py-oauth2.json"))

    credentials = storage.get()

    if credentials is None or credentials.invalid:   # Flow to rebuild credentials if they expire or are not created
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))





def initialize_upload(youtube: object, options: Namespace) -> object:
    """
    Initializes and manages the upload of a video to YouTube.

    Parameters:
    youtube (object): Authenticated YouTube service object --> Instance to connect to YT account.
    options (Namespace): Options for the video upload --> Specified upload configuration parameters.

    Return:
    Video upload request object.
    """
    tags = None
    if getattr(options, 'keywords', None):  # Use getattr to handle cases where keywords might not be defined
        tags = options.keywords.split(",")

    body = dict(
        snippet=dict(
            title=options.title,  
            description=options.description, 
            tags=tags,
            categoryId=options.category, 
            defaultLanguage=options.defaultLanguage,
            defaultAudioLanguage=options.defaultAudioLanguage 
        ),
        status=dict(
            publishAt=options.publishAt if hasattr(options, 'publishAt') else None,
            privacyStatus=options.privacyStatus  
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        # media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True)  # Use brackets to access 'file'
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request, youtube)





def upload_thumbnail(youtube: object, video_id: str, thumbnail_file: str) -> dict:
    """
    Uploads a thumbnail for a video on YouTube.

    Parameters:
    youtube (object): Authenticated YouTube service object.
    video_id (str): ID of the video to which the thumbnail will be assigned.
    thumbnail_file (str): Path to the thumbnail image file.

    Return:
    YouTube API response.
    """ 
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=thumbnail_file
    )
    response = request.execute()

    print("Thumbnail set for video id: %s" % video_id)
    return response

def resumable_upload(insert_request: object, youtube: object) -> int:
    """
    Implements an exponential backoff strategy to resume a failed upload.
    Uploads the data created in "initialize upload"

    Parameters:
    insert_request (object): Insert request object.
    youtube (object): Authenticated YouTube service object.

    Return:
    1 if the upload was successful, 0 in case of quota error.
    """
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    video_id = response['id']
                    print(f"Video id {video_id} was successfully uploaded.")
                    
                    # Code to upload thumbnail: ignored for now because it doesn't add anything to the videos and avoid overloading API
                    # try: # Upload the thumbnail (if possible) but if it fails, DO NOT stop the code logic
                    #     thumbnail_file = "miniatura_vertical.jpg"
                    #     upload_thumbnail(youtube, video_id, thumbnail_file)
                    # except Exception as e:
                    #     print(f"Error uploading thumbnail: \n{e}")
                        
                    with open("youtube.txt", "w") as file:
                        file.write(video_id)

                    return 1
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
                    
        except HttpError as e:
            if e.resp.status == 403:
                print(e)
                print("Error 403: Quota exceeded. Returning 0.")
                return 0  # Return 0 in case of error 403
            
            elif e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)

            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)





def upload_video_YT(client_secrets_path: str, oauth_storage_path: str, Influencer: object) -> int:
    """
    Uploads a video to YouTube using the provided configuration.
    This function is common to all influencers, each influencer sends their credentials to this function
        --> Once credentials are received, this function will treat everyone equally.

    Parameters:
    client_secrets_path (str): Path to the client_secrets.json file.
    oauth_storage_path (str): Path to the OAuth 2.0 storage file.
    Influencer (object): Influencer object to get the API data of the influencer.

    Return:
    1 if the upload was successful, 0 in case of error.
    """  
    import glob

    mp4_files = glob.glob('*.mp4') # Search for all .mp4 files in the current directory
    if len(mp4_files) == 1:
        file_path = mp4_files[0]  # Use the only .mp4 file found
    else:
        raise ValueError(f"Expected 1 .mp4 file, but found {len(mp4_files)}.")

    title = open("title.txt", "r").read().strip()
    description = open("description.txt", "r").read().strip()
    keywords = open("keywords.txt", "r").read().strip()
    privacyStatus = "private" # "public"  # Only private videos can be scheduled (But they become public when the date is met)
    publish_time = open("date.txt", "r").read().strip()  # Date in UTC time (UK) format YYYY-MM-DDThh:mm:ss.sZ (ex: 2024-02-13T19:00:00.000Z)
    
    # Video configuration Not necessary, because stored in variable --> file_path = "Video.mp4" 
    # Category configuration Not necessary, because stored in YT channel --> category = "---"
    category, language = Influencer.API_Params_YT()

    config_data = {
        "file": file_path,
        "title": title,
        "description": description,
        "keywords": keywords,
        "privacyStatus": privacyStatus,
        "publishAt": publish_time,
        "category": category, 
        "defaultLanguage": language, 
        "defaultAudioLanguage": language  
    }

    with open('config.json', 'w') as config_file:     # Serialize the dictionary to JSON and save it in a file
        json.dump(config_data, config_file, indent=4)

    if not os.path.exists(file_path): # Check if the video file exists
        exit("The video file does not exist.")

    with open('config.json', 'r') as config_file: # Create a dict to simulate args --> Load configuration from a JSON file
        args = json.load(config_file)

    # Argument configuration before calling get_authenticated_service
    args['noauth_local_webserver'] = False  # or True, if it matches your environment
    args['auth_host_port'] = [8080, 8090]  # Common ports for authentication
    args['auth_host_name'] = 'localhost'

    # Simulate obtaining authenticated service and uploading video
    args['logging_level'] = 'ERROR'  # Or any appropriate logging level
    args = Namespace(**args)
    youtube = get_authenticated_service(args, client_secrets_path, oauth_storage_path)
    try:
        return initialize_upload(youtube, args)

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
