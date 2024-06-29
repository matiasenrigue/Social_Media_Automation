from Influencers.Manage_Influencers import get_influencer
import os

"""
Script for Managing Profiles
It asks for an influencer and actions are executed according to their settings
"""

def choose_action(Influencer):

    """
    Function to allow the user to choose what action they want to take with the Videos:
    """

    greeting = Influencer.greet()

    print(f"\n👋 Welcome to the Management program\n")
    divider = "****" * 10
    print(f"{divider}\nSelected Influencer: {greeting}\n{divider}")

    print("\n💼 Choose an action:\n")
    print("\n🧠 Generate Ideas: \n1- Get Topics for New Scripts")
    print("\n📅 Calendar: \n2- Get schedule of upcoming videos")
    print("\n🖼️ Download Photos\n3- Download photos for the videos")
    print("\n✈️ Bulk Uploading:\n4- Upload videos to TIKTOK")
    print("\n🧹 Cleanups:\n5- Clean Folders")

    print("\n\n👤 Change influencer:")
    print(f"0- Change influencer --> Current: {greeting}")

    user = int(input("\n👉: "))
    print("")

    if user == 1:
        Influencer.get_influencer_script_ideas()

    elif user == 2:
        print("\nThis is the only function that I didn't code, I found it useless in the end with the implementation of telegram alerts\n")

    elif user == 3:
        Influencer.download_images_influencer()

    elif user == 4:
        print("\nTiktok Posting was problematic due to API problems. For the moment we only focus on Youtube\n")
    
    elif user == 5:
        from Logic.Tools.Folders import move_state7_folders
        outputs = os.path.join(os.getcwd(), "Outputs")
        move_state7_folders(outputs)

    elif user == 0:
        from Influencers.Manage_Influencers import choose_influencer
        Influencer = choose_influencer()

        # Restart
        choose_action(Influencer)

    else:
        choose_action()

if __name__ == "__main__":

    Influencer = get_influencer()
    Influencer.get_correct_wd()

    choose_action(Influencer)
