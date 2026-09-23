import pymupdf

filename = input("Enter PDF filename: ")

pdf = pymupdf.open(filename)

#sets a place for the texts to go to

full_text = ""

for page in pdf:
    text = page.get_text()
    full_text += text

# checks if no text was extracted
if not full_text.strip():
    print("Error: No text could be extracted from the PDF.")
else:
    print(full_text)