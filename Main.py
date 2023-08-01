import time
import streamlit as st
from utils import get_messages,autoplay_audio
from st_utils import get_credentials,display_message,footer

st.set_page_config(
    page_title='Discord Alarm',page_icon="⏰",layout='wide',initial_sidebar_state='auto')


# DISPLAY FOOTER
footer()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False
if 'sound_alarm_in_settings' not in st.session_state:
    st.session_state['sound_alarm_in_settings']=False
if 'authorization' not in st.session_state:
    st.session_state['authorization']=False
if 'custom_authorization' not in st.session_state:
    st.session_state['custom_authorization']=False


with st.sidebar.expander('About'):
    st.write("This is an automated discord alarm for any new messages in a channel. Authorization key for your discord account can be fetched from Inspect (Networking - typing request), for any query or help reach out to the linkedin or email provided in the footer.")
st.sidebar.divider()

choice = st.sidebar.radio('Select Discord Account',options=['default','custom'],horizontal=True)
st.sidebar.divider()

if choice=="default":
    if not st.session_state['logged_in']:
        username, password = get_credentials()
        with st.sidebar.expander("Login"):
            username_input = st.text_input('Username')
            password_input = st.text_input('Password', type='password')
            login_button = st.button("Log In")
            if login_button:
                if username_input == username and password_input == password:
                    st.success('Logged in successfully!')
                    st.session_state['logged_in']=True
                else:
                    st.error('Invalid username or password. Please try again.')
    else:
        st.sidebar.success('Logged in to Default Account !')
elif choice == "custom":
    authorization_key = st.sidebar.text_input('Authorization Key',type='password')
    if authorization_key:
        st.session_state['authorization'] = True
        st.session_state['custom_authorization'] = authorization_key

st.sidebar.divider()

# NEXT STAGE : ONLY PROCEED IF EITHER YOU ARE LOGGED IN, OR YOU HAVE THE AUTHORIZATION KEY
STAGE_TWO = False

if st.session_state['logged_in'] or st.session_state['authorization']:
    STAGE_TWO = True

alarms = {
    'Frédéric Chopin':{"path":'alarms/Muriel-Nguyen-Xuan-Chopin-valse-opus64-1.ogg',"format":'audio/ogg'}
}

# Sidebar settings button
with st.sidebar.expander('# Settings', expanded=False):
    real_time_monitoring = st.checkbox('Real Time Monitoring On', value=True)
    sleep_duration = st.number_input('Duration for sleep(sec)',min_value=5,max_value=500)
    alarm_choice = st.selectbox('Alarms', ['Frédéric Chopin'])

    if st.button("Play/Stop Audio"):
        if not st.session_state['sound_alarm_in_settings']:
            sound_md = autoplay_audio(alarms[alarm_choice]['path'],alarms[alarm_choice]['format'])
            st.markdown(sound_md,unsafe_allow_html=True)
            st.session_state['sound_alarm_in_settings']=True
            st.write("Playing ...")
        else:
            sound_md = st.empty()
            st.session_state['sound_alarm_in_settings']=False
if STAGE_TWO:
    st.title("Real Time Discord Alarm with Messages")
    if real_time_monitoring:
        # Custom colored bar (Green)
        custom_colored_bar = """
        <div style="height: 10px; background-color: #4CAF50;"></div>
        """

        # Display the custom colored bar (Green)
        st.markdown(custom_colored_bar, unsafe_allow_html=True)
    else:
        # Custom colored bar (Green)
        custom_colored_bar = """
        <div style="height: 10px; background-color: #FF0000;"></div>
        """

        # Display the custom colored bar (Green)
        st.markdown(custom_colored_bar, unsafe_allow_html=True)
        st.write("")
        st.warning("REAL TIME MONITORING STOPPED !")
    st.divider()
    channel_id_message = "Channel ID [Optional]" if st.session_state['logged_in'] else "Channel ID"
    channel_id_input = st.sidebar.text_input(channel_id_message)
    st.sidebar.divider()

CHANNEL_ID=None
if st.session_state['logged_in']:
    if choice == "default":
        authorization_key = st.secrets['DEFAULT']['authorization']
        channel_id = st.secrets['CHANNEL_ID']['channel_id']
        if channel_id_input:
            CHANNEL_ID = channel_id_input
        else:
            CHANNEL_ID = channel_id
        STAGE_THREE=True
    else:
        if not authorization_key:
            st.sidebar.error('Custom Authorization Key Not Set')
            STAGE_TWO=False
            STAGE_THREE=False
        else:
            if channel_id_input:
                CHANNEL_ID = channel_id_input
                STAGE_THREE=True
            else:
                st.sidebar.error("Please provide a valid Channel Id.")
                CHANNEL_ID = None
                STAGE_THREE=False
elif st.session_state['authorization'] and choice == "custom":
    if channel_id_input:
        CHANNEL_ID = channel_id_input
        STAGE_THREE=True
    elif st.session_state['logged_in']:
        CHANNEL_ID = st.secrets['CHANNEL_ID']['channel_id']
        STAGE_THREE=True
    else:
        st.sidebar.error("Please provide a valid Channel Id.")
        CHANNEL_ID = None
        STAGE_THREE=False
else:
    STAGE_THREE=False

TEST_PASSED = False

if STAGE_THREE:
    messages = get_messages(channel_id=CHANNEL_ID,authorization_key=authorization_key)
    if type(messages)==list:
        TEST_PASSED = True
    else:
        TEST_PASSED = False
        st.error(f"Messages not retrieved with status code {messages['code']} \n Please Check the **Channel ID** or **Authorization Key**")

    if TEST_PASSED:
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

        
if STAGE_THREE and TEST_PASSED and real_time_monitoring:
    while True:
        messages = get_messages(channel_id=CHANNEL_ID,authorization_key=authorization_key)
        if type(messages)==list:
            if last_message_content == messages[0]['content'] and last_message_time == messages[0]['timestamp']:
                st.session_state['alarm_state']='not running'
                continue
            else:
                new_message = messages[0]
                st.header("New Message Recieved !")
                display_message(new_message,expand=True)
                last_message_content = new_message['content']
                last_message_time = new_message['timestamp']
                sound_md = autoplay_audio(alarms[alarm_choice]['path'],alarms[alarm_choice]['format'])
                st.markdown(sound_md,unsafe_allow_html=True)
        else:
            TEST_PASSED = False
            st.error(f"Messages not retrieved with status code {messages} \n Please Check the **Channel ID** or **Authorization Key**")

        
        time.sleep(sleep_duration)

