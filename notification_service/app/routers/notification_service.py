from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification import Notification, NotificationTemplate, NotificationType
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

# Initialize the router
notification_router = APIRouter()

# Pydantic model for creating a notification
class NotificationCreate(BaseModel):
    user_id: str
    type: NotificationType
    content: str
    sent_at: Optional[datetime] = None

# Pydantic model for creating a notification template
class NotificationTemplateCreate(BaseModel):
    name: str
    type: NotificationType
    body: str

# Pydantic model for updating a notification template
class NotificationTemplateUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[NotificationType] = None
    body: Optional[str] = None

# Endpoint to create a new notification
@notification_router.post("/create_notification", response_model=dict)
def create_notification(notification_data: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = Notification(
        id=str(uuid.uuid4()),
        user_id=notification_data.user_id,
        type=notification_data.type,
        content=notification_data.content,
        sent_at=notification_data.sent_at if notification_data.sent_at else None,
        created_at=datetime.now()
    )
    db.add(new_notification)
    db.commit()
    return {"message": "Notification created successfully", "notification_id": new_notification.id}

# Endpoint to retrieve notifications by user ID
@notification_router.get("/get_notifications/{user_id}", response_model=List[dict])
def get_notifications(user_id: str, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user")
    
    return [
        {
            "id": notification.id,
            "user_id": notification.user_id,
            "type": notification.type.value,
            "content": notification.content,
            "sent_at": notification.sent_at,
            "created_at": notification.created_at,
            "extra": notification.extra
        }
        for notification in notifications
    ]

# Endpoint to create a new notification template
@notification_router.post("/create_template", response_model=dict)
def create_template(template_data: NotificationTemplateCreate, db: Session = Depends(get_db)):
    new_template = NotificationTemplate(
        id=str(uuid.uuid4()),
        name=template_data.name,
        type=template_data.type,
        body=template_data.body,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_template)
    db.commit()
    return {"message": "Template created successfully", "template_id": new_template.id}

# Endpoint to update an existing notification template
@notification_router.put("/update_template", response_model=dict)
def update_template(template_data: NotificationTemplateUpdate, db: Session = Depends(get_db)):
    template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_data.id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template_data.name:
        template.name = template_data.name
    if template_data.type:
        template.type = template_data.type
    if template_data.body:
        template.body = template_data.body
    template.updated_at = datetime.now()

    db.commit()
    return {"message": "Template updated successfully", "template_id": template.id}

# Endpoint to get a list of all templates
@notification_router.get("/get_templates", response_model=List[dict])
def get_templates(db: Session = Depends(get_db)):
    templates = db.query(NotificationTemplate).all()
    if not templates:
        raise HTTPException(status_code=404, detail="No templates found")
    
    return [
        {
            "id": template.id,
            "name": template.name,
            "type": template.type.value,
            "body": template.body,
            "created_at": template.created_at,
            "updated_at": template.updated_at,
            "extra": template.extra
        }
        for template in templates
    ]
