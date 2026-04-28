import db

def add_comment(event_id, user_id, comment):
    sql = "INSERT INTO comments (event_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [event_id, user_id, comment])

def get_comments(event_id):
    sql = """SELECT comments.comment, users.username 
             FROM comments 
             JOIN users ON comments.user_id = users.id 
             WHERE comments.event_id = ?
             ORDER BY comments.created_at DESC"""
    return db.query(sql, [event_id])
