import sys

"""
Script for Mass Video Production
"""

def choose_action(user_input=None):

    """
    Function to allow the user to choose what action they want to take with Mass Production
    """

    if user_input is None:
        print("\n💼 Choose an action:\n")
        print("\n🏭 Mass Production: \n1- Produce videos from the available topics for each influencer")
        print("\n🔨 Fixes: \n2- Mass edit all those videos marked with an 'X' to be edited again")
        print("\n✅ Approval Machine:\n3- Approve all videos that meet the requirement to be approved in bulk")
        print("\n🚀 Uploading Machine:\n4- Upload 6 videos that meet the requirement to be approved in bulk")
        print("\n🥊 FORCED Approval Machine:\n5- Approve videos without reviewing them based on level (reviewed by workflow)")
        print("\n\n⚙️ CONFIGURE UPLOADS: \n987- Simple Upload to configure the uploads of an influencer")

        user_input = input("\n👉: ")
        print("")

    user = int(user_input)

    if user == 1:
        from Logic.Industrialization.Manage_Mass_PRODUCTION import from_title_to_video
        from_title_to_video()

    elif user == 2:
        from Logic.Industrialization.Manage_Mass_PRODUCTION import conservative_reediting
        conservative_reediting()

    elif user == 3:
        from Logic.Industrialization.Manage_Mass_POSTING import bulk_approve
        bulk_approve()

    elif user == 4:
        from Logic.Industrialization.Manage_Mass_POSTING import upload_YT_bulk
        
        import os
        os.system('osascript -e \'display notification "Mass_production.py started" with title "Cron Job Notification"\'')
        upload_YT_bulk()
        os.system('osascript -e \'display notification "Mass_production.py ended" with title "Cron Job Notification"\'')

    elif user == 5:
        from Logic.Industrialization.Manage_Mass_POSTING import bulk_approve
        bulk_approve(forced="Activated")

    elif user == 987:  # Single upload config
        from Logic.Uploads.Uploading import post_ONE_SINGLE_video
        from Influencers.Manage_Influencers import choose_influencer
        Influencer = choose_influencer()
        Influencer.get_correct_wd()
        post_ONE_SINGLE_video(Influencer)

    else:
        choose_action()

if __name__ == "__main__":

    try:
        print(f"\n👋 Welcome to the Mass Video Production program")

        from Logic.Tools.Folders import get_social_media_wd
        get_social_media_wd()

        # Check if arguments were passed to the script
        if len(sys.argv) > 1:
            user_input = sys.argv[1]  # Take the first argument passed to the script (excluding the script name)
            choose_action(user_input)
        else:
            choose_action()

    except:
        import ipdb, traceback, sys

        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        # ipdb.post_mortem(tb)
