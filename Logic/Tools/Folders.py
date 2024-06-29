import os
from datetime import datetime
from io import BytesIO
import re
import time
import os
import shutil
from typing import List, Optional, Tuple


"""
Script with different functions to handle folders:

    Creation and Organization of Folders:
        - template_folders: Creates a folder structure based on an ID and other parameters.
        - set_folder_name: Renames a folder based on a title file.

    Selection and Filtering of Folders:
        - choose_folder: Allows the user to select a folder based on valid states.
        - select_multiple_folders: Selects multiple folders that match valid states.

    Folder Status Update:
        - update_folder_status: Updates the status of a folder based on the files present.

    Working Directory Management:
        - get_correct_wd: Ensures that the script runs from the correct directory.
        - get_social_media_wd: Ensures that the script runs from the "SocialMedia" directory.

    Specific Functions for English Influencers:
        - get_reference_wd_folders: Gets reference folders to translate into English.
        - copy_reference_folder: Copies reference folders to English.

    Deletion and Movement of Folders:
        - delete_state0_folders: Deletes folders with state 'State0'.
        - delete_state1_folders: Deletes folders with state 'State1'.
        - move_state8_folders: Moves folders with state 'State8' to a specific folder.
        - move_state7_folders: Moves folders with state 'State7' to a specific folder.
"""


def template_folders(id: str) -> str:
    """
    Creates a template of folders for a specific account.

    Args:
        id (str): Unique identifier of the topic.

    Returns:
        str: Path of the created folder.

    Template under which all folders of each account will be created:
    "ID-##_State_Date_Title"

    --> State being the state the video is in
    """

    # saving_path = os.path.join(os.getcwd(), 'Outputs', 'publicaciones')
    today_date = datetime.now().strftime("%Y-%m-%d")
    saving_path = os.path.join(os.getcwd(), "Outputs")
    os.makedirs(saving_path, exist_ok=True)

    # List all folders in the target directory
    existing_folders = [folder for folder in os.listdir(saving_path) if os.path.isdir(os.path.join(saving_path, folder))]

    # Find the highest existing index for today's date and the given team
    max_index = 0
    for folder in existing_folders:
        # if folder.startswith(f"{socialmedia}_{today_date}_{team}_"):
        # FCB-14_E9_Title_Date
        unique_num = folder.split('_')[0]
        folder_index = int(unique_num.split('-')[1])
        if folder_index > max_index:
            max_index = folder_index

    # Create the new folder with the next index
    state = "State0"  # Empty folder
    title = "NoTitle"
    new_index = max_index + 1
    folder_name = f"{id}-{new_index}_{state}_{today_date}_{title}"
    date_folder = os.path.join(saving_path, folder_name)
    os.makedirs(date_folder, exist_ok=True)

    return date_folder





def set_folder_name(folder_path: str) -> str:
    """
    Renames a folder using the contents of a title file.

    Args:
        folder_path (str): Path of the folder to rename.

    Returns:
        str: New path of the renamed folder.
    """
    import unidecode

    rest_time = 2

    title_file = os.path.join(folder_path, 'title.txt')

    # Get the title of the folder
    try:
        with open(title_file, 'r', encoding='utf-8') as file:
            dirty_title = file.read()
            title_no_accents = unidecode.unidecode(dirty_title)
            title = re.sub(r"[^a-zA-Z0-9 \-_]", "", title_no_accents)

    except Exception as e:
        print(f"\nError adding title to the folder: {e}\n")
        title = "NoTitle"

    name_parts = folder_path.split('_')
    if len(name_parts) > 1:
        name_parts[-1] = f"{title}"  # Assuming the state position is the third in the pattern
        new_folder_path = "_".join(name_parts)
    else:
        new_folder_path = folder_path

    os.rename(folder_path, new_folder_path)  # add a time.sleep in between to allow other functions to adapt to the change
    time.sleep(rest_time)

    return new_folder_path




