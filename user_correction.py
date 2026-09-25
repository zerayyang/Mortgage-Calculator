def correct_value(mortgage_data):

    print("Which value would you like to correct?")

    print("1. Annual income")

    print("2. House price")

    print("3. Down payment")

    print("4. Interest rate")

    print("5. Amortization years")

    choice = input("\nEnter 1-5: ")

    while choice not in ["1", "2", "3", "4", "5"]:

        print("Invalid choice. Please enter a number from 1-5.")

        choice = input("\nEnter 1-5: ")

    if choice == "1":

        while True:

            try:

                new_value = float(input("Enter the correct annual income: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.annual_income.value = new_value

        print(f"Annual income changed to: ${mortgage_data.annual_income.value}")

    elif choice == "2":

        while True:

            try:

                new_value = float(input("Enter the correct house price: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.house_price.value = new_value

        print(f"House price changed to: ${mortgage_data.house_price.value}")

    elif choice == "3":

        while True:

            try:

                new_value = float(input("Enter the correct down payment: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.down_payment.value = new_value

        print(f"Down payment changed to: ${mortgage_data.down_payment.value}")

    elif choice == "4":

        while True:

            try:

                new_value = float(input("Enter the correct interest rate: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.interest_rate.value = new_value

        print(f"Interest rate changed to: {mortgage_data.interest_rate.value}%")

    elif choice == "5":

        while True:

            try:

                new_value = float(input("Enter the correct amortization years: "))

                break

            except ValueError:

                print("Invalid input. Please enter a number.")

        mortgage_data.amortization_years.value = new_value

        print(f"Amortization changed to: {mortgage_data.amortization_years.value} years")


def verify_mortgage_data(mortgage_data):

    answer = input("\nHuman Verification:\nAre the extracted values correct? (yes/no): ")

    while answer.lower() not in ["yes", "no"]:

        print("Invalid input. Please enter yes or no.")

        answer = input("Are the extracted values correct? (yes/no): ")

    if answer.lower() == "yes":

        print("\nMortgage information confirmed by user.\n")

    elif answer.lower() == "no":

        correcting = True

        while correcting:

            print("Human Verification:")

            correct_value(mortgage_data)

            another = input("\nWould you like to correct another value? (yes/no): ")

            while another.lower() not in ["yes", "no"]:

                print("Invalid input. Please enter yes or no.")

                another = input("\nWould you like to correct another value? (yes/no): ")

            if another.lower() == "no":

                correcting = False