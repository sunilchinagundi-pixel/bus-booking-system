from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BusBase(BaseModel):
    name: str
    bus_type: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    total_seats: int
    available_seats: int
    bus_operator: str
    booking_url: str
    amenities: Optional[str] = None
    rating: Optional[float] = 0.0

class BusCreate(BusBase):
    pass

class Bus(BusBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BusSearch(BaseModel):
    source: str
    destination: str
    travel_date: datetime
    limit: int = 50

class BookingBase(BaseModel):
    bus_id: int
    passenger_name: str
    passenger_email: str
    phone: str
    num_tickets: int
    travel_date: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    total_price: float
    booking_date: datetime
    status: str

    class Config:
        from_attributes = True