def choose_folder(valid_states: List[int]) -> os.path:
    """
    Searches for folders that match the specified states and allows the user to select one.
    IMPORTANT!! Must be in the correct directory
    
    Args:
        valid_states (List[int]): List of valid states (for example, [3, 4, 5, 6]).

    Returns:
        os.path: Path of the selected folder.
    """
            
    saving_path = os.path.join(os.getcwd(), "Outputs")
    existing_folders = [folder for folder in os.listdir(saving_path) if os.path.isdir(os.path.join(saving_path, folder))]

    folders_dict = {}  # {id}-{number}_{state}_{today_date}_{title}
    for folder in existing_folders:
        parts = folder.split('_')
        state = parts[1]
        id_raw = parts[0]  # ANI-25
        _, id = id_raw.split("-")
        state_num = int(state.replace("State", ""))
        if state_num in valid_states:
            folders_dict[int(id)] = folder  # add folder by ID to the folders dictionary

    # Print the found folders with the specified format
    print("\n📂 Folders found:")
    for id in sorted(folders_dict.keys()):
        folder = folders_dict[id]
        parts = folder.split('_')  # {id}-{number}_{state}_{today_date}_{title}
        state, date, title = parts[1], parts[2], "_".join(parts[3:])
        id = parts[0].split('-')[1]
        print(f"id: {id} : {state} | Title: {title} | Date: {date}")

    # Allow the user to select a folder
    while True:
        try:
            selection = int(input("\n📂 Select the folder ID: "))
            selected_folder = folders_dict[selection]
            selected_folder_path = os.path.join(saving_path, selected_folder)
            return selected_folder_path
        except:
            pass








def select_multiple_folders(valid_states: List[int], base_directory: str = "") -> List[str]:
    """
    Searches for folders that match the specified states and allows the user to select one.
    IMPORTANT!! Must be in the correct directory

    Args:
        - valid_states (list): List of valid states (for example, [3, 4, 5, 6]).
        - base_directory (directory): if accessing from another reference directory, use that as reference,
            if not, use cwd
    
    Returns:
        List[str]: List of paths of the selected folders.

    DIFFERENCE WITH THE PREVIOUS:
    Returns a list of folders to be able to loop through
    """

    if base_directory:
        saving_path = os.path.join(base_directory, "Outputs")

    else:
        saving_path = os.path.join(os.getcwd(), "Outputs")

    existing_folders = [folder for folder in os.listdir(saving_path) if os.path.isdir(os.path.join(saving_path, folder))]
    folders_info = []  # Store tuples of (ID, folder name)

    for folder in existing_folders:
        parts = folder.split('_')
        id_part = parts[0].split('-')[1]
        state = parts[1]
        state_num = int(state.replace("State", ""))

        if state_num in valid_states:
            id = int(id_part)  # Convert ID to integer for numerical sorting
            folders_info.append((id, folder))

    # Sort the folders by ID
    folders_info.sort(key=lambda x: x[0])

    # Return only the names of the folders, sorted by ID
    folders_sorted_by_id = [name for id, name in folders_info]

    return folders_sorted_by_id






def update_folder_status(folder_path: os.path) -> os.path:

    rest_time = 2  # Rest time before renaming in seconds

    """
    Updates the status of a folder based on the files present in it, respecting dependencies between states.
    
    Args:
        folder_path (path): Path of the folder to evaluate.

    Returns:
        path: New path of the folder with the updated status.

    Rules for status update:
    - If "text.txt" exists, update to State 1.
    - If "audios/labs.mp3" exists, update to State 2.
    - If "transcription_flat.json" exists, update to State 3.
    - If "Video.mp4" exists, update to State 4.
    - If "thumbnail_vertical.jpg" exists, update to State 5.
    - If "approved.txt" exists, update to State 6.
    - If "Instagram.txt" or "Youtube.txt" exists, update to State 7.
    - If both "Instagram.txt" and "Youtube.txt" exist, update to State 8.
    - If "english.txt" exists, update to State 9.

    The function returns the new name of the folder with the updated status.
    """
    state = 0
    files = os.listdir(folder_path)
    audios_exist = os.path.exists(os.path.join(folder_path, "audios"))
    audios = os.listdir(os.path.join(folder_path, "audios")) if audios_exist else []

    # Rules for status update
    if "denied.txt" in files:
        state = "X"

    else:
        if "text.txt" in files:
            state = 1
        if "labs.mp3" in audios:
            state = max(state, 2)
        if state >= 2 and "flattened_transcription.json" in files:
            state = 3
        # if state >= 3 and "Video.mp4" in files:
        #     state = 4
        if state >= 3 and any(file.endswith(".mp4") for file in files):
            state = 4
        if state >= 4 and "thumbnail_vertical.jpg" in files:
            state = 5
        if state >= 5 and "approved.txt" in files:
            state = 6
        if state >= 6 and "youtube.txt" in files:
            state = 7
        if state >= 7 and "tiktok.txt" in files:
            state = 8
        # if state >= 6:
        #     if "tiktok.txt" in files or "youtube.txt" in files:
        #         state = 7
        #         if "tiktok.txt" in files and "youtube.txt" in files:
        #             state = 8
        if state >= 8 and "english.txt" in files:
            state = 9

    # FCB-1_State1_State4_NoTitle
    # FCB-2_State1_2024-02-08_NoTitle
    # Reconstruct the folder name with the new state
    name_parts = folder_path.split('_')
    if len(name_parts) > 1:
        name_parts[1] = f"State{state}"  # Assuming the state position is the third in the pattern
        new_folder_path = "_".join(name_parts)
    else:
        new_folder_path = folder_path

    # Rename the folder in the file system
    print("\n⌛ Wait 4 seconds to rename folder")
    time.sleep(rest_time)
    os.rename(folder_path, new_folder_path)  # add a time.sleep in between to allow other functions to adapt to the change
    time.sleep(rest_time)

    return new_folder_path







