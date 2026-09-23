# main.py

# takes a file and reads through it
# initial setup for file reading
filename = input("Enter file name: ")

# uses r to read the numbers inside the file
try:
    with open(filename, "r") as file:

        for line in file:

            # to see what is being read in the file
            print(line) 

            parts=(line.split(":"))

            value = float(parts[1])

            if parts[0] == "Income":
                income = value

            elif parts[0] == "House Price":
                house_price = value

            elif parts[0] == "Down Payment":
                down_payment = value

            elif parts[0] == "Interest Rate":
                interest_rate = value

            elif parts[0] == "Amortization Years":
                amortization_years = value
        
    mortgage_needed = house_price - down_payment

    maximum_mortgage = income * 4

    annual_rate = interest_rate / 100
    monthly_rate = annual_rate / 12
    number_of_payments = amortization_years * 12

    monthly_payment =( mortgage_needed * (monthly_rate * (1 + monthly_rate) ** number_of_payments)/
    ((1 + monthly_rate) ** number_of_payments - 1) )
    monthly_payment = round(monthly_payment, 2)

    if( mortgage_needed > maximum_mortgage):
        print("\nYou cannot afford this house. \nThe mortgage needed is: ", mortgage_needed, "\nThe maximum mortgage you can afford is: ", maximum_mortgage,"\nThe monthly payment is: ", monthly_payment)

    else:
        print("\nYou can afford this house.\nThe mortgage needed is: ", mortgage_needed, "\nThe maximum mortgage you can afford is: ", maximum_mortgage,"\nThe monthly payment is: ", monthly_payment)
        
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found in this folder.")
