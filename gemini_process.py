import re
import json
import pdfplumber
import spacy
import requests
import google.generativeai as genai

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to create the Gemini API prompt
def create_gemini_prompt(text):
    prompt = f"""
    Extract the following information from the given text:
    - Name
    - Phone
    - Address

    Provide the output in this sample JSON format:
    {{
        'Name': 'John Doe',
        'Phone': '+1 (620) 130-7224',
        'Address': '447 Sutter St 3rd Floor, San Francisco, CA 94108, United States'
    }}

    if no address is found, place it as "no address found". if no Name is found, place it as "no name found". if no phone is found, place it as "no phone found".
    
    Text:
    {text}
    """
    return prompt

# Function to extract details using Gemini API
def extract_details_with_gemini(text):
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = create_gemini_prompt(text)
    response = model.generate_content(prompt)
    
    # Clean the response text
    cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
    
    try:
        response_json = json.loads(cleaned_response)
        formatted_response = {
            'Name': response_json.get('Name', ''),
            'Phone': response_json.get('Phone', ''),
            'Address': response_json.get('Address', '')
        }
        return formatted_response
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Cleaned response text: {cleaned_response}")
        return None

# Main function
def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    details = extract_details_with_gemini(text)
    return details

# Example usage
if __name__ == "__main__":
    pdf_path = "uploads\Bhargav_Patki_Resume.pdf"  # Replace with the path to your PDF
    result = process_pdf(pdf_path)
    if result:
        print(json.dumps(result, indent=4))
    else:
        print("Failed to extract details from the PDF")