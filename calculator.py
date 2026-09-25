def calculate_monthly_rate(interest_rate):
    # Convert the percentage into decimal form
    annual_rate = interest_rate / 100

    # Canadian fixed mortgage rates are compounded semi-annually
    semi_annual_rate = annual_rate / 2

    # Convert the semi-annual rate into an equivalent monthly rate
    monthly_rate = (1 + semi_annual_rate) ** (1 / 6) - 1

    return monthly_rate

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

    monthly_rate = calculate_monthly_rate(interest_rate)  # Calling the function above to calculate the monthly rate using a more accurate Canadian mortgage model

    number_of_payments = amortization_years * 12


    # mortgage calculation formula to calculate the monthly payment

    monthly_payment = (
        mortgage_needed * (monthly_rate * (1 + monthly_rate) ** number_of_payments)
        / ((1 + monthly_rate) ** number_of_payments - 1)
    )


    # rounds up the monthly payment to 2 decimal places for easier reading

    monthly_payment = round(monthly_payment, 2)

    return mortgage_needed, maximum_mortgage, monthly_payment