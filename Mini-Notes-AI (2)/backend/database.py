from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
