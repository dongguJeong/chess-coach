from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Game
from app.services.lichess_client import fetch_user_games


#router = APIRouter(prefix="/api/games", ...): 
# 이 라우터의 모든 엔드포인트 앞에 자동으로 /api/games가 붙습니다. 
# 그래서 아래 @router.post("/collect/{username}")는 
# 실제로 /api/games/collect/{username}이 됩니다.
router = APIRouter(prefix="/api/games", tags=["games"])

@router.post("/collect/{username}")
async def collect_games(
    username : str, 
    max_games : int = 500 , 
    db : Session = Depends(get_db)) :
    games = await fetch_user_games(username, max_games)

    saved_count = 0
    skipped_count = 0

    for g in games :
        existing = db.query(Game).filter(Game.lichess_game_id == g['id']).first()
        if existing :
            skipped_count += 1
            continue

        game = Game(
            lichess_game_id=g["id"],
            pgn_raw=g.get("pgn", ""),
            white_player=g.get("players", {}).get("white", {}).get("user", {}).get("name"),
            black_player=g.get("players", {}).get("black", {}).get("user", {}).get("name"),
            result=g.get("winner", "draw"),
            eco=g.get("opening", {}).get("eco"),
            time_control=g.get("speed"),
            opening_name=g.get("opening", {}).get("name"),
            played_at=datetime.fromtimestamp(g.get("createdAt", 0) / 1000) if g.get("createdAt") else None,
        )

        db.add(game)
        saved_count += 1

    # db.commit(): 모든 게임을 db.add()로 세션에 올려두기만 하다가, 
    # 반복문이 끝난 뒤 한 번에 커밋합니다. (건마다 커밋하면 느립니다)
    db.commit()
    return {"saved" : saved_count , "skipped" : skipped_count,"total_fetched": len(games)}