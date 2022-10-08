from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    age: int = Field(..., ge=0, le=100, description="User age must be more than 0 and less than 100")
    email: str = Field("example@mail.com", regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UserResponse(BaseModel):
    name: str
    age: int
    email: str


class Game(BaseModel):
    id: int
    name: str


class GameResponse(BaseModel):
    name: str


class GameList(BaseModel):
    games: list[GameResponse]


class Connection(BaseModel):
    user_id: int
    game_id: int
