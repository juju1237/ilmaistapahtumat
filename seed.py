import random
import sqlite3
from datetime import datetime, timedelta

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM events")
db.execute("DELETE FROM event_classes")
db.execute("DELETE FROM comments")

user_count = 10**6
event_count = 10**6
class_count = 10**6
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               [f"user{i}", "hashed_password"])

for i in range(1, event_count + 1):
    user_id = random.randint(1, user_count)
    title = f"Event {i}"
    description = f"Description for event {i}"
    date = (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
    time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"
    location = f"Location {i}"
    image_blob = None
    db.execute("""INSERT INTO events (title, description, date, time, location, user_id, image)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
               [title, description, date, time, location, user_id, image_blob])

for i in range(1, class_count + 1):
    event_id = random.randint(1, event_count)
    class_title = f"Class {i}"
    db.execute("INSERT INTO event_classes (event_id, title) VALUES (?, ?)",
               [event_id, class_title])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    event_id = random.randint(1, event_count)
    comment = f"Comment {i} by user {user_id}"
    created_at = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d %H:%M:%S")
    db.execute("""INSERT INTO comments (comment, created_at, user_id, event_id)
                  VALUES (?, ?, ?, ?)""",
               [comment, created_at, user_id, event_id])

db.commit()
db.close()
