import streamlit as st
from main import summarize
from text_reader import TextReader

# Initialize TextReader
text_reader = TextReader()

# Page configuration
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

# Initialize session state variables
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"

if "current_document" not in st.session_state:
    st.session_state.current_document = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

# Sidebar for chat management and document analysis
with st.sidebar:
    st.title("Chats")
    
    # New chat button
    if st.button("New chat"):
        new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.active_chat = new_chat_name
        st.rerun()
    
    st.divider()
    
    # Document Analysis Section
    st.subheader("📁 Document Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a document to analyze",
        type=['txt', 'pdf', 'docx'],
        help="Upload TXT, PDF, or DOCX files"
    )
    
    # URL input
    url = st.text_input("Or enter a URL:", placeholder="https://example.com")
    
    # Process uploaded file
    if uploaded_file:
        with st.spinner("📖 Extracting text with TextReader..."):
            extracted_text = text_reader.extract_from_upload(uploaded_file)
        
        if extracted_text.startswith("Error:"):
            st.error(extracted_text)
        else:
            st.success(f"✅ Extracted {len(extracted_text)} characters!")
            st.session_state.current_document = extracted_text
            st.session_state.document_name = uploaded_file.name
    
    # Process URL
    if url:
        with st.spinner("🌐 Extracting text from URL with TextReader..."):
            extracted_text = text_reader.extract_from_url(url)
        
        if extracted_text.startswith("Error:"):
            st.error(extracted_text)
        else:
            st.success(f"✅ Extracted {len(extracted_text)} characters!")
            st.session_state.current_document = extracted_text
            st.session_state.document_name = url
    
    st.divider()
    st.subheader("Previous Chats")
    
    # Chat buttons
    for chat_name in st.session_state.chats:
        if st.button(chat_name):
            st.session_state.active_chat = chat_name
            st.rerun()
    
    st.divider()
    st.subheader("Settings")

# main chat 
st.title("AI Assistant")

# Get current chat messages
active_chat = st.session_state.active_chat
messages = st.session_state.chats[active_chat]

st.caption(f"Current chat: **{active_chat}**")

# Display existing messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Show document context if available
if st.session_state.current_document:
    st.info(f"📄 Currently analyzing: **{st.session_state.document_name}**")

# user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save and display user message
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        if st.session_state.current_document:
            # User has a document loaded - check if question is about the document
            doc_keywords = ['document', 'file', 'url', 'this', 'analyze', 'summarize', 'about', 'extract', 'read']
            if any(word in user_input.lower() for word in doc_keywords):
                prompt = f"Based on this document:\n\n{st.session_state.current_document[:3000]}\n\nQuestion: {user_input}\n\nAnswer:"
                response = summarize(prompt)
            else:
                response = summarize(user_input)
        else:
            # No document, regular chat
            response = summarize(user_input)
        
        st.write(response)
    
    # Save assistant response
    messages.append({"role": "assistant", "content": response})

