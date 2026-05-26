import React, { useState, useEffect } from 'react';

const SearchBar = ({
  searchTerm,
  onSearchChange,
  onTopicChange,
  onSourceChange,
  selectedTopic,
  selectedSource,
  topics,
  sources
}) => {
  const [filteredTopics, setFilteredTopics] = useState([]);
  const [filteredSources, setFilteredSources] = useState([]);

  useEffect(() => {
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      setFilteredTopics(
        topics
          .filter((topic) => topic.name.toLowerCase().includes(term))
          .map((topic) => topic.name)
      );
      setFilteredSources(
        sources.filter((source) => source.toLowerCase().includes(term))
      );
    } else {
      setFilteredTopics([]);
      setFilteredSources([]);
    }
  }, [searchTerm, topics, sources]);

  return (
    <div className="search-bar">
      <h2>Search & Filter</h2>

      <div className="search-input">
        <input
          type="text"
          placeholder="Search articles..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      <div className="filters">
        <div className="filter-group">
          <label>Topic:</label>
          <select
            value={selectedTopic}
            onChange={(e) => onTopicChange(e.target.value)}
          >
            <option value="">All Topics</option>
            {topics.map((topic) => (
              <option key={topic.name} value={topic.name}>
                {topic.name} ({topic.count})
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Source:</label>
          <select
            value={selectedSource}
            onChange={(e) => onSourceChange(e.target.value)}
          >
            <option value="">All Sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
        </div>
      </div>

      {searchTerm && (
        <div className="search-suggestions">
          <h3>Suggestions:</h3>
          {(filteredTopics.length > 0 || filteredSources.length > 0) ? (
            <>
              {filteredTopics.length > 0 && (
                <div>
                  <strong>Topics:</strong>
                  <span>{filteredTopics.join(', ')}</span>
                </div>
              )}
              {filteredSources.length > 0 && (
                <div>
                  <strong>Sources:</strong>
                  <span>{filteredSources.join(', ')}</span>
                </div>
              )}
            </>
          ) : (
            <p>No matching topics or sources yet.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
