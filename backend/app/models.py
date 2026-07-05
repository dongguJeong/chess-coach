from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base

#Base를 상속받아야 이 클래스가 실제 테이블로 인식됩니다 
# (Step 4에서 정의한 그 Base).

#__tablename__: 실제 PostgreSQL에 생성될 테이블 이름입니다.

#lichess_game_id에 unique=True를 준 이유: 
# 같은 게임을 중복 수집했을 때 걸러내기 위함입니다.

#is_parsed: 지금 당장은 안 쓰지만, 
# Phase 2에서 "아직 파싱 안 된 게임만 조회"할 때 쓸 플래그입니다. 지금 컬럼을 미리 넣어두면 나중에 마이그레이션을 또 안 해도 됩니다.

class Game(Base) :
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    lichess_game_id = Column(String(20), unique=True,index=True, nullable=False)
    pgn_raw=Column(Text, nullable=False)
    white_player = Column(String(50))
    black_player = Column(String(50))
    result = Column(String(10))
    eco = Column(String(5), nullable=True)
    opening_name=Column(String(200), nullable=True)
    time_control = Column(String(20), nullable=True)
    played_at = Column(DateTime, nullable=True)
    collected_at = Column(DateTime, server_default=func.now())
    is_parsed = Column(Boolean, default=False)
 