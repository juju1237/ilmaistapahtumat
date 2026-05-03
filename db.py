"""
db.py: Database utility module for SQLite operations in a Flask application.

Provides functions for managing database connections, executing SQL queries,
and retrieving query results. Ensures foreign key constraints are enabled and uses
Flask's `g` object for storing the last inserted row ID.
"""


import sqlite3
from flask import g

def get_connection():
    """
    Makes a connection to the SQLite database.

    - Enables foreign key constraints using PRAGMA.
    - Sets the row factory to return rows as dictionary-like objects.

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """

    con = sqlite3.connect("database.db", timeout=20)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=None):
    """
    Executes a SQL statement with optional parameters and commits the changes.

    - Opens a new database connection.
    - Executes the provided SQL statement with the given parameters.
    - Commits the transaction and stores the last inserted row ID in Flask's `g` object.
    - Closes the database connection.

    Returns:
        None
    """
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    """
    Retrieves the ID of the last inserted row.
    """
    return g.last_insert_id

def query(sql, params=None):
    """
    Executes a SQL query and retrieves all results.

    - Opens a new database connection.
    - Executes the provided SQL query with the given parameters.
    - Fetches all rows from the query result.
    - Closes the database connection.
    """

    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
