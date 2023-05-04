import psycopg2
from decouple import config

conn = psycopg2.connect(
    host=config('HOST'),
    user=config('DATABASES_USER'),
    password=config('DATABASES_PASSWORD'),
    database=config('DATABASES_NAME')
)
db = conn.cursor()
