import pymupdf

# purpose is to extract text from the PDF file, 
# return it as texts for the LLM to read and exact the meaning of it(numbers, empty numbers, etc)

def extract_pdf_text(filename): # created function to call for easier extraction of text from PDF file

    # Open the PDF
    pdf = pymupdf.open(filename)

    # Empty string to copy the full text into
    full_text = ""

    # Loop to go through every page
    for page in pdf:
        
        text = page.get_text() # varable to hold the text from each page throughout the loop
        # get_text is a short cut from PyMuPDF

        full_text += text #Adds the texts from each page onto the full_text variable

    # Check if any text was actually extracted
    #Prevents the function from returning an empty string if the PDF is blank or has no text
    if not full_text.strip():
        return None

    # Give the extracted text back to whoever called this function
    return full_text