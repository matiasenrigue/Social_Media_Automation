from Influencers.Manage_Influencers import video_production_influencers
from Logic.Tools.Folders import select_multiple_folders, update_folder_status, set_folder_name, delete_state1_folders 
import os
import time
import threading
import traceback

from Logic.Videos.Script_Logic import GPT_script_main
from Logic.Videos.Video_Recording import video_editing_YT
from Logic.Voiceover.Audio_Editing import audio_editing
from Logic.Voiceover.Subtitles import get_subtitles, correct_subtitles, phonetic_correction
from Logic.Videos.Script_Logic import treat_script
from Logic.Voiceover.Narration import audio_recording
from Logic.Videos.Thumbnails_Shorts import industrial_thumbnails


"""
This script is designed to automate video production workflows for influencers, encompassing tasks from initial title generation to final video editing and uploading. It includes two primary workflows:

From Title to Video:
- This workflow generates complete videos from a given title with minimal supervision.
- It is ideal when the title prompt is well-optimized and requires minimal manual intervention.

Conservative Re-editing:
- This workflow focuses on re-editing videos that have been sent back for corrections.
- It is designed to handle videos at an advanced stage, ensuring they meet quality standards before final publishing.
"""


def from_title_to_video() -> None:
    """
    Function to industrially produce videos from level 0 to level 4.

    Industrial production NOT conservative:
        - Audio is recorded without supervising the text.
    """

    base_wd = os.getcwd()
    influencer_list = video_production_influencers()

    def workflow_from_title_to_video(Influencer: object, influencer_wd: os.path) -> None:
        """
        This mass production function works from outside the folder.

        :param Influencer: Influencer object.
        :param influencer_wd: Working directory of the influencer.
        :return: None
        """
        production_file = os.path.join(os.getcwd(), "a_Management", "themes_production.txt")
        old_file = os.path.join(os.getcwd(), "a_Management", "themes_old.txt")
        
        if not os.path.exists(old_file):  # Avoid failure the first time a new influencer runs (no old file)
            open(old_file, 'w').close()

        with open(production_file, 'r') as file:
            lines_doc1 = file.readlines()
            num_topics = len(lines_doc1)

        for x in range(num_topics):
            try:
                with open(production_file, 'r') as file:
                    lines_doc1 = file.readlines()

                with open(old_file, 'r') as file:
                    lines_doc2 = file.readlines()

                title = lines_doc1.pop(0)  # Get the video title from themes_production

                print(f"\n\n🎬 Starting to produce Video: {title}\n")

                folder = GPT_script_main(Influencer, title)  # Get script and create folder
                os.chdir(folder)  # Change directory to folder
                os.makedirs("images", exist_ok=True)
                os.makedirs("audios", exist_ok=True)

                treat_script()  # Organize Script

                images_path = os.path.join(folder, "images")  # Fill the video with images
                Influencer.get_influencer_images(images_path)

                avoid_phonetic_correction_english = Influencer.avoid_phonetic_correction()  # Returns None or not
                phonetic_correction(avoid_phonetic_correction_english)  # Perform phonetic correction
                stop = audio_recording(Influencer)  # Record audio
                
                if stop:  # Stop execution if the text is not complete
                    print("\nText went wrong, give the API 2 minutes to rest\n")
                    time.sleep(120)
                    os.chdir(influencer_wd)
                    delete_state1_folders(influencer_wd)
                    continue
                
                audio_editing(Influencer, mass_production="YES")  # Edit Audio
                get_subtitles()  # Subtitles
                correct_subtitles(mass_production="YES")  # Correct Subtitles

                video_editing_YT()  # Edit Video
                industrial_thumbnails(Influencer, folder)  # Create 40 thumbnails, then discard 39

                os.chdir(influencer_wd)  # Logging logic: Perform outside influencer directory

                if lines_doc1:
                    lines_doc2.insert(0, title)  # Add video title to themes_old
                    with open(production_file, 'w') as file:  # Remove title from themes_production
                        file.writelines(lines_doc1)
                    with open(old_file, 'w') as file:  # Add title to themes_old
                        file.writelines(lines_doc2)
                else:
                    lines_doc2.insert(0, title + "\n")  # Add video title to themes_old and add a newline
                    with open(production_file, 'w') as file:  # Remove title from themes_production
                        file.writelines("")
                    with open(old_file, 'w') as file:  # Add title to themes_old
                        file.writelines(lines_doc2)

                folder = set_folder_name(folder)
                update_folder_status(folder)  # Update folder status after exiting it just in case
                delete_state1_folders(influencer_wd)

            except Exception as e:
                print(f"An error occurred: {e}\n With the title: {title}")
                traceback.print_exc()
                os.chdir(influencer_wd)
                delete_state1_folders(influencer_wd)

    for Influencer in influencer_list:
        Influencer.get_correct_wd()
        influencer_wd = os.getcwd()  # Change directory to influencer directory
        workflow_from_title_to_video(Influencer, influencer_wd)
        os.chdir(base_wd)








def conservative_reediting() -> None:
    """
    Function to industrially produce videos from level X (sent back for re-editing).
    """

    from Logic.Videos.Video_Recording import video_editing_YT

    base_wd = os.getcwd()
    influencer_list = video_production_influencers()

    def workflow_voice_to_video(Influencer: object, influencer_wd: str) -> None:
        """
        This mass production function works from outside the folder.

        :param Influencer: Influencer object.
        :param influencer_wd: Working directory of the influencer.
        :return: None
        """

        valid_states = ["X"]
        folder_list = select_multiple_folders(valid_states)

        for folder in folder_list:
            os.chdir(folder)
            video_editing_YT()

            file_to_delete = "denied.txt"  # Delete the file that marks this folder as to be re-edited
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

            os.chdir(influencer_wd)
            update_folder_status(folder)  # Update folder status after exiting it just in case

    for Influencer in influencer_list:
        Influencer.get_correct_wd()
        influencer_wd = os.getcwd()
        workflow_voice_to_video(Influencer, influencer_wd)
        os.chdir(base_wd)
