import psycopg2
from pprint import pprint
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class User:

    def __init__(conn):
        pass

    def _create_table(self):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(60) NOT NULL UNIQUE,
        CHECK (email LIKE '%@%')
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        number VARCHAR(12) NOT NULL UNIQUE,
        user_id INTEGER NOT NULL REFERENCES users(user_id),
        CHECK (number LIKE '+%')
        );
        """) 
        conn.commit()


    def show_info(self):
        cur.execute("""
        SELECT * FROM users
        JOIN phones using(user_id);""")
        pprint(cur.fetchall())
    

    def _info(self):
        cur.execute("""
        SELECT * FROM users
        JOIN phones using(user_id);""")
        return cur.fetchall()

        
    def add_user(self, name, last_name, email):
        self._create_table()
        cur.execute("""
        INSERT INTO users (name, last_name, email)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
        """, (name, last_name, email))
        conn.commit()


    def update_user(self, colum, data, user_id):
        if colum == 'number':
            last_number = input('Введите номер, который нужно сменить: ')
            cur.execute("""
        UPDATE phones SET number=%s
        WHERE user_id=%s AND number=%s;""", (data, user_id, last_number))
        else:
            cur.execute("""
        UPDATE users SET %(colum)s='%(data)s'
        WHERE user_id=%(id)s;"""%{'colum': colum, 'data': data, 'id': user_id})
        conn.commit()


    def add_number(self, number, user_id):
        self._create_table()
        cur.execute("""
        INSERT INTO phones(number, user_id)
        VALUES (%s, %s)
        ON CONFLICT (number) DO NOTHING;        
        """, (number, user_id))
        conn.commit()


    def delete_number(self, user_id, number):
        cur.execute("""
        DELETE FROM phones WHERE user_id=%s AND number=%s;
        """, (user_id, number))
        conn.commit()


    def delete_user(self, user_id):
        cur.execute("""
        DELETE FROM phones WHERE user_id=%s;
        """, (user_id,))
        cur.execute("""
        DELETE FROM users WHERE user_id=%s;
        """, (user_id,))
        conn.commit()


    def find_user(self, data):
        l_data = data.split()
        l_users = self._info()
        for el in l_users:
            if set(l_data).issubset(el):
                    pprint(el) 


if __name__ == '__main__':
    with psycopg2.connect(database='home_work', user=os.getenv('LOGIN'), password=os.getenv('PASS')) as conn:
        with conn.cursor() as cur:
            Client = User()
            Client.add_user('Seva', 'Mayorov', 'seva@')
            Client.add_number('+79999999999', 1)
            Client.add_user('Vlada', 'Mayorova', 'vlada@')
            Client.add_number('+79999999990', 1)
            Client.add_number('+78888888888', 2)
            Client.update_user('name', 'Sevochka', 1)
            Client.update_user('number', '+70000000002', 1)
            Client.delete_number(2, '+78888888888')
            Client.find_user('Mayorova')
            Client.delete_user(2)
            Client.show_info()
    conn.close()