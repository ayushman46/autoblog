import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def generate_blog(chunks):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Create a blog post from these notes: {''.join(chunks)}"
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"API Error: {str(e)}")