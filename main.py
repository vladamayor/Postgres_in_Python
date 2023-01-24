import psycopg2
from pprint import pprint


with open('settings.txt', 'r') as f:
    password_db = f.readline()

conn = psycopg2.connect(database='home_work', user='postgres', password=password_db)

cur = conn.cursor()

class User:

    def __init__(self):
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

        
    def add_user(self, name, last_name, email):
        self._create_table()
        cur.execute("""
        INSERT INTO users (name, last_name, email)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
        """, (name, last_name, email))
        conn.commit()
        cur.execute("""
        SELECT * FROM users;
        """)
        pprint(cur.fetchall())


    def update_user(self, name, last_name, email, last_number, new_number, user_id):
        cur.execute("""
        UPDATE users SET name=%s, last_name=%s, email=%s
        WHERE user_id=%s;""", (name, last_name, email, user_id))
        cur.execute("""
        UPDATE phones SET number=%s
        WHERE user_id=%s AND number=%s;""", (new_number, user_id, last_number))
        conn.commit()
        self.show_info()


    def add_number(self, number, user_id):
        self._create_table()
        cur.execute("""
        INSERT INTO phones(number, user_id)
        VALUES (%s, %s)
        ON CONFLICT (number) DO NOTHING;        
        """, (number, user_id))
        conn.commit()
        cur.execute("""
        SELECT * FROM phones;
        """)
        pprint(cur.fetchall())


    def delete_number(self, user_id, number):
        cur.execute("""
        DELETE FROM phones WHERE user_id=%s AND number=%s;
        """, (user_id, number))
        conn.commit()
        self.show_info()


    def delete_user(self, user_id):
        cur.execute("""
        DELETE FROM phones WHERE user_id=%s;
        """, (user_id,))
        cur.execute("""
        DELETE FROM users WHERE user_id=%s;
        """, (user_id,))
        conn.commit()
        self.show_info()


    def find_user(self, name, last_name, email, number):
        cur.execute("""
        SELECT user_id FROM users
        JOIN phones USING(user_id)
        WHERE name=%s OR last_name=%s OR email=%s OR number=%s;
        """, (name, last_name,  email, number))
        pprint(cur.fetchall())


if __name__ == '__main__':
    Client = User()
    Client.add_user('Seva', 'Mayorov', 'seva@')
    Client.add_number('+79999999999', 1)
    Client.add_user('Vlada', 'Mayorova', 'vlada@')
    Client.add_number('+79999999990', 1)
    Client.add_number('+78888888888', 2)
    Client.update_user('Sevochka', 'Mayorov', 'seva@', '+79999999999', '+71111111111', 1)
    Client.delete_number(1, '+79999999990')
    Client.find_user('Vlada', 'Mayorova', 'vlada@', None)
    Client.delete_user(2)


cur.close()
conn.close()