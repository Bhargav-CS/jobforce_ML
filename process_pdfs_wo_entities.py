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

# Function to extract details from text
def extract_details(text):
    doc = nlp(text)
    entities = {"Name": "", "Phone": "", "Email": "", "Address": ""}
    
    # Extract name (Assuming NER label 'PERSON' for person names)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["Name"]:
            entities["Name"] = ent.text.strip()
    
    # Regex for phone number
    phone_match = re.search(r'\+?\d{1,2}\s?\(?\d{3}\)?\s?\d{3}-\d{4}', text)
    if phone_match:
        entities["Phone"] = phone_match.group().strip()
    
    # Regex for email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        entities["Email"] = email_match.group().strip()
    
    # Heuristic for address (looking for patterns like street names, city names, etc.)
    address_match = re.search(r'\d{1,5}\s\w+\s\w+.*', text)
    if address_match:
        entities["Address"] = address_match.group().strip()
    else:
        # Fallback: Extract address using spaCy's GPE (Geopolitical Entity) and ORG (Organization) labels
        address_parts = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "ORG"]:
                address_parts.append(ent.text.strip())
        entities["Address"] = ', '.join(address_parts)

    return entities

# Main function
def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    details = extract_details(text)
    return details

# Example usage
if __name__ == "__main__":
    pdf_path = "uploads/Bhargav_Patki_Resume.pdf"  # Replace with the path to your PDF
    result = process_pdf(pdf_path)
    print(json.dumps(result, indent=4))