/**
 * @fileOverview React Plotly chart for TCP flag counts
 */

import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { API } from './api.jsx'; // Adjust the path to your API file

export function TcpFlagChart() {
  const [flagData, setFlagData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.partthree(); // Assuming API.partthree() gives this flag JSON
        const raw = response.data;

        // Single object inside array
        if (Array.isArray(raw) && raw.length > 0) {
          setFlagData(raw[0]);
        }
      } catch (err) {
        console.error("Error fetching TCP flag data", err);
      }
    };

    fetchData();
  }, []);

  const keys = Object.keys(flagData);
  const values = Object.values(flagData);

  return (
    <div>
      <h2 style={{ color: 'orange', textAlign: 'center' }}>TCP Flag Distribution</h2>
      <Plot
        data={[
          {
            x: keys,
            y: values,
            type: 'bar',
            marker: {
              color: 'orange'
            },
            hovertemplate: "<b>%{x}</b>: %{y}<extra></extra>"
          }
        ]} 
        
        layout={{
          title: {
            text: 'TCP Flag Distribution',
            font: { size: 20, color: 'orange' }
          },
          xaxis: {
            title: 'TCP Flag',
            tickangle: -45,
            color: 'white'
          },
          yaxis: {
            title: 'Count',
            color: 'white'
          },
          plot_bgcolor: 'rgba(20,20,20,1)',
          paper_bgcolor: 'rgba(10,10,10,1)',
          font: { color: 'white' },
          margin: { l: 40, r: 40, t: 60, b: 80 }
        }}
        style={{ width: '100%', height: '500px' }}
      />
    </div>
  );
}
