import sys
import json

from models import MortgageExtraction, MortgageCalculationResult
from ai_analyst import analyze_mortgage


# Read everything Node sends through stdin
input_data = json.loads(sys.stdin.read())


# Rebuild the structured Python models
mortgage_data = MortgageExtraction.model_validate(
    input_data["mortgageData"]
)

calculation_results = MortgageCalculationResult.model_validate(
    input_data["calculationResults"]
)

mode = input_data["mode"]


# Run the existing AI analyst
analysis = analyze_mortgage(
    mortgage_data,
    calculation_results,
    mode
)


# IMPORTANT:
# stdout must contain only JSON because Node parses it
print(analysis.model_dump_json())