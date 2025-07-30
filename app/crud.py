from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

# Order CRUD operations
def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    db_order = models.Order(
        first_name=order.first_name,
        last_name=order.last_name,
        date_of_birth=order.date_of_birth
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    return db.query(models.Order).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate) -> Optional[models.Order]:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        update_data = order.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> bool:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    return False

# Activity Log CRUD operations
def create_activity_log(db: Session, activity_log: schemas.ActivityLogCreate) -> models.ActivityLog:
    db_activity_log = models.ActivityLog(
        order_id=activity_log.order_id,
        action=activity_log.action,
        endpoint=activity_log.endpoint,
        method=activity_log.method,
        details=activity_log.details
    )
    db.add(db_activity_log)
    db.commit()
    db.refresh(db_activity_log)
    return db_activity_log

def get_activity_logs(db: Session, skip: int = 0, limit: int = 100) -> List[models.ActivityLog]:
    return db.query(models.ActivityLog).offset(skip).limit(limit).all()

def get_activity_logs_by_order(db: Session, order_id: int) -> List[models.ActivityLog]:
    return db.query(models.ActivityLog).filter(models.ActivityLog.order_id == order_id).all() 