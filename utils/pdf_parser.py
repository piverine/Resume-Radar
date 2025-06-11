import fitz

def extract_text_from_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    text=""
    for page in doc:
        text+=page.get_text()
    return text

if __name__=="__main__":
    pdf_path="uploads/resume.pdf"
    print(extract_text_from_pdf(pdf_path))

