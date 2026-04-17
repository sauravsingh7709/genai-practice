import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text="Hello i am saurav"

tokens=enc.encode(text)
print("Token is:",tokens)
tokens=[13225, 575, 939, 96446, 407]
decoded=enc.decode(tokens)
print(decoded)