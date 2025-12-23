import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getCurrentUser: () => api.get('/auth/me'),
};

// Post APIs
export const postAPI = {
  createPost: (data) => api.post('/posts/', data),
  getPosts: (skip = 0, limit = 20) => api.get(`/posts/?skip=${skip}&limit=${limit}`),
  getPost: (id) => api.get(`/posts/${id}`),
  deletePost: (id) => api.delete(`/posts/${id}`),
};

// Comment APIs
export const commentAPI = {
  createComment: (postId, content) => api.post(`/posts/${postId}/comments`, { content }),
  getComments: (postId) => api.get(`/posts/${postId}/comments`),
  deleteComment: (commentId) => api.delete(`/posts/comments/${commentId}`),
};

// Reaction APIs
export const reactionAPI = {
  createReaction: (postId, isLike) => api.post(`/posts/${postId}/reactions`, { is_like: isLike }),
  deleteReaction: (postId) => api.delete(`/posts/${postId}/reactions`),
};

// Bot APIs
export const botAPI = {
  createBot: (data) => api.post('/bots/', data),
  getBots: () => api.get('/bots/'),
  getBot: (id) => api.get(`/bots/${id}`),
  toggleBot: (id) => api.patch(`/bots/${id}/toggle`),
  deleteBot: (id) => api.delete(`/bots/${id}`),
  processPosts: (hours = 24) => api.post(`/bots/process-posts?hours=${hours}`),
};

export default api;
