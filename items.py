import db

def add_item(title, description, date, time, location, user_id):
    sql = "INSERT INTO items (title, description, date, time, location, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    result = db.execute(sql, [title, description, date, time, location, user_id])
    return result[0] if result else None

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
        items.title,
        items.description,
        items.date,
        items.time,
        items.location,
        users.id user_id,
        users.username
    FROM items, users
    WHERE items.user_id = users.id AND items.id = ?
    """
    return db.query(sql, [item_id])[0]

def edit_event(item_id, title, description, date, time, location):
    sql = """UPDATE items SET title = ?,
                                description = ?,
                                date = ?,
                                time = ?,
                                location = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, date, time, location, item_id])

def remove_event(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])
