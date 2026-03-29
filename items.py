import db

def add_item(title, description, date, time, location, user_id):
    sql = "INSERT INTO items (title, description, date, time, location, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, description, date, time, location, user_id])
