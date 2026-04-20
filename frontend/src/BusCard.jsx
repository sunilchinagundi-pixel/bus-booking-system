import React from 'react';
import './index.css';

function BusCard({ bus, onSelect, isExpanded, onToggleExpand }) {
  return (
    <div className="bus-card">
      <div className="bus-header" onClick={onToggleExpand}>
        <div className="bus-info">
          <h3>{bus.name}</h3>
          <p className="bus-operator">{bus.bus_operator}</p>
          <span className={`bus-type ${bus.bus_type}`}>{bus.bus_type.toUpperCase()}</span>
          <span className="rating">⭐ {bus.rating}</span>
        </div>
        <div className="bus-times">
          <div>
            <span className="time">{new Date(bus.departure_time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</span>
            <p className="label">Departure</p>
          </div>
          <div className="route-duration">→</div>
          <div>
            <span className="time">{new Date(bus.arrival_time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</span>
            <p className="label">Arrival</p>
          </div>
        </div>
        <div className="bus-pricing">
          <div className="price">₹{bus.price}</div>
          <p className="seats">{bus.available_seats} seats available</p>
        </div>
      </div>

      {isExpanded && (
        <div className="bus-details">
          <div className="details-row">
            <span className="label">Bus Type:</span>
            <span>{bus.bus_type}</span>
          </div>
          <div className="details-row">
            <span className="label">Amenities:</span>
            <span>{bus.amenities}</span>
          </div>
          <div className="details-row">
            <span className="label">Total Seats:</span>
            <span>{bus.total_seats}</span>
          </div>
          <div className="details-row">
            <span className="label">Available Seats:</span>
            <span>{bus.available_seats}</span>
          </div>
          <button 
            className="book-btn" 
            onClick={() => {
              window.open(bus.booking_url, '_blank');
              onSelect(bus);
            }}
          >
            Book Now on {bus.bus_operator}
          </button>
        </div>
      )}
    </div>
  );
}

export default BusCard;
