# Bus Booking System

A full-stack bus booking application built with FastAPI (Python backend) and React (JavaScript frontend) with PostgreSQL database.

## Features

✅ **Search Buses** - Find buses by source, destination, and date
✅ **Bus Details** - View bus amenities, ratings, operator info, and real-time seat availability
✅ **Government & Private Buses** - Filter and view both types of buses
✅ **Top 5 Display** - Shows top 5 results initially, expandable to show more
✅ **Direct Booking** - Links to official booking websites
✅ **Real-time Availability** - Updated seat counts
✅ **Responsive Design** - Works on desktop and mobile

## Project Structure

```
vrbus/
├── venv/                    # Python virtual environment
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main app component
│   │   ├── App.css         # App styles
│   │   ├── SearchForm.jsx  # Search form component
│   │   ├── BusCard.jsx     # Bus card component
│   │   ├── index.jsx       # React entry point
│   │   └── index.css       # Global styles
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── package.json        # Node dependencies
│   └── .env                # Frontend environment variables
└── README.md               # This file
```

## Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **PostgreSQL 12+** (or you can modify to use SQLite for quick testing)

## Installation & Setup

### 1. Backend Setup

#### Step 1a: Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Step 1b: Configure Database

Option A: Using PostgreSQL (Recommended)
```bash
# Update .env file with your PostgreSQL credentials
# .env example:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/busdb
```

Option B: Using SQLite (Quick Testing)
```bash
# Modify database.py:
# Change: DATABASE_URL = "postgresql://..."
# To: DATABASE_URL = "sqlite:///./test.db"
```

#### Step 1c: Run the backend

```bash
python main.py
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 2. Frontend Setup

#### Step 2a: Install dependencies

```bash
cd frontend
npm install
```

#### Step 2b: Start the development server

```bash
npm start
```

The frontend will open at: `http://localhost:3000`

## API Endpoints

### Search Buses
```
POST /api/buses/search
Content-Type: application/json

{
  "source": "Bangalore",
  "destination": "Goa",
  "travel_date": "2024-04-20T00:00:00",
  "limit": 5
}

Response: [
  {
    "id": 1,
    "name": "Volvo Express",
    "bus_type": "private",
    "source": "Bangalore",
    "destination": "Goa",
    "departure_time": "2024-04-20T06:00:00",
    "arrival_time": "2024-04-20T14:00:00",
    "price": 850,
    "available_seats": 15,
    "bus_operator": "Volvo Travels",
    "booking_url": "https://volvo-travels.com/book",
    "amenities": "AC, WiFi, USB charging, Meal",
    "rating": 4.5
  }
]
```

### Get Bus Details
```
GET /api/buses/{bus_id}
```

### Create Booking
```
POST /api/bookings
Content-Type: application/json

{
  "bus_id": 1,
  "passenger_name": "John Doe",
  "passenger_email": "john@example.com",
  "phone": "9876543210",
  "num_tickets": 2,
  "travel_date": "2024-04-20T00:00:00"
}

Response: {
  "id": 1,
  "bus_id": 1,
  "passenger_name": "John Doe",
  "total_price": 1700,
  "status": "confirmed"
}
```

### Cancel Booking
```
PUT /api/bookings/{booking_id}/cancel
```

## Usage

1. **Start Backend**: Run `python main.py` from backend folder
2. **Start Frontend**: Run `npm start` from frontend folder
3. **Search for Buses**:
   - Select source city (e.g., Bangalore)
   - Select destination city (e.g., Goa)
   - Pick travel date
   - Click "Search Buses"
4. **View Results**:
   - Top 5 buses are displayed
   - Click on any bus to expand and see full details
   - Click "Show X more buses" to see additional results
5. **Book a Bus**:
   - Click "Book Now" to redirect to the bus operator's booking page

## Features Explanation

### Search Functionality
- Searches buses by source, destination, and date
- Filters for available seats only
- Orders results by price (lowest first)

### Expandable Results
- Initially shows top 5 buses
- Click "Show more" to expand the list
- Click on bus card to see full details

### Bus Information Displayed
- Bus name and operator
- Departure and arrival times
- Price per ticket
- Available seats
- Bus type (Government/Private)
- Rating and amenities
- Direct link to booking website

## Database Schema

### Buses Table
- id: Primary key
- name: Bus name
- bus_type: government or private
- source: Departure city
- destination: Arrival city
- departure_time: DateTime
- arrival_time: DateTime
- price: Price per ticket (float)
- total_seats: Total capacity
- available_seats: Current availability
- bus_operator: Operating company
- booking_url: Link to book
- amenities: Comma-separated amenities
- rating: User rating (0-5)

### Bookings Table
- id: Primary key
- bus_id: Foreign key to buses
- passenger_name: Name
- passenger_email: Email
- phone: Contact number
- num_tickets: Number of tickets
- total_price: Total booking amount
- booking_date: When booked
- travel_date: When traveling
- status: pending, confirmed, or cancelled

## Customization

### Add More Sample Data
Edit `populate_sample_data()` in `main.py` to add more buses:

```python
models.Bus(
    name="Your Bus Name",
    bus_type="private",  # or "government"
    source="From City",
    destination="To City",
    departure_time=datetime.now() + timedelta(days=1, hours=8),
    arrival_time=datetime.now() + timedelta(days=1, hours=14),
    price=500,
    total_seats=50,
    available_seats=20,
    bus_operator="Operator Name",
    booking_url="https://booking-link.com",
    amenities="AC, WiFi, Meal",
    rating=4.5
)
```

### Modify Cities List
Edit the cities array in `SearchForm.jsx`:
```javascript
const cities = ['Bangalore', 'Goa', 'Mumbai', 'Pune', 'Hyderabad', 'Delhi', 'Chennai', 'Kolkata'];
```

### Change Styling
All styles are in `App.css`. Modify colors, sizes, and layouts as needed.

## Deployment

### Backend (Heroku/Railway/Render)
1. Create `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Push to hosting platform
3. Set environment variables (DATABASE_URL)

### Frontend (Netlify/Vercel)
1. Run `npm build`
2. Push to GitHub
3. Connect to Netlify/Vercel
4. Set `REACT_APP_API_URL` environment variable

## Troubleshooting

### PostgreSQL Connection Error
- Check PostgreSQL is running
- Verify credentials in .env
- Test connection: `psql -U postgres -d busdb -c "SELECT 1"`

### CORS Error
- Backend CORS is configured for all origins (`allow_origins=["*"]`)
- If error persists, check API URL in frontend .env

### Port Already in Use
- Backend: `uvicorn main:app --port 8001`
- Frontend: `PORT=3001 npm start`

### Module Not Found
- Backend: `pip install -r requirements.txt` in venv
- Frontend: `npm install`

## Technologies Used

**Backend:**
- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Pydantic - Data validation
- Uvicorn - ASGI server

**Frontend:**
- React 18 - UI framework
- Axios - HTTP client
- CSS3 - Styling
- React DOM - DOM rendering

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Payment integration (Stripe, Razorpay)
- [ ] Real-time booking updates (WebSocket)
- [ ] Reviews and ratings system
- [ ] Multiple language support
- [ ] Email notifications
- [ ] Admin panel for bus operators
- [ ] Advanced filtering (stops, WiFi, AC type, etc.)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.

---

**Ready to share!** You can now share this project with others. They just need to follow the Installation & Setup section.
