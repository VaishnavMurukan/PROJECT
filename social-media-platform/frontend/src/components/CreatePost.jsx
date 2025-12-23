import React, { useState } from 'react';
import { postAPI } from '../services/api';

const CreatePost = ({ onPostCreated }) => {
  const [content, setContent] = useState('');
  const [topic, setTopic] = useState('');
  const [keywords, setKeywords] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await postAPI.createPost({
        content,
        topic: topic || null,
        keywords: keywords || null
      });
      setContent('');
      setTopic('');
      setKeywords('');
      if (onPostCreated) onPostCreated();
    } catch (error) {
      alert('Error creating post: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post-box">
      <h3>Create Post</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <textarea
            placeholder="What's on your mind?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows="3"
          />
        </div>
        <div className="form-group">
          <input
            type="text"
            placeholder="Topic (optional)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>
        <div className="form-group">
          <input
            type="text"
            placeholder="Keywords (comma-separated, optional)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
        </div>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Posting...' : 'Post'}
        </button>
      </form>
    </div>
  );
};

export default CreatePost;
