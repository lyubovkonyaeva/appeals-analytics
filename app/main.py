from flask import Flask, render_template, request
from app.database import get_connection

app = Flask(__name__)

@app.route("/")

def index():
    params = []
    conditions = []

    STATUSES = ["новое", "в работе", "закрыто"]

    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    status = request.args.get("status", "")

    if q:
        conditions.append("(tickets.title LIKE ? OR tickets.text LIKE ?)")
        params += [f"%{q}%", f"%{q}%"]
    if category:
        conditions.append("(tickets.category_id = ?)")
        params.append(category)
    if status:
            conditions.append("(tickets.status = ?)")
            params.append(status)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    conn = get_connection()
    tickets = conn.execute(f"""
        SELECT tickets.id, tickets.title, tickets.status, tickets.created_at, categories.name AS category
        FROM tickets
        LEFT JOIN categories ON tickets.category_id = categories.id
        {where}
        ORDER BY tickets.created_at DESC
        LIMIT 50 
    """, params).fetchall()
    categories = conn.execute("SELECT id, name FROM categories").fetchall()
    conn.close()
    return render_template("tickets.html", tickets=tickets, categories=categories, statuses=STATUSES,
        q=q, category=category, status=status,)

if __name__ == "__main__":
    app.run(debug=True)