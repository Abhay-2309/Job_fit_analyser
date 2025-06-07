import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Could not find GOOGLE_API_KEY in your .env file.")
    exit()

print("Fetching available models...\n")

# List all available models
for m in genai.list_models():
  # Check if the 'generateContent' method is supported
  if 'generateContent' in m.supported_generation_methods:
    print(f"Model found: {m.name}")
    print("--------------------")