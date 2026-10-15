from google import genai

api_key="AQ.Ab8RN6KfngRAVYrcUw_v1UMyyRpy_amSiDCNK9HeoSi6nANKGg"

client=genai.Client(api_key=api_key)

prompt="what is ai agent in simple words"


response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)


print(response.text)