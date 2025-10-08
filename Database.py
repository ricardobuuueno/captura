def create_database(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    #conn.commit()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_id INTEGER,
            name TEXT,
            document TEXT,
            params TEXT,
            FOREIGN KEY (search_id) REFERENCES searches (id)
        )
    ''')
    #conn.commit()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_id INTEGER,
            number TEXT,
            author TEXT,
            defendant TEXT,
            subject TEXT,
            last_event TEXT,
            params TEXT,
            FOREIGN KEY (party_id) REFERENCES parties (id)
        )
    ''')
    #conn.commit()    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER,
            code TEXT,
            description TEXT,
            principal TEXT,
            FOREIGN KEY (process_id) REFERENCES processes (id)
        )
    ''')
    #conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS additional_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_id INTEGER,
            key TEXT,
            value TEXT,
            FOREIGN KEY (process_id) REFERENCES processes (id)
        )
    ''')
    #conn.commit()


def reset_database(conn, cursor):
    cursor.execute("DELETE FROM searches")
    cursor.execute("DELETE FROM parties")
    cursor.execute("DELETE FROM processes")
    cursor.execute("DELETE FROM subjects")
    cursor.execute("DELETE FROM additional_info")
    conn.commit()