# Deployment Guide

## Option 1: Docker (Easiest for Sharing)

### Prerequisites
- Docker & Docker Compose installed

### Deploy
```bash
cd vrbus
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Option 2: Deploy to Cloud Services

### Heroku (Discontinued - Use Alternative)

### Railway.app (Recommended)
1. Sign up at railway.app
2. Create new project
3. Connect GitHub repository
4. Add services: PostgreSQL, Python backend
5. Deploy frontend to Vercel/Netlify

### Render.com
1. Sign up at render.com
2. Create Web Service
3. Connect GitHub
4. Set environment variables
5. Deploy

### Vercel (Frontend Only)
1. Push frontend to GitHub
2. Import project at vercel.com
3. Set `REACT_APP_API_URL` environment variable
4. Deploy

### Netlify (Frontend Only)
1. Push frontend to GitHub
2. Deploy to netlify.com
3. Set build command: `npm run build`
4. Set publish directory: `build`

---

## Option 3: Traditional VPS (DigitalOcean, AWS, Linode)

### Backend Setup
```bash
# SSH into server
ssh root@your_ip

# Install dependencies
apt update && apt install python3-pip python3-venv postgresql postgresql-contrib nodejs npm

# Clone repo
git clone <your-repo>
cd vrbus/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Create .env with database URL
echo "DATABASE_URL=postgresql://user:pass@localhost/busdb" > .env

# Run with gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Frontend Setup
```bash
cd vrbus/frontend

# Install dependencies
npm install

# Build
npm run build

# Serve with nginx
sudo apt install nginx
# Configure nginx as reverse proxy
```

### Setup Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

---

## Option 4: Share as Zip/GitHub

### Create Shareable Package

1. Clean up:
```bash
cd vrbus
rm -rf backend/__pycache__ frontend/node_modules frontend/build venv/.git
```

2. Create zip:
```bash
zip -r busapp.zip vrbus/
```

3. Share and recipients can:
```bash
unzip busapp.zip
cd vrbus

# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/busdb
SECRET_KEY=your-secret-key-here
DEBUG=False  # Set to False in production
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-api.com
```

---

## Production Checklist

- [ ] Change DEBUG to False
- [ ] Set strong SECRET_KEY
- [ ] Use environment variables (not hardcoded secrets)
- [ ] Enable HTTPS
- [ ] Setup database backups
- [ ] Configure CORS properly (not `["*"]`)
- [ ] Use database connection pooling
- [ ] Setup monitoring and logging
- [ ] Add rate limiting
- [ ] Setup CI/CD pipeline

---

## Monitoring & Maintenance

### Logs
```bash
# Backend logs
tail -f /var/log/fastapi.log

# Frontend logs
# Check browser console
```

### Database Backup
```bash
# PostgreSQL backup
pg_dump -U postgres busdb > backup.sql

# Restore
psql -U postgres busdb < backup.sql
```

### Performance Monitoring
- Use New Relic, Datadog, or Sentry
- Monitor API response times
- Track database queries

---

## Scaling

### Horizontal Scaling
- Run multiple backend instances
- Use load balancer (Nginx, HAProxy)
- Cache responses (Redis)

### Database Optimization
- Add indexes to frequently queried columns
- Implement pagination
- Use database replication

---

## Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| CORS errors | Update backend CORS settings with your domain |
| 502 Bad Gateway | Check if backend is running, verify proxy config |
| Database connection failed | Verify DATABASE_URL, check firewall rules |
| Out of memory | Increase server RAM or optimize queries |
| Slow API | Add database indexes, implement caching |

---

## Support

For deployment issues, check:
1. Application logs
2. Server resources (CPU, RAM, disk)
3. Database connection status
4. Network configuration
5. Firewall rules
