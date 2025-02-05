from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hugging Face API Token (Replace with your actual token)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "code")
HF_MODEL = "deepseek-ai/DeepSeek-Coder-7B"

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

    return text[:5000]  # Limit to 5000 characters for API efficiency

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

        api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

        # ✅ Reduce context size to prevent timeout
        limited_text = pdf_content[:2500]  # Only send first 5000 characters

        prompt = f"""
        You are an AI that only answers based on the provided document.
        If the document does not contain the answer, say "I don't know."

        --- DOCUMENT ---
        {limited_text}
        --- END OF DOCUMENT ---

        Question: {question}
        """

        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 300}  # Reduce response size
        }

        # ✅ Lower timeout (20s → 10s) to fail faster
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)

        try:
            response_json = response.json()
        except ValueError:
            return jsonify({'error': 'Invalid API response (not JSON).'}), 500

        # ✅ Check Response Format
        if isinstance(response_json, list) and len(response_json) > 0:
            answer = response_json[0].get("generated_text", "No answer generated.")
        elif isinstance(response_json, dict) and "generated_text" in response_json:
            answer = response_json["generated_text"]
        else:
            answer = response_json.get("error", "Could not generate response.")

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timed out. Try reducing the document size and retry.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': answer})




if __name__ == '__main__':
    app.run(debug=True)
