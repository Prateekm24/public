from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hugging Face API Token (Replace with your actual token)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "api_key")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")
    except Exception as e:
        return str(e)
    return text

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>CSII Chatbot API</title>
        </head>
        <body>
            <h1>Welcome to the CSII Chatbot API</h1>
            <p>Upload a PDF and ask questions about its content.</p>
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    
    extracted_text = extract_text_from_pdf(file_path)
    return jsonify({'message': 'File uploaded successfully', 'content': extracted_text})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    pdf_content = data.get('content')
    
    if not question or not pdf_content:
        return jsonify({'error': 'Missing question or PDF content'}), 400
    
    try:
        api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": f"Document: {pdf_content}\n\nQuestion: {question}",
            "parameters": {"max_length": 200}
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response_json = response.json()
        
        if isinstance(response_json, list) and len(response_json) > 0:
            answer = response_json[0].get("generated_text", "No answer generated.")
        else:
            answer = response_json.get("error", "Could not generate response.")

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
