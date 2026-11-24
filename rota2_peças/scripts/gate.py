import subprocess
import sys

def run_gate():
    print("--- EXECUTANDO QUALITY GATE ---")
    result = subprocess.run(["pytest", "test_app.py"], capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode == 0:
        print("✅ QUALITY GATE PASSOU: Todos os testes estao GREEN.")
        sys.exit(0)
    else:
        print("❌ QUALITY GATE FALHOU: Existem testes em estado RED.")
        sys.exit(1)

if __name__ == "__main__":
    run_gate()