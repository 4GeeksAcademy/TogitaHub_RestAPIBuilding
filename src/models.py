from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    favorite_planets: Mapped[list['Planet']] = relationship(secondary='user_favorite_planets', back_populates='favorited_by')
    favorite_people: Mapped[list['Person']] = relationship(secondary='user_favorite_people', back_populates='favorited_by')
    favorite_vehicles: Mapped[list['Vehicle']] = relationship(secondary='user_favorite_vehicles', back_populates='favorited_by')

    def serialize(self):
        return {"id": self.id, "username": self.username, "email": self.email}

class Planet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str | None] = mapped_column(String(120))
    terrain: Mapped[str | None] = mapped_column(String(120))
    population: Mapped[float | None] = mapped_column(Float)
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_planets', back_populates='favorite_planets')

    def serialize(self):
        return {"id": self.id, "name": self.name, "climate": self.climate, "terrain": self.terrain, "population": self.population}

class Person(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str | None] = mapped_column(String(20))
    homeworld_id: Mapped[int | None] = mapped_column(ForeignKey('planet.id'))
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_people', back_populates='favorite_people')

    def serialize(self):
        return {"id": self.id, "name": self.name, "gender": self.gender, "homeworld_id": self.homeworld_id}

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str | None] = mapped_column(String(120))
    manufacturer: Mapped[str | None] = mapped_column(String(120))
    crew: Mapped[int | None] = mapped_column(Integer)
    passengers: Mapped[int | None] = mapped_column(Integer)
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_vehicles', back_populates='favorite_vehicles')

    def serialize(self):
        return {"id": self.id, "name": self.name, "model": self.model, "manufacturer": self.manufacturer, "crew": self.crew, "passengers": self.passengers}

# Tablas de asociación (deben definirse después de las clases de los modelos)
planet_residents = db.Table('planet_residents',
    db.Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

vehicle_pilots = db.Table('vehicle_pilots',
    db.Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

user_favorite_planets = db.Table('user_favorite_planets',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

user_favorite_people = db.Table('user_favorite_people',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

user_favorite_vehicles = db.Table('user_favorite_vehicles',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True)
)