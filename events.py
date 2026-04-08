import db

def add_event(title, description, date, time, location, user_id):
    sql = "INSERT INTO events (title, description, date, time, location, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    result = db.execute(sql, [title, description, date, time, location, user_id])
    return result[0] if result else None

def get_events():
    sql = "SELECT id, title FROM events ORDER BY id DESC"
    return db.query(sql)

def get_event(event_id):
    sql = """SELECT events.id,
        events.title,
        events.description,
        events.date,
        events.time,
        events.location,
        users.id user_id,
        users.username
    FROM events, users
    WHERE events.user_id = users.id AND events.id = ?
    """
    return db.query(sql, [event_id])[0]

def edit_event(event_id, title, description, date, time, location):
    sql = """UPDATE events SET title = ?,
                                description = ?,
                                date = ?,
                                time = ?,
                                location = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, date, time, location, event_id])

def remove_event(event_id):
    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def find_events(query):
    sql = """SELECT id, title
            FROM events
            WHERE description LIKE ?
            OR title LIKE ?
            OR time LIKE ?
            OR date LIKE ?
            ORDER BY id DESC"""
    res = "%" + query + "%"
    return db.query(sql, [res, res, res, res])

