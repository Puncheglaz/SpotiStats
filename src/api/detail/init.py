import config
import detail.entity.userType
from detail.entity.user import User, hash_password

import pyodbc
import os
import sys
import secrets
import string

def init():

    conn = pyodbc.connect('Driver={SQL Server};'
                            f'Server={config.DB_SERVER_NAME};'
                            'Database=master;'
                            'Trusted_Connection=yes;',
                            autocommit=True)
    cur = conn.cursor()

    cur.execute(f"SELECT name FROM sys.databases WHERE name = '{config.DB_DATABASE_NAME}'")
    db_exists = bool(cur.fetchall())

    if not db_exists:
        print('Initializing database...')

        db_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'data');

        with conn.cursor() as cur:
            cur.execute(
                'CREATE DATABASE Library ON'
                '(Name=Library,'
                f"FileName='{db_file_path}\\library.mdf')"
                'LOG ON'
                '(Name=Library_log,'
                f"FileName='{db_file_path}\\library_log.mdf');"
                )

    conn.close()
    conn = pyodbc.connect('Driver={SQL Server};'
                            f'Server={config.DB_SERVER_NAME};'
                            f'Database={config.DB_DATABASE_NAME};'
                            'Trusted_Connection=yes;'
                            'AutoTranslate=yes;',
                            autocommit=True, ansi=True)

    if not db_exists:
        with open('data/init.sql', 'r', encoding='utf8') as f:
            script = f.read()
            for statement in script.split('\nGO'):
                if statement.strip():
                    # print(statement)
                    with conn.cursor() as cur:
                        cur.execute(statement)

        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        User.register(conn, config.DIRECTOR_LOGIN, hash_password(password), config.ROLE_NAME_DIRECTOR, config.DIRECTOR_NAME, config.DIRECTOR_PHONE)
        print('\nRegistered Director account:' +
                '\n    login:    ' + config.DIRECTOR_LOGIN +
                '\n    password: ' + password +
                '\n'
            )


    with conn.cursor() as cur:
        cur.execute('SELECT userType FROM UserTypes WHERE name = ?', config.ROLE_NAME_VISITOR)
        detail.entity.userType.visitor = cur.fetchall()[0][0]
        cur.execute('SELECT userType FROM UserTypes WHERE name = ?', config.ROLE_NAME_LIBRARIAN)
        detail.entity.userType.librarian = cur.fetchall()[0][0]
        cur.execute('SELECT userType FROM UserTypes WHERE name = ?', config.ROLE_NAME_DIRECTOR)
        detail.entity.userType.director = cur.fetchall()[0][0]

    return conn
