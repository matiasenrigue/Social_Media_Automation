from pydub import AudioSegment
import os
from datetime import datetime
import re
import json
from typing import Optional, Tuple


"""
This script processes recorded audio files by editing their volume, speed, and adding background music. 
It includes functions to adjust volume levels, combine audio segments, and save/load configurations 
for consistent audio processing.

Functions:

1. adjust_volume_to_common_level:
    - Ensures all audio files in the specified folder are at the same volume level.
    - Saves the adjusted audio files with a prefix.

2. combine_audios:
    - Combines volume-adjusted audio files in the specified folder into a single MP3 file.
    - Adds brief pauses between segments and a final pause.

3. audio_editing:
    - Edits the audio by adjusting volume, speed, and adding background music.
    - Saves the audio with and without background music for further processing.

4. save_configuration:
    - Saves the audio configuration (song path, volume, voice increase) to a JSON file.

5. load_configurations:
    - Loads the audio configuration from a JSON file.
"""





def adjust_volume_to_common_level(audio_folder: os.path = 'audios') -> None:
    """
    Function to ensure all audios are at the same volume level.

    Args:
        audio_folder (str): folder where the audio files are located.
    """

    audios = []
    volume_levels = []

    # Compile the regular expression to identify the desired files
    file_pattern = re.compile(r'^part\d+\.mp4$')  # Assumes .mp4 extension, adjust as needed

    # Load all files that match the pattern and measure their volume
    for file in os.listdir(audio_folder):
        if file_pattern.match(file):
            file_path = os.path.join(audio_folder, file)
            segment = AudioSegment.from_file(file_path)
            audios.append((file, segment))
            volume_levels.append(segment.dBFS)

    # Avoid division by zero if there are no matching files
    if not volume_levels:
        return

    # Determine the target volume level
    target_volume = sum(volume_levels) / len(volume_levels)

    # Adjust the volume of each audio to the target level and save
    for file, segment in audios:
        volume_difference = target_volume - segment.dBFS
        adjusted_segment = segment.apply_gain(volume_difference)

        # Save the adjusted segment
        output_path = os.path.join(audio_folder, f"adjusted_{file}")  # Overwrite the original file
        adjusted_segment.export(output_path, format='mp4')  # Adjust the format if needed


def combine_audios(audio_folder: os.path = 'audios', output_name: str = 'labs.mp3') -> None:
    """
    Combine all volume-adjusted audio files in the specified folder into a single MP3 file.
    Assumes adjusted files are saved with the prefix 'adjusted_'.

    Args:
        audio_folder (str): Directory where the adjusted audio files are located.
        output_name (str): Name of the combined output file.
    """
    audios = []

    # Filter only files that start with 'adjusted_' and end with '.mp4'
    audio_files = sorted([file for file in os.listdir(audio_folder) if file.startswith('adjusted_') and file.endswith('.mp4')],
                         key=lambda x: int(x.replace('adjusted_part', '').split('.')[0]))

    for file in audio_files:
        file_path = os.path.join(audio_folder, file)
        segment = AudioSegment.from_file(file_path)
        audios.append(segment)
        audios.append(AudioSegment.silent(duration=375))  # Add a pause of 0.375 seconds between files

    audios.append(AudioSegment.silent(duration=1000))  # Add final pause to avoid immediate ending
    combined = AudioSegment.empty()
    # Ensure to remove the last unnecessary pause
    for segment in audios:
        combined += segment

    output_path = os.path.join(audio_folder, output_name)
    combined.export(output_path, format='mp3')





