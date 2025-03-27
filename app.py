from flask import Flask, request, redirect, jsonify
import asyncio
import aiohttp
import random
import string
import psycopg2
from psycopg2 import sql

app = Flask(__name__)


# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='url_shortener',
        user='valsorim',
        password='1234'
    )
    return conn


# Generate a random shortened URL (e.g., a random 6-character string)
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# Async function to check URL availability
async def check_url_availability(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                return response.status == 200
        except Exception:
            return False


# URL Shortening Endpoint with async URL availability check
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')

    # Check URL availability using asyncio
    is_available = asyncio.run(check_url_availability(original_url))

    if not is_available:
        return jsonify({'error': 'URL is not reachable'}), 400

    # Generate a shortened URL
    short_url = generate_short_url()

    # Save the mapping in the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        sql.SQL("INSERT INTO urls (original_url, short_url) VALUES (%s, %s)"),
        [original_url, short_url]
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'short_url': short_url})


# Redirect Endpoint
@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    # Look up the original URL from the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        sql.SQL("SELECT original_url FROM urls WHERE short_url = %s"),
        [short_url]
    )
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is None:
        return jsonify({'error': 'URL not found'}), 404

    return redirect(result[0])


if __name__ == '__main__':
    app.run(debug=True)
