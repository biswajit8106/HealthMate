import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../../style/pages/AdminDashboard.css';
import {
  Tooltip as ReTooltip, Legend as ReLegend,
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  ResponsiveContainer
} from 'recharts';

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AA336A', '#33AA99', '#9933AA'];


const AdminDashboard = () => {
  const [stats, setStats] = useState({});
  const [userGrowth, setUserGrowth] = useState([]);
  const [symptomCheckUsage, setSymptomCheckUsage] = useState([]);
  const [reportAnalyzerTrends, setReportAnalyzerTrends] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [statsRes, userGrowthRes, symptomCheckRes, reportAnalyzerRes, recentActivityRes] = await Promise.all([
          axios.get('http://localhost:5000/admin/dashboard/stats'),
          axios.get('http://localhost:5000/admin/dashboard/user_growth'),
          axios.get('http://localhost:5000/admin/dashboard/symptom_check_usage'),
          axios.get('http://localhost:5000/admin/dashboard/report_analyzer_trends'),
          axios.get('http://localhost:5000/admin/dashboard/recent_activity'),
        ]);
        setStats(statsRes.data);
        setUserGrowth(userGrowthRes.data);
        setSymptomCheckUsage(symptomCheckRes.data);
        setReportAnalyzerTrends(reportAnalyzerRes.data);
        setRecentActivity(recentActivityRes.data);
      } catch (err) {
        setError('Failed to fetch admin dashboard data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllData();
  }, []);

  if (loading) return <p>Loading admin dashboard...</p>;
  if (error) return <p className="error">{error}</p>;

  const userGrowthData = userGrowth.map(item => ({
    name: item.year && item.month ? `${item.year}-${item.month.toString().padStart(2, '0')}` : '',
    count: item.count
  })).filter(item => item.name !== '');

  const symptomCheckData = symptomCheckUsage.map(item => ({
    date: item.date,
    count: item.count
  }));

  const reportAnalyzerData = reportAnalyzerTrends.map(item => ({
    date: item.date,
    count: item.count
  }));

  return (
    <div className="admin-dashboard">
      <h2>Admin Dashboard Overview</h2>

      <section className="stats-cards">
        <div className="card">
          <h3>Total Users</h3>
          <p>{stats.total_users ?? 0}</p>
        </div>
        <div className="card">
          <h3>Total Reports Generated</h3>
          <p>{stats.total_reports ?? 0}</p>
        </div>
        <div className="card">
          <h3>Total Analyzer Uploads</h3>
          <p>{stats.total_analyzer_uploads ?? 0}</p>
        </div>
      </section>

      <section className="charts-section">
        <h3>User Growth Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={userGrowthData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <ReTooltip />
            <ReLegend />
            <Line type="monotone" dataKey="count" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="charts-section">
        <h3>Symptom Check Usage</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={symptomCheckData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis allowDecimals={false} />
            <ReTooltip />
            <ReLegend />
            <Line type="monotone" dataKey="count" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="charts-section">
        <h3>Report Analyzer Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={reportAnalyzerData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis allowDecimals={false} />
            <ReTooltip />
            <ReLegend />
            <Line type="monotone" dataKey="count" stroke="#FF8042" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="recent-activity">
        <h3>Recent Activity Logs</h3>
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>ID</th>
              <th>User ID</th>
              <th>Details</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {recentActivity.map((item, index) => (
              <tr key={index}>
                <td>{item.type === 'user_registration' ? 'User Registration' : 'Report Generated'}</td>
                <td>{item.type === 'user_registration' ? item.user_id : item.report_id}</td>
                <td>{item.user_id}</td>
                <td>{item.type === 'user_registration' ? item.name : item.predicted_disease}</td>
                <td>{item.created_at ? new Date(item.created_at).toLocaleString() : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default AdminDashboard;
