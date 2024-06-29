import os
import time
import threading
import sys
from datetime import datetime
from openai import OpenAI
from Logic.Tools import params
from Logic.Videos.Script_Logic import checking_theme

"""
Script to interact with an LLM to obtain scripts and descriptions optimized for SEO. Includes the following functions:

    To interact with GPT:
        - show_timer: Displays a timer in the console while waiting for the LLM response.
        - LLM_OpenAI_GPT: Interacts with the OpenAI GPT model to get a response based on the given instructions.
    
    To get Script:
        - get_script_from_LLM: Gets scripts from an LLM and saves them in specific files.
        
    To get Video Description:
        - get_description_from_LLM: Gets a description to maximize SEO and saves it in the corresponding file.
    
    To get new Topics for videos:
        - get_topics_for_videos_from_LLM
"""


timer_active = False

def show_timer() -> None:
    """
    Displays a timer in the console while timer_active is True.
    """
    global timer_active
    timer_active = True
    start = time.time()
    while timer_active:
        elapsed_time = time.time() - start
        sys.stdout.write(f"\rResponse time: {elapsed_time:.2f} seconds")
        sys.stdout.flush()
        time.sleep(1)




def LLM_OpenAI_GPT(system_instructions_LLM: str, specific_request_instructions: str, GPT_model: str = "gpt-4-turbo") -> str:
    """
    Interacts with the OpenAI GPT model to get a response based on the given instructions.

    :param system_instructions_LLM: General instructions for the system.
    :param specific_request_instructions: Specific instructions for the video.
    :param GPT_model: GPT model to use (default is "gpt-4-turbo").
    :return: GPT model response.
    """
    global timer_active
    client = OpenAI(api_key=params.OPENAIKEY)
    
    message_history = [
        {
            "role": "system",
            "content": system_instructions_LLM
        },
        {
            "role": "user",
            "content": specific_request_instructions
        }
    ]

    timer_thread = threading.Thread(target=show_timer)
    timer_thread.start()

    chat_completion = client.chat.completions.create(
        model=GPT_model,
        messages=message_history,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    timer_active = False
    
    response = chat_completion.choices[0].message.content
    return response





def get_script_from_LLM(video_folder: str, title: str, clean_data_folder: os.path, system_instructions_video_script_LLM: str) -> None:
    """
    Gets scripts from an LLM and saves them in specific files.

    :param video_folder: Folder where the video will be saved.
    :param title: Title of the video including the theme.
    :param clean_data_folder: Folder where clean data is stored.
    :param system_instructions_video_script_LLM: Specific instructions for the LLM regarding the video.
    """
    
    # Check that the theme is legitimate
    video_title, theme = title.split("/")
    video_title = video_title.strip()
    theme = theme.strip()
    checking_theme(theme, specified_folder=clean_data_folder)
  
    # Write Script
    print(f"\n🔄 Writing script for the theme {theme}...\n")
    response = LLM_OpenAI_GPT(system_instructions_video_script_LLM, specific_request_instructions=video_title, GPT_model="gpt-4-turbo")
    
    # Save Script:
    text_file = os.path.join(video_folder, "text.txt")
    theme_file = os.path.join(video_folder, "theme.txt")
    with open(text_file, "w") as file:
        file.write(response)
    with open(theme_file, "w") as file_t:
        file_t.write(theme)
    print("\n\n🐒 Script successfully saved")
    print("\nWait 2 seconds to save the scripts...")
    time.sleep(2)





#### Get Video Description: Useful for SEO

def get_description_from_LLM(video_folder: os.path, system_instructions_description_LLM: str) -> None:
    """
    Gets a description to maximize SEO and saves it in the corresponding file.

    :param video_folder: Folder where the video will be saved.
    :param system_instructions_description_LLM: Specific instructions for the LLM regarding the description.
    """
    
    # Ensure the file does not exist before creating it again by mistake
    if os.path.isfile(os.path.join(video_folder, "footer_PRE.txt")):
        print(f"\nThe file already exists, no need to search for more keywords\n")
        return None
    else:
        print(f"\n🔄 Generating description...\n")

    # Get Footer
    title = open(os.path.join(video_folder, "title.txt"), "r").read().strip()        
    video_metadata = f"Title: {title}"
    print(f"\n🔄 Writing description for the video {title}...\n")
    response = LLM_OpenAI_GPT(system_instructions_description_LLM, specific_request_instructions=video_metadata, GPT_model="gpt-4-turbo")
    print("\n\n🧠 New description created")
    
    # Add AI Voice disclaimer
    response += "\n ---- \n Voice in the video is AI Generated from a script I provided to a TTS Model \n ---"
    
    # Saving logic
        # Rename keyword file PART 1 (save to variable)
    with open(os.path.join(video_folder, "footer.txt"), 'r') as file:
        previous_keywords = file.readlines()
    time.sleep(1)  # ensure enough time to read the file into the variable
        # Save new keyword file
    with open(os.path.join(video_folder, "footer.txt"), "w") as file:
        file.write(response)   
        # Rename keyword file PART 2 (save file variable)
    previous_keywords_str = ''.join(previous_keywords)  
    with open(os.path.join(video_folder, "footer_PRE.txt"), "w") as file:
        file.write(previous_keywords_str)






# Get Topics for Future Videos   

def verify_correct_topics(filename: str, management_folder: os.path, clean_data_folder: os.path) -> None:
    """
    Function to verify that the codes returned by the GPT API match the themes of the Image folders ("Clean Data").
    
    :param filename: Name of the file containing the new themes.
    :param management_folder: Path to the management folder.
    :param clean_data_folder: Path to the clean data folder.
    """
    
    # Get correct themes
    Correct_Themes_List = os.listdir(clean_data_folder) 

    # Open the newly created file
    with open(os.path.join(management_folder, filename), 'r', encoding='utf-8') as file:
        content = file.read() 
    themes = content.split("\n")
    
    # Check videos whose theme code does not match any correct theme
    incorrect_themes = []
    i = 0
    num_themes = len(themes)
    for theme in themes:
        title, code = theme.split("/")
        code = code.strip()

        if code in Correct_Themes_List:
            i += 1
        else:
            incorrect_themes.append(theme)

    # Notify human if there are errors or not   
    print(f"\nThere are {i} videos with correct theme codes out of {num_themes} possible\n")
    if incorrect_themes:
        print("\n\n🚨🚨🚨 Videos with incorrect theme codes to be corrected 🚨🚨🚨\n\n")
        for theme in incorrect_themes:
            print(f"\n❌ {theme}\n")
    else:
        print("\n✅ All themes are correct.\n")





def get_topics_for_videos_from_LLM(system_instructions_topics_LLM: str, clean_data_folder: os.path) -> None:
    """
    Function to get themes for future scripts for videos, avoiding repeating videos.

    :param clean_data_folder: Path to the clean data folder.
    """
    
    management_folder = os.path.join(os.getcwd(), "a_Management")
    os.makedirs(management_folder, exist_ok=True)

    # Put already done themes in str
    Done_Videos = "" 
    try:
        for file in os.listdir(management_folder):
            if file.startswith("themes_") and file.endswith(".txt"):
                with open(os.path.join(management_folder, file), 'r', encoding='utf-8') as file:
                    Done_Videos += file.read() + "\n"
                    
        if not Done_Videos:
            Done_Videos = "No subjects yet"
    except Exception as e:
        print(f"An error occurred: {e}")
        Done_Videos = "No subjects yet"

    # Talk to LLM
    print("\n🔄 Thinking scripts...\n")
    response = LLM_OpenAI_GPT(system_instructions_topics_LLM, specific_request_instructions=Done_Videos, GPT_model="gpt-4-turbo")
    

    # Save Response
    time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"themes_new_{time_stamp}.txt"
    text_file = os.path.join(os.getcwd(), management_folder, filename)
    with open(text_file, "w") as file:
        file.write(response)

    # Verify everything is OK
    verify_correct_topics(filename, management_folder, clean_data_folder)
