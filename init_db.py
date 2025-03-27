import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="url_shortener",
    user="valsorim",
    password="1234"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        original_url TEXT NOT NULL,
        short_url VARCHAR(6) UNIQUE NOT NULL
    )
""")

conn.commit()
cur.close()
conn.close()

print("Database and table created successfully!")
