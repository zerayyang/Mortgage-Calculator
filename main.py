from pdf_reader import extract_pdf_text
from pdf_fallback import extract_pdf_with_ai
from ai_extractor import extract_mortgage_data
from user_correction import verify_mortgage_data
from validator import validate_until_correct
from calculator import calculate_mortgage



# Extract text from PDF using the function defined in pdf_reader.py

# hard coded the PDF file name for now for testing, but will change it to a variable later on so that the user can input the PDF file name

pdf_text = extract_pdf_text("sample_mortgage_application.pdf")



# If PyMuPDF cannot read the PDF, use the AI PDF reader instead

if pdf_text is None:

    print("\nNo readable text found. Trying AI PDF reader...\n")

    mortgage_data = extract_pdf_with_ai("sample_mortgage_application.pdf")

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


if results.mortgage_needed > results.maximum_mortgage:

    print("\nYou cannot afford this house. \nThe mortgage needed is: ", results.mortgage_needed, "\nThe maximum mortgage you can afford is: ", results.maximum_mortgage,"\nThe monthly payment is: ", results.monthly_payment)

else:

    print("\nYou can afford this house.\nThe mortgage needed is: ", results.mortgage_needed, "\nThe maximum mortgage you can afford is: ", results.maximum_mortgage,"\nThe monthly payment is: ", results.monthly_payment)



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