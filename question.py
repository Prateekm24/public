import requests

upload_url = "http://127.0.0.1:5000/upload"
file_path = r"C:\Users\gyanu\csii-chatbot\files\uploads\HRMS.pdf"  # Use raw string (r"")

with open(file_path, "rb") as file:
    response = requests.post(upload_url, files={"file": file})

print(response.json())  # Should print extracted PDF content
