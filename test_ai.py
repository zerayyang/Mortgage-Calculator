import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv() 

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Say: AI connection successful!"
)

print(response.output_text)