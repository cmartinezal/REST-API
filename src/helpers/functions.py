import sqlite3


def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    """format data to dictionary"""
    data = {}
    for idx, col in enumerate(cursor.description):
        if (col[0]) == 'superpowers' and isinstance(row[idx], str):
            data[col[0]] = row[idx].split(', ')
        else:
            data[col[0]] = row[idx]
    return data


def get_db_data(query: str) -> dict:
    """execute select query to get db data"""

    con = sqlite3.connect("superheroes.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data


def get_db_data_by_value(query: str, value: int) -> dict:
    """execute select query to get db data by value"""

    con = sqlite3.connect("superheroes.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute(query, [value])
    data = cur.fetchall()
    con.close()
    return data


def insert_row(query: str, value: int, select_query: str) -> dict:
    """insert new row"""

    con = sqlite3.connect("superheroes.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute(query, [value])
    con.commit()
    cur.execute(select_query)
    data = cur.fetchall()
    con.close()
    return data


def update_row(query: str, value: int, row_id: int, select_query: str) -> dict:
    """update existing row"""

    con = sqlite3.connect("superheroes.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute(query, [value, row_id])
    con.commit()
    cur.execute(select_query, [row_id])
    data = cur.fetchall()
    con.close()
    return data


def delete_row(query: str, value: int) -> dict:
    """delete existing row"""

    con = sqlite3.connect("superheroes.db")
    con.row_factory = row_to_dict
    cur = con.cursor()
    cur.execute(query, [value])
    con.commit()
    con.close()
    return 0


def body_is_valid(superhero: dict) -> bool:
    """validate superhero data"""

    if 'name' in superhero and len(superhero.keys()) == 1:
        return True
    return False
