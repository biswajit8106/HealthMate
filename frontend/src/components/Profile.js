import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch user data from API endpoint
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/user/profile', { withCredentials: true });
        setUser(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching profile data:', err);
        setError('Failed to load user data: ' + (err.message || err.toString()));
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div>Loading user information...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!user) {
    return <div>No user data available.</div>;
  }

  return (
    <div className="profile-container" style={{ maxWidth: '400px', margin: '0 auto', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>User Profile</h2>
      <p><strong>Name:</strong> {user.name || 'N/A'}</p>
      <p><strong>Age:</strong> {user.age || 'N/A'}</p>
      <p><strong>Gender:</strong> {user.gender || 'N/A'}</p>
      <p><strong>Email:</strong> {user.email || 'N/A'}</p>
    </div>
  );
};

export default Profile;
