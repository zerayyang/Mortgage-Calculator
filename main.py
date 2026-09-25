from pdf_reader import extract_pdf_text
from pdf_fallback import extract_pdf_with_ai
from ai_extractor import extract_mortgage_data
from user_correction import verify_mortgage_data
from validator import validate_until_correct
from calculator import calculate_mortgage



# Extract text from PDF using the function defined in pdf_reader.py

# hard coded the PDF file name for now for testing, but will change it to a variable later on so that the user can input the PDF file name

pdf_text = extract_pdf_text("sample_mortgage_application.pdf")



# If PyMuPDF cannot read the PDF, use the AI PDF reader instead

if pdf_text is None:

    print("\nNo readable text found. Trying AI PDF reader...\n")

    mortgage_data = extract_pdf_with_ai("sample_mortgage_application.pdf")

else:

    try:

        mortgage_data = extract_mortgage_data(pdf_text)

    except Exception as error: # Exception is built into python, tells the user that the AI extraction failed and prints the error message

        print("\nAI extraction failed:", error)

        exit()




# Let the user verify and correct the extracted mortgage information

verify_mortgage_data(mortgage_data)


# Validate the mortgage information and keep correcting until it passes

validate_until_correct(mortgage_data)


mortgage_needed, maximum_mortgage, monthly_payment,ltv = calculate_mortgage(mortgage_data)

if mortgage_needed > maximum_mortgage:

    print("\nYou cannot afford this house. \nThe mortgage needed is: ", mortgage_needed, "\nThe maximum mortgage you can afford is: ", maximum_mortgage,"\nThe monthly payment is: ", monthly_payment)

else:

    print("\nYou can afford this house.\nThe mortgage needed is: ", mortgage_needed, "\nThe maximum mortgage you can afford is: ", maximum_mortgage,"\nThe monthly payment is: ", monthly_payment)

