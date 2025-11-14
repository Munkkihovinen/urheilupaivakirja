import db

def get_activities():
    sql = """SELECT a.id, a.sent_at, a.sport, a.duration_in_minutes, a.user_id, u.username
             FROM activities a, users u
             WHERE a.user_id = u.id
             ORDER BY sent_at"""
    return db.query(sql)

def add_activity(sport: str, duration_in_minutes: int, content: str, user_id: int):
    sql = """INSERT INTO activities (sent_at, sport, duration_in_minutes, content, user_id)
            VALUES (datetime('now'), ?, ?, ?, ?)"""
    db.execute(sql, [sport, duration_in_minutes, content, user_id])
    return db.last_insert_id()

