def validate_mortgage_data(mortgage_data):
    errors = []

   
    income = mortgage_data.annual_income.value
    house_price = mortgage_data.house_price.value
    down_payment = mortgage_data.down_payment.value
    interest_rate = mortgage_data.interest_rate.value
    amortization_years = mortgage_data.amortization_years.value

    if income is None:
        errors.append("Annual income is missing.")

    if house_price is None: 
        errors.append("House price is missing.")

    if down_payment is None: 
        errors.append("Down payment is missing.")

    if interest_rate is None: 
        errors.append("Interest rate is missing.")

    if amortization_years is None: 
        errors.append("Amortization period is missing.")
        
    return errors