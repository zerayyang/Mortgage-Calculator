def calculate_monthly_rate(interest_rate):
    # Convert the percentage into decimal form
    annual_rate = interest_rate / 100

    # Canadian fixed mortgage rates are compounded semi-annually
    semi_annual_rate = annual_rate / 2

    # Convert the semi-annual rate into an equivalent monthly rate
    monthly_rate = (1 + semi_annual_rate) ** (1 / 6) - 1

    return monthly_rate

def calculate_ltv(mortgage_needed, house_price):
     # Calculate what percentage of the house price is financed by the mortgage
    ltv = (mortgage_needed / house_price) * 100
    return ltv #Loan-to-Value ratio.


def calculate_total_interest(mortgage_needed, monthly_payment, number_of_payments):

    # Calculate the total amount paid over the entire amortization
    total_paid = monthly_payment * number_of_payments

    # Subtract the original mortgage to find the total interest paid
    total_interest = total_paid - mortgage_needed

    return total_interest

def calculate_amortization_schedule(
    mortgage_needed,
    monthly_payment,
    monthly_rate,
    number_of_payments
):

    # Start the remaining balance at the original mortgage amount
    balance = mortgage_needed

    # Store the information for each monthly payment
    schedule = []

    # Go through every monthly mortgage payment
    for payment_number in range(1, number_of_payments + 1):

        # Calculate the interest charged on the remaining balance this month
        interest_payment = balance * monthly_rate

        # Calculate how much of the monthly payment goes toward paying off the mortgage
        principal_payment = monthly_payment - interest_payment

        # Reduce the remaining mortgage balance by the principal paid
        balance = balance - principal_payment

        # Store this month's mortgage information in the schedule
        schedule.append({
            "payment_number": payment_number,
            "interest_payment": round(interest_payment, 2),
            "principal_payment": round(principal_payment, 2),
            "remaining_balance": round(balance, 2)
        })

    return schedule


#Gross Debt Service (GDS) ratio
def calculate_gds(
    annual_income,
    monthly_payment,
    property_taxes,
    heating_cost,
    condo_fees
):
    # Convert annual income into monthly income
    monthly_income = annual_income / 12

    # Convert annual property taxes into a monthly cost
    monthly_property_taxes = property_taxes / 12


    # Calculate total monthly housing costs

    monthly_housing_costs = (
        monthly_payment
        + monthly_property_taxes
        + heating_cost
        + (condo_fees * 0.5)
    )

    # Calculate the percentage of gross monthly income used for housing costs
    gds = (monthly_housing_costs / monthly_income) * 100

    return gds


#TDS (Total Debt Service).
def calculate_tds(
    annual_income,
    monthly_payment,
    property_taxes,
    heating_cost,
    condo_fees,
    monthly_debt_payments
):

    # Convert annual income into monthly income
    monthly_income = annual_income / 12

    # Convert annual property taxes into a monthly cost
    monthly_property_taxes = property_taxes / 12

    # Calculate total monthly housing costs
    monthly_housing_costs = (
        monthly_payment
        + monthly_property_taxes
        + heating_cost
        + (condo_fees * 0.5)
    )

    # Add other monthly debt payments to the housing costs
    total_monthly_debt_costs = monthly_housing_costs + monthly_debt_payments

    # Calculate the percentage of gross monthly income used for housing and debt
    tds = (total_monthly_debt_costs / monthly_income) * 100

    return tds

#main calculator function to calculate the mortgage needed, maximum mortgage, and monthly payment based on the extracted mortgage data
def calculate_mortgage(mortgage_data):

    # Get the mortgage values from the extracted mortgage data

    income = mortgage_data.annual_income.value

    house_price = mortgage_data.house_price.value

    down_payment = mortgage_data.down_payment.value

    interest_rate = mortgage_data.interest_rate.value

    amortization_years = mortgage_data.amortization_years.value

    property_taxes = mortgage_data.property_taxes.value

    heating_cost = mortgage_data.heating_cost.value

    condo_fees = mortgage_data.condo_fees.value

    monthly_debt_payments = mortgage_data.monthly_debt_payments.value


    # basic mortgage calculation formula to calculate the monthly payment and check if the user can afford the house

    mortgage_needed = house_price - down_payment

    ltv = calculate_ltv(mortgage_needed, house_price)  # Calculate the loan-to-value percentage

    maximum_mortgage = income * 4

    monthly_rate = calculate_monthly_rate(interest_rate)  # Calling the function above to calculate the monthly rate using a more accurate Canadian mortgage model

    number_of_payments = int(amortization_years * 12) # changed into int so it dont show erorr as float


    # mortgage calculation formula to calculate the monthly payment

    monthly_payment = (
        mortgage_needed * (monthly_rate * (1 + monthly_rate) ** number_of_payments)
        / ((1 + monthly_rate) ** number_of_payments - 1)
    )


    # rounds up the monthly payment to 2 decimal places for easier reading

    monthly_payment = round(monthly_payment, 2)




    amortization_schedule = calculate_amortization_schedule(
    mortgage_needed,
    monthly_payment,
    monthly_rate,
    number_of_payments
)



    total_interest = calculate_total_interest(mortgage_needed, monthly_payment, number_of_payments)



    gds = calculate_gds(
    income,
    monthly_payment,
    property_taxes,
    heating_cost,
    condo_fees
)

    tds = calculate_tds(
    income,
    monthly_payment,
    property_taxes,
    heating_cost,
    condo_fees,
    monthly_debt_payments
)

    return mortgage_needed, maximum_mortgage, monthly_payment, ltv, total_interest, amortization_schedule, gds, tds