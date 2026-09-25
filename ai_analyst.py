import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Create the OpenAI client using the API key stored in .env
CHATGPT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load the instructions for the mortgage analysis agent
with open("agents/analyst.md", "r") as file:
    analyst_instructions = file.read()


def analyze_mortgage(mortgage_data, results, mode):

    # Combine the verified mortgage data and calculated mortgage results
    # into one message for the analysis agent
    analysis_input = f"""
Analysis Mode: {mode}

Verified Mortgage Data:
{mortgage_data.model_dump_json(indent=2)}

Calculated Mortgage Results:
{results.model_dump_json(indent=2)}
"""

    # Send the mortgage information and analyst instructions to the AI
    response = CHATGPT.responses.create(
        model="gpt-5.6-luna",
        instructions=analyst_instructions,
        input=analysis_input
    )

    # Return the AI's mortgage analysis
    return response.output_text