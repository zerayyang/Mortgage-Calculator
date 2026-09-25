import os

from dotenv import load_dotenv

from openai import OpenAI

from models import MortgageExtraction


# Load API key

load_dotenv()

CHATGPT = OpenAI(

    api_key=os.getenv("OPENAI_API_KEY")

)


# Load extraction agent instructions

with open("agents/extractor.md", "r") as file:

    instructions_provided = file.read()


def extract_mortgage_data(pdf_text):

    response = CHATGPT.responses.parse(

        model="gpt-5.6-luna",

        instructions=instructions_provided,

        input=pdf_text,

        text_format=MortgageExtraction

    )

    mortgage_data = response.output_parsed

    return mortgage_data