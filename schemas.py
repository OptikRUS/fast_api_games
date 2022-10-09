from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(None)  # Field(None) - необязательное поле/Field(...) - обязательное
    name: str = Field(..., max_length=80)
    age: int = Field(None, ge=0, le=100, description="User age must be more than 0 and less than 100")
    email: str = Field("example@mail.com",
                       max_length=120,
                       regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UserResponse(BaseModel):
    name: str
    age: int = Field(None)
    email: str

    class Config:
        orm_mode = True


class Game(BaseModel):
    id: int = Field(None)
    name: str = Field(..., max_length=120)


class GameResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Connection(BaseModel):
    user_id: int
    game_id: int
