import sqlite3

def init_db(db_name="rota2.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Ativar Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Criar tabela de produtos com restrição de estoque não negativo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL CHECK (stock >= 0)
        );
    """)
    
    # Criar tabela de compatibilidade
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compatibility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            motorcycle_model TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    conn.close()

def seed_db(db_name="rota2.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Inserir dados de teste caso a tabela esteja vazia
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Pastilha de Travão Dianteira', 45.00, 3)")
        cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Kit Transmissão', 120.00, 15)")
        
        cursor.execute("INSERT INTO compatibility (product_id, motorcycle_model) VALUES (1, 'Honda CG 150 Titan')")
        cursor.execute("INSERT INTO compatibility (product_id, motorcycle_model) VALUES (2, 'Honda CG 150 Titan')")
        cursor.execute("INSERT INTO compatibility (product_id, motorcycle_model) VALUES (2, 'Yamaha YBR 125')")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_db()
    print("Banco de dados inicializado com sucesso!")