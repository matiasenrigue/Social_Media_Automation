# 1. Creation of the Influencer:

Create a new folder for the new influencer and include these 2 files:

  - Use the template <NEW_INFLUENCER.py> to create the characteristics of the Influencer (voice, colors, etc.)
    - Create the NEW_INFLUENCER.py file to define the characteristics of the influencer
    - Save in: `<InfluencerFolder/Logic/NEW_INFLUENCER.py>`

  - Use the template <NEW_INFLUENCER_LLM_Interaction.py> to create the style of the Influencer (video scripts, descriptions, keywords)
    - Create the NEW_INFLUENCER_LLM_Interaction.py file to define the influencer's scripts using prompt engineering
    - Save in: `<InfluencerFolder/Logic/NEW_INFLUENCER_LLM_Interaction.py>`

### Obtain Multimedia for the Influencer

  - Obtain Photos for the influencer and save them in a folder in the "Clean Data Folder" (inside the influencer folder)
    - The structure should be the following (example with a fruits influencer): 
      - `<InfluencerFolder/clean_data>`:
        - `<InfluencerFolder/clean_data/apple>` (apple pictures)
        - `<InfluencerFolder/clean_data/banana>` (banana pictures)
    
  - Obtain Music for the influencer and save it in the data folder in music (outside the influencer folder, in the main folder of the project)
    - Save in: `<data/music>`

# 2. Registration of the Influencer

In the Influencers folder, register the influencer in the Influencer.py file in the appropriate function:
  - if we want them to be available to produce videos
  - if we want them to be available to upload videos

# 3. Register with the YouTube API

Register the Influencer in the YouTube API of Google Cloud Platform.
Save the credentials in the folder `<InfluencerFolder/API_info/client_secrets>`
