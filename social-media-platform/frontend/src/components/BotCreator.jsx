import { useState } from 'react';
import api from '../services/api';
import './BotCreator.css';

const BotCreator = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [bots, setBots] = useState([]);
  const [showBotList, setShowBotList] = useState(false);
  
  const [botData, setBotData] = useState({
    name: '',
    age_group: '25-35',
    profession: '',
    region: 'Global',
    interests: '',
    emotional_bias: 'neutral',
    like_probability: 0.5,
    dislike_probability: 0.2,
    comment_probability: 0.4,
    min_response_delay: 5,
    max_response_delay: 60
  });

  const ageGroups = ['18-25', '25-35', '35-50', '50+'];
  const regions = ['Global', 'North America', 'Europe', 'Asia', 'South America', 'Africa', 'Oceania'];
  const emotionalBiases = [
    { value: 'positive', label: '😊 Positive', color: '#4caf50' },
    { value: 'neutral', label: '😐 Neutral', color: '#9e9e9e' },
    { value: 'negative', label: '😠 Negative', color: '#f44336' }
  ];

  const presetTemplates = [
    {
      name: 'Tech Enthusiast',
      icon: '💻',
      data: {
        profession: 'Software Developer',
        interests: 'technology, AI, programming, innovation, coding',
        emotional_bias: 'positive',
        like_probability: 0.8,
        dislike_probability: 0.05,
        comment_probability: 0.6
      }
    },
    {
      name: 'Art Lover',
      icon: '🎨',
      data: {
        profession: 'Artist',
        interests: 'art, design, creativity, music, culture',
        emotional_bias: 'positive',
        like_probability: 0.75,
        dislike_probability: 0.1,
        comment_probability: 0.5
      }
    },
    {
      name: 'Sports Fan',
      icon: '⚽',
      data: {
        profession: 'Fitness Coach',
        interests: 'sports, fitness, health, teams, competition',
        emotional_bias: 'positive',
        like_probability: 0.7,
        dislike_probability: 0.15,
        comment_probability: 0.55
      }
    },
    {
      name: 'Critical Thinker',
      icon: '🤔',
      data: {
        profession: 'Analyst',
        interests: 'news, politics, science, debate',
        emotional_bias: 'negative',
        like_probability: 0.25,
        dislike_probability: 0.5,
        comment_probability: 0.7
      }
    },
    {
      name: 'Casual User',
      icon: '😎',
      data: {
        profession: 'Student',
        interests: 'music, movies, gaming, memes, entertainment',
        emotional_bias: 'neutral',
        like_probability: 0.5,
        dislike_probability: 0.2,
        comment_probability: 0.35
      }
    },
    {
      name: 'Business Pro',
      icon: '💼',
      data: {
        profession: 'Business Manager',
        interests: 'business, finance, marketing, entrepreneurship',
        emotional_bias: 'neutral',
        like_probability: 0.45,
        dislike_probability: 0.25,
        comment_probability: 0.6
      }
    }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBotData(prev => ({
      ...prev,
      [name]: name.includes('probability') || name.includes('delay') 
        ? parseFloat(value) 
        : value
    }));
  };

  const applyTemplate = (template) => {
    setBotData(prev => ({
      ...prev,
      ...template.data,
      name: template.name.replace(' ', '') + '_' + Math.floor(Math.random() * 1000)
    }));
    setMessage({ type: 'info', text: `Applied "${template.name}" template!` });
  };

  const fetchBots = async () => {
    try {
      const response = await api.get('/bots/');
      setBots(response.data);
    } catch (error) {
      console.error('Error fetching bots:', error);
    }
  };

  const createBot = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const payload = {
        name: botData.name,
        profile: {
          age_group: botData.age_group,
          profession: botData.profession,
          region: botData.region,
          interests: botData.interests,
          emotional_bias: botData.emotional_bias,
          like_probability: botData.like_probability,
          dislike_probability: botData.dislike_probability,
          comment_probability: botData.comment_probability,
          min_response_delay: botData.min_response_delay,
          max_response_delay: botData.max_response_delay
        }
      };

      await api.post('/bots/', payload);
      setMessage({ type: 'success', text: `🤖 Bot "${botData.name}" created successfully!` });
      
      // Reset form
      setBotData({
        name: '',
        age_group: '25-35',
        profession: '',
        region: 'Global',
        interests: '',
        emotional_bias: 'neutral',
        like_probability: 0.5,
        dislike_probability: 0.2,
        comment_probability: 0.4,
        min_response_delay: 5,
        max_response_delay: 60
      });
      
      fetchBots();
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to create bot' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const triggerBotProcessing = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/bots/process-posts');
      const data = response.data;
      setMessage({ 
        type: 'success', 
        text: `🚀 Processed ${data.posts_processed} posts with ${data.bots_active} bots. ${data.interactions} interactions created!` 
      });
      fetchBots();
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to trigger bot processing' });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleBot = async (botId, currentStatus) => {
    try {
      const endpoint = currentStatus ? `/bots/${botId}/deactivate` : `/bots/${botId}/activate`;
      await api.patch(endpoint);
      fetchBots();
      setMessage({ 
        type: 'success', 
        text: `Bot ${currentStatus ? 'deactivated' : 'activated'} successfully!` 
      });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to toggle bot status' });
    }
  };

  const activateAllBots = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/bots/activate-all');
      setMessage({ type: 'success', text: response.data.message });
      fetchBots();
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to activate all bots' });
    } finally {
      setIsLoading(false);
    }
  };

  const deactivateAllBots = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/bots/deactivate-all');
      setMessage({ type: 'success', text: response.data.message });
      fetchBots();
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to deactivate all bots' });
    } finally {
      setIsLoading(false);
    }
  };

  const deleteBot = async (botId, botName) => {
    if (!window.confirm(`Are you sure you want to delete "${botName}"?`)) return;
    try {
      await api.delete(`/bots/${botId}`);
      setMessage({ type: 'success', text: `Bot "${botName}" deleted!` });
      fetchBots();
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to delete bot' });
    }
  };

  const openModal = () => {
    setIsOpen(true);
    fetchBots();
  };

  return (
    <>
      {/* Floating Button */}
      <button 
        className="bot-floating-btn"
        onClick={openModal}
        title="Create Bots"
      >
        🤖
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="bot-modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="bot-modal" onClick={e => e.stopPropagation()}>
            <div className="bot-modal-header">
              <h2>🤖 Bot Creator Studio</h2>
              <button className="bot-close-btn" onClick={() => setIsOpen(false)}>×</button>
            </div>

            <div className="bot-modal-tabs">
              <button 
                className={!showBotList ? 'active' : ''} 
                onClick={() => setShowBotList(false)}
              >
                ➕ Create Bot
              </button>
              <button 
                className={showBotList ? 'active' : ''} 
                onClick={() => { setShowBotList(true); fetchBots(); }}
              >
                📋 My Bots ({bots.length})
              </button>
            </div>

            {message.text && (
              <div className={`bot-message ${message.type}`}>
                {message.text}
              </div>
            )}

            {!showBotList ? (
              <div className="bot-modal-content">
                {/* Templates */}
                <div className="bot-templates">
                  <h3>Quick Templates</h3>
                  <div className="template-grid">
                    {presetTemplates.map((template, idx) => (
                      <button 
                        key={idx} 
                        className="template-btn"
                        onClick={() => applyTemplate(template)}
                      >
                        <span className="template-icon">{template.icon}</span>
                        <span className="template-name">{template.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Bot Form */}
                <form onSubmit={createBot} className="bot-form">
                  <div className="form-section">
                    <h3>Basic Info</h3>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Bot Name *</label>
                        <input
                          type="text"
                          name="name"
                          value={botData.name}
                          onChange={handleInputChange}
                          placeholder="e.g., TechBot_01"
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>Profession</label>
                        <input
                          type="text"
                          name="profession"
                          value={botData.profession}
                          onChange={handleInputChange}
                          placeholder="e.g., Software Engineer"
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Age Group</label>
                        <select name="age_group" value={botData.age_group} onChange={handleInputChange}>
                          {ageGroups.map(age => (
                            <option key={age} value={age}>{age}</option>
                          ))}
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Region</label>
                        <select name="region" value={botData.region} onChange={handleInputChange}>
                          {regions.map(region => (
                            <option key={region} value={region}>{region}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <div className="form-group full-width">
                      <label>Interests (comma-separated)</label>
                      <input
                        type="text"
                        name="interests"
                        value={botData.interests}
                        onChange={handleInputChange}
                        placeholder="e.g., technology, music, sports, art"
                      />
                    </div>
                  </div>

                  <div className="form-section">
                    <h3>Personality</h3>
                    <div className="form-group">
                      <label>Emotional Bias</label>
                      <div className="emotional-bias-selector">
                        {emotionalBiases.map(bias => (
                          <button
                            key={bias.value}
                            type="button"
                            className={`bias-btn ${botData.emotional_bias === bias.value ? 'selected' : ''}`}
                            style={{ '--bias-color': bias.color }}
                            onClick={() => setBotData(prev => ({ ...prev, emotional_bias: bias.value }))}
                          >
                            {bias.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="form-section">
                    <h3>Behavior Settings</h3>
                    <div className="slider-group">
                      <label>
                        Like Probability: <span className="slider-value">{Math.round(botData.like_probability * 100)}%</span>
                      </label>
                      <input
                        type="range"
                        name="like_probability"
                        min="0"
                        max="1"
                        step="0.05"
                        value={botData.like_probability}
                        onChange={handleInputChange}
                        className="slider like-slider"
                      />
                    </div>

                    <div className="slider-group">
                      <label>
                        Dislike Probability: <span className="slider-value">{Math.round(botData.dislike_probability * 100)}%</span>
                      </label>
                      <input
                        type="range"
                        name="dislike_probability"
                        min="0"
                        max="1"
                        step="0.05"
                        value={botData.dislike_probability}
                        onChange={handleInputChange}
                        className="slider dislike-slider"
                      />
                    </div>

                    <div className="slider-group">
                      <label>
                        Comment Probability: <span className="slider-value">{Math.round(botData.comment_probability * 100)}%</span>
                      </label>
                      <input
                        type="range"
                        name="comment_probability"
                        min="0"
                        max="1"
                        step="0.05"
                        value={botData.comment_probability}
                        onChange={handleInputChange}
                        className="slider comment-slider"
                      />
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Min Response Delay (sec)</label>
                        <input
                          type="number"
                          name="min_response_delay"
                          value={botData.min_response_delay}
                          onChange={handleInputChange}
                          min="1"
                          max="300"
                        />
                      </div>
                      <div className="form-group">
                        <label>Max Response Delay (sec)</label>
                        <input
                          type="number"
                          name="max_response_delay"
                          value={botData.max_response_delay}
                          onChange={handleInputChange}
                          min="1"
                          max="600"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="form-actions">
                    <button type="submit" className="create-btn" disabled={isLoading}>
                      {isLoading ? '⏳ Creating...' : '🤖 Create Bot'}
                    </button>
                    <button 
                      type="button" 
                      className="process-btn"
                      onClick={triggerBotProcessing}
                      disabled={isLoading}
                    >
                      🚀 Activate All Bots
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="bot-list">
                {bots.length === 0 ? (
                  <div className="no-bots">
                    <span className="no-bots-icon">🤖</span>
                    <p>No bots created yet!</p>
                    <button onClick={() => setShowBotList(false)}>Create your first bot</button>
                  </div>
                ) : (
                  <>
                    <div className="bot-list-header">
                      <div className="bot-list-actions">
                        <button 
                          className="process-all-btn"
                          onClick={triggerBotProcessing}
                          disabled={isLoading}
                        >
                          🚀 Process Posts
                        </button>
                        <button 
                          className="activate-all-btn"
                          onClick={activateAllBots}
                          disabled={isLoading}
                        >
                          ✅ Activate All
                        </button>
                        <button 
                          className="deactivate-all-btn"
                          onClick={deactivateAllBots}
                          disabled={isLoading}
                        >
                          ⛔ Deactivate All
                        </button>
                      </div>
                      <div className="bot-stats-summary">
                        <span className="active-count">🟢 {bots.filter(b => b.is_active).length} active</span>
                        <span className="inactive-count">🔴 {bots.filter(b => !b.is_active).length} inactive</span>
                      </div>
                    </div>
                    <div className="bot-cards">
                      {bots.map(bot => (
                        <div key={bot.id} className={`bot-card ${!bot.is_active ? 'inactive-card' : ''}`}>
                          <div className="bot-card-header">
                            <span className="bot-avatar">🤖</span>
                            <div className="bot-info">
                              <h4>{bot.name}</h4>
                              <span className={`bot-status ${bot.is_active ? 'active' : 'inactive'}`}>
                                {bot.is_active ? '🟢 Active' : '🔴 Inactive'}
                              </span>
                            </div>
                            <div className="bot-card-actions">
                              <button 
                                className={`toggle-btn ${bot.is_active ? 'deactivate' : 'activate'}`}
                                onClick={() => toggleBot(bot.id, bot.is_active)}
                                title={bot.is_active ? 'Deactivate' : 'Activate'}
                              >
                                {bot.is_active ? '⏸️' : '▶️'}
                              </button>
                              <button 
                                className="delete-btn"
                                onClick={() => deleteBot(bot.id, bot.name)}
                                title="Delete bot"
                              >
                                🗑️
                              </button>
                            </div>
                          </div>
                          <div className="bot-card-body">
                            <div className="bot-detail">
                              <span className="label">Profession:</span>
                              <span>{bot.profile?.profession || 'N/A'}</span>
                            </div>
                            <div className="bot-detail">
                              <span className="label">Interests:</span>
                              <span className="interests">{bot.profile?.interests || 'N/A'}</span>
                            </div>
                            <div className="bot-detail">
                              <span className="label">Bias:</span>
                              <span className={`bias ${bot.profile?.emotional_bias}`}>
                                {bot.profile?.emotional_bias === 'positive' ? '😊' : 
                                 bot.profile?.emotional_bias === 'negative' ? '😠' : '😐'} 
                                {bot.profile?.emotional_bias}
                              </span>
                            </div>
                            <div className="bot-stats">
                              <span title="Like probability">👍 {Math.round((bot.profile?.like_probability || 0) * 100)}%</span>
                              <span title="Dislike probability">👎 {Math.round((bot.profile?.dislike_probability || 0) * 100)}%</span>
                              <span title="Comment probability">💬 {Math.round((bot.profile?.comment_probability || 0) * 100)}%</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default BotCreator;
