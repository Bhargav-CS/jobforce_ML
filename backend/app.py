import os
import re
import spacy
import pdfplumber
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemini_process import extract_details_with_gemini

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)  # Enable CORS for all routes
nlp = spacy.load("en_core_web_sm")


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    file_name = path.split('/')[-1]
    dir_name = os.path.join(app.static_folder, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    app.logger.debug("Received request to /upload")
    if 'pdf' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['pdf']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        app.logger.error("File is not a PDF")
        return jsonify({"error": "File is not a PDF"}), 400

    try:
        text = extract_text_from_pdf(file)
        entities = extract_details(text)
        app.logger.debug("Successfully extracted entities")
        return jsonify(entities), 200
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/extract_with_gemini', methods=['POST'])
def extract_with_gemini():
    app.logger.debug("Received request to /extract_with_gemini")
    if 'pdf' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['pdf']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        app.logger.error("File is not a PDF")
        return jsonify({"error": "File is not a PDF"}), 400

    try:
        text = extract_text_from_pdf(file)
        entities = extract_details_with_gemini(text)
        app.logger.debug("Successfully extracted entities with Gemini")
        return jsonify(entities), 200
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_details(text):
    # Using spaCy NER model
    doc = nlp(text)
    entities = {"Name": "", "Phone": "", "Address": ""}
    
    # Extract name (Assuming NER label 'PERSON' for person names)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["Name"]:
            entities["Name"] = ent.text.split('\n')[0].strip()
    
    # Regex for phone number (customize based on locale)
    phone_match = re.search(r'\+?\d{1,2}\s?\(?\d{3}\)?\s?\d{3}-\d{4}', text)
    if phone_match:
        entities["Phone"] = phone_match.group().strip()

    # Extract address (simple heuristic: long continuous text near keywords like 'Address')
    address_match = re.search(r'Address[:\s]*(.*)', text, re.IGNORECASE)
    if address_match:
        entities["Address"] = address_match.group(1).strip()
    else:
        # Fallback: Extract address using spaCy's GPE (Geopolitical Entity) and ORG (Organization) labels
        address_parts = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "ORG"]:
                address_parts.append(ent.text.strip())
        entities["Address"] = ', '.join(address_parts)

    return entities

if __name__ == '__main__':
    app.run(debug=True, port=3000)