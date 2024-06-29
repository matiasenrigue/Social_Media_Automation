# Social Media Automation

⭐ **Portfolio Project**: This repository showcases my skills in Python development through a comprehensive package for automating social media content creation and management.

## Demo
Check out the [YouTube demo](https://youtu.be/PpNS5vbUkyI) to see how the project works.

## Features

⚙️ My code handles various influencer profiles, generating ideas, producing videos, and posting them. It also organizes folder structures and posting schedules. The system operates autonomously, and I receive alerts via Telegram in case of any issues.

### Management.py
For managing the various influencers' profiles:
- Get topics for new videos
- Organize folders
- Bulk download pictures

### Mass_production.py
For managing videos production of all the influencers and the same time:
- Produce videos in bulk
- Re-edit videos
- Approve videos before uploading
- Upload videos to YT on the background while respecting all limits

### Videos.py
In case you want more control and supervision (I don't use it):
- Edit video parts (script, images, narration)
- Choose thumbnails
- Approve/deny videos


## Usage
This project provides a template for building a mass production system for AI-generated influencer videos. Note that specific components such as prompts, editing styles, and thumbnail styles are hidden to preserve uniqueness. Tutorials for substituting these components:
- Prompt engineering for LLM
- MoviePy for video editing
- PIL for thumbnail creation

## Installation

Clone the repository:
```sh
git clone https://github.com/matiasenrigue/Social_Media_Automation.git
cd Social_Media_Automation
```

Install the required dependencies:
```sh
pip install -r requirements.txt
```

## Running the Scripts

1. **Management.py**: Use for managing influencer profiles.
    ```sh
    python Management.py
    ```

2. **Mass_production.py**: Use for bulk video production.
    ```sh
    python Mass_production.py
    ```

3. **Videos.py**: Use for more controlled video editing.
    ```sh
    python Videos.py
    ```

## Folder Structure
- `Logic/`: Contains the core logic for automation.
- `NEW_INFLUENCER/`: Example folder for managing a new influencer.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please contact me at [matienrigue1@gmail.com](mailto:matienrigue1@gmail.com).



