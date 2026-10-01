from email import errors

from user_correction import correct_value


def validate_mortgage_data(mortgage_data):
    errors = []

   
    income = mortgage_data.annual_income.value
    house_price = mortgage_data.house_price.value
    down_payment = mortgage_data.down_payment.value
    interest_rate = mortgage_data.interest_rate.value
    amortization_years = mortgage_data.amortization_years.value
    property_taxes = mortgage_data.property_taxes.value
    heating_cost = mortgage_data.heating_cost.value
    condo_fees = mortgage_data.condo_fees.value
    monthly_debt_payments = mortgage_data.monthly_debt_payments.value

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

    if property_taxes is None:
        errors.append("Property taxes are missing.")
    elif property_taxes < 0:
        errors.append("Property taxes cannot be negative.")

    if heating_cost is None:
        errors.append("Heating cost is missing.")
    elif heating_cost < 0:
        errors.append("Heating cost cannot be negative.")

    if condo_fees is None: 
        errors.append("Condo fees are missing.")
    elif condo_fees < 0:
        errors.append("Condo fees cannot be negative.")

    if monthly_debt_payments is None:
        errors.append("Monthly debt payments are missing.")
    elif monthly_debt_payments < 0:
        errors.append("Monthly debt payments cannot be negative.")

    return errors



def validate_until_correct(mortgage_data):

    errors = validate_mortgage_data(mortgage_data)

    while len(errors) > 0:

        # Prints the errors if there are any

        # looped it for a nicer formatting

        total_errors = len(errors)

        print(f"\nTotal errors (machine check): {total_errors}\n")

        for i in range(total_errors):

            print(f"Error[{i + 1}]: {errors[i]}\n")

        print("The mortgage information contains invalid values.")

        print("\nPlease correct the invalid information.")

        correct_value(mortgage_data)

        # Check the values again after the correction

        errors = validate_mortgage_data(mortgage_data)

    print("\nMortgage information passed machine validation.")