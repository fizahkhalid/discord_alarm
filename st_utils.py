import streamlit as st
from utils import format_timestamp

def get_credentials():
    username = st.secrets['CREDENTIALS']['Username']
    password = st.secrets['CREDENTIALS']['Password']
    return username, password

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

def footer():
    custom_footer = """
    <div style="position: fixed; bottom: 0; left: 0; width: 140%; background-color: #333333; padding: -1px; text-align: center;">
        <p>Developed by: Fizah Khalid | <a href="https://www.linkedin.com/in/fizahkhalid/" target="_blank">LinkedIn Profile</a>| Email: fizah.khalid26@gmail.com</p>
    </div>
    """
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style+custom_footer, unsafe_allow_html=True)