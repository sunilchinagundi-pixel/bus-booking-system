import React, { useState } from 'react';
import './index.css';

function SearchForm({ onSearch, loading }) {
  const [source, setSource] = useState('Bangalore');
  const [destination, setDestination] = useState('Goa');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ source, destination, date });
  };

  const cities = ['Bangalore', 'Goa', 'Mumbai', 'Pune', 'Hyderabad', 'Delhi', 'Chennai', 'Kolkata'];

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>From</label>
        <input
          type="text"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Enter source city"
          list="city-suggestions"
          autoComplete="off"
        />
      </div>

      <div className="form-group">
        <label>To</label>
        <input
          type="text"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="Enter destination city"
          list="city-suggestions"
          autoComplete="off"
        />
      </div>

      <datalist id="city-suggestions">
        {cities.map(city => (
          <option key={city} value={city} />
        ))}
      </datalist>

      <div className="form-group">
        <label>Travel Date</label>
        <input 
          type="date" 
          value={date} 
          onChange={(e) => setDate(e.target.value)}
          min={new Date().toISOString().split('T')[0]}
        />
      </div>

      <button type="submit" disabled={loading} className="search-btn">
        {loading ? 'Searching...' : 'Search Buses'}
      </button>
    </form>
  );
}

export default SearchForm;
