import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

print("Hindsight client connected!")
bank = client.create_bank(
    bank_id="product-hindsight",
    name="ProductHindsight"
)

print("Memory bank created!")
client.retain(
    bank_id="product-hindsight",
    content="A developer reported a connector configuration problem in Hyperswitch."
)

print("Memory saved!")
result = client.recall(
    bank_id="product-hindsight",
    query="Have we seen a connector configuration problem before?"
)

print("Recalled memory:")
print(result)