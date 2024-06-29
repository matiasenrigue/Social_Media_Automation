import requests
from requests.exceptions import HTTPError
from PIL import Image
from io import BytesIO
import time
import os
from datetime import datetime
import sys

from Logic.Tools import params


import threading
import time

from pyunsplash import PyUnsplash
import pixabay.core
from Logic.Tools.Shuffle_pics import sort_by_aspect



"""
Script to download images based on a query using multiple APIs (Pexels and Unsplash).

Functions:

1. pexels_download_manager:
    - Manages image downloads using multiple APIs (Pexels and Unsplash).
    - Stores images in specific folders and calls a function to sort images by aspect.

2. download_image:
    - Downloads an image from a given URL and saves it to a specified folder.
    - Handles HTTP errors and other exceptions during the download process.

3. download_from_Pexels:
    - Downloads images from the Pexels API based on a search query.
    - Saves images in a specified folder.

4. download_from_Unsplash:
    - Downloads images from the Unsplash API based on a search query.
    - Saves images in a specified folder.
"""


def pexels_download_manager(query: str, download_folder: os.path, k: int) -> None:
    """
    Function to manage image downloads using multiple APIs:
    - Using the APIs of Pexels and Unsplash.
    - Images are stored in specific folders.

    :param query: Image search query.
    :param download_folder: Folder where images will be saved.
    :param k: Number of pages of results to download.
    :return: None
    """

    bonus_download_folder = os.path.join(download_folder, "extra")
    os.makedirs(bonus_download_folder, exist_ok=True)

    try:
        thread_Pexels = threading.Thread(target=download_from_Pexels, args=(query, download_folder, k))
        thread_Pexels.start()
    except Exception as e:
        print(f"Error downloading {e}")

    try:
        thread_Unsplash = threading.Thread(target=download_from_Unsplash, args=(query, bonus_download_folder, k))
        thread_Unsplash.start()
    except Exception as e:
        print(f"Error downloading {e}")

    try:
        thread_Pexels.join()
    except Exception as e:
        print(f"Error downloading {e}")

    try:
        thread_Unsplash.join()
    except Exception as e:
        print(f"Error downloading {e}")

    sort_by_aspect(bonus_download_folder)




def download_image(url: str, full_path: os.path) -> str:
    """
    Function to download an image from a specific URL and save it in a given folder.

    :param url: URL of the image to download.
    :param full_path: Full path where the image will be saved.
    :return: "stop" if the download should be stopped, None otherwise.
    """

    try:
        image_response = requests.get(url)
        image_response.raise_for_status()  # This will raise an error if the status is not 200

        image_data = BytesIO(image_response.content)
        image = Image.open(image_data)
        image.save(full_path)

    except HTTPError as e:  # Check if the status code is 404, and if so, DO NOT stop the script
        if e.response.status_code == 404:
            print(f"⚠️ Warning: Image not found (Error 404).")
        else:  # For other HTTP errors, stop the script execution
            print(f"❌ HTTP error downloading the image: {e}")
            return "stop"

    except Exception as e:  # Other errors (e.g., problems opening the image, errors saving the image)
        print(f"❌ Could not download the image. Error: {e}")




def download_from_Pexels(query: str, download_folder: os.path, k: int) -> None:
    """
    Function to download images through the Pexels API.

    :param query: Image search query.
    :param download_folder: Folder where images will be saved.
    :param k: Number of pages of results to download.
    :return: None
    """
    num_results = 80  # maximum
    api_key = params.Pexels_key

    headers = {
        "Authorization": api_key
    }

    linux_seconds = datetime.now().strftime("%s")

    for j in range(k):
        qurl = f"https://api.pexels.com/v1/search?query={query}&page={j+1}&per_page={num_results}"
        r = requests.get(qurl, headers=headers)
        response = r.json()
        photo_list = response["photos"]

        i = 1
        for photo in photo_list:
            source = photo["src"]
            vertical_link = source["portrait"]
            
            file_name = f"{query}_Pexels_{j}_{i}_{linux_seconds}.jpg"
            full_path = os.path.join(download_folder, file_name)

            stop = download_image(vertical_link, full_path)
            if stop:
                break
            i += 1
            time.sleep(3)

    sys.exit("Pexels finished")




def download_from_Unsplash(query: str, download_folder: os.path, k: int) -> None:
    """
    Function to download images through the Unsplash API.

    :param query: Image search query.
    :param download_folder: Folder where images will be saved.
    :param k: Number of pages of results to download.
    :return: None
    """

    pu = PyUnsplash(api_key=params.Unsplash_key)
    linux_seconds = datetime.now().strftime("%s")

    for j in range(k + 1):
        photos = pu.photos(type_='random', count=30, featured=True, query=query, orientation="portrait")
        list_photos = photos.body

        i = 1
        for photo in list_photos:
            urls = photo["urls"]
            high_quality_link = urls["full"]
            file_name = f"{query}_Unsplash_{j}_{i}_{linux_seconds}.jpg"
            full_path = os.path.join(download_folder, file_name)

            stop = download_image(high_quality_link, full_path)
            if stop:
                break
            i += 1
            time.sleep(3)




def download_from_Pixabay(query: str, download_folder: str) -> None:
    """
    CURRENTLY UNUSED
    Function to download images through the Pixabay API.

    :param query: Image search query.
    :param download_folder: Folder where images will be saved.
    :return: None
    """

    px = pixabay.core(params.Pixabay_key)
    linux_seconds = datetime.now().strftime("%s")

    pictures = px.query(
        query=query,
        orientation="vertical",
        minHeight=1200,
        category=["animals", "nature"]
    )

    i = 1
    for picture in pictures:
        file_name = f"{query}_Pixabay_{i}_{linux_seconds}.jpg"
        full_path = os.path.join(download_folder, file_name)

        try:
            picture.download(full_path, "largeImage")
        except Exception as e:
            print(e)

        i += 1
        time.sleep(3)
