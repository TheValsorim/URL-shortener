# Checking connection
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="url_shortener",
        user="valsorim",
        password="1234"
    )
    print("Uspesno povezano na bazu podataka!")
    conn.close()
except Exception as e:
    print("Greska prilikom povezivanja:", e)
