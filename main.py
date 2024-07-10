import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_table

if __name__ == '__main__':
    DSN = 'postgresql://postgres:1324@localhost:5432/database_ORM_python'
    engine = sqlalchemy.create_engine(DSN)

    create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.close()
