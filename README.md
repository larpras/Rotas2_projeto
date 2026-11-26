# Rota 2 Motopeças - Evolução de Engenharia com IA e TDD

Este repositório contém a implementação da evolução do sistema **Rota 2 Motopeças** (`rota2_peças`), desenvolvida para a disciplina de **Engenharia de Software Avançada com IA** da UNINASSAU (Sistemas de Informação, 8º Período - 2026).

## 🚀 Funcionalidades Implementadas (RF-03)

* **Busca Inteligente por Modelo de Moto:** Permite filtrar peças através do relacionamento entre produtos e modelos de motocicletas na base de dados SQLite (`GET /api/products/search?model=...`).
* **Indicador de Estoque Crítico:** Identificação automática de itens com estoque inferior a 5 unidades via flag de backend (`low_stock_alert`) e destaque visual na interface web.
* **Integridade Relacional:** Persistência SQLite configurada com suporte a chaves estrangeiras (`PRAGMA foreign_keys = ON`) e restrição de integridade `CHECK (stock >= 0)`.
* **Quality Gate Automatizado:** Execução de suíte de testes com Pytest (`test_app.py`) orquestrada por `scripts/gate.py`, garantindo o ciclo RED/GREEN antes da integração.

---

## 🛠️ Ambiente e Execução

* **Ambiente Validado:** Python 3.15 | Flask | Pytest 9.2.0 | SQLite 3

### 1. Instalação das Dependências
```bash
pip install flask pytest
```

### 2. Inicialização e Carga Inicial do Banco de Dados
```bash
python database.py
```

### 3. Execução do Quality Gate (Testes Automatizados)
```bash
python scripts/gate.py
```

### 4. Inicialização da Aplicação Web
```bash
python app.py
```
Acesse o painel no navegador através do endereço: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Estrutura do Projeto

```text
rota2_peças/
├── app.py              # API Flask, rotas de busca e interface web
├── database.py         # Configuração do esquema SQLite e carga inicial (seed)
├── test_app.py         # Suíte de testes automatizados (Pytest)
├── scripts/
│   └── gate.py         # Script de Quality Gate (verificação RED/GREEN)
├── .gitignore          # Regras para ignorar arquivos temporários e bancos locais
└── README.md           # Documentação do projeto
```

---

## 🛡️ Higienização do Repositório (Checklist Git)
Antes de realizar o `git push`, certifique-se de que os seguintes artefatos locais **não** foram enviados ao repositório remoto (devem constar no `.gitignore`):
* `rota2.db` (banco de dados local gerado em tempo de execução)
* `__pycache__/` e `*.pyc` (bytecode compilado do Python)
* `.pytest_cache/` (cache local de execução de testes)
* `.env` (eventuais variáveis de ambiente)

projeto apresentado em 24 de nov de 2026 no 8ºperiodo de sistema de informação 
