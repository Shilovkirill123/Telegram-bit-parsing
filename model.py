from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


engine = create_engine('sqlite:///films.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    id_kinopoisk = Column(String, unique = True)
    name = Column(String)
    tagline = Column(String)
    genre = Column(String)
    actors = Column(String)
    director = Column(String)
    rating = Column(String)
    rating_imdb = Column(String)
    year = Column(String)

    def __repr__(self):
        return (
            f'https://www.kinopoisk.ru/film/{self.id_kinopoisk}\nНазвание фильма: {self.name}\nСлоган: {self.tagline}\n' 
            f'Жанр: {self.genre}\nАктеры: {self.actors}\nРежисер: {self.director}\nРейтинг: {self.rating}\n'
            f'Рейтинг imdb: {self.rating_imdb}\nГод: {self.year}'
        ) 
'''
class Film_genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    id_kinopoisk = Column(String, ForeignKey('films.id_kinopoisk', ondelete='CASCADE'), index=True)
    genre = Column(String)

class Genres(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    genres = Column(String)
'''
Film.metadata.create_all(engine)










