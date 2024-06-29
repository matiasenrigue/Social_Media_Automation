import dropbox
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import os
import re
import subprocess
import pytz
from typing import Dict, Optional, Tuple

"""
Useful functions for managing and manipulating data related to images and videos. The main functions include:

    Data Loading:
        - get_data: Loads image paths and necessary sources for the project.

    Image Retrieval and Conversion:
        - from_link_to_picture: Retrieves an image from a web link or a file path.
        - convert_windows_path_to_wsl: Converts a Windows path to a Linux path in WSL.

    Image Creation and Confirmation:
        - create_empty_image: Creates an empty image to avoid errors in processes requiring an image.
        - wait_for_confirmation: Waits for user confirmation to proceed with the process.

    Opening Folders:
        - open_folder: Opens a specific folder within the current working directory.

    Time Conversion:
        - utc_to_spanish_time: Converts UTC time to Spanish time and formats the text.

    Video Name Retrieval:
        - get_video_name: Retrieves the video name according to the 'title.txt' file.
"""





def get_data(Industrial: str = "") -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Load necessary data, such as image paths and sources.

    Args:
        Industrial (str): Indicates if the path is industrial. Default is "".

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: Dictionary of backgrounds and dictionary of font paths.
    """

    current_path = os.getcwd()

    if Industrial:
        data_path = os.path.join(current_path, "..", "..", "..", "data")
    else:
        data_path = os.path.join(current_path, "..", "data")

    images_path = os.path.join(data_path, 'images')
    fonts_path = os.path.join(data_path, 'fonts')

    backgrounds = {
        "FCB": os.path.join(images_path, 'plantilla_historias_barça.jpg')
    }

    font_path_dict = {
        "Gagalin": f"{fonts_path}/Gagalin-Regular.otf",
        "GFSDidot": f"{fonts_path}/GFSDidot-Regular.ttf",
        "Anton": f"{fonts_path}/Anton-Regular.ttf",
        "Sifonn": f"{fonts_path}/SIFONN_PRO.otf",
        "Komikax": f"{fonts_path}/KOMIKAX_.ttf"
    }

    return backgrounds, font_path_dict





def from_link_to_picture(link_photo: str) -> Image.Image:
    """
    Retrieve an image from a web link or a file path.

    Args:
        link_photo (str): Link or path to the image.

    Returns:
        Image.Image: Image object.

    First, determine if a link is from the internet or from Windows files.
    - If from the web, make a request and return the image.
    - If from a Windows path, convert to a Linux path and obtain the image.
    """

    # Check if the link is a URL
    if link_photo.startswith('http://') or link_photo.startswith('https://'):
        response = requests.get(link_photo)
        image = Image.open(BytesIO(response.content))
        return image
    else:
        # Convert Windows path to Linux path (WSL)
        linux_path = convert_windows_path_to_wsl(link_photo)
        print("Converted path:", linux_path)
        # Open the image from the file
        image = Image.open(linux_path)
        return image





def convert_windows_path_to_wsl(original_path: str) -> str:
    """
    Converts a Windows path to a Linux path in WSL.

    Args:
        original_path (str): Windows path to convert.

    Returns:
        str: Path converted to WSL format.

    If it's a Linux path, it doesn't change.
    """

    original_path = original_path.replace('"', '').strip()

    try:
        original_path = original_path.replace(r'wsl$', r'wsl.localhost')
    except:
        pass

    # Convert a Windows WSL path to a Linux path
    wsl_pattern = r'\\\\wsl\.localhost\\Ubuntu\\home(.+)'
    wsl_match = re.match(wsl_pattern, original_path)

    if wsl_match:
        print("\nConverting Windows WSL path to Linux path...\n")
        linux_path = '/home' + wsl_match.group(1).replace('\\', '/')
        print(f"Linux path: {linux_path}\n")
        return linux_path
    
    else: # Check if it's a macOS path and return it as is: means working on mac and path is okay
        mac_pattern = r'^/Users/(.+)'
        mac_match = re.match(mac_pattern, original_path)
        if mac_match:
            return original_path
        else:
            print("\nPath conversion not found.\n")
            return original_path





def create_empty_image() -> Image.Image:
    """
    Creates an empty image to avoid errors in processes that require an image.

    Returns:
        Image.Image: Empty image object.

    Function to create an empty image if we need to create an image but don't have one
    - For example: a function that creates a thumbnail, instead of breaking the code if it doesn't download the image, it creates a black image
    --> This way the rest of the execution is not affected
    """

    empty_image_data = BytesIO() # Create a BytesIO object to represent an empty image
    image = Image.new('RGB', (10, 10)) # Create a small but manageable 10x10 pixel image
    image.save(empty_image_data, format='PNG')
    empty_image_data.seek(0)
    return image





def wait_for_confirmation() -> None:
    """
    Function to wait for user confirmation before continuing with the creation process.
    
    I don't think this function will be used anymore, but I leave it for nostalgia of the time when everything was more manual.
    """

    response = ""
    while response.lower() != "okay":
        response = input("\n👉 Type 'Okay' to continue: ")




def open_folder(new_folder: str = "") -> None:
    """
    Opens a specific folder within the current working directory.

    Args:
        new_folder (str): Relative path of the folder to open from the CWD. If left empty, opens the CWD.
    """
    
    current_path = os.getcwd()
    full_path = os.path.join(current_path, new_folder)

    if os.name == 'nt':  # For Windows
        os.startfile(full_path)
    else:  # For POSIX environments (Linux/Unix, macOS)
        if platform.system() == 'Linux':
            try:
                # Detect if we are in WSL
                if "microsoft" in platform.release().lower():  # Specific to WSL
                    windows_path = full_path.replace('/', '\\')
                    access_windows_path = f"\\\\wsl$\\Ubuntu{windows_path}"
                    subprocess.run(["explorer.exe", access_windows_path])
                else:
                    # For other Linux systems not in WSL
                    subprocess.run(["xdg-open", full_path])
            except Exception as e:
                print(f"Could not open the folder: {e}")
        elif platform.system() == 'Darwin':  # For macOS
            try:
                subprocess.run(["open", full_path])
            except Exception as e:
                print(f"Could not open the folder: {e}")




def utc_to_spanish_time(utc_time_str: str) -> str:
    """
    Converts UTC time to Spanish time and formats the text.

    Args:
        utc_time_str (str): UTC time in string format.

    Returns:
        str: Converted and formatted time in Spanish.
    """
    # Parse the UTC date and time from the input string
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Define the Spanish timezone (including daylight saving time)
    spain_timezone = pytz.timezone("Europe/Madrid")

    # Convert UTC time to Spanish time
    spain_time = utc_time.replace(tzinfo=pytz.utc).astimezone(spain_timezone)

    # Format the date and time to the desired format
    spain_time_str = spain_time.strftime("%d de %B (%m) de %Y a las %H horas")

    # Replace the month name in English with Spanish
    # Note: strftime does not handle month names in Spanish natively on all platforms
    months_english_to_spanish = {
        "January": "Enero", "February": "Febrero", "March": "Marzo",
        "April": "Abril", "May": "Mayo", "June": "Junio",
        "July": "Julio", "August": "Agosto", "September": "Septiembre",
        "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    for eng, esp in months_english_to_spanish.items():
        spain_time_str = spain_time_str.replace(eng, esp)

    return spain_time_str





def get_video_name(folder_path: Optional[str] = None) -> str:
    """
    Retrieves the video name according to the 'title.txt' file.

    Args:
        folder_path (Optional[str]): Path to the folder containing the 'title.txt' file. Default is None.

    Returns:
        str: Video name.
    """
    import unidecode

    if folder_path:
        title_file = os.path.join(folder_path, 'title.txt')
    else:
        title_file = os.path.join(os.getcwd(), 'title.txt')

    # Retrieve the title from the folder
    try:
        with open(title_file, 'r', encoding='utf-8') as file:
            raw_title = file.read()
            title_no_accents = unidecode.unidecode(raw_title)
            title = re.sub(r"[^a-zA-Z0-9 \-_]", "", title_no_accents)
            return title
    except Exception as e:
        print(f"\nError retrieving the video title: {e}\n")
        return "Video"
