import bcrypt
import sqlite3

from sqlalchemy import false

# hasło "admin123" po zahashowaniu
hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
con = sqlite3.connect("users.db")
cur = con.cursor()

class User:
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

def is_closed():
    try:
        con.execute("SELECT 1")
        return False
    except sqlite3.ProgrammingError:
        return True


def new_user(username, password):
    if is_closed():
        con = sqlite3.connect("users.db")
        cur = con.cursor()
    if len(username) >16 or len(password) >64:
        return False
    hash_pwd = bcrypt.hashpw(password, bcrypt.gensalt())
    cur.execute('''insert into api_users(usr_username, usr_password, usr_is_admin) values (?, ?, ?)''', [username,hash_pwd, False])
    con.commit()
    return True

def close_db():
    con.close()


if cur.execute('''SELECT name FROM sqlite_master WHERE name='api_users' ''').fetchone() is None:
    cur.execute('''CREATE TABLE api_users(usr_ID INTEGER PRIMARY KEY,usr_username TEXT,usr_password TEXT,usr_is_admin BOOLEAN)''')
    con.commit()
    cur.execute('''insert into api_users(usr_username,usr_password,usr_is_admin) values (?,?,?)''', ["admin", hashed_pw, True])
    con.commit()

USERS_DB = {}

query = [list(row) for row in cur.execute('''SELECT usr_username, usr_password FROM api_users''').fetchall()]
for user in query:
    USERS_DB[user[0]] = user[1]

con.close()