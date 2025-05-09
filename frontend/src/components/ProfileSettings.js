import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProfileSettings = () => {
  const [profile, setProfile] = useState({
    name: '',
    age: '',
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/user/profile', {
          withCredentials: true,
        });
        setProfile({
          name: response.data.name || '',
          age: response.data.age || '',
          email: response.data.email || '',
          password: '',
        });
      } catch (error) {
        console.error('Failed to fetch profile', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('http://localhost:5000/api/user/profile', profile, {
        withCredentials: true,
      });
      setMessage('Profile updated successfully.');
    } catch (error) {
      setMessage('Failed to update profile.');
      console.error(error);
    }
  };

  if (loading) return <p>Loading profile...</p>;

  return (
    <div className="profile-settings">
      <h2>Profile & Settings</h2>
      {message && <p className="message">{message}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={profile.name} onChange={handleChange} required />
        </label>
        <label>
          Age:
          <input type="number" name="age" value={profile.age} onChange={handleChange} required />
        </label>
        <label>
          Email:
          <input type="email" name="email" value={profile.email} onChange={handleChange} required />
        </label>
        <label>
          Password:
          <input type="password" name="password" value={profile.password} onChange={handleChange} placeholder="Enter new password" />
        </label>
        <div>
          <button type="submit">Save Changes</button>
        </div>
      </form>
    </div>
  );
};

export default ProfileSettings;
