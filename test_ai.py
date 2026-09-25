from pdf_reader import extract_pdf_text

from validator import validate_mortgage_data

from pdf_fallback import extract_pdf_with_ai

from ai_extractor import extract_mortgage_data

from user_correction import correct_value








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



answer = input("\nHuman Verification:\nAre the extracted values correct? (yes/no): ")

while answer.lower() not in ["yes", "no"]:

    print("Invalid input. Please enter yes or no.")

    answer = input("Are the extracted values correct? (yes/no): ")

if answer.lower() == "yes":

    print("\nMortgage information confirmed by user.\n")

elif answer.lower() == "no":

    correcting = True

    while correcting:

        print("Human Verification:")

        correct_value(mortgage_data)

        another = input("\nWould you like to correct another value? (yes/no): ")

        while another.lower() not in ["yes", "no"]:

            print("Invalid input. Please enter yes or no.")

            another = input("\nWould you like to correct another value? (yes/no): ")

        if another.lower() == "no":

            correcting = False

# setting up the erros for any mistakes in the PDF file

errors = validate_mortgage_data(mortgage_data)

while len(errors) > 0:

    # Prints the errors if there are any

    # looped it for a nicer formatting

    total_errors = len(errors)

    print(f"\nTotal errors (machine check): {total_errors}\n")

    for i in range(total_errors):

        print(f"Error[{i + 1}]: {errors[i]}\n")

    print("The mortgage information contains invalid values.")

    print("\nPlease correct the invalid information.")

    correct_value(mortgage_data)

    # Check the values again after the correction

    errors = validate_mortgage_data(mortgage_data)

print("\nMortgage information passed machine validation.")