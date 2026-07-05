from fastapi import FastAPI

from app.database import Base, engine
from app import models

# app.include_router(games.router) 추가 — 
# 이 한 줄로 games.py에 정의한 /api/games/collect/{username} 
# 엔드포인트가 실제 서버에 등록됩니다.
from app.routers import games

#rom app import models: models.py를 import해야 Base가 
# Game 클래스의 존재를 알게 됩니다. 
# import 안 하면 create_all()이 아무 테이블도 안 만듭니다.

#Base.metadata.create_all(bind=engine): 
# Base를 상속받은 모든 모델(지금은 Game 하나)을 실제 PostgreSQL에 테이블로 생성합니다. 
# 이미 테이블이 있으면 건드리지 않고, 없으면 새로 만듭니다.

Base.metadata.create_all(bind=engine)

app = FastAPI(title='AI Chess Coach')

app.include_router(games.router)

@app.get('/')
def root():
    return {"status" : "ok"}

