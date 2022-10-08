import json

from fastapi import FastAPI, Query

from schemas import User, UserResponse, Game, GameList, Connection
from fixtures.utils import save_data

app = FastAPI()


@app.post("/users",
          response_model=UserResponse,  # модель для Response, создает схему Response в доке
          # response_model_exclude_unset=True, удаляет пустые параметры в Response
          # response_model_include={"name", "age", "email"}, указание параметров из Response
          )
async def create_user(user: User):
    save_data('fixtures/users.json', user)
    return user


@app.post("/games", response_model=Game,
          response_model_exclude={"id"}  # удаляет параметры в Response, но не схему Response в доке
          )
async def create_game(game: Game):
    save_data('fixtures/games.json', game)
    return game


@app.get("/games", response_model=GameList)
async def get_games():
    with open('fixtures/games.json') as file:
        games_data = json.load(file)
        print(games_data)
        all_games = GameList(games=games_data)
    return all_games


@app.get("/users/{pk}", response_model=UserResponse)
async def get_user(pk: int = Query(None, description="Get info about current user and info about all connected games")):
    with open('fixtures/users.json') as file:
        users_data = json.load(file)
        return UserResponse(**users_data[pk-1])


@app.post("/connect", response_model=Connection)
async def connect_to_game(connection: Connection):
    save_data('fixtures/connections.json', connection)
    return connection
