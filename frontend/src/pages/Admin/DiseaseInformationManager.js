import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/DiseaseInformationManager.css';

const DiseaseInformationManager = () => {
  const [diseases, setDiseases] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newDiseaseName, setNewDiseaseName] = useState('');
  const [newDiseaseDescription, setNewDiseaseDescription] = useState('');

  const fetchDiseases = async () => {
    try {
      const res = await axios.get('http://localhost:5000//admin/disease_info/');
      setDiseases(res.data);
    } catch (err) {
      setError('Failed to fetch diseases');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiseases();
  }, []);

  const addDisease = async () => {
    try {
      await axios.post('http://localhost:5000//admin/disease_info/', {
        name: newDiseaseName,
        description: newDiseaseDescription,
      });
      setNewDiseaseName('');
      setNewDiseaseDescription('');
      fetchDiseases();
    } catch (err) {
      setError('Failed to add disease');
      console.error(err);
    }
  };

  if (loading) return <p>Loading diseases...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Disease Information Manager</h2>
      <div>
        <input
          type="text"
          placeholder="Disease Name"
          value={newDiseaseName}
          onChange={(e) => setNewDiseaseName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Description"
          value={newDiseaseDescription}
          onChange={(e) => setNewDiseaseDescription(e.target.value)}
        />
        <button onClick={addDisease}>Add Disease</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Disease Name</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {diseases.map((disease) => (
            <tr key={disease.name}>
              <td>{disease.name}</td>
              <td>{disease.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DiseaseInformationManager;
