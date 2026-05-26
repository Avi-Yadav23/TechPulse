import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TrendingTopics = ({ topics }) => {
  if (!topics || topics.length === 0) {
    return (
      <div className="trending-topics">
        <h2>Trending Topics</h2>
        <p>No topic data available</p>
      </div>
    );
  }

  return (
    <div className="trending-topics">
      <h2>Trending Topics (Last 24h)</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={topics}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendingTopics;