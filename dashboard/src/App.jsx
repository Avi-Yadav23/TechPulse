import React, { useState, useEffect } from 'react';
import ArticleFeed from './components/ArticleFeed';
import TrendingTopics from './components/TrendingTopics';
import SourceBreakdown from './components/SourceBreakdown';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [topics, setTopics] = useState([]);
  const [sources, setSources] = useState({});
  const [stats, setStats] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedSource, setSelectedSource] = useState('');
  const [loading, setLoading] = useState(true);

  const API_BASE = process.env.REACT_APP_API_URL || '/api';

  const fetchArticles = async () => {
    try {
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (selectedTopic) params.append('topic', selectedTopic);
      if (selectedSource) params.append('source', selectedSource);
      params.append('limit', '50');

      const response = await fetch(API_BASE + '/articles?' + params.toString());
      const data = await response.json();
      setArticles(data.articles || []);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTopics = async () => {
    try {
      const response = await fetch(API_BASE + '/topics/trending');
      const data = await response.json();
      setTopics(data.topics || []);
    } catch (error) {
      console.error('Error fetching topics:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(API_BASE + '/stats');
      const data = await response.json();
      setStats(data);
      setSources(data.sources || {});
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      await fetchArticles();
      await fetchTopics();
      await fetchStats();
    };

    loadData();

    const articleInterval = setInterval(fetchArticles, 60000);
    const topicsInterval = setInterval(fetchTopics, 300000);
    const statsInterval = setInterval(fetchStats, 60000);

    return () => {
      clearInterval(articleInterval);
      clearInterval(topicsInterval);
      clearInterval(statsInterval);
    };
  }, [searchTerm, selectedTopic, selectedSource]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>TechPulse</h1>
        <p>AI & Tech News Aggregator</p>
        {!loading && stats.last_scrape_at && (
          <div className="stats-bar">
            <span>Total Articles: {stats.total_articles?.toLocaleString() || 0}</span>
            <span>Last Update: {new Date(stats.last_scrape_at).toLocaleTimeString()}</span>
            <span>Duplicates Removed: {stats.duplicates_removed_24h?.toLocaleString() || 0}</span>
          </div>
        )}
      </header>

      <main>
        <SearchBar
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          onTopicChange={setSelectedTopic}
          onSourceChange={setSelectedSource}
          selectedTopic={selectedTopic}
          selectedSource={selectedSource}
          topics={topics}
          sources={Object.keys(sources)}
        />

        <div className="dashboard-content">
          <section className="article-feed">
            <ArticleFeed articles={articles} loading={loading} />
          </section>

          <aside className="sidebar">
            <TrendingTopics topics={topics} />
            <SourceBreakdown sources={sources} />
          </aside>
        </div>
      </main>
    </div>
  );
}

export default App;
