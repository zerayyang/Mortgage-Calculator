import sys
import json

from models import MortgageExtraction, MortgageCalculationResult
from ai_analyst import analyze_mortgage


# Read the JSON data sent from the Node.js server
input_data = json.loads(sys.stdin.read())


# Get the mortgage data from the JSON
mortgage_data_json = input_data["mortgageData"]


# Get the mortgage calculation results from the JSON
calculation_results_json = input_data["calculationResults"]


# Get the analysis mode chosen by the mortgage agent
mode = input_data["mode"]


# Convert the mortgage JSON data back into the
# MortgageExtraction Pydantic model
mortgage_data = MortgageExtraction.model_validate(
    mortgage_data_json
)


# Convert the calculation JSON data back into the
# MortgageCalculationResult Pydantic model
calculation_results = MortgageCalculationResult.model_validate(
    calculation_results_json
)


# Send the verified mortgage information and calculations
# to our existing mortgage analysis system
analysis = analyze_mortgage(
    mortgage_data,
    calculation_results,
    mode
)


# Convert the structured MortgageAnalysis result into JSON
# and print it so the Node.js server can receive it
print(analysis.model_dump_json())