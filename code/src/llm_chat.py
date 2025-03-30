from google import genai
from google.genai import errors
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
def prompt_model(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt.splitlines()
        )
        return True, response.text
    except errors.APIError as e:
        return False, e.message