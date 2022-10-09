from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database_config import Base


# Declare Many-to-Many
game_users = Table(
    'game_users', Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
    )


# User model
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer)
    email = Column(String(120), unique=True, nullable=False)
    games = relationship("GameModel", secondary="game_users", back_populates='users')


# Game model
class GameModel(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    users = relationship("UserModel", secondary="game_users", back_populates='games')
