import os
import asyncio
import telegram
import threading
from datetime import datetime
import random
import time
from Logic.Tools.Utils import wait_for_confirmation, open_folder, utc_to_spanish_time
from Logic.Tools.Folders import choose_folder, update_folder_status, select_multiple_folders, move_state8_folders
from Logic.Tools import params
from Logic.Uploads.Youtube_API import upload_video_YT
from Logic.Uploads.Calendar import check_or_create_schedule, find_next_available_date, update_schedule_with_files

from Logic.Uploads.Telegram_Messages import send_telegram


"""
This script manages the process of verifying, scheduling, and uploading videos for influencers. 
It includes functions for verifying necessary files, uploading videos to YouTube, 
and updating the schedule with details of uploaded videos.

Functions:

1. verify_files:
    - Verifies the existence of necessary files before uploading a video.
    - Prompts the user to correct any missing files and re-verifies until all required files are present.
    - (Only useful if you are supervising content)

2. upload_youtube:
    - Checks if a video has already been uploaded to YouTube.
    - Uploads the video if it hasn't been uploaded yet and returns the status.

3. confirmation_message:
    - Logs a confirmation message with details of the uploaded video, including title and upload date.

4. post_one_video_multiple_times:
    - Executes the process of uploading a video multiple times for an influencer.
    - Manages folders in a specific state and updates the schedule accordingly.

5. post_ONE_SINGLE_video:
    - Executes the process of uploading a single video for an influencer.
    - Manages folders in a specific state and updates the schedule accordingly.
"""



# Configure logging
import logging
logging.basicConfig(filename='/Users/matias/code/SocialMedia/cron.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')




def verify_files() -> None:

    """
    Function to verify that all these files exist, avoid uploading if they do not exist
    """

    required_files = [
        "vertical_thumbnail.jpg",
        "footer.txt",
        "title.txt",
        "keywords.txt",
        "date.txt"
        ]

    all_exist = True

    for file in required_files:
        if os.path.isfile(file):
            print(f"The file {file} exists ✅")
        else:
            print(f"⚠️ The file {file} does not exist ❌")
            all_exist = False

    print("\n")

    if not all_exist:
        time.sleep(3) # give user time to read what is missing
        open_folder() # See which ones are missing
        wait_for_confirmation() # Confirm that change has been made
        verify_files() # Call again





def upload_youtube() -> str:
    """
    Function to upload video to Youtube.
    
    - Check if the Youtube.txt file exists.
        -If it does not exist, upload (and create it upon upload)
        -If it exists, it means it has already been uploaded, and do not upload
    """

    def video_has_been_published() -> bool:
        return os.path.exists("youtube.txt")

    if not video_has_been_published(): # Video has not been uploaded yet, so upload it
        print("\n🔄 Publishing content on youtube...\n")
        return "Pending"

    else:  # Video has already been uploaded: Do not upload
        print("\n⚠️ The file has already been uploaded to youtube.\n")
        return ""





def confirmation_message() -> None:
    """
    Information to have in the logs
    """

    title = open("title.txt", "r").read().strip()
    utc_date = open("date.txt", "r").read().strip()
    date = utc_to_spanish_time(utc_date)
    
    string = "\n\n _____________________________ \n "
    string += f"\nThe video has been uploaded: {title}"
    string += f"\n📅 On the date: {date}"
    string += "\n\n _____________________________ \n "

    print(string)
    logging.info(string)







