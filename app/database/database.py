from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import Config

Base = declarative_base()


def get_engine_and_session():
    if not hasattr(get_engine_and_session, "engine"):
        get_engine_and_session.engine = create_engine(
            Config.DATABASE_URL, connect_args={"check_same_thread": False}
        )
        get_engine_and_session.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine_and_session.engine
        )
    return get_engine_and_session.engine, get_engine_and_session.SessionLocal


def initialize_db():
    engine, _ = get_engine_and_session()
    Base.metadata.create_all(bind=engine)


def get_db():
    _, session_local = get_engine_and_session()
    db: Session = session_local()
    try:
        yield db
    finally:
        db.close()
