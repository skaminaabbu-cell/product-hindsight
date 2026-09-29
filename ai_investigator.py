import os
from dotenv import load_dotenv
from groq import Groq
from hindsight_connection import client

load_dotenv()

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Ask Hindsight for previous knowledge
query = """
What problems have developers reported in Hyperswitch?
What problems have appeared repeatedly?
What did previous investigations learn?
"""

memory = client.recall(
    bank_id="product-hindsight",
    query=query
)

# Give the memories to Groq
prompt = f"""
You are ProductHindsight, an AI product investigator.

Use ONLY the information in the Hindsight memories below.

Explain:

1. Main developer problems
2. Repeated problems
3. What previous investigations learned
4. Evidence from the memories
5. What should be investigated next

Do not invent information.
Do not claim that one problem caused another unless the evidence clearly shows it.

HINDSIGHT MEMORIES:
{memory}
"""

response = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\n=== PRODUCTHINDSIGHT AI INVESTIGATION ===\n")
print(response.choices[0].message.content)