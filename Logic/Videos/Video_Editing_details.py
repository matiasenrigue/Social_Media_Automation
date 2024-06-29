import os
from datetime import datetime
from Logic.Tools.Folders import choose_folder, update_folder_status, set_folder_name, delete_state0_folders
from Logic.Tools.Utils import open_folder
import time


"""
Script to allow editing videos in specific parts

Idea: Mass production works at a crazy pace; this script is useful in case you want to review the produced content and have the option to correct only a specific part of the video
"""


def show_menu() -> str:
    """
    Function to show the menu to the user and let them choose what they want to do.

    Returns:
        str: Option chosen by the user.
    """
    sep = "-"
    print(f"\n {sep*10} \n🔨 Available options:\n")
    print('"voice". Record audio')
    print('"correct". Record corrected audio')
    print("1. Audio (audio_editing)")
    print("2. Subtitles (get_subtitles)")
    print("3. Correct Subtitles (correct_subtitles)")
    print("4. Video (video_editing)")
    print("5. Exit")
    option = input("\n👉 Enter the number of the action you want to perform: ")
    return option




def process_option(folder: os.path, Influencer: object) -> bool:
    """
    Function for the user to choose.

    Args:
        folder (str): Path to the current folder.
        Influencer (object): Object with methods to perform various actions (e.g., record voice).

    Returns:
        bool: True if the process continues, False if the program exits.
    """
    option = show_menu()

    if option == "1":
        from Logic.Voiceover.Audio_Editing import audio_editing
        audio_editing(Influencer)
        process_option(folder, Influencer)  # recursion

    elif option == "2":
        from Logic.Voiceover.Subtitles import get_subtitles
        get_subtitles()
        folder = update_level(folder, Influencer)  # this also calls the function recursively at the end

    elif option == "3":
        from Logic.Voiceover.Subtitles import correct_subtitles
        correct_subtitles()
        time.sleep(3)
        open_folder()
        process_option(folder, Influencer)  # recursion

    elif option == "4":
        from Logic.Videos.Video_Recording import video_editing_YT
        video_editing_YT()
        folder = update_level(folder, Influencer)  # indirect recursion

    elif option == "voice":
        from Logic.Voiceover.Subtitles import phonetic_correction
        from Logic.Videos.Script_Logic import treat_script
        from Logic.Voiceover.Narration import audio_recording
        treat_script()
        folder = set_folder_name(folder)
        phonetic_correction()
        audio_recording(Influencer)
        folder = update_level(folder, Influencer)  # indirect recursion

    elif option == "correct":
        from Logic.Voiceover.Narration import re_record_audio
        re_record_audio(Influencer)
        process_option(folder, Influencer)  # indirect recursion

    elif option == "5":
        print("Exiting the program...")
        return False

    else:
        print("Unrecognized option, please try again.")
    return True




def update_level(old_folder: os.path, Influencer: object) -> str:
    """
    Update the status of the folder.

    Args:
        old_folder (str): Path to the previous folder.
        Influencer (object): Object with methods to perform various actions (e.g., record voice).

    Returns:
        str: New path to the folder.
    """
    new_folder = update_folder_status(old_folder)
    os.chdir(new_folder)  # change to the new folder
    time.sleep(2)  # give time to change cwd
    process_option(new_folder, Influencer)




def edit_video_main(Influencer: object) -> None:
    """
    Function that encapsulates all the video editing logic.

    Args:
        Influencer (object): Object with methods to perform various actions (e.g., record voice).
   
    Applies to folders in the following states:
    1. With script
    2. With script and voice
    3. With script, voice, and subtitles
    4. With script, voice, subtitles, and video
    """
    # First, it is necessary to be in the indicated directory
    valid_states = [1, 2, 3, 4]
    folder = choose_folder(valid_states)

    # open_folder(folder)
    print(folder)

    parent_path = os.path.abspath(os.path.join(folder, os.pardir))
    delete_state0_folders(parent_path)

    os.chdir(folder)
    os.makedirs("images", exist_ok=True)
    os.makedirs("audios", exist_ok=True)

    process_option(folder, Influencer)


