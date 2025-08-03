/**
 * @fileOverview React component that displays the "About" section.
 * It fetches a description from the backend using the API service.
 */

import React, { useState, useEffect } from 'react';
import { API } from './api.jsx';

export function About() {
  const [description, setDescription] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.about();
        setDescription(response.data);
      } catch (error) {
        console.error('Failed to fetch about data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="about">
      <p>{description}</p>
    </div>
  );
}
