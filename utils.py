import json
import requests
from dateutil import parser
import base64


def get_messages(channel_id,authorization_key):
    headers = {
        "authorization":authorization_key
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    r = requests.get(url=url,headers=headers)
    json_objects = json.loads(r.text)
    return json_objects

def format_timestamp(timestamp):
    # Convert timestamp to a more readable format
    datetime_obj = parser.parse(timestamp)
    formatted_timestamp_date = datetime_obj.strftime('%d-%m-%Y')  # Ensure the seconds fraction has three digits
    formatted_timestamp_time = datetime_obj.strftime('%H:%M')  # Ensure the seconds fraction has three digits
    return formatted_timestamp_date,formatted_timestamp_time

def autoplay_audio(file_path,format):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:{format};base64,{b64}" type={format}>
            </audio>
            """
        return md