def get_correct_wd(desired_directory: str) -> None:
    """
    Ensures that the script runs from the correct directory: the root folder of each influencer

    Args:
        desired_directory (str): Name of the desired directory.
    """

    # Check if we are already in the desired directory
    if os.path.basename(os.getcwd()) != desired_directory:
        # Change to the directory if we are not already in it
        try:
            os.chdir(desired_directory)
            print(f"\n📂 Changed to directory: {desired_directory}\n")
        except FileNotFoundError:
            print(f"\n📂 The directory {desired_directory} does not exist in the current location.\n")
    else:
        pass
        #print(f"\n📂 You are already in the directory: {desired_directory}\n")






def get_social_media_wd() -> None:
    """
    Ensures that the script runs from the "SocialMedia" directory.
    Attempts to change to the "SocialMedia" directory, whether it is forward or backward in the path.
    """

    desired_directory = "SocialMediaGitHub"
    current_directory = os.getcwd()

    if os.path.basename(current_directory) == desired_directory:
        pass
        # print(f"\n📂 You are already in the directory: {desired_directory}\n")
        return

    # Search backward (up the directory structure)
    path_parts = current_directory.split(os.sep)
    for i in range(len(path_parts), 0, -1):
        potential_path = os.sep.join(path_parts[:i])
        if os.path.basename(potential_path) == desired_directory:
            os.chdir(potential_path)
            print(f"\n📂 Changed to directory: {potential_path}\n")
            return

    # Search forward (down the directory structure)
    for root, dirs, files in os.walk(current_directory):
        if desired_directory in dirs:
            os.chdir(os.path.join(root, desired_directory))
            print(f"\n📂 Changed to directory: {os.path.join(root, desired_directory)}\n")
            return
        break  # Avoid searching beyond the immediate subdirectory level

    print(f"\n📂 The directory {desired_directory} was not found forward or backward from the current location.\n")





#### FUNCTIONS FOR ENGLISH INFLUENCERS


def get_reference_wd_folders(desired_directory: str) -> List[str]:
    """
    Gets the reference folders (from the Spanish influencer) to translate into English.

    Args:
        desired_directory (str): Name of the desired directory.

    Returns:
        List[str]: List of folders without the "english.txt" file.
    """

    print("\n🔄 Checking list of folders to translate into English...")

    # The reference path of the copied influencer and its Saving Path
    reference_path = os.path.join(os.getcwd(), "..", desired_directory)
    reference_saving_path = os.path.join(reference_path, "Outputs")

    # Take all folders with status: 6 (approved), 7, and 8 (Youtube and/or Tiktok)
    reference_folders = select_multiple_folders(valid_states=[6, 7, 8], base_directory=reference_saving_path)

    # Filter those that do or do not have the english.txt file (If they don't have it, it means they haven't been translated yet)
    folders_without_english_file = []
    for folder in reference_folders:
        file_path = os.path.join(folder, "english.txt")
        if not os.path.exists(file_path):
            folders_without_english_file.append(folder)

    return folders_without_english_file





