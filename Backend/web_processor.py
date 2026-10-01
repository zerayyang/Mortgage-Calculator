import sys
from pdf_reader import extract_pdf_text
from pdf_fallback import extract_pdf_with_ai
from ai_extractor import extract_mortgage_data


# Get the uploaded PDF filename sent by the Node server
pdf_filename = sys.argv[1]

# First try extracting normal PDF text with PyMuPDF
pdf_text = extract_pdf_text(pdf_filename)


# Check whether readable text appears to be mortgage-related
def is_mortgage_document(text):

    mortgage_keywords = [
        "mortgage",
        "mortgage application",
        "loan amount",
        "down payment",
        "purchase price",
        "property value",
        "interest rate",
        "amortization",
        "borrower",
        "property taxes",
        "principal",
        "lender"
    ]

    text = text.lower()

    matches = 0

    for keyword in mortgage_keywords:

        if keyword in text:
            matches += 1

    # Require at least 2 mortgage-related terms
    return matches >= 2


# If PyMuPDF cannot read the PDF, use the AI PDF fallback
if pdf_text is None:

    mortgage_data = extract_pdf_with_ai(pdf_filename)

# Otherwise check the document before sending it to the extraction agent
else:

    if not is_mortgage_document(pdf_text):

        print(
            "ERROR: This does not appear to be a mortgage-related document.",
            file=sys.stderr
        )

        sys.exit(1)

    mortgage_data = extract_mortgage_data(pdf_text)


# Convert the structured mortgage data into JSON
# and print it so the Node server can receive it
print(mortgage_data.model_dump_json())