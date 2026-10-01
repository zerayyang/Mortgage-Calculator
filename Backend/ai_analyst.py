from pathlib import Path
import sys
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from models import MortgageAnalysis
from analyst_tools import get_mortgage_data, get_calculation_results #fxn from analyst_tools.py to convert the structured data into a dictionary for the AI to analyze

# Load environment variables from the .env file
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Create the OpenAI client using the API key stored in .env
CHATGPT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load the instructions for the mortgage analysis agent
with open(Path(__file__).resolve().parent / "agents" / "analyst.md", "r", encoding="utf-8") as file:
    analyst_instructions = file.read()



# Define the approved tools that the AI analyst is allowed to request
analyst_tools = [
    {
        "type": "function",
        "name": "get_mortgage_data",
        "description": "Get the verified mortgage data extracted from the user's mortgage document.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_calculation_results",
        "description": "Get the verified mortgage calculations produced by the mortgage calculation engine.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def analyze_mortgage(mortgage_data, results, mode):

    # Tell the AI which analysis mode to use and instruct it
    # to retrieve the verified information using its approved tools
    analysis_input = f"""
Analysis Mode: {mode}

Analyze this mortgage using the approved tools available to you.
Use the tools to retrieve the verified mortgage data and calculated mortgage results.
"""

    # Send the request to the AI and give it access to the approved tools
    response = CHATGPT.responses.parse(
        model="gpt-5.6-luna",
        instructions=analyst_instructions,
        input=analysis_input,
        tools=analyst_tools,
        text_format=MortgageAnalysis
    )

    # Check whether the AI requested any approved tools
    tool_outputs = []

    for item in response.output:

        # Check if this output item is a function call
        if item.type == "function_call":

            print("AI requested tool:", item.name, file=sys.stderr)

            # Run the mortgage data tool if the AI requested it
            if item.name == "get_mortgage_data":
                tool_result = get_mortgage_data(mortgage_data)

            # Run the calculation results tool if the AI requested it
            elif item.name == "get_calculation_results":
                tool_result = get_calculation_results(results)

            
            else:
                continue

            # Store the tool result so it can be sent back to the AI
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(tool_result)
            })

    # If the AI requested tools, send the tool results back to it
    if len(tool_outputs) > 0:

        response = CHATGPT.responses.parse(
            model="gpt-5.6-luna",
            instructions=analyst_instructions,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=analyst_tools,
            text_format=MortgageAnalysis
        )

    # Get the structured mortgage analysis from the AI response
    analysis = response.output_parsed

    # Return the structured analysis
    return analysis