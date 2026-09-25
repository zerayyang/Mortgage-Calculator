

def calculate_mortgage(mortgage_data):

    # Get the mortgage values from the extracted mortgage data

    income = mortgage_data.annual_income.value

    house_price = mortgage_data.house_price.value

    down_payment = mortgage_data.down_payment.value

    interest_rate = mortgage_data.interest_rate.value

    amortization_years = mortgage_data.amortization_years.value


    # basic mortgage calculation formula to calculate the monthly payment and check if the user can afford the house

    mortgage_needed = house_price - down_payment

    maximum_mortgage = income * 4

    annual_rate = interest_rate / 100

    monthly_rate = annual_rate / 12

    number_of_payments = amortization_years * 12


    # mortgage calculation formula to calculate the monthly payment

    monthly_payment = (
        mortgage_needed * (monthly_rate * (1 + monthly_rate) ** number_of_payments)
        / ((1 + monthly_rate) ** number_of_payments - 1)
    )


    # rounds up the monthly payment to 2 decimal places for easier reading

    monthly_payment = round(monthly_payment, 2)

    return mortgage_needed, maximum_mortgage, monthly_payment