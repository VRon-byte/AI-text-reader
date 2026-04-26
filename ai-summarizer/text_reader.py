import os
from typing import Optional
import requests
import PyPDF2
import docx
from bs4 import BeautifulSoup
import validators


class TextReader:
    """Extract text from files (.txt, .pdf, .docx) and URLs"""

    def __init__(self):
        self.supported_files = {
            '.txt': self._read_txt,
            '.pdf': self._read_pdf,
            '.docx': self._read_docx
        }

    def extract_from_file(self, file_path: str) -> Optional[str]:
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' not found."
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.supported_files:
                return self.supported_files[ext](file_path)
            return f"Error: Unsupported file type '{ext}'."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def extract_from_upload(self, uploaded_file) -> Optional[str]:
        try:
            file_name = uploaded_file.name
            ext = os.path.splitext(file_name)[1].lower()

            if ext == '.txt':
                return uploaded_file.getvalue().decode('utf-8')

            elif ext == '.pdf':
                with open("temp_scholar.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())
                text = self._read_pdf("temp_scholar.pdf")
                os.remove("temp_scholar.pdf")
                return text

            elif ext == '.docx':
                with open("temp_scholar.docx", "wb") as f:
                    f.write(uploaded_file.getvalue())
                text = self._read_docx("temp_scholar.docx")
                os.remove("temp_scholar.docx")
                return text

            return f"Unsupported file type: {ext}"
        except Exception as e:
            return f"Error: {str(e)}"

    def extract_from_url(self, url: str) -> Optional[str]:
        try:
            if not validators.url(url):
                return "Error: Invalid URL format"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            text = ' '.join(line for line in lines if line)
            return text[:10000] if len(text) > 10000 else text
        except Exception as e:
            return f"Error fetching URL: {str(e)}"

    def _read_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _read_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text

    def _read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])