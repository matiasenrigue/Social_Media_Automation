import re
import os
import sys
from Logic.Tools.Folders import update_folder_status



"""
Manage and handle scripts coming from an LLM. Includes the following functions:

    - treat_script: Processes a script and its footer, separating and saving its components in separate files.
    - checking_theme: Checks that the video theme corresponds to a photo folder, avoiding failures during recording and API calls if the folder does not exist.
    - GPT_script_main: Main function to manage and handle scripts coming from an LLM, creating and updating folders as needed.
"""



def treat_script() -> None:
    """
    Processes a script and its footer, separating and saving its components in separate files.
    """

    def separate_script_and_footer_and_save(text: str) -> None:
        """
        Separates the text into script, title, thumbnail, footer, and SEO, then saves them in individual files.
        """

        # Clean up possible issues from the LLM: unwanted characters
        text = text.replace('"', '') 
        text = text.replace('{', '')
        text = text.replace('}', '')
        text = text.replace('<', '')
        text = text.replace('>', '')
        
        # Separate text into parts        
        parts = text.split('$$$$')
        if len(parts) != 5:
            raise ValueError("\n❌ The code could not be separated correctly.\n")
        script, title, thumbnail, footer, seo = parts
        script = script.strip()
        script = script.replace('#', '')
        footer = footer.strip()
        title = title.strip()
        thumbnail = thumbnail.strip()
        seo = seo.strip()

        # Handle the Footer:
        footer_parts = footer.split('#')  # Separate text and existing hashtags in the footer
        footer_text = footer_parts[0].strip()  # Extract the text, removing extra space at the end
        existing_hashtags = footer_parts[1:]  # Retrieve the existing hashtags, if any        
        new_hashtags = ["shorts"]  # Add new hashtags to the existing ones
        updated_hashtags = ['#' + hashtag for hashtag in existing_hashtags + new_hashtags]
        updated_footer = "{} \n.\n {}".format(footer_text, ' '.join(updated_hashtags))

        # Save Files
        with open('script.txt', 'w', encoding='utf-8') as script_file:
            script_file.write(script)
        with open('footer.txt', 'w', encoding='utf-8') as footer_file:
            footer_file.write(updated_footer)
        with open('title.txt', 'w', encoding='utf-8') as title_file:
            title_file.write(title)
        with open('thumbnail.txt', 'w', encoding='utf-8') as thumbnail_file:
            thumbnail_file.write(thumbnail)
        with open("keywords.txt", 'w', encoding='utf-8') as keywords_file:
            keywords_file.write(seo)

    # Use the function to separate Script
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            separate_script_and_footer_and_save(text)
            print("\n✅ The script and the footer have been saved correctly.\n")
    except ValueError as e:
        print(e)
    except Exception as e:
        print("An error occurred:", e)






def checking_theme(video_theme: str, specified_folder: str = None) -> None:
    """
    Checks that the video theme corresponds to a photo folder.
    If it does not correspond, it triggers sys.exit() before calling the API in a loop.

    Utility: 
        - avoid code failure when recording has already started and APIs have been called.
        - Triggering the failure before calling the APIs saves money by avoiding failures.
    
    :param video_theme: The theme of the video.
    :param specified_folder: The path of the specified folder.
    
    Feeling lost? Check the explanation I wrote in <NEW_INFLUENCER/NEW_INFLUENCER_LLM_Interaction.py get_topics_NEW_INFLUENCER>
    """
    
    video_theme = video_theme.strip()
    video_theme = video_theme.capitalize()
    
    if specified_folder:
        raw_data_folder = specified_folder
    else:
        raw_data_folder = os.path.join(os.getcwd(), "clean_data")

    # Check if the folder exists or not     
    theme_folder = os.path.join(raw_data_folder, video_theme)
    if os.path.exists(theme_folder):
        print(f"\n ✅ The photo folder for the theme {video_theme} exists")
    else:
        sys.exit(f"\n❌ WARNING! The theme folder does not exist: {video_theme}\nCheck for spelling errors!!")





def GPT_script_main(Influencer: object, title: str = "") -> str:
    """
    Main function to manage and handle scripts coming from an LLM.

    :param Influencer: Influencer object that handles folder creation and script processing.
    :param title: Optional title for the script.
    :return: The path of the updated folder.
    """
    folder = Influencer.create_folder()
    Influencer.main_ScriptGPT(folder, title)
    folder = update_folder_status(folder)
    return folder