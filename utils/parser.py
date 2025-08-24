import os
from io import BytesIO

def parse_doc_file(upload_file):
    filename = upload_file.filename
    ext = os.path.splitext(filename)[1].lower()
    content = upload_file.file.read()

    if ext == ".pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        import docx
        doc = docx.Document(BytesIO(content))
        text = "\n".join([p.text for p in doc.paragraphs])
    elif ext in [".md", ".txt"]:
        text = content.decode("utf-8", errors="ignore")
    else:
        raise RuntimeError(f"Unsupported file extension: {ext}")

    if not text or not text.strip():
        raise RuntimeError("Parsed document is empty.")

    return text
