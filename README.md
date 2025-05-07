# Toolbox API

A simple text processing service that accepts text input and responds with a specific message.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Process Text
- **URL**: `/process`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "text": "your text here (1-100 characters)"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Hi I'm your toolbox agent"
  }
  ```

## API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc