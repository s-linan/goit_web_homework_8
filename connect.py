from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


# connect to cluster

def connect_to_db():
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
            ssl=True)


connect_to_db()
