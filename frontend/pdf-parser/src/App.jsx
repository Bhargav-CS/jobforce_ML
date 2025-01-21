import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState({ Name: "", Phone: "", Address: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError("Please upload a PDF file.");
      return;
    }
    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await axios.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setData(response.data);
    } catch (err) {
      setError("Failed to extract data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGeminiExtract = async () => {
    if (!file) {
      setError("Please upload a PDF file.");
      return;
    }
    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await axios.post("/extract_with_gemini", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setData(response.data);
    } catch (err) {
      setError("Failed to extract data with Gemini. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App container mt-5">
      <h1 className="text-center mb-4">PDF Data Extractor</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="mb-3">
          <input type="file" accept="application/pdf" onChange={handleFileChange} className="form-control" />
        </div>
        <button type="submit" className="btn btn-primary w-100">Upload & Extract</button>
      </form>

      {loading && <p className="text-center">Processing...</p>}
      {error && <p className="text-center text-danger">{error}</p>}

      <div className="results">
        <h2 className="text-center">Extracted Data</h2>
        <div className="mb-3">
          <label className="form-label">Name:</label>
          <input type="text" value={data.Name} readOnly className="form-control" />
        </div>
        <div className="mb-3">
          <label className="form-label">Phone:</label>
          <input type="text" value={data.Phone} readOnly className="form-control" />
        </div>
        <div className="mb-3">
          <label className="form-label">Address:</label>
          <textarea value={data.Address} readOnly className="form-control" rows="3"></textarea>
        </div>
      </div>

      {data.Name && (
        <>
          <p className="text-center mt-3">Not the results you were hoping for? Let's try again with more concentration.</p>
          <button onClick={handleGeminiExtract} className="btn btn-secondary w-100 mt-3">Extract with AI</button>
        </>
      )}
    </div>
  );
}

export default App;