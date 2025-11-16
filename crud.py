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

