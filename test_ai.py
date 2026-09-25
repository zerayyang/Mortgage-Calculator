from pdf_reader import extract_pdf_text

from validator import validate_until_correct

from pdf_fallback import extract_pdf_with_ai

from ai_extractor import extract_mortgage_data

from user_correction import correct_value, verify_mortgage_data








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









# Print the result

print(mortgage_data.model_dump_json(indent=3))

# Format the JSON using 3 spaces of indentation so people can read it easily.






verify_mortgage_data(mortgage_data)






# setting up the erros for any mistakes in the PDF file
validate_until_correct(mortgage_data)