import db

def get_activities(search: str | None = None):
    sql = """SELECT a.id, a.sent_at, s.name AS sport, a.duration_in_minutes, a.content, a.user_id, u.username
            FROM activities a
            JOIN users u ON a.user_id = u.id
            JOIN sports s ON s.id = a.sport"""
    params = []
    if search:
        sql += " WHERE (LOWER(a.content) LIKE LOWER(?) OR LOWER(s.name) LIKE LOWER(?))"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    sql += " ORDER BY a.sent_at"

    return db.query(sql, params)

def get_activity(activity_id: int):
    sql = """
        SELECT a.id, a.sent_at, s.name AS sport, a.duration_in_minutes, a.content, a.user_id, u.username
        FROM activities a
        JOIN users u ON a.user_id = u.id
        JOIN sports s ON s.id = a.sport
        WHERE a.id = ?
        LIMIT 1
    """
    rows = db.query(sql, [activity_id])
    return rows[0] if rows else None

def get_activities_by_user_id(user_id: int):
    sql = """
        SELECT a.id, a.sent_at, s.name AS sport, a.duration_in_minutes, a.content, a.user_id, u.username
        FROM activities a
        JOIN users u ON a.user_id = u.id
        JOIN sports s ON s.id = a.sport
        WHERE a.user_id = ?
        ORDER BY a.sent_at
    """
    return db.query(sql, [user_id])

def add_activity(sport: str, duration_in_minutes: int, content: str, user_id: int):
    sql = """INSERT INTO activities (sent_at, sport, duration_in_minutes, content, user_id)
            VALUES (datetime('now'), ?, ?, ?, ?)"""
    db.execute(sql, [sport, duration_in_minutes, content, user_id])
    return db.last_insert_id()

def update_activity(activity_id: int, sport: str, duration_in_minutes: int, content: str):
    sql = """
        UPDATE activities
        SET sport = ?, duration_in_minutes = ?, content = ?
        WHERE id = ?
    """
    db.execute(sql, [sport, duration_in_minutes, content, activity_id])

def remove_activity(activity_id: int):
    db.execute("DELETE FROM activities WHERE id = ?", [activity_id])

def is_username_taken(username: str):
    sql = "SELECT id FROM users WHERE username = ?"
    return db.query(sql, [username])

def create_user(username: str, password_hash: str):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_user_by_username(username: str):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    rows = db.query(sql, [username])
    return rows[0] if rows else None

def get_username_by_id(user_id: int):
    row = db.query("SELECT username FROM users WHERE id = ? LIMIT 1", [user_id])
    return row[0]["username"] if row else None

def get_sports():
    return db.query("SELECT id, name FROM sports ORDER BY name")

def get_comments_for_activity(activity_id: int):
    sql = """
        SELECT c.id, c.content, c.sent_at, c.user_id, u.username
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.activity_id = ?
        ORDER BY c.sent_at
    """
    return db.query(sql, [activity_id])

def add_comment(activity_id: int, user_id: int, content: str):
    sql = """
        INSERT INTO comments (content, sent_at, user_id, activity_id)
        VALUES (?, datetime('now'), ?, ?)
    """
    db.execute(sql, [content, user_id, activity_id])