from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv
from models import MortgageExtraction

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

CHATGPT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


with open(Path(__file__).resolve().parent / "agents" / "extractor.md", "r", encoding="utf-8") as file:
    instructions_provided = file.read()


def extract_pdf_with_ai(filename):

    with open(filename, "rb") as pdf_file: # reads pdf in read binary mode, which is necessary for PDF files

        uploaded_pdf = CHATGPT.files.create(
            file=pdf_file,
            purpose="user_data"
        )


    response = CHATGPT.responses.parse(
    model="gpt-5.6-luna",
    instructions=instructions_provided,
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": uploaded_pdf.id
                }
            ]
        }
    ],
    text_format=MortgageExtraction
)
    return response.output_parsed
