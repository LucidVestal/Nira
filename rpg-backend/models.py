from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Character(Base):
    __tablename__ = "characters"
    __table_args__ = {"schema": "rpg"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    race = Column(String)
    class_ = Column("class", String)
    level = Column(Integer, default=1)
    hp = Column(Integer, default=10)
    notes = Column(Text)

class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {"schema": "rpg"}

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("rpg.characters.id"))
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)

class Location(Base):
    __tablename__ = "locations"
    __table_args__ = {"schema": "rpg"}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    discovered = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"schema": "rpg"}

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    description = Column(Text, nullable=False)
    location_id = Column(Integer, ForeignKey("rpg.locations.id"))
