from abc import ABC, abstractmethod
import os

class INFLUENCER(ABC):

    """
    Template for creating an influencer

    Reasons to use an abstract class:
    - Create a common contract of what an influencer should have
    - Prevent a class from being instantiated alone
    - Encourage code reuse
    
    And above all, to be able to loop over influencers
    """

    def __init__(self):
        pass



    @abstractmethod
    def get_correct_wd(self) -> None:
        """
        Ensures the script runs from the correct directory.
        """
        pass



    @abstractmethod
    def create_folder(self) -> os.path:
        """
        Creates a folder for the influencer NEW_INFLUENCER and returns its path.
        """
        pass



    @abstractmethod
    def greet(self) -> str:
        """
        Returns a specific greeting for the influencer NEW_INFLUENCER.
        """
        pass



    @abstractmethod
    def get_credentials(self) -> tuple[str, str]:
        """
        Gets the necessary credentials for the influencer NEW_INFLUENCER.
        """
        pass



    @abstractmethod
    def influencer_sound(self) -> tuple[str, int, int, float]:
        """
        Returns the characteristic sound of the influencer NEW_INFLUENCER:
                    - song, song_volume_decibels, voice_boost, voice_speed
        """
        pass



    @abstractmethod
    def default_influencer_sound(self) -> tuple[str, int, int, float]:
        """
        Returns the default sound when mass-produced.        
        """
        pass



    @abstractmethod
    def record_voice(self, text) -> bytes:
        """
        Function to record the particular voice of the influencer NEW_INFLUENCER.
        
        :param text: Text of the script for the TTS model voice to read
        """
        pass



    @abstractmethod
    def get_influencer_script_ideas(self) -> None:
        """
        Gets topic ideas for future videos of the influencer NEW_INFLUENCER.
        """
        pass



    @abstractmethod
    def main_ScriptGPT(self, video_folder: os.path, title: str = "") -> None:
        """
        Gets the particular styles of the influencer NEW_INFLUENCER to write a script like those on their channel.
        
        :param video_folder: Path to the folder where the video will be saved.
        :param title: Title of the video including the topic.
        """
        pass



    @abstractmethod
    def get_influencer_images(self, video_folder: os.path) -> None:
        """
        Gets images for the video according to the logic of the influencer NEW_INFLUENCER.
        
        :param video_folder: Path to the folder where the video is stored.   
        """ 
        pass



    @abstractmethod
    def download_influencer_images(self) -> None:
        """
        Downloads images according to the logic of the influencer NEW_INFLUENCER.        
        """
        pass



    @abstractmethod
    def get_thumbnail_colors(self) -> list[tuple[int, int, int]]:
        """
        Returns a list of colors to use in thumbnails, according to the colors of the influencer NEW_INFLUENCER.
        """
        pass



    @abstractmethod
    def get_keywords(self, video_folder: os.path) -> None:
        """
        Improves the SEO of the videos
            - Ensures that the keywords do not exceed the limit
            - Generates an explanatory description that uses many SEO words
        
        :param video_folder: Path to the folder where the video is stored.
        """
        pass 



    @abstractmethod
    def avoid_phonetic_correction(self) -> None:
        """
        Function to determine the parameter of the Phonetic Correction function in Spanish:
            - YES = avoid phonetic correction
            - NONE = Do not avoid phonetic correction in Spanish (= do correct phonetics)
        """
        pass
    


    @abstractmethod
    def video_upload_days(self) -> list:
        """
        Returns a list of the days of the week when the influencer uploads videos.

        Returns:
            list: List of days of the week (0 for Monday, 6 for Sunday).
        """
        pass
    


    @abstractmethod
    def youtube_api_parameters(self) -> tuple:
        """
        Returns the configuration of the API parameters for uploading to YouTube
        
        Returns:
            Tuple: (Video_Category, Video_Language)
        """
        pass
