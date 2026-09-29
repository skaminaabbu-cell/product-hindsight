from hindsight_connection import client

query = "What problems have developers reported in Hyperswitch?"

result = client.recall(
    bank_id="product-hindsight",
    query=query
)

print("\n=== ProductHindsight Investigation ===")
print(result)