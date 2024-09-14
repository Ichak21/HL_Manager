from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
import os

# URL de la base de données (ex. SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/_off_line_v0.db")

# Crée l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base de déclaration pour les modèles
Base = declarative_base()

# Création d'une session locale pour interagir avec la BDD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour initialiser la base de données
def init_db():
    Base.metadata.create_all(bind=engine)