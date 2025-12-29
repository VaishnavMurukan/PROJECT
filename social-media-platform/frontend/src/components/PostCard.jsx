import React, { useState, useEffect } from 'react';
import { commentAPI, reactionAPI } from '../services/api';

const PostCard = ({ post, currentUser, onUpdate }) => {
  const [comments, setComments] = useState([]);
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [userReaction, setUserReaction] = useState(null);

  useEffect(() => {
    if (showComments) {
      loadComments();
    }
  }, [showComments]);

  const loadComments = async () => {
    try {
      const response = await commentAPI.getComments(post.id);
      setComments(response.data);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  };

  const handleReaction = async (isLike) => {
    try {
      if (userReaction === isLike) {
        // Remove reaction
        await reactionAPI.deleteReaction(post.id);
        setUserReaction(null);
      } else {
        // Add or update reaction
        await reactionAPI.createReaction(post.id, isLike);
        setUserReaction(isLike);
      }
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error('Error updating reaction:', error);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      await commentAPI.createComment(post.id, newComment);
      setNewComment('');
      loadComments();
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds

    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  };

  return (
    <div className="post-card">
      <div className="post-header">
        <div className="post-avatar">
          {post.user.username.charAt(0).toUpperCase()}
        </div>
        <div className="post-info">
          <h4>{post.user.username}</h4>
          <small>{formatDate(post.created_at)}</small>
        </div>
      </div>

      {post.topic && <span className="post-topic">{post.topic}</span>}

      <div className="post-content">
        <p>{post.content}</p>
      </div>

      {/* Media Gallery */}
      {post.media && post.media.length > 0 && (
        <div className={`post-media-gallery ${post.media.length === 1 ? 'single' : post.media.length === 2 ? 'double' : 'multi'}`}>
          {post.media.map((media, index) => (
            <div key={index} className="media-item">
              {media.media_type === 'image' ? (
                <img 
                  src={`http://localhost:8000${media.url}`} 
                  alt="Post media" 
                  onClick={() => window.open(`http://localhost:8000${media.url}`, '_blank')}
                />
              ) : (
                <video 
                  src={`http://localhost:8000${media.url}`} 
                  controls
                  preload="metadata"
                />
              )}
            </div>
          ))}
        </div>
      )}

      <div className="post-actions">
        <button 
          onClick={() => handleReaction(true)}
          className={userReaction === true ? 'active' : ''}
        >
          👍 Like ({post.like_count})
        </button>
        <button 
          onClick={() => handleReaction(false)}
          className={userReaction === false ? 'active' : ''}
        >
          👎 Dislike ({post.dislike_count})
        </button>
        <button onClick={() => setShowComments(!showComments)}>
          💬 Comment ({post.comment_count})
        </button>
      </div>

      {showComments && (
        <div className="comments-section">
          <div className="comment-input">
            <input
              type="text"
              placeholder="Write a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddComment(e)}
            />
            <button onClick={handleAddComment}>Post</button>
          </div>

          {comments.map((comment) => (
            <div key={comment.id} className="comment">
              <div className="comment-author">
                {comment.author_name}
                {comment.is_bot && <span className="bot-badge">BOT</span>}
              </div>
              <div>{comment.content}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PostCard;
