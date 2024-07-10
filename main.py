import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from dotenv import dotenv_values


from models import create_table

if __name__ == '__main__':

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        print(load_dotenv(dotenv_path))

    DSN = (f'{dotenv_values()['connection_driver']}://'
           f'{dotenv_values()['login']}:'
           f'{dotenv_values()['password']}@'
           f'{dotenv_values()['host']}:'
           f'{dotenv_values()['port']}/'
           f'{dotenv_values()['title_database']}')

    engine = sqlalchemy.create_engine(DSN)

    create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.close()
