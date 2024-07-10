import os
import certifi
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

directory_path = r'..\assets\AndrewHuberman\sleep'
full_path = os.path.abspath(directory_path)

print("Full path:", full_path)
print("Does the directory exist?", os.path.exists(full_path))

print("certifi version:", certifi.__version__)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}]
    )
    print("Connection successful.")
except Exception as e:
    print("An error occurred:", e)