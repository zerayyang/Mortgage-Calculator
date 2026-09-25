from pydantic import BaseModel

#Basemodel usegae:
#1. ORGANIZE the data
#2. CHECK that the data follows your rules

class ExtractedField(BaseModel):#Basemodel is a class from pydantic that allows us to create a model for the data we want to extract from the PDF
    value: float | None # so value could be either a number or blank if the LLM could not find it in the PDF
    evidence: str # make sure LLM did not fabricate the numbers, and if it did, it will be able to show the evidence of where it got the number from
    confidence: float # a number between 0 and 1 to show how confident the LLM is in its extraction of the number from the PDF. 1 means it is very confident, 0 means it is not confident at all.


# Define the complete mortgage extraction structure
class MortgageExtraction(BaseModel): #Basemodel is a class from pydantic that allows us to create a model for the data we want to extract from the PDF

    #using the defined class ExtractField to define all the information needed for the mortgage calculation
    annual_income: ExtractedField

    house_price: ExtractedField

    down_payment: ExtractedField

    interest_rate: ExtractedField

    amortization_years: ExtractedField

    property_taxes: ExtractedField

    heating_cost: ExtractedField

    condo_fees: ExtractedField

    monthly_debt_payments: ExtractedField


class MortgageCalculationResult(BaseModel):
    mortgage_needed: float
    monthly_payment: float
    ltv: float
    total_interest: float
    amortization_schedule: list
    gds: float
    tds: float
    stress_test_rate: float
    stress_monthly_payment: float
    stress_gds: float
    stress_tds: float


class MortgageAnalysis(BaseModel):
    summary: str
    results_explanation: str
    stress_test_explanation: str
    risks: list[str]
    final_analysis: str