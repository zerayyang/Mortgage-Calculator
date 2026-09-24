def validate_mortgage_data(mortgage_data):
    errors = []

   
    income = mortgage_data.annual_income.value
    house_price = mortgage_data.house_price.value
    down_payment = mortgage_data.down_payment.value
    interest_rate = mortgage_data.interest_rate.value
    amortization_years = mortgage_data.amortization_years.value

    if income is None:
        errors.append("Annual income is missing.")

    elif income <= 0:   #can not have negative income or 0 income, as it will not be able to afford any house
        errors.append("Annual income must be greater than 0.")

    if house_price is None: 
        errors.append("House price is missing.")

    elif house_price <= 0:
        errors.append("House price must be greater than 0.")

    if down_payment is None: 
        errors.append("Down payment is missing.")
        #did not add a check for negative down payment, as it is possible to have a negative down payment if the user is taking out a loan to pay for the down payment

    if interest_rate is None: 
        errors.append("Interest rate is missing.")

    elif interest_rate < 0:
        errors.append("Interest rate cannot be negative.")

    if amortization_years is None: 
        errors.append("Amortization period is missing.")
    elif amortization_years <= 0:
        errors.append("Amortization period must be greater than 0.")

    # Check that the down payment does not exceed the house price
    if down_payment is not None and house_price is not None:
        if down_payment > house_price:
            errors.append("Down payment cannot be greater than house price.")
            
    return errors