def audio_editing(Influencer: object, mass_production: str = ""):
    """
    Function to edit the audio:
    Edits:
        - Edits the speed and volume of the voice
        - Adds a second of silence so it does not start immediately

    Args:
        Influencer (object): Object with methods to configure the sound of the influencer.
        mass_production (str, optional): Additional parameter for mass productions. Default is an empty string.

    Output:
        - An audio without music to send to the function that makes the subtitles.
        - An audio with music to use in the video.
    """

    # Set all to similar volume level
    print("\n🔄 Adjusting the volume of the audios...")
    adjust_volume_to_common_level()

    # Combine previous audios
    print("\n🔄 Combining audios...")
    combine_audios()

    # Import Background Music:
    current_dir = os.getcwd()

    print("\n🔄 Choosing music...\n")

    if mass_production:  # Parameter set for mass productions to avoid choosing
        config_exists = os.path.exists(os.path.join(os.getcwd(), "config", "config_audio.json"))

        if config_exists:  # Check if the file exists
            song_path, decibels, voice_increase = load_configurations()
        else:  # If it does not exist, set default values
            song_path, decibels, voice_increase, voice_speed = Influencer.default_influencer_sound()
    else:  # In case of wanting to choose in detail
        song_path, decibels, voice_increase, voice_speed = Influencer.influencer_sound()

    mp3_path = os.path.join(current_dir, "..", "..", "..", "data", "music", song_path)

    # Load the audio file
    main_audio = AudioSegment.from_file("audios/labs.mp3")
    silence = AudioSegment.silent(duration=250)  # 1000 milliseconds, 1 second
    main_audio = silence + main_audio

    # Increase the volume of the original audio
    volume_increase = voice_increase  # Increase by 10 dB
    main_audio = main_audio + volume_increase

    # Speed up the original audio
    speed_factor = 1.125  # Speed factor (1.3 for 30% faster)
    main_audio = main_audio.speedup(playback_speed=speed_factor)

    # Save without music for subtitles
    audio_subtitles_path = os.path.join("audios", "audio_subtitles.mp3")
    main_audio.export(audio_subtitles_path, format="mp3")
    print("\n🎧 Audio for subtitles created")

    # Add background music
    background_music = AudioSegment.from_file(mp3_path)
    volume_reduction = decibels  # Reduce the volume of the background music by -10 with classical
    background_music = background_music + volume_reduction

    # Ensure the background music is the same length as the main audio
    final_length = len(main_audio)
    background_music = background_music[:final_length]

    # Overlay the background music with the main audio
    combined_audio = main_audio.overlay(background_music)

    # Save the sped-up audio
    audio_path = os.path.join("audios", "audio_music.mp3")
    combined_audio.export(audio_path, format="mp3")
    print("\n🎧 Audio with music created")

    # Save chosen configurations:
    save_configuration(song_path, decibels, voice_increase)





def save_configuration(song_path: os.path, decibels: int, voice_increase: int) -> None:
    """
    Save the audio configurations in a JSON file.

    Args:
        song_path (str): Path of the selected song.
        decibels (int): Decibels of the background music.
        voice_increase (int): Volume increase of the voice.
    """
    
    # Verify if the "config" folder exists in the current working directory (cwd), if not, create it
    config_path = os.path.join(os.getcwd(), "config")
    if not os.path.exists(config_path):
        os.makedirs(config_path, exist_ok=True)

    # Create a dictionary with the choices
    configuration = {
        "song": song_path,
        "background_music_volume_decibels": decibels,
        "voice_increase": voice_increase
    }

    # Save the dictionary in a JSON file inside the "config" folder
    with open(os.path.join(config_path, "config_audio.json"), "w") as json_file:
        json.dump(configuration, json_file, indent=4)





def load_configurations() -> Tuple[str, int, int]:
    """
    Load the audio configurations from a JSON file.

    Returns:
        Tuple[str, int, int]: Path of the song, volume of the song in decibels, and voice volume increase.
    """
    # Define the path to the JSON file inside the "config" folder
    config_path = os.path.join(os.getcwd(), "config", "config_audio.json")

    with open(config_path, "r") as json_file:
        configuration = json.load(json_file)

    # Access the values and save them as variables
    song_path = configuration["song"]
    decibels = configuration["background_music_volume_decibels"]
    voice_increase = configuration["voice_increase"]

    return song_path, decibels, voice_increase
