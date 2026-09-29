from hindsight_connection import client

client.retain(
    bank_id="product-hindsight",
    content="ProductHindsight found recurring developer problems in Hyperswitch GitHub issues."
)

print("Investigation saved to Hindsight memory!")