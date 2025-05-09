import React, { useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import '../style/components/ReportAnalyzer.css';

const ReportAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [explanation, setExplanation] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setExtractedText('');
    setExplanation('');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');
    setExtractedText('');
    setExplanation('');

    try {
      const response = await axios.post('/api/reportanalyzer/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setExtractedText(response.data.extracted_text);
        setExplanation(response.data.explanation);
      }
    } catch (err) {
      setError('An error occurred while analyzing the report.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <Navbar />
      <div className="report-analyzer-container">
        <h2 className="title">🩺 Medical Report Analyzer</h2>

        <form onSubmit={handleSubmit} className="upload-form">
          <label className="file-label">
            Upload Report:
            <input
              type="file"
              accept=".pdf,image/png,image/jpeg"
              onChange={handleFileChange}
              className="file-input"
            />
          </label>

          {file && <p className="selected-file">📁 Selected File: <strong>{file.name}</strong></p>}

          <button type="submit" disabled={loading} className="analyze-btn">
            {loading ? 'Analyzing...' : 'Analyze Report'}
          </button>
        </form>

        {error && <div className="error-msg">{error}</div>}

        {extractedText && (
          <div className="result-section">
            <h3>📋 Extracted Text</h3>
            <textarea
              readOnly
              value={extractedText}
              rows={10}
              className="result-textarea"
            />
          </div>
        )}

        {explanation && (
          <div className="result-section">
            <h3>🧠 Chatbot Explanation</h3>
            <p className="explanation-text">{explanation}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportAnalyzer;
