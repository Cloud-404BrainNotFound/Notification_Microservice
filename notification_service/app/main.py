from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import notification  # 导入所有模型

from app.routers.notification_service import notification_router  # 导入通知相关的 router


# 创建数据库表

notification.Base.metadata.create_all(bind=engine)


app = FastAPI()


# 这是一个router的示例

app.include_router(notification_router, prefix="/notifications", tags=["notifications"])


@app.get("/")
def read_root():
    return {"Hello": "World"}