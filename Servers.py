import subprocess
import os

# Defina os caminhos das pastas onde estão os app.py
folders = [
    "cadastrarProduto",
    "Cardapio",
    "estoque",
    "historico",
    "itemOrdem",
    "manterMenu",
]
apps = [
    "cadastrarProduto.py",
    "cardapio.py",
    "controleEstoque.py",
    "historico.py",
    "itemOrdem.py",
    "itemMenu.py"]

def start_servers():
    processes = []
    for folder in folders:
        for app in apps:
            
            app_path = os.path.join(folder, app)
            if os.path.exists(app_path):
                print(f"Iniciando servidor em {folder}...")
                p = subprocess.Popen(["python", app_path])
                processes.append(p)

    # Aguarda o término de todos os processos
    for p in processes:
        p.wait()

if __name__ == "__main__":
    start_servers()