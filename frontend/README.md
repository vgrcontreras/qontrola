# Qontrola Frontend

A Streamlit-based frontend application for the Qontrola project management system.

## Features

- JWT-based authentication with the FastAPI backend
- Modern and responsive login interface
- User dashboard with authentication status
- Secure token handling and session management

## Setup

1. Install dependencies:
   ```bash
   cd frontend
   pip install -r requirements.txt
   # or using poetry
   poetry install
   ```

2. Configure environment variables (optional):
   ```bash
   export BACKEND_URL=http://localhost:8000
   export REQUEST_TIMEOUT=10
   ```

3. Run the application:
   ```bash
   streamlit run src/main.py
   # or directly
   streamlit run src/login.py
   ```

## Configuration

The application can be configured using environment variables:

- `BACKEND_URL`: URL of the FastAPI backend (default: http://localhost:8000)
- `REQUEST_TIMEOUT`: HTTP request timeout in seconds (default: 10)
- `PAGE_TITLE`: Application page title (default: Qontrola)
- `PAGE_ICON`: Application page icon (default: 🔐)

## Usage

1. Start the FastAPI backend server
2. Run the Streamlit frontend application
3. Navigate to the provided URL (usually http://localhost:8501)
4. Login with your credentials
5. Access the dashboard after successful authentication

## Authentication Flow

1. User enters email and password
2. Frontend sends credentials to `/token/` endpoint
3. Backend validates credentials and returns JWT token
4. Frontend stores token in session state
5. Token is used for subsequent API calls to protected endpoints

## File Structure

```
frontend/src/
├── main.py          # Main entry point
├── login.py         # Login page and authentication logic
└── config.py        # Configuration settings
```

## Dependencies

- `streamlit`: Web application framework
- `requests`: HTTP client for API calls
- `pydantic`: Data validation and settings management
