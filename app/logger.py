from fastapi import Request, Response
from sqlalchemy.orm import Session
from .database import SessionLocal
from .crud import create_activity_log
from .schemas import ActivityLogCreate
import time
from typing import Callable
import json

class ActivityLogger:
    """Middleware to log all user activity to database."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Get request details
            method = request.method
            url = str(request.url)
            path = request.url.path
            
            # Determine action based on method and path
            action = self._determine_action(method, path)
            
            # Process the request
            start_time = time.time()
            
            # Create a custom response class to capture response details
            response_body = b""
            
            async def custom_send(message):
                if message["type"] == "http.response.body":
                    response_body = message.get("body", b"")
                await send(message)
            
            # Process request
            await self.app(scope, receive, custom_send)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Log the activity
            await self._log_activity(
                action=action,
                endpoint=path,
                method=method,
                details=f"Response time: {response_time:.3f}s"
            )
    
    def _determine_action(self, method: str, path: str) -> str:
        """Determine the action based on HTTP method and path."""
        if method == "GET":
            if path == "/orders":
                return "READ_ALL"
            elif path.startswith("/orders/"):
                return "READ_ONE"
            elif path == "/activity-logs":
                return "READ_LOGS"
            else:
                return "READ"
        elif method == "POST":
            if path == "/orders":
                return "CREATE"
            elif path == "/upload":
                return "UPLOAD"
            else:
                return "CREATE"
        elif method == "PUT":
            return "UPDATE"
        elif method == "DELETE":
            return "DELETE"
        else:
            return "UNKNOWN"
    
    async def _log_activity(self, action: str, endpoint: str, method: str, details: str = None):
        """Log activity to database."""
        try:
            db = SessionLocal()
            activity_log = ActivityLogCreate(
                action=action,
                endpoint=endpoint,
                method=method,
                details=details
            )
            create_activity_log(db, activity_log)
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
        finally:
            db.close()

def log_activity_middleware(request: Request, call_next: Callable) -> Response:
    """FastAPI middleware function for logging activity."""
    # Get request details
    method = request.method
    path = request.url.path
    
    # Determine action
    action = _determine_action(method, path)
    
    # Process request
    start_time = time.time()
    response = call_next(request)
    response_time = time.time() - start_time
    
    # Log activity asynchronously
    import asyncio
    asyncio.create_task(_log_activity_async(
        action=action,
        endpoint=path,
        method=method,
        details=f"Response time: {response_time:.3f}s"
    ))
    
    return response

def _determine_action(method: str, path: str) -> str:
    """Determine the action based on HTTP method and path."""
    if method == "GET":
        if path == "/orders":
            return "READ_ALL"
        elif path.startswith("/orders/"):
            return "READ_ONE"
        elif path == "/activity-logs":
            return "READ_LOGS"
        else:
            return "READ"
    elif method == "POST":
        if path == "/orders":
            return "CREATE"
        elif path == "/upload":
            return "UPLOAD"
        else:
            return "CREATE"
    elif method == "PUT":
        return "UPDATE"
    elif method == "DELETE":
        return "DELETE"
    else:
        return "UNKNOWN"

async def _log_activity_async(action: str, endpoint: str, method: str, details: str = None):
    """Asynchronously log activity to database."""
    try:
        db = SessionLocal()
        activity_log = ActivityLogCreate(
            action=action,
            endpoint=endpoint,
            method=method,
            details=details
        )
        create_activity_log(db, activity_log)
    except Exception as e:
        print(f"Error logging activity: {str(e)}")
    finally:
        db.close() 