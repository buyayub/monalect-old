from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool


engine = create_engine(
        'sqlite:///:memory:',
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )


#engine = create_engine('sqlite:///test.db')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import monalect.models
    Base.metadata.create_all(bind=engine)

init_db()
