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
        if first_name != "":
            cur.execute("""
                        update client set first_name = %s where id = %s
                        """, (first_name,  client_id)
                        )

        if last_name != "":
            cur.execute("""
                        update client set last_name = %s where id = %s
                        """, (last_name, client_id)
                        )

        if email != "":
            cur.execute("""
                        update client set email = %s where id = %s
                        """, (email, client_id)
                        )

        if phones != "":
            cur.execute("""
                        update client_phones set phone = %s where client_id = %s
                        """, (phones, client_id)
                        )


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


def find_client(conn, first_name="%", last_name="%", email="%", phone="%"):
    with conn.cursor() as cur:
        cur.execute("""
                    select first_name,last_name,email,phone from client LEFT JOIN client_phones  ON client.id = client_phones.client_id
where lower(first_name) like %s and lower(last_name) like %s  and lower(email) like %s  and phone like %s ;
                    """, (f'%{first_name.lower()}%', f'%{last_name.lower()}%', f'%{email.lower()}%', f'%{phone}%'))
        print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="Введите пароль от базы") as conn:

        # create_db(conn)
        # add_client(conn, "Петр", "Петров", "J9zQz@example.com", "+7-888-999-99-99")
        # add_phone(conn,"4", "+7-778-999-00-00")
        # change_client(conn, "2", "Иван", "Грозный", "", "+7-555-999-99-99")
        # delete_client(conn, "3")
        # delete_phone(conn, "4", "+7-888-999-99-99")
        find_client(conn, "ВА")
