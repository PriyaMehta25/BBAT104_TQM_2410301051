import sqlite3
from config.settings import DB_PATH


def connect():
    con = sqlite3.connect(DB_PATH)
    con.execute('PRAGMA foreign_keys = ON')
    return con


def fetchall(query, params=()):
    con = connect()
    try:
        return con.execute(query, params).fetchall()
    finally:
        con.close()


def fetchone(query, params=()):
    con = connect()
    try:
        return con.execute(query, params).fetchone()
    finally:
        con.close()


def execute(query, params=()):
    con = connect()
    try:
        cur = con.execute(query, params)
        con.commit()
        return cur.lastrowid
    finally:
        con.close()
