import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../style/components/MedicationRecommendation.css';

const MedicationRecommendationClean = () => {
  const [recentDisease, setRecentDisease] = useState(null);
  const [recentMedications, setRecentMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecentMedicine = async () => {
      try {
        const recentResponse = await axios.get('http://localhost:5000/api/medicine/recent');
        setRecentDisease(recentResponse.data.predicted_disease);
        setRecentMedications(recentResponse.data.medications);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchRecentMedicine();
  }, []);

  return (
    <div className="medication-recommendation">
      <h3>Recent Prescribed Medicines</h3>
      {loading ? (
        <p>Loading recent medicine data...</p>
      ) : error ? (
        <p className="error">Error: {error}</p>
      ) : recentDisease ? (
        <div>
          <p><strong>Disease:</strong> {recentDisease}</p>
          <p><strong>Medicines:</strong></p>
          <table>
            <thead>
              <tr>
                <th>Medicine Name</th>
                <th>Dosage</th>
                <th>Timing</th>
              </tr>
            </thead>
            <tbody>
              {recentMedications.length > 0 ? (
                recentMedications.map((med, index) => (
                  <tr key={index}>
                    <td>{med.name || med}</td>
                    <td>{med.dosage || 'To be decided'}</td>
                    <td>{med.timing || 'To be decided'}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3">No medicines prescribed.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No recent medicine data found.</p>
      )}
    </div>
  );
};

export default MedicationRecommendationClean;
