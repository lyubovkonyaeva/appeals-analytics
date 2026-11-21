from flask import Flask, render_template, request
from app.database import get_connection
from app.services.stats import get_stats
from app.services.charts import category_bar_html, status_pie_html

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

@app.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):
    conn = get_connection()
    ticket = conn.execute("""
        SELECT tickets.*, categories.name AS category
        FROM tickets
        LEFT JOIN categories ON tickets.category_id = categories.id
        WHERE tickets.id = ?
    """, (ticket_id,)).fetchone()
    conn.close()

    if ticket is None:
        return "Обращение не найдено", 404
    return render_template("ticket.html", ticket=ticket)

@app.route("/stats")
def stats():
    data = get_stats()
    return render_template(
        "stats.html",
        total_tickets=data["total_tickets"],
        tickets_per_category=data["tickets_per_category"],
        tickets_per_status=data["tickets_per_status"],
        bar_html=category_bar_html(data["tickets_per_category"]),
        pie_html=status_pie_html(data["tickets_per_status"]),
    )

if __name__ == "__main__":
    app.run(debug=True)