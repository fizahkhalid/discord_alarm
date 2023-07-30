import streamlit as st
import time
from utils import get_credentials,get_messages
from datetime import datetime
from dateutil import parser
import base64

# Footer text
st.footer("Developed by: Fizah Khalid | [LinkedIn Profile](https://www.linkedin.com/in/fizahkhalid/)")


def format_timestamp(timestamp):
    # Convert timestamp to a more readable format
    datetime_obj = parser.parse(timestamp)
    formatted_timestamp_date = datetime_obj.strftime('%d-%m-%Y')  # Ensure the seconds fraction has three digits
    formatted_timestamp_time = datetime_obj.strftime('%H:%M')  # Ensure the seconds fraction has three digits
    
    return formatted_timestamp_date,formatted_timestamp_time

def display_message(message,expand=False):
    text = message['content']
    author = message['author']['username']
    attachments = [element['url'] for element in message['attachments'] if element['content_type'].startswith("image")]
    date_str,time_str = format_timestamp(message['timestamp'])

    # Message layout
    with st.expander(f"Posted by {author} - at: {time_str} | {date_str}",expanded=expand):
        st.write(f"**{author}** said:")
        st.info(text)
        if len(attachments):
            st.image(attachments, width=400, caption=f"Posted by {author}")

choice = st.sidebar.radio('Select Discord Account',options=['default','custom'],horizontal=True)
st.sidebar.divider()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False

if 'sound_alarm_in_settings' not in st.session_state:
    st.session_state['sound_alarm_in_settings']=False

if 'authorization' not in st.session_state:
    st.session_state['authorization']=False

if choice == "default":
    if not st.session_state['logged_in']:
        username, password = get_credentials()
        username_input = st.sidebar.text_input('Username')
        password_input = st.sidebar.text_input('Password', type='password')
        login_button = st.sidebar.button("Log In")
        if login_button:
            if username_input == username and password_input == password:
                st.sidebar.success('Logged in successfully!')
                st.session_state['logged_in']=True
            else:
                st.sidebar.error('Invalid username or password. Please try again.')
    else:
        st.sidebar.success('Logged in to Default Account !')
    st.sidebar.divider()
else:
    authorization_key = st.sidebar.text_input('Authorization Key',type='password')
    if authorization_key:
        st.session_state['authorization'] = True
    st.sidebar.divider()

channel_id_message = "Channel ID [Optional]" if st.session_state['logged_in'] else "Channel ID"
channel_id_input = st.sidebar.text_input(channel_id_message)


if st.session_state['logged_in'] and choice=="default":
    authorization_key = st.secrets['DEFAULT']['authorization']
    channel_id = st.secrets['CHANNEL_ID']['channel_id']
    if channel_id_input:
        CHANNEL_ID = channel_id_input
    else:
        CHANNEL_ID = st.secrets['CHANNEL_ID']['channel_id']
        
elif st.session_state['authorization'] and choice=="custom":
    if channel_id_input:
        CHANNEL_ID = channel_id_input
    elif st.session_state['logged_in']:
        CHANNEL_ID = st.secrets['CHANNEL_ID']['channel_id']
    else:
        st.sidebar.error("Please provide a valid Channel Id.")
        CHANNEL_ID = None
else:
    CHANNEL_ID = None
st.sidebar.divider()

alarms = {
    'Frédéric Chopin':{"path":'alarms/Muriel-Nguyen-Xuan-Chopin-valse-opus64-1.ogg',"format":'audio/ogg'}
}

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
    
# Sidebar settings button
with st.sidebar.expander('# Settings', expanded=False):
    option1 = st.checkbox('Real Time Monitoring On', value=True)
    sleep_duration = st.number_input('Duration for sleep(sec)',min_value=5,max_value=500)
    option2 = st.selectbox('Alarms', ['Frédéric Chopin'])

    if st.button("Play/Stop Audio"):
        if not st.session_state['sound_alarm_in_settings']:
            sound_md = autoplay_audio(alarms[option2]['path'],alarms[option2]['format'])
            st.markdown(sound_md,unsafe_allow_html=True)
            st.session_state['sound_alarm_in_settings']=True
            st.write("Playing ...")
        else:
            sound_md = st.empty()
            st.session_state['sound_alarm_in_settings']=False


        # st.audio(audio_bytes,format=alarms[option2]['format'])
PROCEED=False
if CHANNEL_ID:
    st.header("Messages")
    messages = get_messages(channel_id=CHANNEL_ID,authorization_key=authorization_key)
    if type(messages)==list:
        if len(messages)>0:
            last_message = messages[0]
            index=0
            for message in messages:
                if index==5:
                    break
                display_message(message)
                index+=1
        else:
            last_message=None
        PROCEED = True
    else:
        last_message = None
        st.error("Messages are not being Populated !")
        test_messages = get_messages(CHANNEL_ID,authorization_key)
        if 'code' in test_messages.keys():
            PROCEED = False
            st.error("Retrieving Messaged Returned Error Code: ",messages['code'])


    st.divider()
    if last_message:
        st.header("Last Message")
        display_message(last_message,True)
        st.divider()
        last_message_content = last_message['content']
        last_message_time = last_message['timestamp']
    else:
        last_message_content = None
        last_message_time = None
else:
    st.info("Please Enter a Channel ID to Proceed")

if CHANNEL_ID and option1 and PROCEED:
    while True:
        messages = get_messages(channel_id=CHANNEL_ID,authorization_key=authorization_key)
        if last_message_content == messages[0]['content'] and last_message_time == messages[0]['timestamp']:
            st.session_state['alarm_state']='not running'
            continue
        else:
            new_message = messages[0]
            st.header("New Message Recieved !")
            display_message(new_message,expand=True)
            last_message_content = new_message['content']
            last_message_time = new_message['timestamp']
            sound_md = autoplay_audio(alarms[option2]['path'],alarms[option2]['format'])
            st.markdown(sound_md,unsafe_allow_html=True)

        time.sleep(sleep_duration)
if not option1:
    st.warning("REAL TIME MONITORING STOPPED !")
                

