import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_users_table():
    query = "CREATE TABLE IF NOT EXISTS users(" \
    "id SERIAL PRIMARY KEY," \
    "email VARCHAR(100) UNIQUE," \
    "hashed_password VARCHAR(500)," \
    "created_at TIMESTAMP);"

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

def get_user_by_email(email: str) -> dict | None:
    query = "SELECT id, email, hashed_password, created_at FROM users where email = %s"

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            columns = [d[0] for d in cursor.description]
            users = cursor.fetchone()

    if users is None:
        return None
    else:
        return dict(zip(columns, users))

def get_user_by_id(user_id: int | str) -> dict | None:
    query = "SELECT id, email, hashed_password, created_at FROM users where id = %s"

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            columns = [d[0] for d in cursor.description]
            users = cursor.fetchone()
    
    if users is None:
        return None
    else:
        return dict(zip(columns, users))

def insert_user(email: str, password_hash: str) -> None:
   ##created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = "INSERT INTO users (email, hashed_password, created_at)" \
    " VALUES(%s, %s, %s) ON CONFLICT (email) DO NOTHING "

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email, password_hash, datetime.utcnow()))


