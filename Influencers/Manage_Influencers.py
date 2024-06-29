import os
from NEW_INFLUENCER.Logic.NEW_INFLUENCER import Influencer_NEW_INFLUENCER

# Some Influencers I have, as an Example
from PrAnimales.ANI_Logic.ANIMALS import Influencer_ANI
from PrFilosofia.FILO_Logic.FILO_INFLUENCER import Influencer_FILO
from PrEngPhilosophy.FILENG_Logic.FILENG_Influencer import ENG_Influencer_PHILOSOPHY



# Dictionary mapping influencer names to their corresponding classes
INFLUENCERS_MAP = {
    "Animals": Influencer_ANI(),
    "Spanish_Filosofia": Influencer_FILO(),
    "English_Philosophy": ENG_Influencer_PHILOSOPHY()
}



def video_production_influencers() -> list:
    """
    Function to return a list of influencers who will RECORD videos to loop over.
    - Utility for mass operations

    Return: Influencer object
    """
    production_influencers = [
        Influencer_ANI(),
        ENG_Influencer_PHILOSOPHY(),
        Influencer_FILO()
    ]

    return production_influencers



def active_posting_influencers() -> list:
    """
    Function to return a list of influencers who will UPLOAD videos to loop over.
    - Utility for mass operations

    Return: Influencer object
    """
    available_influencers = [
        Influencer_ANI(),
        ENG_Influencer_PHILOSOPHY(),
        Influencer_FILO()
    ]

    return available_influencers




def get_influencer() -> object:
    """
    Function that reads the selected influencer file to get the influencer in question.

    Return: Corresponding Influencer object.
    """
    influencer_file = os.path.join(os.getcwd(), "z_Hidden_Folders", "selected_influencer.txt")

    try:
        if not os.path.exists(os.path.dirname(influencer_file)):  # Create folder if it doesn't exist
            os.makedirs(os.path.dirname(influencer_file))
        
        if os.path.exists(influencer_file):  # If influencer file exists, initiate the indicated influencer
            with open(influencer_file, 'r', encoding='utf-8') as file:
                influencer_id = file.read().strip()
        else:  # If it doesn't exist, create it with this function
            choose_influencer()
            with open(influencer_file, 'r', encoding='utf-8') as file:
                influencer_id = file.read().strip()
                
    except Exception as e:  # Assuming the influencer was misspelled: if there was a file but the object couldn't be selected
        print(f"There was an error: {e}\n\nChoose Influencer:")
        choose_influencer()
        with open(influencer_file, 'r', encoding='utf-8') as file:
            influencer_id = file.read().strip()

    # Get the correct influencer from the influencer map
    influencer = INFLUENCERS_MAP.get(influencer_id)

    return influencer




def choose_influencer() -> object:
    """
    Function to choose influencers and work on them.
    Also returns the influencer object to make the change effective.

    Return: Selected Influencer object.
    """
    from Logic.Tools.Folders import get_social_media_wd

    get_social_media_wd()  # change working directory to social media
    available_influencers = list(INFLUENCERS_MAP.keys())
    influencer_file = os.path.join(os.getcwd(), "z_Hidden_Folders", "selected_influencer.txt")

    print("\n👤 Please choose an influencer from the following list:")
    for index, name in enumerate(available_influencers, start=1):
        print(f"{index}. {name}")

    selection = int(input("\nEnter the influencer number: "))

    if 0 < selection <= len(available_influencers):
        chosen_influencer = available_influencers[selection - 1]
        print(f"\n👤 You have selected: {chosen_influencer}")

        with open(influencer_file, "w") as file:
            file.write(chosen_influencer)

        influencer = get_influencer()
        influencer.get_correct_wd()  # change working directory to influencer
        return influencer
    else:
        print("\nInvalid selection. Please try again.")
        return choose_influencer()
