import openai
import requests

# Set Story3 API
api_key = "Put here your Story3 API"
# Set OpenAI API key
openai.api_key = "Put Here youur OpenAI API Key"

def generate_story_prompt(base_story, categories):
    """
    Generate a prompt for creating a story based on the given 'base_story' and 'categories'.
    """
    prompt = f"""
    # Create a story using 'Foundation Story' and 'categories' and end the story in suspense.
    # Story should be of length between 100 to 1200 characters.
    # Begin with a clear concept or theme for your story.
    # Most importantly, the story should have good engagement and be interesting.
    # Return only the story; no need to give a story title or any heading in the output.
    BaseStory: ###{base_story}###
    categories: ###{' '.join(categories)}###
    """
    return prompt


def create_story(prompt):
    """
    Generate a story based on the given prompt using OpenAI GPT-3.5 Turbo model.
    """
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response["choices"][0]["text"]
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_full_story(base_story, categories):
    """
    Generate a full story using the provided 'base_story' and 'categories'.
    """
    prompt = generate_story_prompt(base_story, categories)
    full_story = create_story(prompt)
    return full_story


def generate_story_title(story):
    """
    Generate a title for the given story.
    """
    prompt = f"""
    Generate a title for the below story, and only return the title without heading.
    Story: {story}
    """
    story_title = create_story(prompt)
    return story_title


def generate_story_twists(story):
    """
    Generate 5 twists for the given story and return them separated by '\n'.
    """
    prompt = f"""
        # Generate 5 twists for the below story and return output separated by '\n'
        # Reveal the suspense of the story in twists.
        # Twist should be of length up to 200 characters long.
        # Make each twist interesting, and some twists can be related to each other.

        ######         
        Story: {story}
        ######
        """
    story_twists = create_story(prompt)
    return story_twists.split('\n')[1:]


def generate_twist_title(twist):
    """
    Generate a title for the given twist sentence. The title should be of a maximum of 4 words.
    """
    prompt = f"""
        Generate a title for below sentence. Title should be of max 4 words.
        #{twist}#
        """
    twist_title = create_story(prompt)
    return twist_title


def generate_complete_story(base_story, categories):
    """
    Generate a complete story with title, full story, twist titles, and twists.
    """
    story_full = get_full_story(base_story, categories)
    story_title = generate_story_title(story_full)
    story_twists = generate_story_twists(story_full)
    story_twist_titles = [generate_twist_title(twist) for twist in story_twists]

    return [story_title, story_full, story_twist_titles, story_twists]


# Example usage:
"""
story = "there was a boy who lived in a village, every night he heard some strange sound"
categories = ['Horror', 'Thrill']
result = generate_complete_story(story, categories)
print(result)
"""

def create_story_onstory3(api_key, title, body):

    """
    Create a story using the provided 'title' and 'body' on the Story3 platform.
    """
    api_url = "https://story3.com/api/v2/stories"
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": api_key
    }
    request_body = {
        "title": title,
        "body": body,
    }

    try:
        response = requests.post(api_url, json=request_body, headers=headers)

        if response.status_code == 201:
            print("Story created successfully!")
            story_data = response.json()
            return story_data
        else:
            print(f"Failed to create story. Status code: {response.status_code}")
            print("Error response:", response.text)

    except requests.RequestException as e:
        print("Error making API request:", e)


def publish(api_key, twist_hash_id):
    """
    Publish a twist with the provided 'twist_hash_id' on the Story3 platform.
    """
    api_url = f"https://story3.com/api/v2/twists/{twist_hash_id}/publish"
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": api_key
    }
    request_body = {}

    try:
        response = requests.post(api_url, json=request_body, headers=headers)

        if response.status_code == 201:
            print("Published successfully!")
        else:
            print(f"Failed to publish. Status code: {response.status_code}")
            print("Error response:", response.text)

    except requests.RequestException as e:
        print("Error making API request:", e)


def create_twist(api_key, hash_parent_id, title, body, is_extra_twist=True):
    """
    Create a twist using the provided parameters on the Story3 platform.
    """
    api_url = "https://story3.com/api/v2/twists"
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": api_key
    }
    request_body = {
        "hashParentId": hash_parent_id,
        "isExtraTwist": is_extra_twist,
        "title": title,
        "body": body
    }

    try:
        response = requests.post(api_url, json=request_body, headers=headers)

        if response.status_code == 201:
            print("Twist created successfully!")
            twist_data = response.json()
            return twist_data
        else:
            print(f"Failed to create twist. Status code: {response.status_code}")
            print("Error response:", response.text)

    except requests.RequestException as e:
        print("Error making API request:", e)


def publish_story(story_title, story, twists_data):
    """
    Publish a complete story with title, story, and twists on the Story3 platform.
    """
    hash_id_records = []

    story_data = create_story_onstory3(api_key, story_title, story)

    if story_data:
        story_hashid = story_data['hashId']
        hash_id_records.append(story_hashid)

        for twist in twists_data:
            twist_title, twist_body, parent_index = twist
            parent_hashid = hash_id_records[int(parent_index)]

            twist_data = create_twist(api_key, parent_hashid, twist_title, twist_body)

            if twist_data:
                twist_hashid = twist_data['hashId']
                hash_id_records.append(twist_hashid)
                publish(api_key, twist_hashid)
        publish(api_key, story_hashid)

def get_analytics():
    """
    Retrieve analytics data for all published stories on the Story3 platform.
    """
    api_url = "https://story3.com/api/v2/stories/my"
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": api_key
    }
    request_body = {}
    published_stories_data = None

    try:
        response = requests.get(api_url, json=request_body, headers=headers)

        if response.status_code == 200:
            published_stories_data = response.json()
        else:
            return response.status_code, response.text

    except requests.RequestException as e:
        return e

    if published_stories_data:
        all_analytics_data = []
        for story in published_stories_data:
            hash_id = story['hashId']
            api_url_revenue = f"https://story3.com/api/v2/analytics/{hash_id}"
            published_stories_revenue_data = None

            try:
                response = requests.get(api_url_revenue, json=request_body, headers=headers)

                if response.status_code == 200:
                    published_stories_revenue_data = response.json()
                else:
                    return response.status_code, response.text

            except requests.RequestException as e:
                return e

            all_analytics_data.append(published_stories_revenue_data)

    return all_analytics_data

# Example usage:
# story_title = "My Exciting Story"
# story_body = "Once upon a time..."
# twists_data = [('Twist 1 Title', 'Twist 1 Body', 0), ('Twist 2 Title', 'Twist 2 Body', 1)]
# publish_story(story_title, story_body, twists_data)

# Example analytics retrieval:
# analytics_data = get_analytics(api_key)
# print(analytics_data)
