import sqlite3
from sqlite3 import Error

def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    
    return None

def create_row(conn, create_row_sql, values):
    try:
        cur = conn.cursor()
        cur.execute(create_row_sql, values)
    except Error as e:
        print(e)

    return cur.lastrowid

def create_rows(conn, create_row_sql, values):
    try:
        cur = conn.cursor()
        cur.executemany(create_row_sql, values)
    except Error as e:
        print(e)

def main():    
    database = "db.db"

    query_create_material_table = """
        CREATE TABLE IF NOT EXISTS Material(
            id          INTEGER     PRIMARY KEY     NOT NULL    ,
            name        TEXT                        NOT NULL
        );
    """

    query_create_carpet_table = """
        CREATE TABLE IF NOT EXISTS Carpet(
            id          INTEGER     PRIMARY KEY     NOT NULL                    ,
            area        REAL                        NOT NULL    DEFAULT 10000   ,
            material_id INTEGER                     NOT NULL                    ,
            FOREIGN KEY (material_id)
                REFERENCES Material (id)
        );
    """

    query_create_coordinates_table = """
        CREATE TABLE IF NOT EXISTS Coordinates(
            id          INTEGER     PRIMARY KEY     NOT NULL    ,
            x           INTEGER                     NOT NULL    ,
            y           INTEGER                     NOT NULL    ,
            carpet_id   INTEGER                     NOT NULL    ,
            FOREIGN KEY (carpet_id)
                REFERENCES Carpet (id)
        );
    """

    query_create_carpet_row = """
        INSERT OR IGNORE INTO Carpet (material_id)
        VALUES (?);
    """
    query_create_default_coordinates_rows = """
        INSERT OR IGNORE INTO Coordinates (x, y, carpet_id)
        VALUES (?, ?, ?);
    """
    
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, query_create_material_table)
        create_table(conn, query_create_carpet_table)
        create_table(conn, query_create_coordinates_table)
    else:
        print("Error! DB connection unsuccessful.")

    with conn:
        """
        1. Restock carpet rolls (i.e. Add a stock of 100x100m roll of carpet to inventory)

        Whenever a stock of 100x100m roll of carpet is added to the inventory:
        * A new record will be added to the Carpet table with a specified material (wool, nylon, fiber, or acrylic) and area (default value is 10000).
        * 4 new records will be added to the Coordinates table referencing the newly added Carpet record. The default values are (0, 0), (100, 0), (100, 100), and (0, 100). These refer to the mapped coordinates of the 100x100m roll of carpet.
        """

        # add a new carpet record
        values = (1,) # wool
        carpet_id = create_row(conn, query_create_carpet_row, values)

        # add default coordinates
        values = [
            (0, 0, carpet_id,),
            (100, 0, carpet_id,),
            (100, 100, carpet_id,),
            (0, 100, carpet_id,)
        ]
        create_rows(conn, query_create_default_coordinates_rows, values)

        """
        2. Cut from a roll of carpet (i.e. Remove an area of size MxN meters from a roll of carpet in
        the inventory)
        """

        """
        3. Select which roll of carpet to cut from.
        """


if __name__ == '__main__':
    main()