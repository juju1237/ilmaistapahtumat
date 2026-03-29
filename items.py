import db

def add_item(title, description, date, time, location, user_id):
    sql = "INSERT INTO items (title, description, date, time, location, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    result = db.execute(sql, [title, description, date, time, location, user_id])
    return result[0] if result else None

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
    items.description,
    items.date,
    items.time,
    users.username
    from items, users
    where items.user_id = users.id AND items.id = ?
    """
    return db.query(sql, [item_id])[0]