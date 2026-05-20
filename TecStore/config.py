class Config:
    SECRET_KEY = 'tecstore_secret_key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/TecStore'

    SQLALCHEMY_TRACK_MODIFICATIONS = False