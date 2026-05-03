"""
events.py: Functions for managing events in the application.

Provides utilities for adding, editing, deleting, and querying events,
as well as handling event-related classes and images.
"""


import db

def add_event(title, description, date, time, location, user_id, classes, image_blob=None):
    """
    Adds a new event to the database.

    Args:
        event_data (EventData): Data for the event.
    """

    sql = """INSERT INTO events
    (title,
    description,
    date,
    time,
    location,
    user_id,
    image)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, date, time, location, user_id, image_blob])

    event_id = db.last_insert_id()

    sql = "INSERT INTO event_classes (event_id, title) VALUES (?, ?)"
    for class_title in classes:
        db.execute(sql, [event_id, class_title])

def get_classes(event_id):
    """
    Retrieves all class titles associated with a specific event.

    Args:
        event_id (int): ID of the event.

    Returns:
        list[sqlite3.Row]: List of class titles for the event.
    """

    sql = "SELECT title FROM event_classes WHERE event_id = ?"
    return db.query(sql, [event_id])

def get_events():
    """
    Retrieves all events from the database.

    Returns:
        List of events with their ID, title, date, and user details.
    """

    sql = """
        SELECT events.id, events.title,
               strftime('%d.%m.%Y', events.date) AS date,
               users.username, users.id AS user_id
        FROM events
        JOIN users ON events.user_id = users.id
        ORDER BY events.id DESC
    """
    return db.query(sql)



def get_event(event_id):
    """
    Retrieves information about a specific event.

    Args:
        event_id (int): ID of the event.

    Returns:
        sqlite3.Row or None: Event details if found, otherwise None.
    """

    sql = """SELECT events.id,
        events.title,
        events.description,
        events.date,
        events.time,
        events.location,
        events.image IS NOT NULL has_image,
        users.id user_id,
        users.username
    FROM events, users
    WHERE events.user_id = users.id AND events.id = ?
    """
    result = db.query(sql, [event_id])
    return result[0] if result else None


def edit_event(event_id, title, description, date, time, location, image_blob=None):
    """
    Updates an event's details in the database.

    Args:
        event_data: Data for the event.
    """

    if image_blob:
        sql = """UPDATE events
                 SET title = ?,
                 description = ?,
                 date = ?,
                 time = ?,
                 location = ?,
                 image = ?
                 WHERE id = ?"""
        db.execute(sql, [title, description, date, time, location, image_blob, event_id])
    else:
        sql = """UPDATE events SET title = ?, description = ?, date = ?, time = ?, location = ?
                 WHERE id = ?"""
        db.execute(sql, [title, description, date, time, location, event_id])


def update_classes(event_id, classes):
    """
    Updates the classes associated with an event.

    Args:
        event_id (int): ID of the event.
        classes (list[str]): List of updated class titles.
    """

    sql = "DELETE FROM event_classes WHERE event_id = ?"
    db.execute(sql, [event_id])

    sql = "INSERT INTO event_classes (event_id, title) VALUES (?, ?)"
    for class_title in classes:
        db.execute(sql, [event_id, class_title])


def remove_event(event_id):
    """
    Deletes an event and its associated data (comments, classes) from the database.

    Args:
        event_id (int): ID of the event to delete.
    """

    sql = "DELETE FROM comments WHERE event_id = ?"
    db.execute(sql, [event_id])

    sql = "DELETE FROM event_classes WHERE event_id = ?"
    db.execute(sql, [event_id])

    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def find_events(query):
    """
    Searches for events matching a query in their title, description, time, date, or classes.

    Args:
        query (str): Search query string.

    Returns:
        list[sqlite3.Row]: List of matching events.
    """

    sql = """SELECT DISTINCT events.id, events.title, events.date
            FROM events
            LEFT JOIN event_classes ON events.id = event_classes.event_id
            WHERE events.description LIKE ?
            OR events.title LIKE ?
            OR events.time LIKE ?
            OR events.date LIKE ?
            OR event_classes.title LIKE ?
            ORDER BY events.id DESC"""
    res = "%" + query + "%"
    return db.query(sql, [res, res, res, res, res])

def update_image(event_id, image):
    """
    Updates the image associated with an event.

    Args:
        event_id (int): ID of the event.
        image (bytes): Binary data for the new image.
    """

    sql = "UPDATE events SET image = ? WHERE id = ?"
    db.execute(sql, [image, event_id])

def get_image(event_id):
    """
    Retrieves the image associated with a specific event.

    Returns:
        bytes or None: Binary data for the image if found, otherwise None.
    """

    sql = "SELECT image FROM events WHERE id = ?"
    result = db.query(sql, [event_id])
    return result[0][0] if result else None

def get_events_with_pagination(offset, page_size):
    """
    Gets specific amount ov events fo one page
    """
    sql = """SELECT id, title, date, location
             FROM events
             ORDER BY id DESC
             LIMIT ? OFFSET ?"""
    return db.query(sql, [page_size, offset])

def event_count():
    """
    Needed for pagination
    """
    sql = "SELECT COUNT(*) FROM events"
    result = db.query(sql)
    return result[0][0] if result else 0
