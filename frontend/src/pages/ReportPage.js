// ReportPage.jsx

import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../style/pages/ReportPage.css';
import logo from '../assets/logo.png';
import SessionCheck from '../components/SessionCheck';

const ReportPage = () => {
    const { state } = useLocation();
    const navigate = useNavigate();

    const {
        name, age, gender, symptoms,
        predicted_disease, confidence, description,
        precautions, medications, diets, workouts
    } = state || {};

    const [downloading, setDownloading] = useState(false);

    const getConfidenceColor = (confidence) => {
        const percent = confidence * 100;
        if (percent >= 75) return 'green';
        if (percent >= 50) return 'orange';
        return 'red';
    };

    const formatArray = (arr) => {
        if (!arr || arr.length === 0) return 'None';
        return arr.join(', ');
    };

    const handleDownloadPDF = async () => {
        setDownloading(true);
        try {
            const response = await fetch('http://localhost:5000/report/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // ✅ Important for session cookies
                body: JSON.stringify({
                    name,
                    age,
                    gender,
                    symptoms,
                    predicted_disease,
                    confidence,
                    description,
                    precautions,
                    medications,
                    diets,
                    workouts
                }),
            });

            if (!response.ok) throw new Error('Failed to generate PDF');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${name}_health_report.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error(err);
            alert('Error downloading PDF.');
        }
        setDownloading(false);
    };

    return (
        <div className="report-page">
            <nav className="navbar">
                <div className="navbar-logo" onClick={() => navigate('/')}>
                    <img src={logo} alt="logo" />
                    <span>HealthMate</span>
                </div>
                <div className="navbar-links">
                    <a onClick={() => navigate('/')}>Home</a>
                    <a onClick={() => navigate('/symptom-checker')}>Symptom Diagnosis</a>
                    <a onClick={() => navigate('/dashboard')}>Dashboard</a>
                </div>
                <div>
                    <button className="logout-button" onClick={() => navigate('/login')}>Logout</button>
                </div>
            </nav>

            <div className="report-content">
                <h2>🩺 HealthMate Diagnosis Report</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Gender:</strong> {gender}</p>
                <p><strong>Age:</strong> {age}</p>
                <p><strong>Symptoms:</strong> {formatArray(symptoms)}</p>
                <p><strong>Predicted Disease:</strong> {predicted_disease}</p>
                <p>
                    <strong>Precision:</strong>
                    <span className={`confidence ${getConfidenceColor(confidence)}`}>
                        {(confidence * 100).toFixed(2)}%
                    </span>
                </p>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Precautions:</strong> {formatArray(precautions)}</p>
                <p><strong>Medications:</strong> {formatArray(medications)}</p>
                <p><strong>Diets:</strong> {formatArray(diets)}</p>
                <p><strong>Workouts:</strong> {formatArray(workouts)}</p>

                <button onClick={handleDownloadPDF} disabled={downloading}>
                    {downloading ? 'Generating PDF...' : '📄 Download Report (PDF with Logo & Stamp)'}
                </button>
            </div>
            <SessionCheck />
        </div>
    );
};

export default ReportPage;
