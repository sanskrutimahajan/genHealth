from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from .database import get_db, create_tables
from .models import Base
from . import crud, schemas, utils
from .logger import log_activity_middleware

# Create FastAPI app
app = FastAPI(
    title="GenHealth API",
    description="REST API for managing orders and extracting patient information from PDFs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add activity logging middleware
app.middleware("http")(log_activity_middleware)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "GenHealth API is running!", "docs": "/docs", "endpoints": {
        "orders": "/orders/",
        "upload": "/upload/",
        "activity_logs": "/activity-logs/"
    }}

# Order CRUD endpoints
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new order."""
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders with pagination."""
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID."""
    order = crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """Update an existing order."""
    updated_order = crud.update_order(db, order_id=order_id, order=order)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order."""
    success = crud.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# File upload endpoint
@app.post("/upload/", response_model=schemas.PatientInfo)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF file and extract patient information."""
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
    # Extract patient information
    patient_info = utils.extract_patient_info_from_pdf(content)
    
    if patient_info is None:
        raise HTTPException(
            status_code=422, 
            detail="Could not extract patient information from PDF. OCR was attempted but no patient information was found. Please ensure the PDF contains clearly readable first name, last name, and date of birth, or use the /orders/ endpoint to manually create an order."
        )
    
    # Create order from extracted information
    order_data = schemas.OrderCreate(
        first_name=patient_info.first_name,
        last_name=patient_info.last_name,
        date_of_birth=patient_info.date_of_birth
    )
    
    # Save to database
    created_order = crud.create_order(db=db, order=order_data)
    
    return patient_info

# Activity logs endpoint
@app.get("/activity-logs/", response_model=List[schemas.ActivityLog])
def read_activity_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all activity logs with pagination."""
    logs = crud.get_activity_logs(db, skip=skip, limit=limit)
    return logs

@app.get("/activity-logs/order/{order_id}", response_model=List[schemas.ActivityLog])
def read_activity_logs_by_order(order_id: int, db: Session = Depends(get_db)):
    """Get activity logs for a specific order."""
    logs = crud.get_activity_logs_by_order(db, order_id=order_id)
    return logs

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 