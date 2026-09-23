import pymupdf

filename = input("Enter PDF filename: ")

pdf = pymupdf.open(filename)

#sets a place for the texts to go to

full_text = ""

for page in pdf:
    text = page.get_text()
    full_text += text

print(full_text)   