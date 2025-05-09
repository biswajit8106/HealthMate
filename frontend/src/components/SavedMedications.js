import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SavedMedications = () => {
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMedications = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/medications/saved', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMedications(response.data);
      } catch (err) {
        setError('Failed to fetch saved medications.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMedications();
  }, []);

  if (loading) return <p>Loading saved medications...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="saved-medications">
      <h2>Saved Medications</h2>
      {medications.length === 0 ? (
        <p>No saved medications found.</p>
      ) : (
        <ul>
          {medications.map((med) => (
            <li key={med.id}>
              <strong>{med.name}</strong> - {med.description}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SavedMedications;
