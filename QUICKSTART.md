# Quick Start Guide

## For First-Time Users

### Step 1: Clone/Download the Project
```bash
git clone <repository-url>
cd vrbus
```

### Step 2: Start Backend (Terminal 1)
```bash
# Navigate to backend
cd backend

# Activate Python virtual environment (if not already)
..\venv\Scripts\activate  # Windows
# or
source ../venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py
```

Backend will start at: **http://localhost:8000**

### Step 3: Start Frontend (Terminal 2)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run frontend
npm start
```

Frontend will start at: **http://localhost:3000**

### Step 4: Use the Application

1. Open http://localhost:3000 in your browser
2. Search for buses:
   - Select "From": Bangalore (or other city)
   - Select "To": Goa (or other city)
   - Pick a date
   - Click "Search Buses"
3. Results will show top 5 buses
4. Click on any bus to see full details
5. Click "Book Now" to go to booking website

---

## Database Setup

### Option A: Using SQLite (Easiest - No Installation Needed)

1. Open `backend/database.py`
2. Find this line:
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/busdb")
   ```
3. Replace with:
   ```python
   DATABASE_URL = "sqlite:///./buses.db"
   ```
4. Save and run backend - it will create database automatically

### Option B: Using PostgreSQL

1. Install PostgreSQL: https://www.postgresql.org/download/
2. Create database:
   ```bash
   psql -U postgres
   CREATE DATABASE busdb;
   ```
3. Update `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/busdb
   ```
4. Run backend

---

## Sample Data

The application includes sample buses for:
- **Route**: Bangalore → Goa
- **Bus Count**: 6 buses (3 government, 3 private)
- **Prices**: ₹450 - ₹900

Data loads automatically on first search.

---

## Features

✅ Search buses by city and date
✅ View 5 buses initially
✅ Expand to see more buses
✅ See bus details (amenities, rating, operator)
✅ Direct booking links
✅ Real-time seat availability
✅ Government and private buses
✅ Mobile responsive

---

## File Structure Overview

```
vrbus/
├── venv/               # Python environment (already created)
├── backend/
│   ├── main.py        # FastAPI app - contains routes
│   ├── models.py      # Database models
│   ├── schemas.py     # Data schemas
│   ├── database.py    # Database config
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx    # Main component
│   │   ├── App.css    # Styling
│   │   ├── SearchForm.jsx
│   │   └── BusCard.jsx
│   ├── package.json
│   └── public/index.html
└── README.md
```

---

## Common Issues & Fix

| Issue | Fix |
|-------|-----|
| Port 8000 in use | Run: `python -m uvicorn main:app --port 8001` |
| Port 3000 in use | Run: `PORT=3001 npm start` |
| npm: command not found | Install Node.js from nodejs.org |
| pip: command not found | Use `python -m pip install -r requirements.txt` |
| Database error | Use SQLite option (see Database Setup above) |

---

## Next Steps

1. ✅ Backend running? Check http://localhost:8000/docs
2. ✅ Frontend running? Check http://localhost:3000
3. ✅ Can search buses? Try searching!
4. ✅ Want to customize? Edit cities, add more buses, change colors

---

**Enjoy! The app is ready to use and share.** 🚌
