import requests

# Upload a PDF file
upload_url = "http://127.0.0.1:5000/upload"
file_path = "C:\\Users\\gyanu\\Desktop\\Prateek\\Murdoch\\SEPT24\\ICT201\\Topic10.pdf"

with open(file_path, "rb") as file:
    response = requests.post(upload_url, files={"file": file})

pdf_content = response.json().get("content", "")

# Ask a question
ask_url = "http://127.0.0.1:5000/ask"
question = "What is this document about?"

response = requests.post(ask_url, json={"question": question, "content": pdf_content})
print("Chatbot Response:", response.json().get("answer", "Error"))
