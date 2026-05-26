import React from 'react';
import moment from 'moment';

const ArticleFeed = ({ articles, loading }) => {
  if (loading) {
    return <div className="loading">Loading articles...</div>;
  }

  if (!articles || articles.length === 0) {
    return <div className="empty-state">No articles found.</div>;
  }

  return (
    <div className="article-feed">
      <h2>Latest Articles</h2>
      <div className="articles-list">
        {articles.map((article) => (
          <div key={article.id} className="article-card">
            <h3>{article.title}</h3>
            <div className="article-meta">
              <span className="source-badge">{article.source}</span>
              <span className="time-ago">
                {moment(article.published_at).fromNow()}
              </span>
            </div>
            {article.summary && (
              <p className="article-summary">{article.summary}</p>
            )}
            <div className="article-tags">
              {article.tags.map((tag) => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
            <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
              Read full article
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ArticleFeed;