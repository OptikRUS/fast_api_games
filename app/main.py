from fastapi import FastAPI, status, HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from .schemas import User, Game, Connection, UserResponse, GameResponse
from .database_config import async_session, engine, Base
from .models import UserModel, GameModel, game_users


app = FastAPI()


@app.on_event("startup")
async def init_tables():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/users",
          response_model=UserResponse,  # модель для Response, создает схему Response в доке и ожидает такой формат
          response_model_exclude_unset=True,  # удаляет пустые параметры в Response
          # response_model_include={"name", "age", "email"}, указание параметров из Response
          status_code=status.HTTP_201_CREATED
          )
async def create_user(user: User):
    async with async_session() as session:
        try:
            session.add(UserModel(**user.dict()))
            await session.flush()
            await session.commit()
            return UserResponse.from_orm(user)
        except IntegrityError as e:
            detail = str(e.orig).split('DETAIL:  ')[-1]
            raise HTTPException(status_code=409, detail=detail)


@app.get("/users/{pk}", response_model=UserResponse)
async def get_user(pk: int):
    async with async_session() as session:
        query = select(UserModel).options(selectinload(UserModel.games)).filter(UserModel.id == pk)
        result = await session.execute(query)
        user_data = result.first()
        if user_data:
            return UserResponse.from_orm(user_data[0])
        raise HTTPException(status_code=404, detail=f"User with id={pk} is not found")


@app.post("/games",
          response_model=GameResponse,
          status_code=status.HTTP_201_CREATED,
          response_model_exclude={"id"}  # удаляет параметры в Response, но не схему Response в доке
          )
async def create_game(game: Game):
    async with async_session() as session:
        try:
            session.add(GameModel(**game.dict()))
            await session.flush()
            await session.commit()
            return GameResponse.from_orm(game)
        except IntegrityError as e:
            detail = str(e.orig).split('DETAIL:  ')[-1]
            raise HTTPException(status_code=409, detail=detail)


@app.get("/games")
async def get_games():
    async with async_session() as session:
        result = await session.execute(select(GameModel).options(selectinload(GameModel.users)))
        all_games = result.scalars().all()
        if all_games:
            return all_games
        raise HTTPException(status_code=204, detail="No games found")


@app.post("/connect", response_model=Connection)
async def connect_to_game(connection: Connection):
    async with async_session() as session:
        try:
            await session.execute(game_users.insert().values(**connection.dict()))
            await session.commit()
        except IntegrityError as e:
            detail = str(e.orig).split('DETAIL:  ')[-1]
            raise HTTPException(status_code=409, detail=detail)
    return connection
