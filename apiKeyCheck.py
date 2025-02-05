import requests

ask_url = "http://127.0.0.1:5000/ask"

payload = {
    "question": "what is the document about and list the table of contents?",
    "content": "Extracted text from the PDF goes here..."
}

response = requests.post(ask_url, json=payload)

print(response.json())  # Should print the chatbot's answer
