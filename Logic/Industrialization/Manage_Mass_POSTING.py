from Influencers.Manage_Influencers import active_posting_influencers
from Logic.Tools.Folders import select_multiple_folders, update_folder_status, set_folder_name, delete_state0_folders
import os
import time

# Configure logging
import logging
logging.basicConfig(filename='/Users/matias/code/SocialMedia/cron.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')




def bulk_approve(forced: str = "") -> None:
    """
    Function to approve multiple videos in bulk.

    :param forced: 
        - If not empty, it will force the approval of the videos.
        - If empty, it will only approve videos that meet the required characteristics for approval.
    :return: None
    """
    from Logic.Videos.Thumbnails_Shorts import save_unique_configuration, prepare_folder_for_unique_configuration

    base_wd = os.getcwd()
    influencer_list = active_posting_influencers()

    def workflow_voice_to_video(Influencer: object, influencer_wd: str) -> None:
        """
        This mass production function works from outside the folder.

        :param Influencer: Influencer object.
        :param influencer_wd: Working directory of the influencer.
        :return: None
        """
        valid_states = [4, 5, "X"]
        folder_list = select_multiple_folders(valid_states)
        outputs_wd = os.path.join(influencer_wd, "Outputs")

        for folder in folder_list:
            folder = os.path.join(outputs_wd, folder)
            
            if forced:  # If approval is forced, delete all thumbnails except one to trick the next code
                prepare_folder_for_unique_configuration(folder)
                
            action = save_unique_configuration(folder)

            if action:
                Influencer.get_keywords(folder)
                
                file_path = os.path.join(folder, "approved.txt")
                with open(file_path, 'w') as file:
                    file.write("Video approved")

                file_to_delete = os.path.join(folder, "denied.txt")  # Delete the file that marks this folder as to be re-edited if it exists
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)

                update_folder_status(folder)  # Update folder status after we have exited it just in case

    for Influencer in influencer_list:
        Influencer.get_correct_wd()
        influencer_wd = os.getcwd()
        workflow_voice_to_video(Influencer, influencer_wd)
        os.chdir(base_wd)





def upload_YT_bulk() -> None:
    """
    Function to ensure there is an internet connection before executing the video upload.
    If yes, it triggers mass video upload.
    :return: None
    """
    
    def check_internet() -> bool:
        """Checks if there is an internet connection."""
        import requests
        import time
        
        try:
            requests.get('http://google.com', timeout=5)
            return True
        except requests.ConnectionError:
            return False
    
    while True:
        if check_internet():
            logging.info("Internet is available: executing task")
            logic_upload_YT_bulk()
            break
        else:
            logging.info("No internet, trying again in 1 minute")
            time.sleep(60)





def logic_upload_YT_bulk() -> None:
    """
    Function to upload multiple YT videos at once.
    
    Note:
        - YouTube API marked my channel as Spam for uploading videos at the same time
        Solution:
            * Run script each time the computer starts (wait for wifi connection to upload videos)
                * (used to run at the same time every day)
                * basically it is running all the time
            * Add longer random time intervals between uploads
                * (used to pause every 1 minute)
                * can be so long that it does not matter if 6 videos or less are uploaded per day
    
    Important:
        - On the computer, configure this code to run at startup, on mac it is done in "launchpad"
    """

    from Logic.Uploads.Uploading import post_one_video_multiple_times
    from Logic.Industrialization.Alert_Influencers import send_alerts
    from Logic.Tools.Folders import move_state7_folders, move_state8_folders
    from datetime import datetime
    import random
    import pytz

    base_wd = os.getcwd()
    influencer_list = active_posting_influencers()
    random.shuffle(influencer_list)  # No need to assign because it is modified in place
    
    now = datetime.now()
    logging.info(now.strftime("Code running on %Y-%m-%d at %Hh-%Mm-%Ss"))

    def upload_workflow(Influencer: object, influencer_wd: os.path) -> None:
        """
        This mass production function works from outside the folder.

        :param Influencer: Influencer object.
        :param influencer_wd: Working directory of the influencer.
        :return: None
        """
        # Prepare files to check if YT API daily limits have been reached
        california_timezone = pytz.timezone('America/Los_Angeles')  # YouTube API works with that time zone
        california_time = datetime.now(california_timezone)        
        logs_folder = os.path.join(influencer_wd, "z_logs_API_YT")
        os.makedirs(logs_folder, exist_ok=True)
        today_date = california_time.strftime("%Y-%m-%d")
        today_logs_folder = os.path.join(logs_folder, today_date)
        os.makedirs(today_logs_folder, exist_ok=True)
        logs_file = os.path.join(today_logs_folder, f"logs_{today_date}.txt")
        greeting = Influencer.Greet()

        # Check if YT API daily limits have been reached
        if not os.path.exists(logs_file):  # If the file does not exist: upload videos from that influencer, otherwise move to the next
            api_limit = post_one_video_multiple_times(Influencer)

            if api_limit:  # Prevent further uploads today to avoid spamming API after reaching the limit
                with open(logs_file, "w") as file:  # Creating this file prevents more influencer uploads in a day
                    file.write("Upload done for this influencer")
                logging.info(f"The influencer of {greeting} just received a 403 error for API overuse, no more videos will be uploaded until tomorrow")

        else:
            logging.info(f"The influencer of {greeting} will not try to upload more videos as they were already rejected")

    i = 0
    while i < 6:  # 6 is the maximum number of videos that can be uploaded per day
        
        logging.info(f"Upload round {i+1}")
        for Influencer in influencer_list:
            Influencer.get_correct_wd()
            influencer_wd = os.getcwd()
            
            outputs = os.path.join(os.getcwd(), "Outputs")  # Remove already uploaded videos from general view
            move_state7_folders(outputs)
            move_state8_folders(outputs)
            
            upload_workflow(Influencer, influencer_wd)
            send_alerts(Influencer, influencer_wd)  # Send alert to Telegram if I need to pay attention to something
            os.chdir(base_wd)
            
            if len(influencer_list) > 1:  # No need to wait if only one influencer is uploaded, it makes no sense
                random_delay = random.randint(60 * 5, 60 * 15)  # Introduce random script behavior waiting different times between influencers
                logging.info(f"Waiting {random_delay / 60:.2f} mins between influencer uploads")
                time.sleep(random_delay)  # wait between 5 mins and 15 mins between each influencer
        
        random_delay = random.randint(60 * 30, 60 * 100)  # Introduce random script behavior being able to upload videos at random times of the day
        logging.info(f"Waiting {random_delay / 60:.2f} mins to start the next upload round")
        time.sleep(random_delay)  # wait between 30 mins and 100 mins to upload another video
        
        i += 1


