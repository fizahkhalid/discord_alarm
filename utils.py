import os
import json
import requests
import configparser
import streamlit as st

def get_messages(channel_id,authorization_key):
    headers = {
        "authorization":authorization_key
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    r = requests.get(url=url,headers=headers)
    json_objects = json.loads(r.text)
    return json_objects

#'2023-07-11T09:00:38.346000+00:00'

def raise_alarm(duration):
    import os
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, 760))

def get_credentials():
    username = st.secrets['CREDENTIALS']['Username']
    password = st.secrets['CREDENTIALS']['Password']
    return username, password