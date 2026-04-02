import io
import re
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    text_parts = []
    try:
        pdf_bytes = io.BytesIO(uploaded_file.read())
        reader = PyPDF2.PdfReader(pdf_bytes)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    except Exception as e:
        return f"[Error: {e}]"
    full_text = "\n".join(text_parts)
    full_text = re.sub(r"[ \t]+", " ", full_text)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    return full_text.strip()
