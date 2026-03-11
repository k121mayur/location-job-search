# Job Nearby Application

A minimalist, mobile-friendly job posting and nearby job discovery application built with Python Flask and SQLite.

## Overview
This application allows:
- **Employers** to post job listings and pin their exact locations on a map.
- **Employees** to set their home location and discover jobs within a 3 km radius using accurate Haversine distance calculations.

## Technology Stack
- **Backend:** Python Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Maps:** Leaflet.js with OpenStreetMap

## Database Schema
The database uses two tables:

**`jobs`**
- `id` (Integer, Primary Key)
- `title` (String, Required)
- `short_description` (String, Optional)
- `description` (Text, Required)
- `latitude` (Float, Required)
- `longitude` (Float, Required)
- `created_at` (DateTime)

**`employees`**
- `id` (Integer, Primary Key)
- `email` (String, Unique, Required)
- `home_latitude` (Float, Optional)
- `home_longitude` (Float, Optional)

## Local Installation

1. **Clone or Download the Repository**
2. **Navigate to the Project Directory**
   ```bash
   cd location-job-search
   ```
3. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Set Environment Variables**
   Ensure the `.env` file is present in the root directory with the default credentials:
   ```env
   EMPLOYER_EMAIL=employer@siliconmango.in
   EMPLOYER_PASSWORD=password
   EMPLOYEE_EMAIL=employee@siliconmango.in
   EMPLOYEE_PASSWORD=password
   SECRET_KEY=your_secret_key_here
   ```
6. **Run the Application**
   ```bash
   cd app
   python app.py
   ```
   The application will automatically create the SQLite database in the `database` folder on the first run.
7. **Access the App**
   Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment Guide

### General VPS Deployment (Linux/Ubuntu)
1. Install Python, pip, and Nginx.
2. Clone the repository to `/var/www/location-job-search`.
3. Set up a virtual environment and install requirements.
4. Use `Gunicorn` to serve the Flask application:
   ```bash
   pip install gunicorn
   cd app
   gunicorn -w 4 -b 127.0.0.1:8000 app:app
   ```
5. Configure Nginx as a reverse proxy to forward port 80/443 traffic to `127.0.0.1:8000`.
6. Use `systemd` or `Supervisor` to keep the Gunicorn process running in the background.

### Render / Railway Deployment
1. Connect your GitHub repository to Render/Railway.
2. Add a Start Command:
   ```bash
   cd app && gunicorn app:app
   ```
3. Add the Environment Variables (from `.env`) in the platform's dashboard.
4. Note: On ephemeral file systems (like Render's free tier), SQLite data will not persist across redeploys. For production, it's recommended to migrate to PostgreSQL or attach a persistent disk.

## Security Note
- Passwords currently exist in plaintext for simplicity. For production setups, generate hashes.
- Endpoints check user role directly from secure session cookies.
