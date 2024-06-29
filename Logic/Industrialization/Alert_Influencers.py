import os
import csv
from datetime import datetime, timedelta
import pytz
from typing import Optional
import time

from Logic.Uploads.Telegram_Messages import send_telegram
from Logic.Tools.Folders import select_multiple_folders


"""
Script to manage alerts and video production for influencers.
- Send alerts when more content needs to be produced.
- Calculate days of scheduled future content.
- Count videos ready to upload.

Functions:
    - send_alerts: Send alerts to influencers based on content status.
    - get_num_videos_ready: Get the number of videos ready to produce.
    - get_num_days_future_content: Calculate the number of days of scheduled content.
"""



def send_alerts(Influencer: object, influencer_wd: os.path) -> None:
    """
    Function to send messages to influencers if they need to be alerted to produce or schedule more videos in the future.

    Args:
        Influencer (object): Object representing the influencer, with a 'Greet' method.
        influencer_wd (str): Path to the influencer's working directory.
    """
    
    num_days_future_content = get_num_days_future_content()
    num_videos_ready_to_upload = get_num_videos_ready()
    name_influencer = Influencer.greet()
    
    if num_days_future_content < 15:  # Change to 5 once the alert has been received outside of trial ( = it works )
        
        message = f"⚠️⚠️ NEED TO UPLOAD VIDEOS ⚠️⚠️\nOnly {str(num_days_future_content)} days in the future with scheduled videos\nFor the Influencer {name_influencer}"
        send_telegram(message)
        time.sleep(10)
        print(message)
    
    elif num_days_future_content < 10 and num_videos_ready_to_upload < 3:
        
        message = f"""
        ⚠️⚠️ NEED TO PRODUCE VIDEOS ⚠️⚠️
        Only {str(num_videos_ready_to_upload)} videos ready 
        Only {str(num_days_future_content)} days in the future with scheduled videos
        For the Influencer {name_influencer}
        """
        clean_message = '\n'.join(line.strip() for line in message.split('\n'))
        send_telegram(clean_message)
        time.sleep(10)
        print(clean_message)





def get_num_videos_ready() -> int:
    """
    Function to return the number of videos in status 6, i.e., videos ready to produce.

    Returns:
        int: Number of videos ready to produce.
    """
    
    video_list = select_multiple_folders([6])
    
    if video_list:
        
        num_videos_ready = len(video_list)
        return num_videos_ready
    
    else:
        return 0 





def get_num_days_future_content() -> int:
    """
    Function to find the last occupied date in the calendar and calculate
    the difference in days between that date and the current date.

    Returns:
        int: Number of days between the last occupied date and today. 0 if there are no occupied dates.
    """
    social_media = "YT"
    calendar_path = os.path.join("a_Management", f"calendar_{social_media}.csv")
    last_occupied_date = None 
    
    try:
        with open(calendar_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            # Find the last occupied date where the title column is not empty
            for row in reader:
                if row['title']:  # If the title column is not empty
                    last_occupied_date = row['date']

        if last_occupied_date:
            last_occupied_date_dt = datetime.strptime(last_occupied_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            current_date = datetime.now()
            days_difference = (last_occupied_date_dt - current_date).days
            return days_difference
        else:
            return 0

    except FileNotFoundError:
        print(f"The file calendar_{social_media}.csv does not exist.")
        return 0
    except Exception as e:
        print(f"Error processing the file: {e}")
        return 0
