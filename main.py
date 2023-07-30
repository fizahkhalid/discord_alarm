from utils import get_message,raise_alarm
import time

last_message = None
last_message_time = None
condition = False
CHANNEL_ID = '1049270613065334845'
stop = False

while not stop:
    messages = get_message(channel_id=CHANNEL_ID)
    if last_message is None:
        if len(messages)>0:
            last_message = messages[0]['content']
            last_message_time = messages[0]['timestamp']
            print(f"Last Message Set to {last_message}")
            print(f"Time of Message was {last_message_time}")
        else:
            last_message = None
    else:
        if last_message == messages[0]['content'] and last_message_time == messages[0]['timestamp']:
            condition = True
            continue
        else:
            new_message = messages[0]['content']
            raise_alarm(duration=3)
            last_message = messages[0]['content']
            last_message_time = messages[0]['timestamp']
    time.sleep(10)

