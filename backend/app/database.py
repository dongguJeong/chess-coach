from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

#engine: .env에 적어둔 DATABASE_URL로 실제 PostgreSQL에 연결하는 객체입니다.
#SessionLocal: DB와 대화(쿼리, 저장)할 때마다 만드는 세션 팩토리입니다.
#Base: 앞으로 만들 모든 테이블(Game, Move 등)이 상속받을 부모 클래스입니다.
#get_db(): FastAPI 라우터에서 Depends(get_db)로 주입받아 쓰는 함수입니다. 요청 하나 처리할 때마다 세션을 열고, 끝나면 자동으로 닫아줍니다.


engine = create_engine(settings.database_url)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal() # 요청 들어올 때마다 새 세션 생성
    try :
        yield db # 이 세션을 라우터에 빌려줌
    finally : 
        db.close()  # 요청 끝나면 무조건 닫음


#왜 매번 새로 만들어야 하나

#요청(request)마다 독립적인 세션이 필요하기 때문입니다.
# FastAPI는 여러 사용자의 요청을 동시에 처리합니다. 예를 들어:
# 요청 A: POST /api/games/collect/userA  → 게임 500개 저장 중
# 요청 B: GET /api/games/1               → 동시에 게임 하나 조회
#이 두 요청이 세션을 하나 공유하면, 
# A가 아직 커밋 안 한 상태에서 B가 어중간한 데이터를 보거나, 
# 세션 내부 상태(추적 중인 객체, 트랜잭션)가 서로 꼬여서 예측 불가능한 버그가 납니다.