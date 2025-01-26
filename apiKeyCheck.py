import requests

ask_url = "http://127.0.0.1:5000/ask"

payload = {
    "question": "What is this document about?",
    "content": "Extracted text from the PDF goes here..."
}

response = requests.post(ask_url, json=payload)

print(response.json())  # Should print the chatbot's answer
