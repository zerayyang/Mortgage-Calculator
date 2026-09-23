import pymupdf


def extract_pdf_text(filename):

    # Open the PDF
    pdf = pymupdf.open(filename)

    # Empty string to store all PDF text
    full_text = ""

    # Go through every page
    for page in pdf:
        text = page.get_text()
        full_text += text

    # Check if any text was actually extracted
    if not full_text.strip():
        return None

    # Give the extracted text back to whoever called this function
    return full_text