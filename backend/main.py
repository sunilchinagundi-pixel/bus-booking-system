from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
import schemas
from database import engine, get_db
import openai
import json
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")  # Replace with actual key

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bus Booking API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data function to populate database (for demo)
def populate_sample_data(db: Session):
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    today_date = base_date - timedelta(days=1)
    sample_buses = [
        models.Bus(
            name="Volvo Express",
            bus_type="private",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=6),
            arrival_time=base_date + timedelta(hours=14),
            price=850,
            total_seats=45,
            available_seats=15,
            bus_operator="Volvo Travels",
            booking_url="https://volvo-travels.com/book",
            amenities="AC, WiFi, USB charging, Meal",
            rating=4.5
        ),
        models.Bus(
            name="Government Bus 101",
            bus_type="government",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=8),
            arrival_time=base_date + timedelta(hours=16),
            price=450,
            total_seats=60,
            available_seats=25,
            bus_operator="Karnataka State Bus",
            booking_url="https://ksrtc.in/book",
            amenities="AC, Basic facilities",
            rating=3.8
        ),
        models.Bus(
            name="Bangalore Mumbai Express",
            bus_type="private",
            source="Bangalore",
            destination="Mumbai",
            departure_time=today_date + timedelta(hours=10),
            arrival_time=today_date + timedelta(hours=22),
            price=1200,
            total_seats=50,
            available_seats=20,
            bus_operator="Redbus Express",
            booking_url="https://redbus.in",
            amenities="AC, WiFi, Snacks",
            rating=4.3
        ),
        models.Bus(
            name="Mumbai Night Bus",
            bus_type="government",
            source="Bangalore",
            destination="Mumbai",
            departure_time=today_date + timedelta(hours=22),
            arrival_time=today_date + timedelta(hours=34),
            price=800,
            total_seats=60,
            available_seats=30,
            bus_operator="Maharashtra State Bus",
            booking_url="https://msrtc.in/book",
            amenities="AC, Basic facilities",
            rating=3.9
        ),
        models.Bus(
            name="SRS Travels",
            bus_type="private",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=18),
            arrival_time=base_date + timedelta(hours=26),
            price=650,
            total_seats=50,
            available_seats=8,
            bus_operator="SRS Transport",
            booking_url="https://srs-travels.com",
            amenities="AC, WiFi, Reclining seats",
            rating=4.2
        ),
        models.Bus(
            name="Tourist Coach",
            bus_type="private",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=20),
            arrival_time=base_date + timedelta(hours=28),
            price=900,
            total_seats=40,
            available_seats=3,
            bus_operator="Tourist Travels",
            booking_url="https://tourist-travels.com",
            amenities="Premium AC, WiFi, Meal, Entertainment",
            rating=4.8
        ),
        models.Bus(
            name="Redbus Express",
            bus_type="private",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=10),
            arrival_time=base_date + timedelta(hours=18),
            price=750,
            total_seats=55,
            available_seats=20,
            bus_operator="Redbus Partner",
            booking_url="https://redbus.in",
            amenities="AC, WiFi, Snacks",
            rating=4.3
        ),
        models.Bus(
            name="MH State Bus",
            bus_type="government",
            source="Bangalore",
            destination="Goa",
            departure_time=base_date + timedelta(hours=12),
            arrival_time=base_date + timedelta(hours=20),
            price=500,
            total_seats=65,
            available_seats=35,
            bus_operator="Maharashtra State Bus",
            booking_url="https://msrtc.in/book",
            amenities="AC, Standard facilities",
            rating=3.5
        ),
        models.Bus(
            name="Bijapur Star",
            bus_type="private",
            source="Bangalore",
            destination="Bijapur",
            departure_time=base_date + timedelta(hours=11),
            arrival_time=base_date + timedelta(hours=23),
            price=720,
            total_seats=40,
            available_seats=20,
            bus_operator="Bijapur Travels",
            booking_url="https://bijapurtravels.com/book",
            amenities="AC, WiFi, Snacks",
            rating=4.0
        ),
        models.Bus(
            name="Bijapur Comfort",
            bus_type="government",
            source="Bangalore",
            destination="Bijapur",
            departure_time=base_date + timedelta(hours=9),
            arrival_time=base_date + timedelta(hours=21),
            price=540,
            total_seats=50,
            available_seats=30,
            bus_operator="Karnataka State Bus",
            booking_url="https://ksrtc.in/book",
            amenities="AC, Basic facilities",
            rating=3.7
        ),
        models.Bus(
            name="Delhi Superfast",
            bus_type="private",
            source="Delhi",
            destination="Mumbai",
            departure_time=base_date + timedelta(hours=7),
            arrival_time=base_date + timedelta(hours=19),
            price=1200,
            total_seats=50,
            available_seats=22,
            bus_operator="Delhi Travels",
            booking_url="https://delhitravels.com/book",
            amenities="AC, WiFi, Reclining seats",
            rating=4.1
        ),
        models.Bus(
            name="Chennai Cruiser",
            bus_type="private",
            source="Chennai",
            destination="Bangalore",
            departure_time=base_date + timedelta(hours=9),
            arrival_time=base_date + timedelta(hours=15),
            price=650,
            total_seats=40,
            available_seats=18,
            bus_operator="Chennai Express",
            booking_url="https://chennaiexpress.com",
            amenities="AC, WiFi, Snacks",
            rating=4.4
        ),
        models.Bus(
            name="Hyderabad Optima",
            bus_type="private",
            source="Hyderabad",
            destination="Pune",
            departure_time=base_date + timedelta(hours=10),
            arrival_time=base_date + timedelta(hours=20),
            price=700,
            total_seats=45,
            available_seats=12,
            bus_operator="Hyderabad Tours",
            booking_url="https://hydtours.com/book",
            amenities="AC, WiFi, Charging ports",
            rating=4.2
        ),
        models.Bus(
            name="Kolkata Comfort",
            bus_type="government",
            source="Kolkata",
            destination="Darjeeling",
            departure_time=base_date + timedelta(hours=6),
            arrival_time=base_date + timedelta(hours=16),
            price=520,
            total_seats=55,
            available_seats=28,
            bus_operator="West Bengal State Bus",
            booking_url="https://wbsrtc.in/book",
            amenities="AC, Basic facilities",
            rating=3.7
        ),
        models.Bus(
            name="Pune Night Rider",
            bus_type="private",
            source="Pune",
            destination="Goa",
            departure_time=base_date + timedelta(hours=22),
            arrival_time=base_date + timedelta(hours=30),
            price=780,
            total_seats=48,
            available_seats=14,
            bus_operator="Pune Travels",
            booking_url="https://punetravels.com",
            amenities="AC, WiFi, Bed seats",
            rating=4.6
        ),
        models.Bus(
            name="Mumbai Express",
            bus_type="government",
            source="Mumbai",
            destination="Pune",
            departure_time=base_date + timedelta(hours=8),
            arrival_time=base_date + timedelta(hours=11),
            price=300,
            total_seats=60,
            available_seats=40,
            bus_operator="Maharashtra State Bus",
            booking_url="https://msrtc.in/book",
            amenities="AC, Basic facilities",
            rating=3.6
        ),
        models.Bus(
            name="Delhi Jaipur Superfast",
            bus_type="private",
            source="Delhi",
            destination="Jaipur",
            departure_time=today_date + timedelta(hours=6),
            arrival_time=today_date + timedelta(hours=12),
            price=600,
            total_seats=45,
            available_seats=25,
            bus_operator="Rajasthan Travels",
            booking_url="https://rajasthantravels.com",
            amenities="AC, WiFi",
            rating=4.0
        ),
        models.Bus(
            name="Chennai Hyderabad AC",
            bus_type="private",
            source="Chennai",
            destination="Hyderabad",
            departure_time=today_date + timedelta(hours=14),
            arrival_time=today_date + timedelta(hours=20),
            price=750,
            total_seats=50,
            available_seats=18,
            bus_operator="APSRTC Partner",
            booking_url="https://apsrtc.in",
            amenities="AC, Snacks",
            rating=4.2
        ),
        models.Bus(
            name="Kolkata Mumbai Express",
            bus_type="private",
            source="Kolkata",
            destination="Mumbai",
            departure_time=base_date + timedelta(hours=20),
            arrival_time=base_date + timedelta(hours=44),
            price=1500,
            total_seats=40,
            available_seats=15,
            bus_operator="West Bengal Travels",
            booking_url="https://wbtravels.com",
            amenities="AC, Meal",
            rating=4.1
        ),
        models.Bus(
            name="Ahmedabad Bangalore Sleeper",
            bus_type="private",
            source="Ahmedabad",
            destination="Bangalore",
            departure_time=today_date + timedelta(hours=21),
            arrival_time=today_date + timedelta(hours=45),
            price=1300,
            total_seats=35,
            available_seats=10,
            bus_operator="Gujarat Travels",
            booking_url="https://gujarattravels.com",
            amenities="AC, Sleeper, WiFi",
            rating=4.4
        ),
        models.Bus(
            name="Pune Delhi Night Bus",
            bus_type="government",
            source="Pune",
            destination="Delhi",
            departure_time=base_date + timedelta(hours=22),
            arrival_time=base_date + timedelta(hours=46),
            price=1100,
            total_seats=55,
            available_seats=28,
            bus_operator="Haryana Roadways",
            booking_url="https://hrtc.in",
            amenities="AC, Basic",
            rating=3.8
        ),
        models.Bus(
            name="Jaipur Udaipur Local",
            bus_type="government",
            source="Jaipur",
            destination="Udaipur",
            departure_time=today_date + timedelta(hours=8),
            arrival_time=today_date + timedelta(hours=14),
            price=400,
            total_seats=60,
            available_seats=35,
            bus_operator="Rajasthan State Bus",
            booking_url="https://rsrtc.in",
            amenities="AC",
            rating=3.7
        ),
        models.Bus(
            name="Hyderabad Vijayawada Express",
            bus_type="private",
            source="Hyderabad",
            destination="Vijayawada",
            departure_time=today_date + timedelta(hours=9),
            arrival_time=today_date + timedelta(hours=13),
            price=350,
            total_seats=50,
            available_seats=22,
            bus_operator="TSRTC Partner",
            booking_url="https://tsrtc.in",
            amenities="AC, WiFi",
            rating=4.0
        ),
        models.Bus(
            name="Surat Vadodara AC",
            bus_type="private",
            source="Surat",
            destination="Vadodara",
            departure_time=today_date + timedelta(hours=7),
            arrival_time=today_date + timedelta(hours=9),
            price=250,
            total_seats=45,
            available_seats=30,
            bus_operator="Gujarat Travels",
            booking_url="https://gujarattravels.com",
            amenities="AC",
            rating=3.9
        ),
        models.Bus(
            name="Lucknow Kanpur State Bus",
            bus_type="government",
            source="Lucknow",
            destination="Kanpur",
            departure_time=today_date + timedelta(hours=10),
            arrival_time=today_date + timedelta(hours=12),
            price=200,
            total_seats=65,
            available_seats=40,
            bus_operator="Uttar Pradesh State Bus",
            booking_url="https://upsrtc.in",
            amenities="Basic",
            rating=3.5
        ),
    ]

    for sample_bus in sample_buses:
        existing = db.query(models.Bus).filter(models.Bus.name == sample_bus.name).first()
        if not existing:
            db.add(sample_bus)
        else:
            existing.bus_type = sample_bus.bus_type
            existing.source = sample_bus.source
            existing.destination = sample_bus.destination
            existing.departure_time = sample_bus.departure_time
            existing.arrival_time = sample_bus.arrival_time
            existing.price = sample_bus.price
            existing.total_seats = sample_bus.total_seats
            existing.available_seats = sample_bus.available_seats
            existing.bus_operator = sample_bus.bus_operator
            existing.booking_url = sample_bus.booking_url
            existing.amenities = sample_bus.amenities
            existing.rating = sample_bus.rating
    db.commit()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Bus Booking API", "version": "1.0.0"}

