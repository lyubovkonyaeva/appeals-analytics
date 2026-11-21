from app.database import get_connection


def get_stats():
    """Считает статистику и возвращает словарь с результатами."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    per_category = conn.execute("""
        SELECT categories.name, COUNT(tickets.id) AS count
        FROM categories
        LEFT JOIN tickets ON tickets.category_id = categories.id
        GROUP BY categories.id
        ORDER BY count DESC
    """).fetchall()
    per_status = conn.execute("""
        SELECT status, COUNT(*) AS count
        FROM tickets
        GROUP BY status
    """).fetchall()
    conn.close()

    return {
        "total_tickets": total,
        "tickets_per_category": per_category,
        "tickets_per_status": per_status,
    }