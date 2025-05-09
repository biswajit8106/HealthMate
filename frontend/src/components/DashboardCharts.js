import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  PieChart, Pie, Cell, Tooltip as ReTooltip, Legend as ReLegend,
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  BarChart, Bar,
  ResponsiveContainer
} from 'recharts';
import '../style/components/DashboardCharts.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AA336A', '#33AA99', '#9933AA'];

const DashboardCharts = () => {
  const [diseaseData, setDiseaseData] = useState([]);
  const [healthTrendsData, setHealthTrendsData] = useState([]);
  const [commonSymptomsData, setCommonSymptomsData] = useState([]);
  const [heatmapData, setHeatmapData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [diseaseRes, trendsRes, symptomsRes, heatmapRes] = await Promise.all([
          axios.get('/report/dashboard/disease_categories'),
          axios.get('/report/dashboard/health_trends'),
          axios.get('/report/dashboard/common_symptoms'),
          axios.get('/report/dashboard/symptom_disease_heatmap'),
        ]);
        setDiseaseData(diseaseRes.data);
        setHealthTrendsData(trendsRes.data);
        setCommonSymptomsData(symptomsRes.data);
        setHeatmapData(heatmapRes.data);
      } catch (err) {
        setError('Failed to fetch dashboard data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllData();
  }, []);

  if (loading) return <p>Loading dashboard charts...</p>;
  if (error) return <p className="error">{error}</p>;

  // Prepare heatmap matrix data
  // Extract unique symptoms and diseases
  const symptoms = [...new Set(heatmapData.map(item => item.symptom))];
  const diseases = [...new Set(heatmapData.map(item => item.disease))];

  // Create matrix with counts
  const heatmapMatrix = symptoms.map(symptom => {
    const row = { symptom };
    diseases.forEach(disease => {
      const found = heatmapData.find(item => item.symptom === symptom && item.disease === disease);
      row[disease] = found ? found.count : 0;
    });
    return row;
  });

  return (
    <div className="dashboard-charts">
      <h2>Dashboard Visualizations</h2>

      <section className="dashboard-section">
        <h3>Pie Chart: Disease Categories Diagnosed</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={diseaseData}
              dataKey="count"
              nameKey="disease"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            >
              {diseaseData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <ReTooltip />
            <ReLegend />
          </PieChart>
        </ResponsiveContainer>
      </section>

      <section className="dashboard-section">
        <h3>Line Chart: Health Trends Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={healthTrendsData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis allowDecimals={false} />
            <ReTooltip />
            <ReLegend />
            <Line type="monotone" dataKey="count" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="dashboard-section">
        <h3>Bar Graph: Most Common Symptoms Submitted</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={commonSymptomsData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="symptom" />
            <YAxis allowDecimals={false} />
            <ReTooltip />
            <ReLegend />
            <Bar dataKey="count" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section className="dashboard-section">
        <h3>Heatmap: Common Symptom-Disease Pairs</h3>
        <div className="heatmap-container">
          <table className="heatmap-table">
            <thead>
              <tr>
                <th>Symptom \ Disease</th>
                {diseases.map(disease => (
                  <th key={disease}>{disease}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {heatmapMatrix.map(row => (
                <tr key={row.symptom}>
                  <td><strong>{row.symptom}</strong></td>
                  {diseases.map(disease => (
                    <td key={disease} className="heatmap-cell" style={{ backgroundColor: `rgba(255, 0, 0, ${Math.min(row[disease] / 10, 1)})` }}>
                      {row[disease]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};

export default DashboardCharts;