# Search buses
@app.post("/api/buses/search")
def search_buses(search: schemas.BusSearch, db: Session = Depends(get_db)):
    try:
        # Use OpenAI to generate bus data
        prompt = f"""
        Generate 20 realistic bus options from {search.source} to {search.destination} in India on {search.travel_date.strftime('%Y-%m-%d')}.
        Each bus should have:
        - name: bus name
        - bus_type: "private" or "government"
        - departure_time: ISO format datetime (around {search.travel_date.strftime('%Y-%m-%d')} 06:00 to 22:00)
        - arrival_time: ISO format datetime (next day if overnight)
        - price: integer between 200-2000 INR
        - total_seats: 40-65
        - available_seats: 10-50
        - bus_operator: realistic Indian operator name
        - booking_url: "https://redbus.in" or similar
        - amenities: comma-separated list
        - rating: float 3.5-4.8

        Return as JSON array of objects. Make sure departure times are on the travel date.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        
        bus_data = json.loads(response.choices[0].message.content.strip())
        print(f"AI generated {len(bus_data)} buses for {search.source} to {search.destination}")
        
        # Convert to Bus objects
        buses = []
        for item in bus_data[:search.limit]:
            try:
                bus = models.Bus(
                    name=item.get('name', 'Unknown Bus'),
                    bus_type=item.get('bus_type', 'private'),
                    source=search.source,
                    destination=search.destination,
                    departure_time=datetime.fromisoformat(item['departure_time']),
                    arrival_time=datetime.fromisoformat(item['arrival_time']),
                    price=int(item.get('price', 500)),
                    total_seats=int(item.get('total_seats', 50)),
                    available_seats=int(item.get('available_seats', 20)),
                    bus_operator=item.get('bus_operator', 'Operator'),
                    booking_url=item.get('booking_url', 'https://redbus.in'),
                    amenities=item.get('amenities', 'AC'),
                    rating=float(item.get('rating', 4.0))
                )
                buses.append(bus)
            except Exception as e:
                continue
        
        # Sort by price
        buses.sort(key=lambda x: x.price)
        
        return buses
    
    except Exception as e:
        print(f"AI failed: {e}, using fallback")
        # Fallback to sample data if AI fails
        populate_sample_data(db)
        travel_date_start = datetime(
            search.travel_date.year,
            search.travel_date.month,
            search.travel_date.day,
            0, 0, 0
        )
        travel_date_end = travel_date_start + timedelta(days=1)
        
        buses = db.query(models.Bus).filter(
            models.Bus.source.ilike(f"%{search.source}%"),
            models.Bus.destination.ilike(f"%{search.destination}%"),
            models.Bus.departure_time >= travel_date_start,
            models.Bus.departure_time < travel_date_end,
            models.Bus.available_seats > 0
        ).order_by(models.Bus.price).limit(search.limit).all()
        
        return buses

# Get all buses
@app.get("/api/buses")
def get_all_buses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    populate_sample_data(db)
    buses = db.query(models.Bus).offset(skip).limit(limit).all()
    return buses

# Get bus by ID
@app.get("/api/buses/{bus_id}")
def get_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

# Create booking
@app.post("/api/bookings")
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == booking.bus_id).first()
    
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    if bus.available_seats < booking.num_tickets:
        raise HTTPException(status_code=400, detail="Not enough available seats")
    
    total_price = bus.price * booking.num_tickets
    
    new_booking = models.Booking(
        bus_id=booking.bus_id,
        passenger_name=booking.passenger_name,
        passenger_email=booking.passenger_email,
        phone=booking.phone,
        num_tickets=booking.num_tickets,
        total_price=total_price,
        travel_date=booking.travel_date,
        status="confirmed"
    )
    
    # Update available seats
    bus.available_seats -= booking.num_tickets
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

# Get bookings
@app.get("/api/bookings/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# Cancel booking
@app.put("/api/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    bus = db.query(models.Bus).filter(models.Bus.id == booking.bus_id).first()
    bus.available_seats += booking.num_tickets
    
    booking.status = "cancelled"
    db.commit()
    
    return booking

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
