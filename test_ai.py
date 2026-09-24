import os
from dotenv import load_dotenv
from openai import OpenAI
from pdf_reader import extract_pdf_text
from validator import validate_mortgage_data
from pydantic import BaseModel


# Define what each extracted field should contain

#Basemodel usegae:
#1. ORGANIZE the data
#2. CHECK that the data follows your rules

class ExtractedField(BaseModel):#Basemodel is a class from pydantic that allows us to create a model for the data we want to extract from the PDF
    value: float | None # so value could be either a number or blank if the LLM could not find it in the PDF
    evidence: str # make sure LLM did not fabricate the numbers, and if it did, it will be able to show the evidence of where it got the number from
    confidence: float # a number between 0 and 1 to show how confident the LLM is in its extraction of the number from the PDF. 1 means it is very confident, 0 means it is not confident at all.


# Define the complete mortgage extraction structure
class MortgageExtraction(BaseModel): #Basemodel is a class from pydantic that allows us to create a model for the data we want to extract from the PDF

    #using the defined class ExtractField to define all the information needed for the mortgage calculation
    annual_income: ExtractedField

    house_price: ExtractedField

    down_payment: ExtractedField

    interest_rate: ExtractedField

    amortization_years: ExtractedField


# Load API key
# python-dotenv reads the .env file (API key locatation) and loads the API key into the environment
load_dotenv()

#From OpenAI library
CHATGPT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") 
)
#api_key defined by OpenAI library, and os.getenv gets the API key from the environment variable defined in the .env file

# Load extraction agent instructions
with open("agents/extractor.md", "r") as file: # named instructions as file
    instructions_provided = file.read() # used python function to read the file & renaming the texts it reads as instructions_provided for easier reference later on


# Extract text from PDF using the function defined in pdf_reader.py
# hard coded the PDF file name for now for testing, but will change it to a variable later on so that the user can input the PDF file name
pdf_text = extract_pdf_text("sample_mortgage_application.pdf")


response = CHATGPT.responses.parse(

    model="gpt-5.6-luna",  # chosen LLM model

    instructions=instructions_provided,  # instructions for extracting the information in extractor.md

    input=pdf_text,  # PDF text that the LLM will analyze, recieved from extarct_pdf_text function in pdf_reader.py

    text_format=MortgageExtraction  # require the response to follow our MortgageExtraction structure

)

# Get the structured result
mortgage_data = response.output_parsed



# setting up the erros for any mistakes in the PDF file 
errors = validate_mortgage_data(mortgage_data)

#Prints the errors if there are any
#looped it for a nicer formatting

total_errors = len(errors)

print(f"\nTotal errors: {total_errors}\n")

for i in range(total_errors):
    print(f"Error[{i + 1}]: {errors[i]}\n")



# Print the result
print(mortgage_data.model_dump_json(indent=3))
#Format the JSON using 3 spaces of indentation so people can read it easily.
