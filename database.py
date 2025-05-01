import sqlite3
from datetime import datetime

def init_db():
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses
                     (id INTEGER PRIMARY KEY,
                      amount REAL,
                      category TEXT,
                      date TEXT)''')

def add_expense(amount, category):
    with sqlite3.connect('expenses.db') as conn:
        conn.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

def get_stats(month=None):
    with sqlite3.connect('expenses.db') as conn:
        query = '''SELECT category, SUM(amount) 
                   FROM expenses 
                   WHERE strftime('%m', date) = ? 
                   GROUP BY category'''
        
        cursor = conn.execute(query, (f"{month:02}",))
        return {row[0]: row[1] for row in cursor.fetchall()}