# GenHealth API - REST API with PDF OCR and Activity Logging

## 🚀 **Project Overview**
I built a complete REST API that extracts patient information from PDF documents using OCR technology and logs all user activity. The API is deployed and publicly accessible.

## 🌐 **Live Demo**
- **API URL**: https://web-production-f830.up.railway.app
- **Documentation**: https://web-production-f830.up.railway.app/docs
- **GitHub**: https://github.com/sanskrutimahajan/genHealth

## ✅ **Requirements Met**

### 1. CRUD Operations for Orders
- **GET** `/orders/` - List all orders
- **POST** `/orders/` - Create new order
- **GET** `/orders/{id}` - Get specific order
- **PUT** `/orders/{id}` - Update order
- **DELETE** `/orders/{id}` - Delete order

### 2. Database Persistence
- **SQLite** for local development
- **PostgreSQL** for production deployment
- **SQLAlchemy ORM** for database operations

### 3. PDF Upload & Patient Info Extraction
- **POST** `/upload/` - Upload PDF files
- **OCR Technology** - Extracts text from image-based PDFs
- **Patient Data** - Extracts first name, last name, and date of birth
- **Automatic Order Creation** - Creates order from extracted data

### 4. Activity Logging
- **Middleware** - Logs all HTTP requests automatically
- **Database Storage** - All activity stored in `activity_logs` table
- **GET** `/activity-logs/` - View all logged activities

### 5. Public Deployment
- **Railway Platform** - Deployed and publicly accessible
- **HTTPS Enabled** - Secure communication
- **Auto-scaling** - Handles traffic automatically

## 🛠️ **Technologies Used**

### Backend Framework
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server for running FastAPI

### Database & ORM
- **SQLAlchemy** - Python ORM for database operations
- **SQLite** - Local development database
- **PostgreSQL** - Production database

### PDF Processing
- **PyPDF2** - PDF text extraction
- **pytesseract** - OCR for image-based PDFs
- **pdf2image** - Convert PDF pages to images
- **Pillow** - Image processing for OCR

### Data Validation
- **Pydantic** - Data validation and serialization

### Deployment
- **Railway** - Cloud deployment platform
- **GitHub** - Version control and CI/CD

## 📁 **Project Structure**
```
genHealth/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and endpoints
│   ├── database.py      # Database connection setup
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic validation schemas
│   ├── crud.py          # Database operations
│   ├── utils.py         # PDF processing and OCR
│   └── logger.py        # Activity logging middleware
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── run.py              # Startup script
└── Procfile            # Railway deployment config
```

## 🎯 **Key Features**

### OCR Implementation
- Automatically detects image-based PDFs
- Converts PDF pages to high-resolution images
- Uses Tesseract OCR to extract text
- Falls back gracefully if OCR fails

### Activity Logging
- Middleware captures all HTTP requests
- Stores request details, timestamps, and responses
- No manual logging required

### Error Handling
- Comprehensive error messages
- Graceful fallbacks for PDF processing
- Proper HTTP status codes

## 🚀 **How to Run Locally**

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanskrutimahajan/genHealth.git
   cd genHealth
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   python run.py
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## 📊 **API Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check and info |
| GET | `/docs` | Interactive API documentation |
| GET | `/orders/` | List all orders |
| POST | `/orders/` | Create new order |
| GET | `/orders/{id}` | Get specific order |
| PUT | `/orders/{id}` | Update order |
| DELETE | `/orders/{id}` | Delete order |
| POST | `/upload/` | Upload PDF and extract patient info |
| GET | `/activity-logs/` | View all activity logs |

## 🎯 **Demo Instructions**

1. **Visit the live API**: https://web-production-f830.up.railway.app/docs
2. **Upload a PDF** using the `/upload/` endpoint
3. **Watch the OCR extraction** in real-time
4. **Check the created order** in `/orders/`
5. **View activity logs** in `/activity-logs/`

## 💡 **Technical Highlights**

- **Modern FastAPI** with automatic OpenAPI documentation
- **Advanced OCR** for handling scanned PDFs
- **Comprehensive logging** for audit trails
- **Production-ready** deployment on Railway
- **Clean, maintainable code** structure
- **Error handling** and graceful fallbacks

The API successfully demonstrates all required functionality and is ready for production use. 