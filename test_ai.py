import os

from dotenv import load_dotenv

from openai import OpenAI

from pdf_reader import extract_pdf_text

from validator import validate_mortgage_data

from models import MortgageExtraction

from pdf_fallback import extract_pdf_with_ai





# Load API key

# python-dotenv reads the .env file (API key locatation) and loads the API key into the environment

load_dotenv()

# From OpenAI library

CHATGPT = OpenAI(

    api_key=os.getenv("OPENAI_API_KEY") 

)

# api_key defined by OpenAI library, and os.getenv gets the API key from the environment variable defined in the .env file





# Load extraction agent instructions

with open("agents/extractor.md", "r") as file: # named instructions as file

    instructions_provided = file.read() # used python function to read the file & renaming the texts it reads as instructions_provided for easier reference later on





# Extract text from PDF using the function defined in pdf_reader.py

# hard coded the PDF file name for now for testing, but will change it to a variable later on so that the user can input the PDF file name

pdf_text = extract_pdf_text("sample_mortgage_application.pdf")









# If PyMuPDF cannot read the PDF, use the AI PDF reader instead

if pdf_text is None:

    print("\nNo readable text found. Trying AI PDF reader...\n")

    mortgage_data = extract_pdf_with_ai("sample_mortgage_application.pdf")

else:

    try:

        response = CHATGPT.responses.parse(

            model="gpt-5.6-luna", # chosen LLM model

            instructions=instructions_provided, # instructions from extractor.md

            input=pdf_text, # extracted PDF text

            text_format=MortgageExtraction # require MortgageExtraction structure

        )

# Get the structured result

        mortgage_data = response.output_parsed

    except Exception as error: # Exception is built into python, tells the user that the AI extraction failed and prints the error message

        print("\nAI extraction failed:", error)

        exit()





# Print the result

print(mortgage_data.model_dump_json(indent=3))

# Format the JSON using 3 spaces of indentation so people can read it easily.

def correct_value(mortgage_data):

    print("Which value would you like to correct?")

    print("1. Annual income")

    print("2. House price")

    print("3. Down payment")

    print("4. Interest rate")

    print("5. Amortization years")

    choice = input("\nEnter 1-5: ")

    while choice not in ["1", "2", "3", "4", "5"]:

        print("Invalid choice. Please enter a number from 1-5.")

        choice = input("\nEnter 1-5: ")

    if choice == "1":

        while True:

            try:

                new_value = float(input("Enter the correct annual income: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.annual_income.value = new_value

        print(f"Annual income changed to: ${mortgage_data.annual_income.value}")

    elif choice == "2":

        while True:

            try:

                new_value = float(input("Enter the correct house price: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.house_price.value = new_value

        print(f"House price changed to: ${mortgage_data.house_price.value}")

    elif choice == "3":

        while True:

            try:

                new_value = float(input("Enter the correct down payment: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.down_payment.value = new_value

        print(f"Down payment changed to: ${mortgage_data.down_payment.value}")

    elif choice == "4":

        while True:

            try:

                new_value = float(input("Enter the correct interest rate: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.interest_rate.value = new_value

        print(f"Interest rate changed to: {mortgage_data.interest_rate.value}%")

    elif choice == "5":

        while True:

            try:

                new_value = float(input("Enter the correct amortization years: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.amortization_years.value = new_value

        print(f"Amortization changed to: {mortgage_data.amortization_years.value} years")


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