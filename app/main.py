from flask import Flask
from app.database import get_connection

app = Flask(__name__)

@app.route("/")

def index():
    conn = get_connection()
    tickets = conn.execute("""
        SELECT tickets.id, tickets.title, tickets.status, tickets.created_at, categories.name AS category
        FROM tickets
        LEFT JOIN categories ON tickets.category_id = categories.id
        ORDER BY tickets.created_id DESC
        LIMIT 50 
    """).fetchall()
    conn.close()
    
