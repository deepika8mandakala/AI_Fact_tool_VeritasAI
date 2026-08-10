import fitz


def extract_pdf_text(file):

    pdf = fitz.open(
        stream=file.file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text