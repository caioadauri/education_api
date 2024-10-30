connector = "mysql+pymysql"
user = "root"
password = "education"
server = "localhost"
port = "3306"
database = "education-api"
class Config:
  SECRET_KEY = "education"
  SQLALCHEMY_DATABASE_URI = f'{connector}://{user}:{password}@{server}:{port}/{database}'