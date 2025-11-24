import db

def get_activities(search: str | None = None):
    sql = """SELECT a.id, a.sent_at, a.sport, a.duration_in_minutes, a.content, a.user_id, u.username
            FROM activities a
            JOIN users u ON a.user_id = u.id"""
    params = []
    if search:
        sql += " WHERE (LOWER(a.content) LIKE LOWER(?) OR LOWER(a.sport) LIKE LOWER(?))"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    sql += " ORDER BY a.sent_at"

    return db.query(sql, params)

def get_activity(activity_id: int):
    sql = """
        SELECT a.id, a.sent_at, a.sport, a.duration_in_minutes, a.content, a.user_id, u.username
        FROM activities a
        JOIN users u ON a.user_id = u.id
        WHERE a.id = ?
        LIMIT 1
    """
    rows = db.query(sql, [activity_id])
    return rows[0] if rows else None

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
