from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# specify database configurations
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 8806,
    'database': 'migration'
}

dbAddress = "mysql+pymysql://{}:{}@{}:{}/{}".format(config['user'], config['password'], config['host'], config['port'], config['database'])
dbEngine = create_engine(dbAddress)
sessionObj = sessionmaker(bind=dbEngine)
dbSession = scoped_session(sessionObj)

cursor = dbSession.execute("show databases")
data = cursor.fetchall()
print(data)
dbSession.flush()
dbSession.commit()
dbSession.close()




