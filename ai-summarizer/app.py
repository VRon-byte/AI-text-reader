import streamlit as st
from main import summarize
#Page configuration*
st.set_page_config(
    page_title="AI Summarizer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#Session state setup *
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"

#Sidebar

with st.sidebar:
    st.title("Chats")

    #New chat button
    if st.button("New chat"):
        new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.active_chat = new_chat_name
        st.rerun()

    st.divider()

    #Chat history placeholder--

    st.subheader("Previous Chats")
 # Generate buttons for each chat
    for chat_name in st.session_state.chats:

        if st.button(chat_name):

            st.session_state.active_chat = chat_name
            st.rerun()
    st.divider()

    #Example settings section--

    st.subheader("Settings")


#Main chat area and display messages

st.title("AI Assistant")

active_chat = st.session_state.active_chat
messages = st.session_state.chats[active_chat]

# Show which chat you're in
st.caption(f"Current chat: **{active_chat}**")

for msg in messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#User input and handling

user_input = st.chat_input("Type your message here...")

if user_input:
    #Save user message
    messages.append({
        "role": "user", "content": user_input
    })
    #display that message
    with st.chat_message("user"):
        st.write(user_input)

    #Placeholder assistant response--
    with st.chat_message("assistant"):
        response = summarize(user_input)
        st.write(response)
    #Save ai response
    messages.append({
        "role": "assistant", "content": response
    })
