from utils import get_credentials,get_message,raise_alarm
import streamlit as st
import time

username_input = st.sidebar.text_input('Username')
password_input = st.sidebar.text_input('Password', type='password')

NEED_TO_LOG_IN=False

if 'login_state' not in st.session_state:
    st.session_state['login_state']=False
    NEED_TO_LOG_IN = True
elif st.session_state['login_state']==False:
    NEED_TO_LOG_IN = True

if NEED_TO_LOG_IN:
    if st.sidebar.button('Log In'):
        username, password = get_credentials()
        if username_input == username and password_input == password:
            # If the entered credentials match the stored credentials, proceed to the next step
            st.sidebar.success('Logged in successfully!')
            st.session_state['login_state']=True
            NEED_TO_LOG_IN = False
        else:
            st.sidebar.error('Invalid username or password. Please try again.')
if not NEED_TO_LOG_IN:
    st.header("Welcome !")
    CHANNEL_ID = st.sidebar.text_input("Enter the channel Id below")
    stop = st.sidebar.checkbox('STOP THE ALARM')
    alarm_duration = st.sidebar.number_input('Duration for alarm in Seconds',min_value=3,max_value=60)
    sleep_duration = st.sidebar.number_input('Duration for sleep in Seconds',min_value=5,max_value=500)
    last_message = None
    last_message_time = None
    if CHANNEL_ID:
        while not stop:
            messages = get_message(channel_id=CHANNEL_ID)
            if last_message is None:
                if len(messages)>0:
                    last_message = messages[0]['content']
                    last_message_time = messages[0]['timestamp']
                    st.write(f"Last Message Set to {last_message}")
                    st.write(f"Time of Message was {last_message_time}")
                else:
                    last_message = None
            else:
                if last_message == messages[0]['content'] and last_message_time == messages[0]['timestamp']:
                    continue
                else:
                    new_message = messages[0]['content']
                    raise_alarm(duration=alarm_duration)
                    last_message = messages[0]['content']
                    last_message_time = messages[0]['timestamp']
            time.sleep(sleep_duration)
        
        if stop:
            st.warning("REAL TIME MONITORING STOPPED !")

