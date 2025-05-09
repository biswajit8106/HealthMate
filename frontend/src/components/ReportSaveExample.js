import React, { useState } from 'react';
import axios from 'axios';

const ReportSaveExample = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [reportData, setReportData] = useState({
    name: 'Biswajit',
    age: '21',
    gender: 'Male',
    symptoms: ['vomiting', 'acidity'],
    predicted_disease: 'GERD',
    confidence: 25,
    description: 'GERD (Gastroesophageal Reflux Disease) is a digestive disorder that affects the lower esophageal sphincter.',
    precautions: [
      'avoid fatty spicy food',
      'avoid lying down after eating',
      'maintain healthy weight',
      'exercise',
    ],
    medications: [
      "['Proton Pump Inhibitors (PPIs)', 'H2 Blockers', 'Antacids', 'Prokinetics', 'Antibiotics']",
    ],
    diets: [
      "['Low-Acid Diet', 'Fiber-rich foods', 'Ginger', 'Licorice', 'Aloe vera juice']",
    ],
    workouts: [
      'Consume smaller meals',
      'Avoid trigger foods (spicy, fatty)',
      'Eat high-fiber foods',
      'Limit caffeine and alcohol',
      'Chew food thoroughly',
      'Avoid late-night eating',
      'Consume non-citrus fruits',
      'Include lean proteins',
      'Stay hydrated',
      'Avoid carbonated beverages',
    ],
  });
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/login', { email, password }, { withCredentials: true });
      setMessage(res.data.message);
    } catch (err) {
      setMessage('Login failed: ' + (err.response?.data?.message || err.message));
    }
  };

  const handleSaveReport = async () => {
    try {
      const res = await axios.post('http://localhost:5000/report/save', reportData, { withCredentials: true });
      setMessage('Report saved and PDF generated successfully.');
      // You can handle the PDF response here if needed
    } catch (err) {
      setMessage('Save report failed: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>

      <h2>Save Report</h2>
      <button onClick={handleSaveReport}>Save Report</button>

      <p>{message}</p>
    </div>
  );
};

export default ReportSaveExample;
