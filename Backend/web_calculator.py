import sys
import json

from models import MortgageExtraction
from calculator import calculate_mortgage


# Read the mortgage data sent by the Node server
input_data = json.loads(sys.stdin.read())


# Convert the JSON into the same structured model
# used by the rest of the Python mortgage system
mortgage_data = MortgageExtraction.model_validate(input_data)


# Calculate the mortgage using the verified information
results = calculate_mortgage(mortgage_data)


# Return the structured calculation results to Node
print(results.model_dump_json())