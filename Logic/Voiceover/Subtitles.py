import whisper_timestamped
import json
import string
import os
from datetime import datetime
import re
from typing import List, Dict, Any, Tuple


"""
Script to obtain and correct subtitles from audios:
- Generates subtitles using the OpenAI model
- Verifies and corrects discrepancies between the original script and the generated subtitles
- Makes specific phonetic corrections to improve pronunciation for Spanish inlfuencers (writes text in Spanish phonetics)
"""





def get_subtitles() -> None:
    """
    Function to obtain subtitles from an audio:
    - Uses the audio without music but already edited (speed, silences, etc.) so that the timings match the final audio with music.
    - Uses the OpenAI model running LOCALLY.
    """
    
    print("\n🔄 Generating Subtitles...\n")

    # Function to flatten the structure of the results
    def flatten_transcription(results: Dict[str, Any]) -> List[Dict[str, Any]]:
        transcription_words = []
        for segment in results["segments"]:
            transcription_words.extend(segment["words"])
        return transcription_words

    # Get subtitles
    audio = os.path.join("audios", "audio_subtitles.mp3")
    model = whisper_timestamped.load_model("base")
    results = whisper_timestamped.transcribe(model, audio)

    # Flatten the transcription
    flattened_transcription = flatten_transcription(results)

    with open('flattened_transcription.json', 'w', encoding='utf-8') as f:
        json.dump(flattened_transcription, f, ensure_ascii=False, indent=4)

    print("\n📄 Subtitles created")








def correct_subtitles(mass_production: str = "") -> None:
    """
    Function that indicates which words in the subtitles file do not match the original script and vice versa.
    - The user must manually correct them.
    - The user must modify the JSON file in the video folder and change the words as needed.

    Args:
        mass_production (str, optional): Additional parameter to avoid sending messages in mass mass_production mode.
    """
    from Logic.Uploads.Telegram_Messages import send_telegram

    def count_words(word_list: List[str]) -> Dict[str, int]:
        counter = {}
        for word in word_list:
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1
        return counter

    def clean_text(text: str) -> List[str]:
        characters_to_remove = string.punctuation + "¡"  # Define special characters to remove
        cleaned_text = text.translate(str.maketrans('', '', characters_to_remove)).lower()  # Remove special characters and convert to lowercase
        return cleaned_text.split()

    print("\n🔄 Verifying subtitles...\n")

    with open("script.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    with open('flattened_transcription.json', 'r', encoding='utf-8') as f:
        generated_subtitles = json.load(f)

    original_words = clean_text(original_text)
    original_counter = count_words(original_words)
    subtitles_counter = {}

    for subtitle in generated_subtitles:
        subtitle_words = clean_text(subtitle['text'])
        for word in subtitle_words:
            if word in subtitles_counter:
                subtitles_counter[word] += 1
            else:
                subtitles_counter[word] = 1

    missing_words_in_subtitles = {}
    extra_words_in_subtitles = {}

    for word, frequency in original_counter.items():
        if word not in subtitles_counter:
            missing_words_in_subtitles[word] = frequency

    for word, frequency in subtitles_counter.items():
        if word not in original_counter:
            extra_words_in_subtitles[word] = frequency

    message = "Subtitle corrections:\n"

    print("\n⚠️ Words to add:\nWords present in the script and missing in the subtitles: word : frequency")
    message += "\n\n⚠️ Words to add:\nWords present in the script and missing in the subtitles: word : frequency\n"
    for word, frequency in missing_words_in_subtitles.items():
        print(f"{word}: {frequency}")
        message += f"\n{word}: {frequency}"

    print("\n⚠️ Words to change:\nWords present in the subtitles and missing in the script: word : frequency")
    message += "\n\n\n⚠️ Words to change:\nWords present in the subtitles and missing in the script: word : frequency\n"
    for word, frequency in extra_words_in_subtitles.items():
        print(f"{word}: {frequency}")
        message += f"\n{word}: {frequency}"

    print("\n\n⚠️ Change the json file to correct the subtitles")
    print("⚠️ Use Ctrl + F to search for the words to change\n\n\n\n")

    with open('subtitle_corrections.txt', 'w', encoding='utf-8') as corrections_file:
        corrections_file.write(message)

    if mass_production:
        pass
    else:
        send_telegram(message)








def phonetic_correction(english: str = "") -> None:
    """
    Function to change the ceceos ("z" and "c" when applicable) to this symbol "θ"
    - Reason: Audio AI pronounces ceceos as s if this symbol is not used
    
    Args:
        english (str, optional): Parameter to not apply this function if the original file is in English.

    Output:
    - A modified script changing those letters when applicable to θ
    - This script is the one that will be given to the AI of ElevenLabs

    English Parameter:
    - To not apply this function if the original file is in English
    - But still pass it here to change the file name and follow the Workflow correctly
    """

    def change_sounds(text):
        modified_words = []

        # Function to add the modified word to the list
        def add_modified_word(match):
            original_word = match.group(0)
            # modified_word = re.sub(r'c([ei])', r'θ\1', original_word, flags=re.IGNORECASE)
            modified_word = re.sub(r'c([eéií])', r'θθ\1', original_word, flags=re.IGNORECASE) # Words with accent (ex: césped) were not being changed
            modified_word = re.sub(r'z', 'θθ', modified_word, flags=re.IGNORECASE)
            # modified_word = re.sub(r'x([aeiou])', r'ch\1', modified_word, flags=re.IGNORECASE)
            modified_words.append(modified_word)
            return modified_word

        # Apply the changes and collect modified words
        text = re.sub(r'\b\w*[cz]\w*\b', add_modified_word, text, flags=re.IGNORECASE)
        # text = re.sub(r'\b\w*([cz]|x[aeiou])\w*\b', add_modified_word, text, flags=re.IGNORECASE)

        return text, modified_words

    """
    Since "H" causes pronunciation problems only in some words in Spanish, simply fix the isolated cases
    """
    replacements_dictionary = {
        'hacia': 'acia',
        'hace': 'ace',
        'hazaña': 'azaña'
    }

    # Read the text file
    with open("script.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    for original_word, replacement in replacements_dictionary.items():  # Replace words with mispronounced H
        original_text = original_text.replace(original_word, replacement)

    if english:  # If the text is in English skip all this

        with open("modified_script.txt", "w", encoding="utf-8") as modified_file:
            modified_file.write(original_text)

    else:  # If not (Spanish) apply transformation

        # Apply the changes and obtain modified words
        modified_text, modified_words = change_sounds(original_text)

        # Print modified words in a single line
        print("\nModified words:", ', '.join(modified_words))

        # Optionally, save the modified text in a new file
        with open("modified_script.txt", "w", encoding="utf-8") as modified_file:
            modified_file.write(modified_text)

        print("\nThe text has been modified and saved as 'modified_script.txt'")
