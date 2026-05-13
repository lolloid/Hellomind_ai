import sqlite3

conn = sqlite3.connect('hellomind.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE users ADD COLUMN ai_name VARCHAR(50) DEFAULT 'HelloMind'")
except Exception as e:
    print(f"Error ai_name: {e}")

try:
    c.execute("ALTER TABLE users ADD COLUMN ai_persona TEXT DEFAULT 'Kamu adalah AI pendamping kesehatan mental yang empatik, ramah, dan suportif.'")
except Exception as e:
    print(f"Error ai_persona: {e}")

conn.commit()
conn.close()
