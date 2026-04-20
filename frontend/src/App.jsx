import React, { useState } from 'react';
import './App.css';
import SearchForm from './SearchForm';
import BusCard from './BusCard';
import axios from 'axios';

function App() {
  const [buses, setBuses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [expandedBusId, setExpandedBusId] = useState(null);
  const [showMore, setShowMore] = useState(false);
  const [error, setError] = useState(null);
  const [resultsRef, setResultsRef] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || (window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin);

  const handleSearch = async ({ source, destination, date }) => {
    setLoading(true);
    setError(null);
    setSearched(true);
    setShowMore(false);
    setExpandedBusId(null);

    try {
      const response = await axios.post(`${API_URL}/api/buses/search`, {
        source: source.trim(),
        destination: destination.trim(),
        travel_date: new Date(date).toISOString(),
        limit: 50
      });

      setBuses(response.data);
    } catch (err) {
      setError('Failed to search buses. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectBus = (bus) => {
    console.log('Selected bus:', bus);
  };

  const visibleBuses = showMore ? buses : buses.slice(0, 5);

  React.useEffect(() => {
    if (showMore && resultsRef) {
      resultsRef.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [showMore, resultsRef]);

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🚌 Bus Booking System</h1>
          <p>Find and book buses across India</p>
        </div>
      </header>

      <main className="app-main">
        <div className="search-container">
          <SearchForm onSearch={handleSearch} loading={loading} />
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching for buses...</p>
          </div>
        )}

        {searched && !loading && buses.length === 0 && (
          <div className="no-results">
            <p>No buses found. Please try different search parameters.</p>
          </div>
        )}

        {buses.length > 0 && !loading && (
          <div className="results-container" ref={(node) => setResultsRef(node)}>
            <h2>Available Buses ({buses.length})</h2>
            <p className="results-summary">Showing {visibleBuses.length} of {buses.length} results sorted by fare.</p>

            <div className="buses-list">
              {visibleBuses.map((bus) => (
                <BusCard
                  key={bus.id}
                  bus={bus}
                  onSelect={handleSelectBus}
                  isExpanded={expandedBusId === bus.id}
                  onToggleExpand={() => setExpandedBusId(expandedBusId === bus.id ? null : bus.id)}
                />
              ))}
            </div>

            {buses.length > 5 && !showMore && (
              <button className="show-more-btn" onClick={() => setShowMore(true)}>
                Show all {buses.length} buses
              </button>
            )}

            {showMore && buses.length > 5 && (
              <button className="show-more-btn" onClick={() => setShowMore(false)}>
                Show top 5
              </button>
            )}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 Bus Booking System. All rights reserved.</p>
        <p className="disclaimer">
          <small>
            We are facilitators of bus search and booking. All bookings are handled by respective bus operators and their websites.
            We do not guarantee availability or pricing. Please verify with the operator directly.
          </small>
        </p>
      </footer>
    </div>
  );
}

export default App;
