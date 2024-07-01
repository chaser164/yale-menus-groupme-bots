import requests
import json
from build_message import build_message_string

def post_to_groupme(bot_dict):
    # Replace with your bot_id
    
    # Endpoint URL
    url = "https://api.groupme.com/v3/bots/post"

    message = build_message_string(bot_dict)
    # Don't send if there are no hits
    if message == 'NO_HITS':
        return
    
    # Data payload
    data = {
        "text": message,
        "bot_id": bot_dict['bot_id']
    }
    
    # Convert data to JSON format
    json_data = json.dumps(data)
    
    try:
        # Send POST request
        response = requests.post(url, data=json_data)
        
        # Check if request was successful (status code 200)
        if response.status_code == 202:
            print(f"{bot_dict['term']} bot delivered the message!")
        else:
            print(f"Failed to post message. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error posting message: {e}")
