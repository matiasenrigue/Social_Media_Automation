import os
import csv
from datetime import datetime, timedelta
import pytz
from typing import Optional


"""
Scripts to manage content:
- create and manage upload schedules
"""



def check_or_create_schedule(social_media: str, Influencer: object) -> None:

    """
    Function that performs the following tasks for each influencer's schedule:

    - Ensures the following 91 days include:
        - Dates on which the influencer will upload videos (frequency varies according to each influencer's strategy)
    - Deletes past schedules
    - Preserves already filled schedules
    - If there is no schedule file for an influencer (new influencer), creates it
    
    Args:
        social_media (str): Name of the social network for which the schedule is made, now always YT
        Influencer (obj): Influencer object from which the desired dates are obtained
    """

    management_folder = os.path.join("..", "..", "a_Management")
    os.makedirs(management_folder, exist_ok=True)
    
    schedule_path = os.path.join("..", "..", "a_Management", f"calendar_{social_media}.csv")
    now_utc = datetime.now(pytz.utc)
    
    print(now_utc)
    
    upload_days_influencer = Influencer.upload_Days()

    # Create a set with all the expected dates and times
    expected_dates = set()
    for i in range(91):  # The next 91 days including today
        date = now_utc + timedelta(days=i)
        
        # 4 uploads a week, leaving days off.
        if date.weekday() in upload_days_influencer:
            hours = ['19:00']

            for hour in hours:
                date_time = datetime.strptime(date.strftime(f"%Y-%m-%d") + "T" + hour + ":00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
                date_time_str = date_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                # Verify the date and time are in the future before adding
                if date_time > now_utc:
                    expected_dates.add(date_time_str)

    try:
        with open(schedule_path, mode='r+', newline='') as file:
            reader = csv.DictReader(file)
            existing_rows = {row['date']: row for row in reader if datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc) >= now_utc}

            # Add missing rows
            for expected_date in expected_dates:
                if expected_date not in existing_rows:
                    existing_rows[expected_date] = {'date': expected_date, 'title': '', 'youtube': '', 'tiktok': ''}

            # Write updated rows to the file
            file.seek(0)
            file.truncate()
            writer = csv.DictWriter(file, fieldnames=['date', 'title', 'youtube', 'tiktok'])
            writer.writeheader()
            for row in sorted(existing_rows.values(), key=lambda x: x['date']):
                writer.writerow(row)

    except FileNotFoundError:
        # If the file doesn't exist, create it with all expected dates
        with open(schedule_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'title', 'youtube', 'tiktok'])
            writer.writeheader()
            for expected_date in sorted(expected_dates):
                writer.writerow({'date': expected_date, 'title': '', 'youtube': '', 'tiktok': ''})






def find_next_available_date(social_media: str) -> Optional[str]:
    """
    Function to find the next available date in the schedule:
    - That is, the most recent date without a "title" column filled

    Args:
        social_media (str): Name of the social network.

    Returns:
        Optional[str]: Next available date if it exists, None otherwise.
    """
    schedule_path = os.path.join("..", "..", "a_Management", f"calendar_{social_media}.csv")
    next_available_date = None

    try:
        with open(schedule_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            # Look for the next available date where the title column is empty
            for row in reader:
                if not row['title']:  # If the title column is empty
                    next_available_date = row['date']
                    break  # Exit the loop once the first available date is found

        if next_available_date:
            # Write the date to date.txt
            with open("date.txt", "w") as date_file:
                date_file.write(next_available_date)

    except FileNotFoundError:
        print(f"The file calendar_{social_media}.csv does not exist.")








def update_schedule_with_files(social_media: str) -> None:
    """
    Function to effectively enter a video into the schedule when it has been uploaded.

    Args:
        social_media (str): Name of the social network.
    """

    schedule_path = os.path.join("..", "..", "a_Management", f"calendar_{social_media}.csv")
    try:
        # Read the selected date
        with open("date.txt", "r") as date_file:
            selected_date = date_file.read().strip()

        # Read the contents of title.txt if it exists
        title = open("title.txt", "r").read().strip() if os.path.exists("title.txt") else None

        # Verify the existence of youtube.txt and tiktok.txt
        youtube_ok = "OK" if os.path.exists("youtube.txt") else None
        tiktok_ok = "OK" if os.path.exists("tiktok.txt") else None

        # Read and update the schedule
        updated_rows = []
        with open(schedule_path, mode='r+', newline='') as file:
            reader = list(csv.DictReader(file))
            for row in reader:
                if row['date'] == selected_date:
                    if title:
                        row['title'] = title
                    if youtube_ok:
                        row['youtube'] = youtube_ok
                    if tiktok_ok:
                        row['tiktok'] = tiktok_ok
                updated_rows.append(row)

            file.seek(0)
            file.truncate()
            writer = csv.DictWriter(file, fieldnames=['date', 'title', 'youtube', 'tiktok'])
            writer.writeheader()
            writer.writerows(updated_rows)

    except FileNotFoundError:
        print("The necessary file does not exist.")
