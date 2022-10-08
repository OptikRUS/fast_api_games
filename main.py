import json

from fastapi import FastAPI, Query

from schemas import User, Game, Connection
from fixtures.utils import save_data

app = FastAPI()


@app.post("/users")
async def create_user(user: User):
    save_data('fixtures/users.json', user)
    return user


@app.post("/games")
async def create_game(game: Game):
    save_data('fixtures/games.json', game)
    return game


@app.get("/games")
async def get_games():
    with open('fixtures/games.json') as file:
        games_data = json.load(file)
    return {'All games': games_data}


@app.get("/users/")
async def get_user(pk: int = Query(None, description="Get info about current user and info about all connected games")):
    with open('fixtures/users.json') as file:
        users_data = json.load(file)
    if pk:
        return {'User info': users_data[pk-1]}
    return {'All users': users_data}


@app.post("/connect")
async def connect_to_game(connection: Connection):
    print(connection)
    save_data('fixtures/connections.json', connection)
    return {'Connection': connection}
