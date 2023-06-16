from mongoengine import connect
import configparser
import pathlib


file_config = pathlib.Path(__file__).parent.parent.joinpath("settings.ini")
config = configparser.ConfigParser()
config.read(file_config)

m_user = config.get("mongo", "user")
m_pass = config.get("mongo", "password")
m_db = config.get("mongo", "db_name")
m_domain = config.get("mongo", "domain")

url = f"mongodb+srv://{m_user}:{m_pass}@{m_domain}/{m_db}?retryWrites=true&w=majority"
m_connect = None

try:
    m_connect = connect(host=url, ssl=True)
except:
    print("Connection to database failed")
    quit()
