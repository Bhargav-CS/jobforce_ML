import re
import json
import pdfplumber
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract name, phone, and address
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
    
    print(entities)

    return entities

# Main function
def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    details = extract_details(text)
    return details

# Example usage
if __name__ == "__main__":
    pdf_path = "example.pdf"  # Replace with the path to your PDF
    result = process_pdf(pdf_path)
    print(json.dumps(result, indent=4))