"""
Helper functions for managing database connection
"""
import sqlite3
from typing import List


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

    try:
        con = sqlite3.connect("superheroes.db")
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return data

    except Exception as e:
        return {'error': str(e)}
    finally:
        con.close()


def get_db_data_by_value(query: str, values: List[int]) -> dict:
    """execute select query to get db data by value"""
    try:
        con = sqlite3.connect("superheroes.db")
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute(query, values)
        data = cur.fetchall()

        return data
    except Exception as e:
        return {'error': str(e)}
    finally:
        con.close()


def insert_row(query: str, values: List[int], select_query: str, select_values: List[int] = []) -> dict:
    """insert new row"""

    try:
        con = sqlite3.connect("superheroes.db")
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute(query, values)
        con.commit()
        cur.execute(select_query, select_values)
        data = cur.fetchall()

        return data
    except Exception as e:
        return {'error': str(e)}
    finally:
        con.close()


def update_row(query: str, value: int, row_id: int, select_query: str) -> dict:
    """update existing row"""
    try:
        con = sqlite3.connect("superheroes.db")
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute(query, [value, row_id])
        con.commit()
        cur.execute(select_query, [row_id])
        data = cur.fetchall()

        return data
    except Exception as e:
        return {'error': str(e)}
    finally:
        con.close()


def delete_row(query: str, values: List[int]) -> dict:
    """delete existing row"""
    try:
        con = sqlite3.connect("superheroes.db")
        con.row_factory = row_to_dict
        cur = con.cursor()
        cur.execute(query, values)
        con.commit()

        return 0
    except Exception as e:
        return {'error': str(e)}
    finally:
        con.close()


def body_is_valid(body: dict, is_superpower: bool = False) -> bool:
    """validate Superhero data"""
    if is_superpower and 'id' in body and len(body.keys()) == 1:
        return True
    if not is_superpower and 'name' in body and len(body.keys()) == 1:
        return True
    return False
