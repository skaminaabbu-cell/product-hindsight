from hindsight_connection import client

query = """
What did ProductHindsight learn from previous investigations
about developer problems in Hyperswitch?
"""

result = client.recall(
    bank_id="product-hindsight",
    query=query
)

print("\n=== PRODUCTHINDSIGHT MEMORY ===\n")
print(result)