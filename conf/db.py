import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')
database_name = config.get('DB', 'DB_NAME')

url = f"postgresql://{username}:{password}@{domain}:{port}/{database_name}"

engine = create_engine(url, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
