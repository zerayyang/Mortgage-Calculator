import sys
from pdf_reader import extract_pdf_text
from pdf_fallback import extract_pdf_with_ai
from ai_extractor import extract_mortgage_data


# Get the uploaded PDF filename sent by the Node server
pdf_filename = sys.argv[1]

# First try extracting normal PDF text with PyMuPDF
pdf_text = extract_pdf_text(pdf_filename)

# If PyMuPDF cannot read the PDF, use the AI PDF fallback
if pdf_text is None:
    mortgage_data = extract_pdf_with_ai(pdf_filename)

# Otherwise send the extracted text to the AI extraction agent
else:
    mortgage_data = extract_mortgage_data(pdf_text)

# Convert the structured mortgage data into JSON
# and print it so the Node server can receive it
print(mortgage_data.model_dump_json())