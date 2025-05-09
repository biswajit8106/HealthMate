import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/UserManagement.css';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      const res = await axios.get('http://localhost:5000/admin/users/');
      setUsers(res.data);
    } catch (err) {
      setError('Failed to fetch users');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const activateUser = async (userId) => {
    try {
      await axios.post(`http://localhost:5000/admin/users/activate/${userId}`);
      fetchUsers();
    } catch (err) {
      setError('Failed to activate user');
      console.error(err);
    }
  };

  const deactivateUser = async (userId) => {
    try {
      await axios.post(`http://localhost:5000/admin/users/deactivate/${userId}`);
      fetchUsers();
    } catch (err) {
      setError('Failed to deactivate user');
      console.error(err);
    }
  };

  const deleteUser = async (userId) => {
    try {
      await axios.delete(`http://localhost:5000/admin/users/delete/${userId}`);
      fetchUsers();
    } catch (err) {
      setError('Failed to delete user');
      console.error(err);
    }
  };

  if (loading) return <p>Loading users...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>User Management</h2>
      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Active</th>
            <th>Admin</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.age}</td>
              <td>{user.gender}</td>
              <td>{user.is_active ? 'Yes' : 'No'}</td>
              <td>{user.is_admin ? 'Yes' : 'No'}</td>
              <td>
                {user.is_active ? (
                  <button onClick={() => deactivateUser(user.user_id)}>Deactivate</button>
                ) : (
                  <button onClick={() => activateUser(user.user_id)}>Activate</button>
                )}
                <button onClick={() => deleteUser(user.user_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserManagement;
