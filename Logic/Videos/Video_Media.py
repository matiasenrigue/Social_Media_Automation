import os
import shutil
import random
from Logic.Tools.Shuffle_pics import random_order




"""
Script to add multimedia content to videos

For now, it only handles images
"""


def video_photos_selector(video_folder: os.path, clean_data_folder: os.path) -> None:
    """
    Function to copy 30 random images from a database (Clean Data Folder) to the folder of a video.

    :param video_folder: Path to the folder where the video images will be saved.
    :param clean_data_folder: Path to the clean data folder containing the images.
    """
    
    # Access the images folder corresponding to the video's theme
    theme_file = os.path.join(os.getcwd(), "theme.txt")
    with open(theme_file, 'r', encoding='utf-8') as file:
        video_theme = file.read()
    video_theme = video_theme.strip()
    video_theme = video_theme.capitalize()
    original_images_folder = os.path.join(clean_data_folder, video_theme)

    # Get the list of files in the original folder (Clean Data)
    files = os.listdir(original_images_folder)
    images = [file for file in files if (file.endswith('.jpg') or file.endswith('.jpeg'))]
    random.shuffle(images)  # Randomly shuffle the list of images
    images_to_copy = images[:30]  # Take the first 30 images from the random list

    # Copy the selected images to the destination folder
    for image in images_to_copy:
        source_path = os.path.join(original_images_folder, image)
        destination_path = os.path.join(video_folder, image)
        shutil.copy(source_path, destination_path)

    # Shuffle the images
    random_order(video_folder)






