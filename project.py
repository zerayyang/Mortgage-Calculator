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
        
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found in this folder.")
