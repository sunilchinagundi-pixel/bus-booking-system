from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bus_type = Column(String)  # "government" or "private"
    source = Column(String, index=True)
    destination = Column(String, index=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    price = Column(Float)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    bus_operator = Column(String)
    booking_url = Column(String)
    amenities = Column(String)  # JSON string or comma-separated
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer)
    passenger_name = Column(String)
    passenger_email = Column(String)
    phone = Column(String)
    num_tickets = Column(Integer)
    total_price = Column(Float)
    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    travel_date = Column(DateTime)
    status = Column(String, default="pending")  # pending, confirmed, cancelled