def copy_reference_folder(folder_list: List[str]) -> List[Tuple[str, str]]:

    """
    Function for English influencers:
    Input: list of folders (access paths)
        Each folder will have a similar pattern to this: "FCB-6_State7_2024-02-09_El General Flick al Rescate del Bara El Nuevo Guardiola"
        Copy each folder from that list in the current directory as follows:
            - Name: Add a prefix "ENG-", change the state to 5, and put today's date: "ENG-FCB-6_State5_TodayDate_Title"
            - Copy "config" and "images" folders with all their files, and from the "Thumbnails" folder only the "Original.jpg" file
            - Copy "text.txt" files

    Output List that stores tuples of ( copy_path , original_path ):
        to be able to loop through the copied folder, and then mark the original with english.txt
    """
    print("\n🔄 Copying folders to English...\n")
    # Get today's date in year-month-day format
    today_date = datetime.now().strftime("%Y-%m-%d")

    copy_original_list = []  # List to store tuples of ( copy_path , original_path )

    for folder in folder_list:
        # Extract the folder name and modify it according to the specifications
        folder_name = os.path.basename(folder)
        name_parts = folder_name.split("_")

        # Change the state to 5 and add "ENG-" prefix to the name
        name_parts[0] = "ENG-" + name_parts[0]
        name_parts[1] = "State0"
        name_parts[2] = today_date  # Replace the date with today's date

        # Reconstruct the name with the modifications
        new_folder_name = "_".join(name_parts)

        # Create the new folder in the current directory
        new_destination_folder = os.path.join(os.getcwd(), "Outputs", new_folder_name)
        os.makedirs(new_destination_folder, exist_ok=True)

        # Copy the "config" and "images" folders completely
        for sub_folder in ["config", "images"]:
            sub_folder_path = os.path.join(folder, sub_folder)
            if os.path.exists(sub_folder_path):
                shutil.copytree(sub_folder_path, os.path.join(new_destination_folder, sub_folder), dirs_exist_ok=True)

        # Copy only "Original.jpg" from the "Thumbnails" folder
        original_thumbnail_path = os.path.join(folder, "Thumbnails", "Original.jpg")
        if os.path.exists(original_thumbnail_path):
            thumbnails_destination = os.path.join(new_destination_folder, "Thumbnails")
            os.makedirs(thumbnails_destination, exist_ok=True)
            shutil.copy(original_thumbnail_path, thumbnails_destination)

        # Copy the "text.txt" file if it exists
        text_txt_path = os.path.join(folder, "text.txt")
        if os.path.exists(text_txt_path):
            shutil.copy(text_txt_path, new_destination_folder)

        copy_original_list.append((new_destination_folder, folder))

        print(f"📂 Folder: {new_folder_name} created")

    return copy_original_list




### DELETION OF USELESS FOLDERS

def delete_state0_folders(path: os.path) -> None:
    """
    Deletes folders with state 'State0'.

    Args:
        path (str): Path of the directory to search for folders.
    """
    # Verify if the path exists
    if not os.path.isdir(path):
        print("\nThe specified path does not exist.")
        return

    # List all items in the path
    for folder_name in os.listdir(path):
        # Build the complete path to the item
        complete_path = os.path.join(path, folder_name)

        # Verify if it is a folder and contains 'State0' in the name
        if os.path.isdir(complete_path) and 'State0' in folder_name:
            # Delete the folder
            shutil.rmtree(complete_path)
            print(f"\nDeleted folder: {folder_name}")





def delete_state1_folders(path: os.path) -> None:
    """
    Deletes folders with state 'State1'.

    Args:
        path (str): Path of the directory to search for folders.
    """
    # Verify if the path exists
    if not os.path.isdir(path):
        print("\nThe specified path does not exist.")
        return

    # List all items in the path
    for folder_name in os.listdir(path):
        # Build the complete path to the item
        complete_path = os.path.join(path, folder_name)

        # Verify if it is a folder and contains 'State1' in the name
        if os.path.isdir(complete_path) and 'State1' in folder_name:
            # Delete the folder
            shutil.rmtree(complete_path)
            print(f"\nDeleted folder: {folder_name}")





def move_state8_folders(path: os.path) -> None:
    """
    Moves folders with state 'State8' to a specific folder.

    Args:
        path (str): Path of the directory to search for folders.
    """
    # Verify if the path exists
    if not os.path.isdir(path):
        print("\nThe specified path does not exist.")
        return

    destination_folder = os.path.join(path, "zID-0_State9_0000-00-00_uploaded videos not english")
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)


    # List all items in the path
    for folder_name in os.listdir(path):
        # Build the complete path to the item
        complete_path = os.path.join(path, folder_name)

        # Verify if it is a folder and contains 'State8' in the name
        if os.path.isdir(complete_path) and 'State8' in folder_name:
            complete_destination = os.path.join(destination_folder, folder_name)
            shutil.move(complete_path, complete_destination)






def move_state7_folders(path: os.path) -> None:
    """
    Moves folders with state 'State7' to a specific folder.

    Args:
        path (str): Path of the directory to search for folders.
    """
    # Verify if the path exists
    if not os.path.isdir(path):
        print("\nThe specified path does not exist.")
        return

    destination_folder = os.path.join(path, "zID-0_State9_0000-00-00_uploaded videos not english")
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)


    # List all items in the path
    for folder_name in os.listdir(path):
        # Build the complete path to the item
        complete_path = os.path.join(path, folder_name)

        # Verify if it is a folder and contains 'State7' in the name
        if os.path.isdir(complete_path) and 'State7' in folder_name:
            complete_destination = os.path.join(destination_folder, folder_name)
            shutil.move(complete_path, complete_destination)
