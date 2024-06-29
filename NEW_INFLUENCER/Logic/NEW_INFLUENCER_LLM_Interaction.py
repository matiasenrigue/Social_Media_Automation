import os
from Logic.Videos.Script_LLM_Interaction import get_script_from_LLM, get_description_from_LLM, get_topics_for_videos_from_LLM

"""
This script is designed to facilitate the creation of content for the NEW_INFLUENCER's YouTube Shorts account. 
It includes three primary functions that interact with a Language Learning Model (LLM) to generate scripts, descriptions, and topic ideas for videos.

Functions:

1. Get Script for NEW_INFLUENCER Videos:
- Retrieves a structured script for a video based on the provided title and clean data.
- It ensures the generated content follows a predefined format including hook, development, conclusion, title, thumbnail, footer, and keywords.

2. Get SEO-Optimized Descriptions:
- Generates a detailed and SEO-optimized description for the video.
- Focuses on enhancing the video's searchability through strategic keyword inclusion.

3. Get Topic Ideas for Future Videos:
- Provides new topic ideas for future videos, organized by a specific coding structure.
- Ensures the topics are relevant and do not repeat previously used themes.

Usage:
- Ensure the paths provided for video storage and clean data are correct.
- Follow the structure and instructions within each function to maintain consistent and effective interaction with the LLM.
"""


def get_script_NEW_INFLUENCER(title: str, video_folder: os.path, clean_data_original_folder: os.path) -> None:
    """
    Function to get the scripts for the NEW_INFLUENCER's Youtube Shorts account.

    :param title: Title of the video that includes the topic.
    :param video_folder: Path to the folder where the video will be saved.
    :param clean_data_original_folder: Path to the clean data folder that contains the images.
    """
    
    instructions_video_script_LLM = """

                **These are not prompts for GPT model, its an advice for the use of this code**
                You should write a prompt engineering that allows you to do the following:
                - Get a script
                - Get a footer
                - Get a title
                - Get a thumbnail
                - Get keywords
                
                The code is expecting the following sturcture as an asnwer from the LLM.
                You will receive one asnwer with this structure, and the code will decompose it as it should
                Be very insistent to the LLM to respect this structure
                
                        "
                        <{hook} {development} {conclusion}>
                        $$$$
                        <{title}>
                        $$$$
                        <{thumbnail}>
                        $$$$
                        <{footer}>
                        $$$$
                        <{keywords}>
                        "
                
    """
    
    get_script_from_LLM(
        video_folder=video_folder, 
        title=title, 
        clean_data_folder=clean_data_original_folder, 
        system_instructions_video_script_LLM=instructions_video_script_LLM
    )





def get_description_NEW_INFLUENCER(video_folder: os.path) -> None:
    """
    Function to get SEO-optimized video descriptions.

    :param video_folder: Path to the folder where the video is saved.
    """

    instructions_description_LLM = """
    
                **These are not prompts for GPT model, its an advice for the use of this code**
                The reason of getting a new description for the video (new footer) is to ask the GPT model to fully focus as much as possible on the task of improving the SEO of the video with keywords
                I found that the keywords strategy works better for the description than in the keywords part of the Video.


    """
    
    get_description_from_LLM(
        video_folder=video_folder,
        system_instructions_description_LLM =instructions_description_LLM
    )




def get_topics_NEW_INFLUENCER(clean_data_original_folder: os.path) -> None:
    """
    Function to get topic ideas for future videos of the influencer NEW_INFLUENCER

    :param clean_data_original_folder: Path to the clean data folder that contains the images.
    """
    
    directory_elements = os.listdir(clean_data_original_folder)  # Get all files and folders in the clean_data directory
    Codes_list = ', '.join(directory_elements) # List of all the folders (used as Codes)
    
    instructions_topics_LLM = f"""
    
    
            **These are not prompts for GPT model, its an advice for the use of this code**
            
            This function is used so the LLM gives you an aswer with the topics of your next videos, you can decide for how many to ask, I normally ask for 25, but that number is random
            
            You should aim for this format:
                - Video Title / Code
            
            What is Code?
                When storing pictures in your "clean_data" folder (insisde your influencer folder) save them organizing them in folders with clear names
                    For example, an animals influencer should use the following folder names for its pics: Tiger, Dog, Polar_Bear...
                    These Folder names will be used as "Code" for the videos.
                
                So, when Python needs to choose images or music for the videos it will choose them based on the "Code" decided now. (which will be saved later in a file called "theme.txt")
                
                This is why its very important that you emphazisse the LLM on writing the "Code"s correctly, if not Python breaks. 
                    You should give him this variable : {Codes_list}
                    Luckily is also wrote a function in charge of checking that the Codes are correctly written 
            
            
            Bonus: When sending the message to the Open AI API it will also send the list of all the videos produced so you dont have to worry about repeating 
                    
    """
    
    get_topics_for_videos_from_LLM(
        system_instructions_topics_LLM=instructions_topics_LLM, 
        clean_data_folder=clean_data_original_folder
    )



