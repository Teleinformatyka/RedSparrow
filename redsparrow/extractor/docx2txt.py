from docx import Document

def docx_to_text(path):
    doc = Document(path)
    result = ''
    for paragraph in doc.paragraphs:
        result += paragraph.text
    return result


