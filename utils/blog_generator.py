import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

def generate_blog(chunks, code_snippets=None, temperature=0.3):
    """Generate blog with automatic code integration"""
    llm = AzureChatOpenAI(
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=temperature
    )

    notes = ' '.join(chunks)
    code_text = "\n\n".join([f"```python\n{snippet}\n```" for snippet in code_snippets]) if code_snippets else ""

    prompt = ChatPromptTemplate.from_template("""
    Create a technical blog post from this video transcript and extracted code:
    
    Transcript:
    {notes}
    
    Extracted Code:
    {code_snippets}
    
    Requirements:
    1. Title with primary programming language
    2. Introduction explaining concepts
    3. Organized sections with headings
    4. Integrated code snippets with explanations
    5. Practical examples
    6. Conclusion with key takeaways
    7. Professional but approachable tone
    """)

    chain = prompt | llm
    return chain.invoke({"notes": notes, "code_snippets": code_text}).content