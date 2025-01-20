from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF for PDF text extraction
import openai
import os
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OpenAI API Key (replace with your actual API key)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
openai.api_key = OPENAI_API_KEY

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
            <p>Use the endpoints to upload PDFs and ask questions.</p>
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
        time.sleep(1)  # Wait 1 second before making an API request

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on the provided document."},
                {"role": "user", "content": f"Document: {pdf_content}\n\nQuestion: {question}"}
    ]
)
        answer = response.choices[0].message.content
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
