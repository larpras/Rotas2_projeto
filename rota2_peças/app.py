from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DB_NAME = "rota2.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Cadastro de novos produtos
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()

    name = data.get('name', '').strip()
    motorcycle_model = data.get('motorcycle_model', '').strip()

    try:
        price = float(data.get('price'))
        stock = int(data.get('stock'))

        if not name or not motorcycle_model:
            return jsonify({'error': 'Preencha todos os campos.'}), 400

        if price <= 0 or stock < 0:
            return jsonify({'error': 'Preço ou estoque inválido.'}), 400

    except (TypeError, ValueError):
        return jsonify({'error': 'Preço e estoque devem ser números válidos.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)',
        (name, price, stock)
    )

    product_id = cursor.lastrowid

    cursor.execute(
        'INSERT INTO compatibility (product_id, motorcycle_model) VALUES (?, ?)',
        (product_id, motorcycle_model)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Produto cadastrado com sucesso!'}), 201

# Exclusão de produtos
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar se o produto existe
    product = cursor.execute(
        'SELECT id FROM products WHERE id = ?',
        (product_id,)
    ).fetchone()

    if product is None:
        conn.close()
        return jsonify({'error': 'Produto não encontrado.'}), 404

    # Excluir primeiro a compatibilidade
    cursor.execute(
        'DELETE FROM compatibility WHERE product_id = ?',
        (product_id,)
    )

    # Excluir o produto
    cursor.execute(
        'DELETE FROM products WHERE id = ?',
        (product_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Produto excluído com sucesso!'})

# RF-03 + Busca Inteligente por Modelo de Moto
@app.route('/api/products/search', methods=['GET'])
def search_products():
    model = request.args.get('model', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if model:
        query = """
            SELECT p.id, p.name, p.price, p.stock, c.motorcycle_model,
                   CASE WHEN p.stock < 5 THEN 1 ELSE 0 END AS low_stock_alert
            FROM products p
            JOIN compatibility c ON p.id = c.product_id
            WHERE c.motorcycle_model LIKE ?
        """
        products = cursor.execute(query, (f"%{model}%",)).fetchall()
    else:
        query = """
            SELECT p.id, p.name, p.price, p.stock,
                   CASE WHEN p.stock < 5 THEN 1 ELSE 0 END AS low_stock_alert
            FROM products p
        """
        products = cursor.execute(query).fetchall()
        
    conn.close()
    return jsonify([dict(row) for row in products])

# Dashboard Simples na Web
@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Rota 2 Motopeças</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; }
            .alert { color: red; font-weight: bold; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Rota 2 Motopeças - Consulta de Compatibilidade</h1>
        <input type="text" id="modelInput" placeholder="Ex: Honda CG 150 Titan">
        <h2>Cadastrar Nova Peça</h2>

<input type="text" id="productName" placeholder="Nome da peça">
<input type="number" id="productPrice" placeholder="Preço" step="0.01">
<input type="number" id="productStock" placeholder="Quantidade em estoque">
<input type="text" id="motorcycleModel" placeholder="Modelo da motocicleta">

<button onclick="registerProduct()">Cadastrar Produto</button>
        <button onclick="search()">Buscar Peças</button>

        <table id="results">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome da Peça</th>
                    <th>Preço (R$)</th>
                    <th>Estoque</th>
                    <th>Alerta</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

        <script>

        async function registerProduct() {
    const product = {
        name: document.getElementById('productName').value,
        price: document.getElementById('productPrice').value,
        stock: document.getElementById('productStock').value,
        motorcycle_model: document.getElementById('motorcycleModel').value
    };

    const response = await fetch('/api/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    alert(data.message);

    document.getElementById('productName').value = '';
    document.getElementById('productPrice').value = '';
    document.getElementById('productStock').value = '';
    document.getElementById('motorcycleModel').value = '';

    search();
 }
 async function deleteProduct(id) {
    const confirmation = confirm('Tem certeza que deseja excluir esta peça?');

    if (!confirmation) {
        return;
    }

    const response = await fetch(`/api/products/${id}`, {
        method: 'DELETE'
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    alert(data.message);
    search();
}

            async function search() {
                const model = document.getElementById('modelInput').value;
                const response = await fetch(`/api/products/search?model=${encodeURIComponent(model)}`);
                const data = await response.json();
                
                const tbody = document.querySelector('#results tbody');
                tbody.innerHTML = '';
                
                data.forEach(item => {
                    const row = `<tr>
                        <td>${item.id}</td>
                        <td>${item.name}</td>
                        <td>${item.price.toFixed(2)}</td>
                        <td>${item.stock}</td>
                        <td class="${item.low_stock_alert ? 'alert' : ''}">
                            ${item.low_stock_alert ? '⚠️ ESTOQUE CRÍTICO' : 'OK'}
                        </td>
                        <td>
    <button onclick="deleteProduct(${item.id})">Excluir</button>
</td>
                    </tr>`;
                    tbody.innerHTML += row;
                });
            }
            search();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, port=5000)