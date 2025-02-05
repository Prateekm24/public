from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
import os
from flask_cors import CORS
from llama_cpp import Llama

app = Flask(__name__)
CORS(app)

# Load Local AI Model (Replace with actual model path)
llm = Llama(model_path="C:\Users\gyanu\models\mistral-7B-v0.1")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file safely with error handling."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                extracted_text = page.get_text("text").strip()
                if extracted_text:  # Avoid adding empty text
                    text += extracted_text + "\n"
    except Exception as e:
        print("Error extracting text:", e)
        return "ERROR: Could not extract text from PDF."

    if not text.strip():
        return "ERROR: Extracted text is empty or unreadable."

    return text[:10000]  # Limit to 10000 characters for processing efficiency

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
    
    # Debugging Print (Check if PDF text is correct)
    print("Extracted PDF Text (First 500 chars):", extracted_text[:500])

    return jsonify({'message': 'File uploaded successfully', 'content': extracted_text})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    pdf_content = data.get('content')

    if not question or not pdf_content:
        return jsonify({'error': 'Missing question or PDF content'}), 400

    try:
        # 🚀 Debugging Print
        print("\n📌 Received Question:", question)
        print("📌 Extracted PDF Content (First 500 chars):", pdf_content[:500])

        # ✅ Run AI Model Locally
        prompt = f"""
        You are an AI that only answers based on the provided document.
        If the document does not contain the answer, say "I don't know."

        --- DOCUMENT ---
        {pdf_content[:10000]}
        --- END OF DOCUMENT ---

        Question: {question}
        """

        response = llm(prompt, max_tokens=300)
        answer = response["choices"][0]["text"]
    
    except Exception as e:
        print("🚨 Error:", e)  # Debugging AI errors
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
