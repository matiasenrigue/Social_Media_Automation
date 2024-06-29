from Logic.Tools.Folders import get_correct_wd, update_folder_status
from Influencers.Manage_Influencers import get_influencer

"""
Script for Video Creation
It asks for an influencer and actions are executed according to their settings
"""



def choose_action(Influencer):

    """
    Function to allow the user to choose what action they want to take with the Videos
    """

    greeting = Influencer.greet()
    print(f"\n👋 Welcome to the Video program\n")

    divider = "****" * 10

    print(f"{divider}\nSelected Influencer: {greeting}\n{divider}")

    print("\n📱 Choose an action:\n\n🎥 Videos: \n1- Create New Video\n2- Create only the Script of a Video")
    print("3- Edit an Already Started Video")
    print("\n🖼️ Thumbnails: \n4- Edit the Video Thumbnail")
    print("\n🕵️ Review Videos\n5- Approve Video\n6- Re-edit Video")
    print("\n✈️ Upload Content:")
    print("7- Upload to Video, Reels, and TikTok")

    print("\n\n👤 Change influencer:")
    print("0- Change influencer")

    user = int(input("\n👉: "))
    print("")

    if user == 1:
        print("\nThis FUnctionnality was replaced by Mass Production\nFor that use Mass_production.py\n")

    elif user == 2:
        from Logic.Videos.Script_Logic import GPT_script_main
        GPT_script_main(Influencer)

    elif user == 3:
        from Logic.Videos.Video_Editing_details import edit_video_main
        edit_video_main(Influencer)

    elif user == 4:
        from Logic.Videos.Thumbnails_Shorts import create_vertical_thumbnail
        create_vertical_thumbnail()

    elif user == 5:
        approve_video()

    elif user == 6:
        deny_video()

    elif user == 0:
        from Influencers.Manage_Influencers import choose_influencer
        Influencer = choose_influencer()

        # Restart
        choose_action(Influencer)

    else:
        choose_action(Influencer)





def approve_video():

    from Logic.Videos.Thumbnails_Shorts import save_unique_configuration

    """
    Creates a file called "approved.txt" in the specified folder if the user types "Approve".
    Additionally, when industrial creation has been used, it retains only one thumbnail and its configurations

    It applies only to folders in state 5: video and thumbnails
    """
    from Logic.Tools.Folders import choose_folder
    import os

    valid_states = [4, 5]
    folder = choose_folder(valid_states)

    # Ask the user to type "Approve" to proceed
    user_input = input('\n👉 Do you want to approve the video? (y/n): ').lower().strip()

    save_unique_configuration(folder)

    while True:
        if user_input == "y":
            file_path = os.path.join(folder, "approved.txt")
            with open(file_path, 'w') as file:
                file.write("Video approved")
            print(f"\nThe video has been approved. 'approved.txt' file created in {folder}.")
            update_folder_status(folder)
            break
        else:
            print("\nOperation canceled. The video has not been approved.")
            user_input = input('\n👉 Do you want to approve the video? (y/n): ').lower().strip()





def deny_video():
    """
    Creates a file called "denied.txt" in the specified folder if the user types "Deny".

    It applies only to folders in state 5: video and thumbnails
    """
    from Logic.Tools.Folders import choose_folder
    import os

    valid_states = [5]
    folder = choose_folder(valid_states)

    # Ask the user to type "Deny" to proceed
    user_input = input('\n👉 Type "Deny" to deny the video and create the file: ').capitalize()

    while True:
        if user_input == "Deny":
            file_path = os.path.join(folder, "denied.txt")
            with open(file_path, 'w') as file:
                file.write("Video denied")
            print(f"\nThe video has been denied. 'denied.txt' file created in {folder}.")
            update_folder_status(folder)
            break
        else:
            print("\nOperation canceled. The video has not been denied.")
            user_input = input('\n👉 Type "Deny" to deny the video and create the file: ').capitalize()






if __name__ == "__main__":

    try:
        Influencer = get_influencer()
        Influencer.get_correct_wd()
        choose_action(Influencer)  # Pass the influencer instance to the function

    except:
        import ipdb, traceback, sys

        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
