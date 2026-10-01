from pathlib import Path

SAMPLE_PDF = Path(__file__).resolve().parents[1] / "Samples" / "sample_mortgage_application.pdf"

from pdf_reader import extract_pdf_text
from pdf_fallback import extract_pdf_with_ai
from ai_extractor import extract_mortgage_data
from user_correction import verify_mortgage_data
from validator import validate_until_correct
from calculator import calculate_mortgage
from ai_analyst import analyze_mortgage



# Extract text from PDF using the function defined in pdf_reader.py

# hard coded the PDF file name for now for testing, but will change it to a variable later on so that the user can input the PDF file name

pdf_text = extract_pdf_text(str(SAMPLE_PDF))



# If PyMuPDF cannot read the PDF, use the AI PDF reader instead

if pdf_text is None:

    print("\nNo readable text found. Trying AI PDF reader...\n")

    mortgage_data = extract_pdf_with_ai(str(SAMPLE_PDF))

else:

    try:

        mortgage_data = extract_mortgage_data(pdf_text)

    except Exception as error: # Exception is built into python, tells the user that the AI extraction failed and prints the error message

        print("\nAI extraction failed:", error)

        exit()




# Let the user verify and correct the extracted mortgage information

verify_mortgage_data(mortgage_data)


# Validate the mortgage information and keep correcting until it passes

validate_until_correct(mortgage_data)



# Calculate the mortgage and store all results in one structured object (defined in models.py)
results = calculate_mortgage(mortgage_data)
# Display the basic mortgage calculation results


print(
    "\nMortgage Calculation Results",
    "\nMortgage needed: $", results.mortgage_needed,
    "\nMonthly payment: $", results.monthly_payment
)

#printing all the values calculated from calculator.py
print("Loan-to-value (LTV):", round(results.ltv, 2), "%")

print("Estimated total interest:", round(results.total_interest, 2))

print(
    "\nAmortization Schedule - First Payment",
    "\nPayment number:", results.amortization_schedule[0]["payment_number"],
    "\nInterest payment: $", results.amortization_schedule[0]["interest_payment"],
    "\nPrincipal payment: $", results.amortization_schedule[0]["principal_payment"],
    "\nRemaining balance: $", results.amortization_schedule[0]["remaining_balance"]
)
print("Gross Debt Service (GDS):", round(results.gds, 2), "%")

print("Total Debt Service (TDS):", round(results.tds, 2), "%")

print("\nMortgage Stress Test")

print("Stress test rate:", round(results.stress_test_rate, 2), "%")

print("Stress test monthly payment: $", round(results.stress_monthly_payment, 2))

print("Stress test GDS:", round(results.stress_gds, 2), "%")

print("Stress test TDS:", round(results.stress_tds, 2), "%")

# Ask the user which type of AI mortgage analysis they want
print("\nAI Mortgage Analysis")
print("1. Serious Mode")
print("2. Surprise Mode")

mode_choice = input("\nChoose analysis mode (1 or 2): ")

# Make sure the user enters a valid choice
while mode_choice not in ["1", "2"]:
    print("Invalid choice. Please enter 1 or 2.")
    mode_choice = input("\nChoose analysis mode (1 or 2): ")

# Convert the user's choice into the analysis mode sent to the AI
if mode_choice == "1":
    analysis_mode = "Serious Mode"
else:
    analysis_mode = "Surprise Mode"

# Send the verified mortgage data and calculated results to the AI analysis agent
analysis = analyze_mortgage(
    mortgage_data,
    results,
    analysis_mode
)

# Display the structured AI mortgage analysis
print("\nAI Mortgage Analysis")

print("\nSummary:")
print(analysis.summary)

print("\nResults Explanation:")
print(analysis.results_explanation)

print("\nStress Test Explanation:")
print(analysis.stress_test_explanation)

print("\nRisks:")
for risk in analysis.risks:
    print("-", risk)

print("\nFinal Analysis:")
print(analysis.final_analysis)