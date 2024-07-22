import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS client (
id SERIAL PRIMARY KEY,
First_name VARCHAR(50) NOT NULL,
Last_name VARCHAR(20) NOT NULL,
Email VARCHAR(50) NOT NULL
)
                 

                    """)
        cur.execute("""
                  CREATE TABLE IF NOT EXISTS client_phones (
id SERIAL PRIMARY KEY,
client_id INTEGER not null REFERENCES client(id),
phone VARCHAR(20) NOT NULL)
                   

                    """)


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                            insert into client (first_name, last_name, email) values (%s, %s, %s) RETURNING id      
                    """, (first_name, last_name, email))

        cur.execute("""
              insert into client_phones (client_id, phone) values ( %s, %s)       
                    """, (int(cur.fetchone()[0]), phones))


def add_phone(conn, client_id, phones):
    with conn.cursor() as cur:

        cur.execute("""
              insert into client_phones (client_id, phone)  values ( %s, %s)       
                    """, (client_id, phones))


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                    update client set first_name = %s, last_name = %s, email = %s where id = %s
                    """, (first_name, last_name, email, client_id)
                    )

        cur.execute("""
                    update client_phones set phone = %s where client_id = %s
                    
                    """, (phones, client_id))


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    delete from client_phones where client_id = %s
                    """, (client_id,))

        cur.execute("""
                    delete from client where id = %s
                    """, (client_id,)
                    )


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    delete from client_phones where client_id = %s and phone = %s
                    """, (client_id, phone))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                    select first_name,last_name,email,phone from client LEFT JOIN client_phones  ON client.id = client_phones.client_id
where first_name =%s or last_name = %s  or email like %s or phone like %s ;
                    """, (first_name, last_name, email, phone))
        print(cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="Ведите свой пароль от Postgres") as conn:

    # create_db(conn)
    # add_client(conn, "Петр", "Петров", "J9zQz@example.com", "+7-888-999-99-99")
    # add_phone(conn,"2", "+7-778-999-00-00")
    # change_client(conn, "1", "Антон", "Путин", "ylTgI@example.com", "+7-905-999-99-99")
    # delete_client(conn, "3")
    # delete_phone(conn, "4", "+7-888-999-99-99")
    find_client(conn, "Петр", "", "", "")
