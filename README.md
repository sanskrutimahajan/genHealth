# GenHealth REST API

A FastAPI-based REST API for managing medical orders with PDF document processing and OCR capabilities.

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete operations for Order entities
- **PDF Processing**: Upload PDF documents and extract patient information using OCR
- **Database Persistence**: SQLite database with automatic table creation
- **Activity Logging**: Comprehensive logging of all API interactions
- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`

## Project Structure

```
genHealth/
├── app/
│   ├── __init__.py          # Python package marker
│   ├── main.py              # FastAPI application and endpoints
│   ├── database.py          # Database connection and session management
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic models for validation
│   ├── crud.py              # Database operations (CRUD)
│   ├── utils.py             # PDF processing and OCR utilities
│   └── logger.py            # Activity logging middleware
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── DEPLOYMENT.md           # Deployment instructions
```

## API Endpoints

### Core Endpoints
- `GET /` - Health check and API info
- `POST /orders/` - Create a new order
- `GET /orders/` - Get all orders
- `GET /orders/{order_id}` - Get specific order
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

### PDF Processing
- `POST /upload/` - Upload PDF and extract patient information

### Activity Logs
- `GET /activity-logs/` - Get all activity logs
- `GET /activity-logs/order/{order_id}` - Get logs for specific order

## Setup and Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system dependencies** (for OCR):
   ```bash
   brew install tesseract poppler  # macOS
   ```

3. **Run the application**:
   ```bash
   python -m app.main
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Key Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation using Python type annotations
- **PyPDF2**: PDF text extraction
- **Tesseract OCR**: Optical Character Recognition for image-based PDFs
- **SQLite**: Lightweight database for data persistence

## Database Models

### Order
- `id`: Primary key
- `first_name`: Patient's first name
- `last_name`: Patient's last name
- `date_of_birth`: Patient's date of birth
- `created_at`: Timestamp when order was created
- `updated_at`: Timestamp when order was last updated

### ActivityLog
- `id`: Primary key
- `timestamp`: When the activity occurred
- `method`: HTTP method (GET, POST, etc.)
- `endpoint`: API endpoint accessed
- `action`: Description of the action
- `order_id`: Associated order (if applicable)
- `details`: Additional details about the activity

## PDF Processing Flow

1. **Upload**: Client uploads PDF via `/upload/` endpoint
2. **Text Extraction**: Attempt to extract text using PyPDF2
3. **OCR Fallback**: If no text found, use Tesseract OCR to process images
4. **Pattern Matching**: Apply regex patterns to extract patient information
5. **Order Creation**: Create order in database with extracted data
6. **Activity Logging**: Log the upload activity

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions to various platforms including Railway, Render, Heroku, and DigitalOcean.

## Testing

The API includes comprehensive error handling and validation. Test the endpoints using the interactive Swagger UI at `/docs`. 