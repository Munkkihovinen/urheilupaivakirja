import db

def get_activities():
    sql = """SELECT a.id, a.sent_at, a.sport, a.duration_in_minutes, u.username
             FROM activities a, users u
             WHERE a.user_id = u.id
             ORDER BY sent_at"""
    return db.query(sql)
