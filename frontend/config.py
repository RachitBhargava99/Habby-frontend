import os


class Config:
    SECRET_KEY = '0917b13a9091915d54b6336f45909539cce452b3661b21f386418a257883b30a'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENDPOINT_ROUTE = 'http://eventster.thinger.appspot.com'
    CAT_URL = '/cat/list'
    SEARCH_URL = '/search'
    EVENT_URL = '/event'
    GOOGLE_API_KEY = 'AIzaSyA7qL5QDcdku9CUUhKPoa7dBp0bl1vB8TY'
