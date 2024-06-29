import os
from Influencers.MainClass import INFLUENCER
from NEW_INFLUENCER.Logic.NEW_INFLUENCER_LLM_Interaction import get_script_NEW_INFLUENCER, get_description_NEW_INFLUENCER, get_topics_NEW_INFLUENCER




class Influencer_NEW_INFLUENCER(INFLUENCER):
    """
    Class to handle specific operations for the influencer: NEW_INFLUENCER
    """


    def __init__(self):
        super().__init__()



    def get_correct_wd(self)-> None:
        """
        Ensures the script runs from the correct directory.
        """
        from Logic.Tools.Folders import get_correct_wd
        desired_directory = "NEW_INFLUENCER"
        get_correct_wd(desired_directory)



    def create_folder(self)-> os.path:
        """
        Creates a folder for the influencer NEW_INFLUENCER and returns its path.
        """
        from Logic.Tools.Folders import template_folders
        new_folder = template_folders("INFLU")
        return new_folder



    def greet(self) -> str:
        """
        Returns a specific greeting for the influencer NEW_INFLUENCER.
        """
        return " NEW 🧠🤔"



    def get_credentials(self)-> tuple[str, str]:
        """
        Obtains the necessary credentials for the influencer NEW_INFLUENCER.
        """
        client_secrets_path = os.path.join("..", "..", "API_info", "client_secrets.json")
        oauth_storage_path = os.path.join("..", "..", "API_info", "Youtube_API.py-oauth2.json")
        api_keys_Youtube = (client_secrets_path, oauth_storage_path)
        return api_keys_Youtube



    def influencer_sound(self) -> tuple[str, int, int, float]:
        """
        Returns the characteristic sound of the influencer NEW_INFLUENCER:
                    - song, song_volume_decibels, voice_increase, voice_speed
                    
        In case of manual production (supervised):
            - Code will ask the user which song to use  
            
        Example: Animals Influencer  
            - Songs are saved in main_folder/data/music         
        """
        print("\n1- Magical Jungle \n2- African Flute\n3- Jungle Drums")
        print("4- War Music \n5- Underwater\n6- Chill Pet")
        song = input("👉 Choose a song: ")

        voice_volume = 9
        voice_speed = 1.17 

        while True:
            if song == "1":
                return "ANIMALS_magical_jungle.mp3", -7, voice_volume, voice_speed

            elif song == "2":
                return "ANIMALS_africa_flute.mp3", -5, voice_volume, voice_speed

            elif song == "3":
                return "ANIMALS_jungle_drums.mp3", -9, voice_volume, voice_speed

            elif song == "4":
                return "ANIMALS_north_war.mp3", -9, voice_volume, voice_speed

            elif song == "5":
                return "ANIMALS_water.mp3", -10, voice_volume, voice_speed

            elif song == "6":
                return "ANIMALS_pets.mp3", -10, voice_volume, voice_speed

            else:
                print("\nInvalid option")

       


    def default_influencer_sound(self) -> tuple[str, int, int, float]:
        """
        Returns the default sound when produced in bulk.  
        
        In case of Mass Production (unsupervised):
            - Code will check the video topic (previosuly given in the folder) and add a song that matches the topic
        
        Example: Animals Influencer  
            - Songs are saved in main_folder/data/music     
        """
                # Songs
        magical_savannah = ("ANIMALS_magical_jungle.mp3", -7)
        jungle_drums = ("ANIMALS_jungle_drums.mp3", -9)
        danger = ("ANIMALS_north_war.mp3", -7)
        water = ("ANIMALS_water.mp3", -10)
        cute_animal = ("ANIMALS_pets.mp3", -10)

        # Animal to song
        animals_song_style = {
            "Monkey": jungle_drums,  # Jungles
            "Gorilla": jungle_drums,  # Jungles
            "Tiger": danger,  # Savannas and forests
            "Lion": danger,  # Savannas
            "Giraffe": magical_savannah,  # Savannas
            "Panda_bear": cute_animal,  # Forests, but often associated with positive emotions
            "Polar_bear": water,  # Arctic regions, but related to water
            "Penguin": water,  # Antarctic, closely associated with water
            "Wolf": danger,  # Wild, often associated with danger
            "Raven": danger,  # Often symbolize mystery or danger
            "Eagle": magical_savannah,  # Varied habitats, symbol of freedom
            "Dolphin": water,  # Oceans
            "Shark": danger,  # Oceans, associated with danger
            "Whale": water,  # Oceans
            "Turtle": water,  # Many are aquatic
            "Jellyfish": water,  # Oceans
            "Octopus": water,  # Oceans
            "Kangaroo": magical_savannah,  # Open landscapes, but more related to the Australian bush
            "Koala": cute_animal,  # Forests, generally evoke a positive image
            "Horse": cute_animal,  # Domesticated, often associated with open fields
            "Dog": cute_animal,  # Domesticated
            "Cat": cute_animal,  # Domesticated
            "Snake": danger,  # Often evoke fear or danger
            "Mosquito": danger,  # Associated with annoyance and diseases
            "Spider": danger,  # Often evoke fear
            "Rat": danger,  # Often associated with danger or filth
            "Squirrel": cute_animal,  # Generally viewed positively, associated with nature
            "Bat": danger,  # Often associated with the night and danger
            "Hippopotamus": magical_savannah,  # Rivers in Africa, but large and can be dangerous
            "Rhinoceros": magical_savannah,  # Savannas
            "Zebra": magical_savannah,  # Savannas
            "Pig": cute_animal,  # Domesticated
            "Reindeer": cute_animal,  # Often associated with positive holiday themes
            "Duck": cute_animal,  # Waterfowl, generally positive
            "Rabbit": cute_animal,  # Often associated with cuteness
            "Cow": cute_animal,  # Domesticated
            "Lobster": water,  # Ocean
            "Fish": water,  # Aquatic
            "Seal": water,  # Aquatic
            "Elephant": magical_savannah,  # Savannas and forests
            "Crocodile": danger,  # Rivers in savannas, associated with danger
        }
        
        theme_file = os.path.join(os.getcwd(), "theme.txt") # Get video Topic and choose a song accordingly
        with open(theme_file, 'r', encoding='utf-8') as file:
            video_theme = file.read()
        video_theme = video_theme.strip()
        video_theme = video_theme.capitalize()
        song_info = animals_song_style[video_theme]
        song, volume = song_info
        voice_volume = 9
        voice_speed = 1.17 

        return song, volume, voice_volume, voice_speed



    def record_voice(self, text) -> bytes:
        """
        Function to record the particular voice of the influencer NEW_INFLUENCER.
        
        :param text: Text of the script for the TTS model to read.
        """
        from Logic.Voiceover.Narration import english_voice
        audio = english_voice(text)
        return audio



    def get_influencer_script_ideas(self)-> None:
        """
        Obtains ideas for future video topics for the influencer NEW_INFLUENCER.
        """
        original_NEW_INFLUENCER_folder = os.getcwd()
        original_clean_data_folder = os.path.join(original_NEW_INFLUENCER_folder, 'clean_data')
        get_topics_NEW_INFLUENCER(original_clean_data_folder)  



    def main_ScriptGPT(self, video_folder: os.path, title: str = "")-> None:
        """
        Obtains the particular styles of the influencer NEW_INFLUENCER to write a script like those on their channel.
        
        :param video_folder: Path of the folder where the video will be saved.
        :param title: Title of the video that includes the topic.
        """
        main_directory_folder = os.getcwd()
        original_clean_data_folder = os.path.join(main_directory_folder, 'clean_data')
        get_script_NEW_INFLUENCER(title, video_folder, original_clean_data_folder)



    def get_influencer_images(self, video_folder: os.path) -> None:
        """
        Obtains images for the video according to the logic of the influencer NEW_INFLUENCER.
        
        :param video_folder: Path of the folder where the video is saved.   
        """ 
        from Logic.Videos.Video_Media import video_photos_selector
        main_directory_folder = os.path.join("..", "..", "clean_data")
        clean_data_folder = os.path.join(main_directory_folder, 'clean_data')
        video_photos_selector(video_folder, clean_data_folder)



    def download_images_influencer(self) -> None:
        """
        Downloads images according to the logic of the influencer NEW_INFLUENCER. (Example: animals influencer)        
        """
        from Logic.Get_Images.Images_Downloader import pexels_download_manager
        from datetime import datetime
        
        animals = {  # Animals for which photos will be downloaded
            "Monkey": 2,  
            "Gorilla": 4,  # "Animal_name" : number_pages_downloaded (around 100 pics per page)
            "Tiger": 5,  
            "Lion": 5,  
        }
        
        os.makedirs("raw_data", exist_ok=True)  
        raw_data_folder = os.path.join(os.getcwd(), "raw_data")

        print("downloads to do")
        for animal in animals:
            query = animal
            k = animals[animal]
            print(f"{query} : {k}")

        for animal in animals:
            query = animal
            k = animals[animal]

            # Create folder with the Query
            linux_seconds = datetime.now().strftime("%s")
            hour = datetime.now().strftime("%H-%M-%S")
            folder_name = f"{query}_{linux_seconds}"
            download_folder = os.path.join(raw_data_folder, folder_name)
            os.makedirs(download_folder, exist_ok=True)

            # Start the download
            print(f"\nStarting download for {query} at {hour} -- Level: {k}\n")
            pexels_download_manager(query, download_folder, k)



    def get_thumbnail_colors(self)-> list[tuple[int, int, int]]:
        """
        Returns a list of colors to use in the thumbnails, according to the colors of the influencer NEW_INFLUENCER.
        """
        background_colors = [
            (5, 102, 247),  # Blue 
            (189, 151, 13)  # Gold
        ]
        return background_colors



    def get_keywords(self, video_folder: os.path)-> None:
        """
        Improves the SEO of the videos:
            - Ensures that the keywords do not exceed the limit
            - Generates an explanatory description that uses many SEO words
        
        :param video_folder: Path of the folder where the video is saved.
        """
        
        # Ensure that keywords do not exceed the limit
        words = open(os.path.join(video_folder,"keywords.txt"), "r").read().strip()
        words = words.replace("'", "").replace('"', '')
        words = words[:400]
        while words and (words[-1] == ',' or words[-1] == ' '):
            words = words[:-1]
        
        with open(os.path.join(video_folder,"keywords.txt"), "w") as file:
            file.write(words)  
        
        # Generate an explanatory description
        get_description_NEW_INFLUENCER(video_folder)  
    


    def avoid_phonetic_correction(self)-> None:
        """
        Function to determine the parameter of the Phonetic Correction function to Spanish:
            - YES = avoid phonetic correction
            - NONE = Do not avoid phonetic correction to Spanish (i.e., do phonetic correction)
        
        - Particularity influencer NEW_INFLUENCER: Writes in Spanish --> "None" to NOT avoid phonetic correction to Spanish
        """
        return None
    
    
    
    def video_upload_days(self) -> list:
        """
        Returns a list of the days of the week when the influencer uploads videos.

        Returns:
            list: List of days of the week (0 for Monday, 6 for Sunday).
        """
        pass
    
    
        
    def youtube_api_parameters(self) -> tuple:
        """
        Returns the configuration of the API parameters for uploading to YouTube
        
        Returns:
            Tuple: (Video_Category, Video_Language)
        """
        pass