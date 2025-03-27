import pytest
import asyncio
import json
from app import app  # Pretpostavljam da se tvoj Flask app nalazi u app.py

@pytest.fixture
def client():
    """Kreira testnog klijenta Flask aplikacije"""
    return app.test_client()

@pytest.mark.asyncio
async def test_shorten_url(client):
    """Testira endpoint za skraćivanje URL-a"""
    with app.app_context():  # Sinhroni kontekst
        response = await asyncio.to_thread(client.post, '/shorten', json={'url': 'https://example.com'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'short_url' in data

@pytest.mark.asyncio
async def test_redirect(client):
    """Testira redirekciju pomoću skraćenog URL-a"""
    with app.app_context():  # Sinhroni kontekst
        # Prvo kreiramo skraćeni URL
        shorten_response = await asyncio.to_thread(client.post, '/shorten', json={'url': 'https://example.com'})
        data = json.loads(shorten_response.data)
        short_url = data['short_url']

        # Sada testiramo redirekciju
        redirect_response = await asyncio.to_thread(client.get, f'/{short_url}')
        assert redirect_response.status_code == 302  # 302 znači da je redirekcija uspela
