/**
 * @fileOverview API Service Configuration.
 * This module configures and exports API service instances for different parts of the application.
 */

import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const API = {
  about: () => api.get('/'),
  partone: () => api.get('/partone'),
  parttwo: () => api.get('/parttwo'),
};
