# AI-Story-Originator

Welcome to the AI-Story-Originator GitHub repository! This application is designed to empower users to create captivating stories using state-of-the-art Language Model (LLM) technology. With the ability to input story foundations, select story types, and generate complete narratives with twists, this application provides a unique and interactive storytelling experience.

## Features

1. **Story Creation:**
   - Input a story foundation of up to 100 characters.
   - Select a story type (e.g., Horror, Funny, etc.).
   - Click the "Generate" button to have the LLM generate a complete story with titles and five twists.

2. **Twist Review and Modification:**
   - View the generated story with detailed information on titles and twists.
   - Modify the result, such as changing the twist order, to tailor the story to your liking.

3. **Approval and Publishing:**
   - Choose between "Approve" or "Discard" to decide whether to publish the story.
   - Approved stories will be published on [Story3.com](https://story3.com/).

4. **Dashboard:**
   - Access a dashboard to view statistics for your published stories.
   - Track the number of views, revenue, and unique viewers for each story.

## Getting Started

To run the application, follow these steps:

1. Install Python 3.10 or a later version.
2. Create a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Navigate to the `Grim_Story_Generator/AIStoryGenerator` folder using `cd Grim_Story_Generator/AIStoryGenerator`.
5. Open `Utils.py` and add your Story3 and OpenAI API Key.
6. Return to the `Grim_Story_Generator` folder using `cd ..`.
7. Run the command `python manage.py runserver` to start the application.
8. Copy the IP address displayed in the terminal and paste it into your browser to access the site.
