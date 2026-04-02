# AI-text-reader
A basic python application tool using AI as a text summarizer for uploaded text.

## Overview
This is a web application that will be able to summarize text using Google's Gemini AI by either text input by the user inside a textbox, url, or a text extraction via file(s) uploaded (With specific formats). 

**For GUI, server/browser handling, file uploading, AI-integration using python:**

**Library/framework used**- Streamlit (web application is executed using ```streamlit run app.py```)

**AI API used**- Gemini API (in ```main.py```) to summarize text in textbox or file, ```python-dotenv``` to create a ```.env``` and store API_KEY

**Text Extraction tools--in progress--:**
Url- ```requests```
file-```pdfplumber, python-docx, PyPDF2```

**How to execute:**

### Downloading Requirements:
-Open terminal (after cloning into editor), it will start in the root folder (GP-AI_Website)

-**To navigate to the AI-text-reader folder in terminal**
```cd AI-text-reader ```

-**Once there, activate a virtual environment:**

Windows: ``` .\\.venv\\Scripts\\activate ```
Mac/Linux: ``` source .venv/bin/activate ```

-**download requirements:**

```Python
pip install -r requirements.txt
```

This will download required tools (Summarized):
```
streamlit 1.54.0
google-genai 1.67.0
python-dotenv 1.2.1
requests 2.32.5
pdfplumber 0.11.9
python-docx 1.2.0
pandas 2.3.3
```

### Execution
-navigate to ai-summarizer folder
```cd ai-summarizer ```

note: This does require a Google API key from a validated account to communicate with the Gemini AI:

-In ```ai-summarizer```, create a new file called ```.env``` and 
connect your API key to ```GEMINI_API=MY_API_KEY``` inside the file

-**run app.py using streamlit**

```streamlit run app.py``` (press return/enter twice if needed)

- **other ways to execute:**
  
Windows: ```python -m streamlit run app.py```
Mac: ```python3 -m streamlit run app.py```




