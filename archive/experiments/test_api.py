from google import genai
import os

os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello."
)

print(response.text)