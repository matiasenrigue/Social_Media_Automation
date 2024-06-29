import os
import random
import datetime
import re
from PIL import Image
import shutil



"""
This script provides utilities for managing and organizing image files within a specified folder. 
It includes functions for converting Windows paths to WSL paths, sorting images by aspect ratio, 
classifying images into subfolders based on orientation, and shuffling images in a folder.

Functions:

1. convert_windows_path_to_wsl:
    - Converts a Windows path to a Linux path in WSL format.
    - Ensures compatibility between Windows and WSL environments.

2. sort_by_aspect:
    - Sorts images from most vertical to most horizontal.
    - Renames images based on a date prefix and their new order.
    - Classifies sorted images into orientation-based subfolders.

3. classify_images:
    - Classifies images into "horizontal" or "vertical" subfolders based on their aspect ratio.
    - Handles images that are square by copying them to both subfolders.

4. random_order:
    - Randomly shuffles the order of image files in a folder.
    - Renames images with a new date-based prefix to reflect their new order.
"""



def convert_windows_path_to_wsl(windows_path: str) -> str:
    """
    Converts a Windows path to a Linux path in WSL.

    Args:
        windows_path (str): Windows path to convert.

    Returns:
        str: Path converted to WSL format.
    """
    # Convert a Windows path for WSL to a Linux path in WSL
    # Example path: "\\wsl$\Ubuntu\home\matias\..."
    pattern = r'^\\\\wsl\$\\Ubuntu(.+)$'
    match = re.match(pattern, windows_path)
    if match:
        # Convert to a Linux path
        # linux_path = '/home' + match.group(1).replace('\\', '/')
        linux_path = match.group(1).replace('\\', '/')
        return linux_path
    else:
        # If it's not a WSL path, return the original path
        return windows_path






def sort_by_aspect(folder_path: str) -> None:
    """
    Sorts images by aspect from most vertical to most horizontal and saves a copy according to their classification.

    Args:
        folder_path (str): Path to the folder with the images.
    """

    folder = convert_windows_path_to_wsl(folder_path)
    new_date = datetime.datetime.now().strftime("%Y-%m-%d-%s")

    images = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                aspect_ratio = height / width
                images.append((file, file_path, aspect_ratio))
        except IOError:
            pass

    images.sort(key=lambda x: x[2], reverse=True)

    for i, (file_name, file_path, _) in enumerate(images):
        prefix = "HD_" if file_name.startswith("HD_") else ""
        new_name = f"{prefix}{new_date}_{i*4+15}.jpg"
        os.rename(file_path, os.path.join(folder, new_name))

    print("\n✅ Sorting by aspect done\n")

    # Here it's assumed that there is a function classify_images
    classify_images(folder)






def classify_images(folder_path: str) -> None:
    """
    Classifies images into subfolders according to their orientation (vertical or horizontal).

    Args:
        folder_path (str): Path to the folder with the images.
    """

    folder = convert_windows_path_to_wsl(folder_path)  # Convert the path
    horizontal_folder = os.path.join(folder, "horizontal")
    vertical_folder = os.path.join(folder, "vertical")

    # Create subfolders if they don't exist
    os.makedirs(horizontal_folder, exist_ok=True)
    os.makedirs(vertical_folder, exist_ok=True)

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                # Check if it's horizontal, vertical, or square
                if width > height:
                    shutil.copy(file_path, horizontal_folder)
                elif height > width:
                    shutil.copy(file_path, vertical_folder)
                else:  # It's square
                    shutil.copy(file_path, horizontal_folder)
                    shutil.copy(file_path, vertical_folder)
        except IOError:
            pass







def random_order(folder_path: str) -> None:
    """
    Shuffles the images in a folder.

    Args:
        folder_path (str): Path to the folder with the images.
    """
    new_date = datetime.datetime.now().strftime("%Y-%m-%d-%s")
    folder = convert_windows_path_to_wsl(folder_path)

    files = os.listdir(folder)
    jpg_files = [file for file in files if (file.endswith('.jpg') or file.endswith('.jpeg')) and file != 'thumbnail.jpg']

    ids = list(range(15, 15 + 4 * len(jpg_files), 4))
    random.shuffle(ids)

    for file, new_id in zip(jpg_files, ids):
        extension = file.split('.')[-1]
        new_name = f"{new_date}_{new_id}.{extension}"
        os.rename(os.path.join(folder, file), os.path.join(folder, new_name))
    print("\n✅ Photo shuffle done\n")
