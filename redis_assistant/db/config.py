import os

import psycopg2
import pymysql
import dotenv

loaded_env = dotenv.load_dotenv(".env")
if not loaded_env:
    exit("Create enviroment file .env!")

def connect_to_postgres():
	db = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            database=os.getenv("POSTGRES_DATABASE")
    )
	return db

def connect_to_mysql():
	db = pymysql.connect(
		user=os.getenv("MYSQL_USER"),
		password=os.getenv("MYSQL_PASSWORD"),
		host=os.getenv("MYSQL_HOST"),
		port=int(os.getenv("MYSQL_PORT")),
		database=os.getenv("MYSQL_DATABASE")
	)
	return db