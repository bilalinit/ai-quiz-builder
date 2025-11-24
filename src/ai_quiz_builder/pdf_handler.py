import pypdf
import io

def extract_text(pdf_bytes): # Renamed parameter from pdf_file to pdf_bytes
    try:
        # Wrap the bytes directly in an io.BytesIO object for pypdf
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        # Clean whitespace: replace multiple newlines/spaces with a single space
        cleaned_text = " ".join(text.split()).strip()
        return cleaned_text
    except Exception as e:
        return f"Error extracting PDF text: {e}"