def post_one_video_multiple_times(Influencer: object) -> str:
    """
    Function to execute all the logic of the code to upload a video multiple times.

    Parameters:
        - Influencer: Object containing the credentials and data of the influencer.

    It applies to folders in the following states:
    6. APPROVED: With script, voice, subtitles, video, and thumbnail.
    """
        
    valid_states = [6]
    folders = select_multiple_folders(valid_states) # this function will access that new folder
    base_cwd = os.path.join(os.getcwd(), "Outputs")

    api_keys_Youtube = Influencer.get_credentials()
    (client_secrets_path, oauth_storage_path) = api_keys_Youtube


    if folders: # avoid code collapse if there are no videos to upload

        folder = folders[0]
        try: # avoid errors from one video stopping the code

            folder_directory = os.path.join(base_cwd, folder)
            os.chdir(folder_directory)
            
            check_or_create_schedule("YT", Influencer)  # Edit CSV to ensure dates are correct (Or create if it does not exist)
            find_next_available_date("YT")  # Find the next available date

            pending_yt = upload_youtube()
            if pending_yt:
                success = upload_video_YT(client_secrets_path, oauth_storage_path, Influencer)

            if success == 1: # add the title to the date only if the video has been successfully uploaded
                update_schedule_with_files("YT")
                confirmation_message()
                os.chdir(base_cwd)
                update_folder_status(folder_directory)
                return None
                
            elif success == 0:
                logging.info("\n6 videos have already been uploaded today for this influencer\n")
                os.chdir(base_cwd)
                return "NO MORE"


        except Exception as e:
            print(f"There was an error uploading the contents of: {folder}.\n Error: {e}")
            logging.info(f"There was an error uploading the contents of: {folder}.\n Error: {e}")
            
            name_influencer = Influencer.greet()
            error_message = f"Token is likely to be expired or revoked\nReal Error Message:\n{str(e)}"
            send_telegram(f"⚠️⚠️ POSSIBLE EXPIRED TOKEN\nThere was an error: for influencer {name_influencer}\n{error_message}")
            return 0
          
                                
    else: # If there are no videos to upload do not try to upload, it makes no sense
        return "NO MORE"
        






def post_ONE_SINGLE_video(Influencer:object) -> None:
    """
    Function to execute all the logic of the code to upload a single video.

    Parameters:
        - Influencer: Object containing the credentials and data of the influencer.

    It applies to folders in the following states:
    6. APPROVED: With script, voice, subtitles, video, and thumbnail.
    """
    import pytz
    valid_states = [6]
    folders = select_multiple_folders(valid_states)
    influencer_wd = os.getcwd()
    base_cwd = os.path.join(influencer_wd, "Outputs")

    api_keys_Youtube = Influencer.get_credentials()
    (client_secrets_path, oauth_storage_path) = api_keys_Youtube
    
    # Get information about log folder to create / delete if necessary
    california_timezone = pytz.timezone('America/Los_Angeles') # Youtube API works with this timezone
    california_datetime = datetime.now(california_timezone)        
    today_date = california_datetime.strftime("%Y-%m-%d")
    logs_folder = os.path.join(influencer_wd, "z_logs_API_YT")
    os.makedirs(logs_folder, exist_ok=True)
    today_logs_folder = os.path.join(logs_folder, today_date)
    os.makedirs(today_logs_folder, exist_ok=True)
    logs_file = os.path.join(today_logs_folder, f"logs_{today_date}.txt")
    
    
    if folders: # avoid code collapse if there are no videos to upload

        folder = folders[0]
        folder_directory = os.path.join(base_cwd, folder)
        os.chdir(folder_directory)
        
        check_or_create_schedule("YT", Influencer)  # Edit CSV to ensure dates are correct (Or create if it does not exist)
        find_next_available_date("YT")  # Find the next available date

        verify_files()

        pending_yt = upload_youtube()

        if pending_yt:
            success = upload_video_YT(client_secrets_path, oauth_storage_path, Influencer)

        if success == 1: # add the title to the date only if the video has been successfully uploaded
            update_schedule_with_files("YT")
            confirmation_message()
            os.chdir(base_cwd)
            update_folder_status(folder_directory)
            
            if os.path.exists(logs_file): # Delete log file only if it exists --> allow influencer uploads today
                os.remove(logs_file)
            
        
        elif success == 0:
            with open(logs_file, "w") as file: # When this file is created, no more influencer uploads are attempted in a day
                file.write("Upload done for this influencer")
            
        
