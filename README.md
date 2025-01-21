
# jobforce_ML

jobforce_ML is a web application designed to extract and process data from PDF files. The application provides two main functionalities: extracting data using a standard method and extracting data using the Gemini AI model for more accurate results. The frontend is built with React and Bootstrap, while the backend is powered by Flask and various Python libraries for PDF processing and natural language processing (NLP).

---

## Project Structure

- **`app.py`**: The main backend application file that handles routes and API endpoints.
- **`gemini_process.py`**: Contains functions to process PDFs using the Gemini AI model.
- **`process_pdfs.py`**: Contains functions to process PDFs using standard methods.
- **`frontend/`**: Contains the React frontend application.
- **`pdf-parser/`**: Contains the source code for the PDF parser frontend.
- **`build/`**: Contains the build files for the frontend.
- **`uploads/`**: Directory to store uploaded PDF files.
- **`env/`**: Contains environment-specific files and dependencies.
- **`requirements.txt`**: Lists the Python dependencies for the project.
- **`render.yaml`**: Configuration file for deploying the application using Render.

---

## Key Functionalities

### PDF Upload and Extraction

1. **Standard Extraction**:
   - Users can upload PDF files through the frontend.
   - The backend processes the uploaded PDF to extract text and relevant details.
   - Extracted data includes fields like Name, Phone, and Address.

2. **Gemini AI Extraction**:
   - Users can opt to extract data using the Gemini AI model for improved accuracy.
   - The backend uses the Gemini API to process the text and extract details.

---

## Backend Details

- **Framework**: Flask
- **Key Routes**:
  - `/upload`: Handles PDF uploads and extracts data using standard methods.
  - `/extract_with_gemini`: Extracts data using the Gemini AI model.

- **Core Functions**:
  - `extract_text_from_pdf`: Extracts text from the PDF using pdfplumber.
  - `extract_details`: Uses spaCy's NER model to extract details from the text.
  - `extract_details_with_gemini`: Uses the Gemini API to extract details from the text.

---

## Frontend Details

- **Framework**: React
- **Styling**: Bootstrap
- **Key Features**:
  - Upload PDF files.
  - View extracted data in an interactive interface.
  - Retry extraction using the Gemini AI model for improved accuracy.
- **API Communication**: Axios is used to make API requests to the backend.

---

## Deployment

- **Link**: [jobforce_ML](https://jobforce-ml.onrender.com/) Since it is a free instance it might take some time to load. Please bear with it 😅

---

## Dependencies

### Python Dependencies
- Flask
- Flask-CORS
- pdfplumber
- spaCy
- google-generativeai

### JavaScript Dependencies
- React
- Bootstrap

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/jobforce_ML.git
   cd jobforce_ML
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python app.py
   ```

4. Navigate to the `frontend/` directory and install frontend dependencies:
   ```bash
   cd frontend
   yarn
   yarn run dev
   ```

5. Open the application in your browser at `http://localhost`.

6. Upload a PDF file through the interface and view the extracted data. Retry extraction using the Gemini AI model if necessary.

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for feature suggestions or bug fixes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

- **Flask** for backend development.
- **React** and **Bootstrap** for the frontend.
- **Gemini API** for enhanced PDF data extraction.
- **spaCy** and **pdfplumber** for natural language processing and PDF parsing.
