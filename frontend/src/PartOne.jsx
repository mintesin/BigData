/**
 * @fileOverview React Plotly chart of cumulative traffic volume over time
 */

import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { API } from './api.jsx'; // adjust path

export function CumulativeTrafficChart() {
  const [plotData, setPlotData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.parttwo(); // Assumes axios: response.data
        const rawData = response.data;

        // Calculate cumulative bytes
        let cumulative = 0;
        const processed = rawData.map(item => {
          cumulative += item.total_bytes;
          return {
            minute: item.minute,
            cumulative_bytes: cumulative
          };
        });

        setPlotData(processed);
      } catch (err) {
        console.error("Error fetching PartTwo data", err);
      }
    };

    fetchData();
  }, []);

  const x = plotData.map(item => item.minute);
  const y = plotData.map(item => item.cumulative_bytes);

  return (
    <div>
      <h2 style={{ color: 'orange', textAlign: 'center' }}>Cumulative Traffic Volume Over Time</h2>
      <Plot
        data={[
          {
            x,
            y,
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: 'orange' },
            line: { width: 2 },
            hovertemplate:
              "<b>Minute</b>: %{x}<br><b>Cumulative Bytes</b>: %{y}<extra></extra>"
          }
        ]}
        layout={{
          title: {
            text: 'Cumulative Traffic Volume Over Time',
            font: { size: 20, color: 'orange' }
          },
          xaxis: {
            title: 'Minute',
            showgrid: true,
            tickangle: -45,
            color: 'white'
          },
          yaxis: {
            title: 'Cumulative Bytes',
            showgrid: true,
            color: 'white'
          },
          hovermode: 'x unified',
          plot_bgcolor: 'rgba(20,20,20,1)',
          paper_bgcolor: 'rgba(10,10,10,1)',
          font: { color: 'white' },
          margin: { l: 40, r: 40, t: 60, b: 80 }
        }}
        style={{ width: "100%", height: "500px" }}
      />
    </div>
  );
}
