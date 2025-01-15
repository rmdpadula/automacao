from cryptography.fernet import Fernet
import pandas as pd
import json

# Gerar chave de criptografia (somente execute isso uma vez e salve a chave gerada)
def gerar_chave():
    chave = Fernet.generate_key()
    print(f"Chave gerada (salve isto com segurança): {chave.decode()}")

# Use a chave gerada e salve-a aqui (mantenha segura)
CHAVE = b"X01d0zqSzxmTpnfNcL15Qh-lpAyxWe_dL87SrKyHAG0="

# Caminhos dos arquivos
EXCEL_FILE = "base.xlsx"
JSON_FILE = "base.json"
CRIPTO_FILE = "base_crypto.json"

# Função para gerar JSON a partir do Excel
def gerar_json():
    try:
        # Ler o Excel
        lojas = pd.read_excel(EXCEL_FILE, dtype={"COD_FILIAL": str})

        # Converter para dicionário
        lojas_dict = lojas.to_dict(orient="records")

        # Adicionar credenciais ao JSON
        dados = {
            "credenciais": {
                "usuario": "netlogic",
                "senha": "DreamTeam@MSP"
            },
            "lojas": lojas_dict
        }

        # Salvar como JSON
        with open(JSON_FILE, "w") as f:
            json.dump(dados, f, indent=4)

        print("Arquivo JSON gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar JSON: {e}")

# Função para criptografar o JSON
def criptografar_json():
    try:
        # Ler o JSON gerado
        with open(JSON_FILE, "r") as f:
            dados = f.read()

        # Criptografar o conteúdo
        fernet = Fernet(CHAVE)
        dados_criptografados = fernet.encrypt(dados.encode())

        # Salvar o arquivo criptografado
        with open(CRIPTO_FILE, "wb") as f:
            f.write(dados_criptografados)

        print("Arquivo JSON criptografado com sucesso!")
    except Exception as e:
        print(f"Erro ao criptografar JSON: {e}")

# Executar o processo completo
if __name__ == "__main__":
    gerar_json()        # Gera o arquivo JSON a partir do Excel
    criptografar_json() # Criptografa o arquivo JSON
