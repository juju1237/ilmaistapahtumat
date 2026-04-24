import db

def add_event(title, description, date, time, location, user_id, classes, image_blob=None):
    sql = "INSERT INTO events (title, description, date, time, location, user_id, image) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, date, time, location, user_id, image_blob])

    event_id = db.last_insert_id()

    sql = "INSERT INTO event_classes (event_id, title) VALUES (?, ?)"
    for title in classes:
        db.execute(sql, [event_id, title])

def get_classes(event_id):
    sql = "SELECT title FROM event_classes WHERE event_id = ?"
    return db.query(sql, [event_id])

def get_events():
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


def edit_event(event_id, title, description, date, time, location):
    sql = """UPDATE events SET title = ?,
                                description = ?,
                                date = ?,
                                time = ?,
                                location = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, date, time, location, event_id])

def remove_event(event_id):
    sql = "DELETE FROM comments WHERE event_id = ?"
    db.execute(sql, [event_id])

    sql = "DELETE FROM event_classes WHERE event_id = ?"
    db.execute(sql, [event_id])

    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def find_events(query):
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
    sql = "UPDATE events SET image = ? WHERE id = ?"
    db.execute(sql, [image, event_id])

def get_image(event_id):
    sql = "SELECT image FROM events WHERE id = ?"
    result = db.query(sql, [event_id])
    return result[0][0] if result else None