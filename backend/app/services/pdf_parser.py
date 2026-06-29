from pypdf import PdfReader

def parse_resume(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    # BROKEN CODE: return was indented inside the loop, so only the first page
    # text was ever returned from the PDF.
    return text