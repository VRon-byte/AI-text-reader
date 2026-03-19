from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API")

client = genai.Client(api_key=api_key)

def summarize(text):
    prompt = f'Summarize any content in key points with the request of the user, and/or have a discussion: \n{text}'
    summarized_text = client.models.generate_content(model="gemini-2.5-flash-lite",
    contents=prompt)
    return summarized_text.text