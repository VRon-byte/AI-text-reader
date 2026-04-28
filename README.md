# Scholar: An AI-text-reader
This is a python-based studying tool targeted towards students. It uses AI for different studying methods between one or more uploaded/input texts and documents.

## Overview
This is a  web application that will be able to create study sessions for one or multiple texts/documents from the textbox, url, or a text extraction via file(s) uploaded (formats: .txt, .pdf, .docx), and summarize, define key terms & concepts, create flashcards, or just discuss with, using Google's Gemini AI version 2.5 flash lite. 

**Architecture:**  This application uses a linear structure for the flow of data, where it follows a sequential pipeline from the "Student" to the "Response". In which:

**1.** Student interacts with interface "Streamlit App" which creates the "Chat UI Library"

**2.** The uploading of text for example moves into "TextReader", a file that extracts the text from documents or URL uploaded

**3.** Following that, "Gemini AI" is immediately accessed and processed to generate an answer to the "student" prompt

**4.** A response is output into the interface for the student to read

<img width="586" height="320" alt="Screenshot 2026-04-28 at 2 22 57 AM" src="https://github.com/user-attachments/assets/2aac1542-1f66-41cf-8ce9-b05e8e2169ab" />


**For GUI, server/browser handling, file uploading, AI-integration using python:**

**Library/framework used:** Streamlit (web application is executed using ```streamlit run app.py```)

**AI API used**- Gemini API (in ```main.py```) to summarize text in textbox or file, ```python-dotenv``` to create a ```.env``` and store API_KEY

**Text Extraction tools:**
Url- ```requests, beautifulsoup, validators```
file-```pdfplumber, python-docx, PyPDF2```

## Developer/General guide for installation & execution:

Cloning Repository into your editor (VScode): 

Press ```Ctrl+Shift+P``` (Windows/Linux) or ```Cmd+Shift+P``` (macOS) to open command pallette (search bar at the top of the editor).

From the command palette type ```Git: Clone``` and select from list, paste URL of the repository or select "Clone from GitHub" then select local destination folder.

Other (create new terminal inside VScode):

Use ```cd  <your selected folder>``` to navigate into the folder to store the project

Run ```git clone https://github.com``` with the GitHub's URL to copy it into the folder

Repository can be accessed when navigating into the folder where project is stored using 
```code <folder name>``` to open it in VScode


### Downloading Requirements:
Open terminal (after cloning into editor), it will start in the root folder ```<folder name>``` where you cloned the repository

**Navigate to the AI-text-reader folder in terminal**
```cd AI-text-reader ```

-**Once there, activate a virtual environment(using .venv or venv):**

Windows: ``` .\\.venv\\Scripts\\activate ```
Mac/Linux: ``` source .venv/bin/activate ```

-**Download requirements:**

```Python
pip install -r requirements.txt
```

This will download required tools (Summarized):
```
streamlit 1.54.0
GitPython 3.1.46
google-genai 1.67.0
python-dotenv 1.2.1
requests 2.32.5
httpx 0.28.1
Tenacity 9.1.4
pdfplumber 0.11.9
pdfminer.six 20251230
python-docx 1.2.0
pandas 2.3.3
numpy 2.4.2
Jinja2 3.1.6
MarkupSafe 3.0.3
altair 6.0.0
pydeck 0.9.1
pydantic 2.12.5
pillow 12.1.1
```

### Execution
Navigate to ai-summarizer folder
```cd ai-summarizer ```

note: This requires a Google API key from a validated account to communicate with the Gemini AI:

 In ```ai-summarizer```, create a new file called ```.env``` and 
connect your API key to ```GEMINI_API=MY_API_KEY``` inside the file

**Run app.py using streamlit**

```streamlit run app.py``` (press return/enter twice if needed)

**Other ways to execute:**
  
Windows: ```python -m streamlit run app.py```
Mac: ```python3 -m streamlit run app.py```

Here is a screenshot of the application that you first see upon execution:

<img width="1427" height="820" alt="Screenshot 2026-04-27 at 3 51 05 PM" src="https://github.com/user-attachments/assets/6274b98d-6eca-4d38-9f2d-e4ef9281f18e" />





