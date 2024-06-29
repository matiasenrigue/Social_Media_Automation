import os
import re
from Logic.Tools import params
from typing import Optional


"""
Script to record audios from ElevenLabs (Spanish voice) or OpenAI (English voice):
- Calls the API and saves the result in MP3.
- Records the audios in separate chunks to facilitate re-recording in case of errors.

Functions:
    - confirm_status_ok: Asks the user if they have checked that the text is correct before proceeding to record the voice.
    - read_text: Reads the content of a text file based on the part number.
    - record_audio: Records the audio of a specific part of the text.
    - re_record_audio: Allows the user to re-record a specific audio.
    - split_and_save_text: Splits a complete text into sentences and saves each sentence in a separate file.
    - audio_recording: Processes the text, splits it into sentences, and calls the recording function for each sentence.
    - Spanish_voice: Generates audio in Spanish using ElevenLabs.
    - English_voice: Generates audio in English using OpenAI.
"""


def read_text(part_number: int) -> Optional[str]:
    """
    Function to read the content of a text file based on the part number.
    The text files are located within the 'texts' subfolder.

    Args:
        part_number (int): Number of the part of the text to read.

    Returns:
        Optional[str]: Content of the text file or None if the file is not found.
    """
    texts_directory = "texts" 
    file_name = f"part{part_number}.txt"
    file_path = os.path.join(texts_directory, file_name) 

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None





def record_audio(part_number: int, Influencer: object) -> None:
    """
    Function to record audio based on the part number.

    Args:
        part_number (int): Number of the part of the text to record.
        Influencer: Object with a `record_voice` method to record the text.
    """
    text = read_text(part_number)
    if text is None:
        return  # Terminate execution if the text could not be read

    print(f"Text: {text}")
    audio = Influencer.record_voice(text)  # Influencer object to determine if the recording is done with an English or Spanish voice

    directory = "audios"
    if not os.path.exists(directory):
        os.makedirs(directory)

    audio_file_name = f"part{part_number}.mp4"
    audio_file_path = os.path.join(directory, audio_file_name)
    with open(audio_file_path, "wb") as file:
        file.write(audio)





def re_record_audio(Influencer: object) -> None:
    """
    Function to re-record a specific audio if the initial result is not satisfactory.

    Args:
        Influencer: Object with a `record_voice` method to record the text.
    """
    part_number = input("\n👉 Which audio do you want to re-record? (Number): ").strip()
    print(f"\nRe-recording audio number: {part_number}\n")
    record_audio(part_number, Influencer)
    print(f"Audio Corrected\n")






def split_and_save_text(full_text: str) -> int:
    """
    Splits the full text into sentences and saves each sentence in a separate file.
    Avoids creating a file for a 'sentence' that is just a period.

    Args:
        full_text (str): Full text to split.

    Returns:
        int: Number of sentences saved in files.
    """

    texts_directory = "texts"
    if not os.path.exists(texts_directory):
        os.makedirs(texts_directory)

    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    counter = 0  # If there is a final period or not, it can generate an empty sentence or not. So we need to be careful to count only the ones that are saved

    for i, sentence in enumerate(sentences, start=1):
        if sentence and not sentence.isspace():  # Verify that the sentence has meaningful content
            file_name = os.path.join(texts_directory, f"part{i}.txt")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(sentence.strip())
            counter += 1

    print(f"\n\n✂️ The text has been split into {counter} parts. \nCheck them before recording\n")
    return counter






def audio_recording(Influencer: object) -> Optional[str]:
    """
    Function to process a text, split it into sentences, and call the recording function for each sentence.

    Args:
        Influencer: Object with a `record_voice` method to record the text.

    Returns:
        Optional[str]: "STOP" if the text has less than 4 sentences, otherwise None.
    """

    with open("modified_script.txt", "r", encoding="utf-8") as file:
        text = file.read()

    number_of_sentences = split_and_save_text(text)
    
    if number_of_sentences < 4: 
        return "STOP"  # Basically: if the video lasts less than 4 sentences stop it because it will not record anything good

    for i in range(1, number_of_sentences + 1):  # Correct the range:
        record_audio(i, Influencer)
        print(f"Audio number {i} of {number_of_sentences} has been recorded")
    
    return None  # If the video lasts at least 4 sentences return "None" and the video production does not stop





def spanish_voice(text: str) -> bytes:
    """
    Generates audio in Spanish using ElevenLabs.

    Args:
        text (str): Text to convert to audio.

    Returns:
        bytes: Generated audio in binary format.
    """
    from elevenlabs import generate, Voice, VoiceSettings, set_api_key
    ElevenLabs_Key = params.ELEVENLABS_KEY
    set_api_key(ElevenLabs_Key)

    audio = generate(  
        text=text,
        voice=Voice(
            voice_id='Your_Eleven-Labs_Voice_ID',
            settings=VoiceSettings(stability=1, similarity_boost=1, style=0.01, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2"
    )

    return audio





def english_voice(text: str) -> bytes:
    """
    Generates audio in English using OpenAI.

    Args:
        text (str): Text to convert to audio.

    Returns:
        bytes: Generated audio in binary format.
    """

    from openai import OpenAI
    from Logic.Tools import params

    client = OpenAI(api_key=params.OPENAIKEY)

    audio = client.audio.speech.create(
        model="tts-1-hd",
        voice="echo",
        input=text,
    )

    audio_bytes = audio.content

    return audio_bytes
