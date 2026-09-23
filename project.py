# main.py

# takes a file and reads through it
# initial setup for file reading
filename = input("Enter file name: ")

# uses r to read the numbers inside the file
try:
    with open(filename, "r") as file:

        content = file.read()
        print("\n--- File Content Below ---")
        print(content)
        
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found in this folder.")
