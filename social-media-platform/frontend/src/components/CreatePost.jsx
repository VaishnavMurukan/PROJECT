import React, { useState, useRef } from 'react';
import { postAPI } from '../services/api';
import api from '../services/api';
import './CreatePost.css';

const CreatePost = ({ onPostCreated }) => {
  const [content, setContent] = useState('');
  const [topic, setTopic] = useState('');
  const [keywords, setKeywords] = useState('');
  const [loading, setLoading] = useState(false);
  const [mediaFiles, setMediaFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files);
    
    for (const file of files) {
      const isImage = file.type.startsWith('image/');
      const isVideo = file.type.startsWith('video/');
      
      if (!isImage && !isVideo) {
        alert(`${file.name} is not a valid image or video file`);
        continue;
      }
      
      if (file.size > 50 * 1024 * 1024) {
        alert(`${file.name} is too large. Maximum size is 50MB`);
        continue;
      }
      
      const preview = URL.createObjectURL(file);
      const mediaType = isImage ? 'image' : 'video';
      
      setMediaFiles(prev => [...prev, {
        id: Date.now() + Math.random(),
        file,
        preview,
        mediaType,
        uploading: false,
        uploaded: false,
        url: null,
        error: null
      }]);
    }
    e.target.value = '';
  };

  const removeMedia = (id) => {
    setMediaFiles(prev => {
      const item = prev.find(m => m.id === id);
      if (item?.preview) URL.revokeObjectURL(item.preview);
      return prev.filter(m => m.id !== id);
    });
  };

  const uploadMedia = async (mediaItem) => {
    const formData = new FormData();
    formData.append('file', mediaItem.file);
    
    try {
      setMediaFiles(prev => prev.map(m => 
        m.id === mediaItem.id ? { ...m, uploading: true } : m
      ));
      
      const response = await api.post('/uploads/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setMediaFiles(prev => prev.map(m => 
        m.id === mediaItem.id 
          ? { ...m, uploading: false, uploaded: true, url: response.data.url }
          : m
      ));
      
      return response.data;
    } catch (error) {
      setMediaFiles(prev => prev.map(m => 
        m.id === mediaItem.id 
          ? { ...m, uploading: false, error: error.response?.data?.detail || 'Upload failed' }
          : m
      ));
      throw error;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim() && mediaFiles.length === 0) {
      alert('Please add some content or media');
      return;
    }
    
    setLoading(true);

    try {
      const uploadedMedia = [];
      for (const mediaItem of mediaFiles) {
        if (!mediaItem.uploaded && !mediaItem.error) {
          const result = await uploadMedia(mediaItem);
          uploadedMedia.push({ media_type: result.media_type, url: result.url });
        } else if (mediaItem.uploaded && mediaItem.url) {
          uploadedMedia.push({ media_type: mediaItem.mediaType, url: mediaItem.url });
        }
      }
      
      await postAPI.createPost({
        content: content || '📷',
        topic: topic || null,
        keywords: keywords || null,
        media: uploadedMedia.length > 0 ? uploadedMedia : null
      });
      
      setContent('');
      setTopic('');
      setKeywords('');
      mediaFiles.forEach(m => { if (m.preview) URL.revokeObjectURL(m.preview); });
      setMediaFiles([]);
      
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
            rows="3"
          />
        </div>
        
        {mediaFiles.length > 0 && (
          <div className="media-preview-container">
            {mediaFiles.map(media => (
              <div key={media.id} className={`media-preview-item ${media.error ? 'error' : ''}`}>
                {media.mediaType === 'image' ? (
                  <img src={media.preview} alt="Preview" />
                ) : (
                  <video src={media.preview} />
                )}
                <div className="media-overlay">
                  {media.uploading && <span className="uploading">⏳</span>}
                  {media.uploaded && <span className="uploaded">✅</span>}
                  {media.error && <span className="error-msg">❌</span>}
                  <button type="button" className="remove-media" onClick={() => removeMedia(media.id)}>✕</button>
                </div>
                <span className="media-type-badge">{media.mediaType === 'image' ? '🖼️' : '🎬'}</span>
              </div>
            ))}
          </div>
        )}
        
        <div className="media-upload-section">
          <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept="image/*,video/*" multiple hidden />
          <button type="button" className="add-media-btn" onClick={() => fileInputRef.current?.click()}>
            📷 Add Photo/Video
          </button>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <input type="text" placeholder="Topic (for bot matching)" value={topic} onChange={(e) => setTopic(e.target.value)} />
          </div>
          <div className="form-group">
            <input type="text" placeholder="Keywords (comma-separated)" value={keywords} onChange={(e) => setKeywords(e.target.value)} />
          </div>
        </div>
        
        <button type="submit" className="btn post-btn" disabled={loading}>
          {loading ? '⏳ Posting...' : '📤 Post'}
        </button>
      </form>
    </div>
  );
};

export default CreatePost;
