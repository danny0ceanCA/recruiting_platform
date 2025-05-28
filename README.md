# Recruiting Platform

This project provides a simple recruiting platform composed of a FastAPI backend and a React frontend.

## Prerequisites

- **Python 3.8+** – used for the FastAPI backend.
- **Node.js** and **npm** – required to run the React frontend.

## Creating a Python Virtual Environment

Run the included `setup.sh` script from the repository root to create and activate a Python virtual environment and install dependencies from the `vendor/` directory:

```bash
./setup.sh
```

The script detects your Python installation, creates `.venv/`, activates it, and installs all packages listed in `requirements.txt`.

## Environment Variables

Copy `.env.example` to `.env` and modify the values as needed:

```bash
cp .env.example .env
```

The main variables are:

- `DATABASE_URL` – database connection string (defaults to the bundled SQLite database)
- `SECRET_KEY` – key used to sign JWT tokens
- `OPENAI_API_KEY` – your API key for OpenAI services

## Running the Backend

After activating the virtual environment and preparing environment variables, start the FastAPI application with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` and documentation can be accessed at `/docs` when running in development mode.

## Running the Frontend

The React app lives in the `Frontend/` directory. Install dependencies once and start the development server:

```bash
cd Frontend
npm install
npm run dev
```

By default the frontend is served at `http://localhost:5173` and communicates with the FastAPI backend.

## Placement API

Two endpoints allow recording and updating interview or placement status:

- `POST /placements/` – create a new placement entry.
- `PATCH /placements/{id}` – update an existing placement.

Both endpoints require authentication just like the other protected routes.
