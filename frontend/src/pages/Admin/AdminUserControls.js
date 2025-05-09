import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/AdminUserControls.css';

const AdminUserControls = () => {
  const [admins, setAdmins] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newAdmin, setNewAdmin] = useState({ name: '', email: '', password: '', role: 'Moderator' });

  const fetchAdmins = async () => {
    try {
      const res = await axios.get('/admin/user_controls/admins');
      setAdmins(res.data);
    } catch (err) {
      setError('Failed to fetch admins');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmins();
  }, []);

  const addAdmin = async () => {
    try {
      await axios.post('/admin/user_controls/admins', newAdmin);
      setNewAdmin({ name: '', email: '', password: '', role: 'Moderator' });
      fetchAdmins();
    } catch (err) {
      setError('Failed to add admin');
      console.error(err);
    }
  };

  const removeAdmin = async (userId) => {
    try {
      await axios.delete(`/admin/user_controls/admins/${userId}`);
      fetchAdmins();
    } catch (err) {
      setError('Failed to remove admin');
      console.error(err);
    }
  };

  const changeRole = async (userId, role) => {
    try {
      await axios.put(`/admin/user_controls/admins/${userId}/role`, { role });
      fetchAdmins();
    } catch (err) {
      setError('Failed to change role');
      console.error(err);
    }
  };

  const changePassword = async (userId, password) => {
    try {
      await axios.put(`/admin/user_controls/admins/${userId}/password`, { password });
      fetchAdmins();
    } catch (err) {
      setError('Failed to change password');
      console.error(err);
    }
  };

  if (loading) return <p>Loading admins...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Admin User Controls</h2>
      <div>
        <input
          type="text"
          placeholder="Name"
          value={newAdmin.name}
          onChange={(e) => setNewAdmin({ ...newAdmin, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          value={newAdmin.email}
          onChange={(e) => setNewAdmin({ ...newAdmin, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          value={newAdmin.password}
          onChange={(e) => setNewAdmin({ ...newAdmin, password: e.target.value })}
        />
        <select
          value={newAdmin.role}
          onChange={(e) => setNewAdmin({ ...newAdmin, role: e.target.value })}
        >
          <option value="Super Admin">Super Admin</option>
          <option value="Moderator">Moderator</option>
        </select>
        <button onClick={addAdmin}>Add Admin</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Change Role</th>
            <th>Change Password</th>
            <th>Remove</th>
          </tr>
        </thead>
        <tbody>
          {admins.map((admin) => (
            <tr key={admin.user_id}>
              <td>{admin.user_id}</td>
              <td>{admin.name}</td>
              <td>{admin.email}</td>
              <td>{admin.role}</td>
              <td>
                <select
                  value={admin.role}
                  onChange={(e) => changeRole(admin.user_id, e.target.value)}
                >
                  <option value="Super Admin">Super Admin</option>
                  <option value="Moderator">Moderator</option>
                </select>
              </td>
              <td>
                <input
                  type="password"
                  placeholder="New Password"
                  onKeyDown={e => {
                    if (e.key === 'Enter') {
                      changePassword(admin.user_id, e.target.value);
                      e.target.value = '';
                    }
                  }}
                />
              </td>
              <td>
                <button onClick={() => removeAdmin(admin.user_id)}>Remove</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminUserControls;
