import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/FeedbackContactRequests.css';

const FeedbackContactRequests = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [replyText, setReplyText] = useState('');
  const [selectedFeedbackId, setSelectedFeedbackId] = useState(null);

  const fetchFeedbacks = async () => {
    try {
      const res = await axios.get('http://localhost:5000/admin/feedback/');
      setFeedbacks(res.data);
    } catch (err) {
      setError('Failed to fetch feedbacks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, []);

  const handleReply = async (feedbackId) => {
    try {
      await axios.post(`http://localhost:5000/admin/feedback/reply/${feedbackId}`, { reply: replyText });
      setReplyText('');
      setSelectedFeedbackId(null);
      fetchFeedbacks();
    } catch (err) {
      setError('Failed to send reply');
      console.error(err);
    }
  };

  const markResolved = async (feedbackId) => {
    try {
      await axios.post(`http://localhost:5000/admin/feedback/mark_resolved/${feedbackId}`);
      fetchFeedbacks();
    } catch (err) {
      setError('Failed to mark resolved');
      console.error(err);
    }
  };

  if (loading) return <p>Loading feedbacks...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Feedback & Contact Requests</h2>
      <ul>
        {feedbacks.map((fb) => (
          <li key={fb.id}>
            <p><strong>User:</strong> {fb.user || 'Anonymous'}</p>
            <p><strong>Message:</strong> {fb.message}</p>
            <p><strong>Reply:</strong> {fb.reply || 'No reply yet'}</p>
            <p><strong>Status:</strong> {fb.resolved ? 'Resolved' : 'Pending'}</p>
            {selectedFeedbackId === fb.id ? (
              <div>
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  placeholder="Type your reply here"
                />
                <button onClick={() => handleReply(fb.id)}>Send Reply</button>
                <button onClick={() => setSelectedFeedbackId(null)}>Cancel</button>
              </div>
            ) : (
              <button onClick={() => setSelectedFeedbackId(fb.id)}>Reply</button>
            )}
            {!fb.resolved && (
              <button onClick={() => markResolved(fb.id)}>Mark as Resolved</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FeedbackContactRequests;
