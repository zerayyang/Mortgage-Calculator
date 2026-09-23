import os
from dotenv import load_dotenv
from openai import OpenAI
from pdf_reader import extract_pdf_text
from pydantic import BaseModel


# Define what each extracted field should contain
class ExtractedField(BaseModel):
    value: float
    evidence: str
    confidence: float


# Define the complete mortgage extraction structure
class MortgageExtraction(BaseModel):
    annual_income: ExtractedField
    house_price: ExtractedField
    down_payment: ExtractedField
    interest_rate: ExtractedField
    amortization_years: ExtractedField


# Load API key
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Load extraction agent instructions
with open("agents/extractor.md", "r") as file:
    instructions = file.read()


# Extract text from PDF
pdf_text = extract_pdf_text("sample_mortgage_application.pdf")


# Send PDF text to AI and force it into our structure
response = client.responses.parse(
    model="gpt-5.6-luna",
    instructions=instructions,
    input=pdf_text,
    text_format=MortgageExtraction
)


# Get the structured result
mortgage_data = response.output_parsed


# Print the result
print(mortgage_data.model_dump_json(indent=2)) ## easier formatting to read the output