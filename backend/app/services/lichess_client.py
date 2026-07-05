import json
import httpx

from app.config import settings

LICHESS_BASE_URL = "https://lichess.org/api/games/user"

async def fetch_user_games(username : str , max_games : int = 500) :
    headers = {
        "Accept": "application/x-ndjson",
        "Authorization": f"Bearer {settings.lichess_token}",
    }
    params = {
        "max": max_games,
        "moves": "true",
        "opening": "true",
        "clocks": "true",
        "pgnInJson": "true",
    }

    games = []

    #httpx.AsyncClient: 
    # 비동기 HTTP 클라이언트를 하나 생성합니다. 
    # async with를 쓰면 이 블록이 끝날 때 클라이언트가 자동으로 연결을 정리(close)해줍니다. 
    # (파일을 with open(...)으로 열면 자동으로 닫히는 것과 같은 원리)
    async with httpx.AsyncClient(timeout = 60.0) as client :

        #client.stream(...): 일반적인 client.get()과 다르게, 응답을 한 번에 통째로 받지 않고 스트리밍으로 받겠다는 뜻입니다.
        #왜 이게 중요하냐면, Lichess가 500게임을 NDJSON으로 보낼 때 
        # 응답 전체를 메모리에 다 올리고 나서 처리하는 게 아니라, 
        # 데이터가 도착하는 대로 한 줄씩 바로 처리할 수 있게 해줍니다. 게임이 많아질수록 이 방식이 메모리 효율적입니다.
        async with client.stream(
            'GET', f"{LICHESS_BASE_URL}/{username}",headers=headers, params=params
        ) as response :
            
            #HTTP 상태 코드가 200번대(성공)가 아니면 즉시 예외를 던집니다.
            response.raise_for_status() 

            # aiter_lines(): 응답 본문을 한 줄씩 비동기로 순회합니다.
            async for line in response.aiter_lines():

                #line.strip(): 빈 줄(공백만 있는 줄)을 걸러냅니다. 
                if line.strip():

                    # json.loads(line): 그 한 줄(문자열)을 Python dict로 변환합니다. 
                    games.append(json.loads(line))
    return games


#Lichess API 응답은 NDJSON(한 줄에 게임 하나씩)이라, 
# 한 번에 .json()으로 파싱하지 않고 aiter_lines()로 
# 한 줄씩 읽어서 json.loads()로 변환합니다.

#settings.lichess_token: Step 3에서 만든 c
# onfig.py의 settings 객체를 그대로 씁니다. 
# 토큰을 코드에 직접 안 적고 .env에서 가져오는 구조입니다.


#이 함수는 아직 DB 저장은 안 하고, 
# Lichess에서 게임 데이터만 받아와서 Python list로 반환합니다.