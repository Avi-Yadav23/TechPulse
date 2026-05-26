import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00bfff', '#ff6b6b', '#4ecdc4'];

const SourceBreakdown = ({ sources }) => {
  if (!sources || Object.keys(sources).length === 0) {
    return (
      <div className="source-breakdown">
        <h2>Source Breakdown</h2>
        <p>No source data available</p>
      </div>
    );
  }

  // Convert sources object to array of objects for Recharts
  const sourceData = Object.entries(sources).map(([name, count]) => ({
    name,
    count,
    fill: COLORS[Object.keys(sources).indexOf(name) % COLORS.length]
  }));

  return (
    <div className="source-breakdown">
      <h2>Articles by Source</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={sourceData}
            dataKey="count"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={120}
            labelLine={false}
            label={({ name, percent }) => (
              `${name}: ${(percent * 100).toFixed(0)}%`
            )}
          >
            {sourceData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SourceBreakdown;