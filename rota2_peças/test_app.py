import pytest
import sqlite3
import os
from app import app
from database import init_db

@pytest.fixture
def client():
    db_test = "test_rota2.db"
    app.config['TESTING'] = True
    
    # Criar banco temporário para os testes
    init_db(db_test)
    conn = sqlite3.connect(db_test)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Bateria 12V', 180.00, 2)")
    cursor.execute("INSERT INTO compatibility (product_id, motorcycle_model) VALUES (1, 'Honda Titan 160')")
    conn.commit()
    conn.close()
    
    import app as app_module
    app_module.DB_NAME = db_test
    
    with app.test_client() as client:
        yield client
        
    if os.path.exists(db_test):
        os.remove(db_test)

def test_search_by_motorcycle_model(client):
    response = client.get('/api/products/search?model=Honda Titan 160')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Bateria 12V'

def test_low_stock_alert_flag(client):
    response = client.get('/api/products/search?model=Honda Titan 160')
    data = response.get_json()
    # Verifica se o estoque baixo (<5) foi ativado corretamente
    assert data[0]['low_stock_alert'] == 1

def test_register_product(client):
    response = client.post('/api/products', json={
        'name': 'Filtro de óleo',
        'price': 35,
        'stock': 10,
        'motorcycle_model': 'Honda CG 160'
    })

    assert response.status_code == 201

    data = response.get_json()
    assert data['message'] == 'Produto cadastrado com sucesso!'

    search = client.get('/api/products/search?model=Honda CG 160')

    products = search.get_json()
    assert len(products) == 1
    assert products[0]['name'] == 'Filtro de óleo'

    assert products[0]['name'] == 'Filtro de óleo'

def test_delete_product(client):
    response = client.delete('/api/products/1')

    assert response.status_code == 200

    data = response.get_json()
    assert data['message'] == 'Produto excluído com sucesso!'

    search = client.get('/api/products/search?model=Honda Titan 160')

    products = search.get_json()
    assert len(products) == 0