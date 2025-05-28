# Recruiting Platform

A lightweight recruiting platform featuring a FastAPI backend and a React frontend. The backend exposes REST APIs while the frontend is built with Vite and Tailwind CSS.

## Backend Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the server**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```
   The API will be available at `http://localhost:8001`.

The backend uses SQLite (`test.db`) by default. Create a `.env` file with `DATABASE_URL` or other settings if needed.

## Frontend Setup

1. **Install Node.js packages**
   ```bash
   cd Frontend
   npm install
   ```
2. **Start the React dev server**
   ```bash
   npm run dev
   ```
   Vite runs on port 5173 by default and expects the API at `http://localhost:8001`.

## Project Structure

- `app/` – FastAPI application
- `Frontend/` – React client
- `requirements.txt` – Python dependencies
- `scripts/` – helper scripts
