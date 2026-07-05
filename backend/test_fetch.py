import asyncio
from app.services.lichess_client import fetch_user_games

async def main():
    games = await fetch_user_games("jokaechat", max_games=1)
    print(f"받은 게임 수: {len(games)}")
    print(games[0])

asyncio.run(main())