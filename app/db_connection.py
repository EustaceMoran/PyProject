from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres::admin@localhost/db"

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


Base = declarative_base()
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд
SessionLockal = sessionmaker(autoflush=False, bind=engine)

