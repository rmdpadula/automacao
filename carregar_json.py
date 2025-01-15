from cryptography.fernet import Fernet
import json

# Chave de criptografia (mesma usada para criptografar)
CHAVE = b"X01d0zqSzxmTpnfNcL15Qh-lpAyxWe_dL87SrKyHAG0="

# Caminho do arquivo criptografado
CRIPTO_FILE = "base_crypto.json"

# Função para descriptografar o JSON
def carregar_dados():
    try:
        # Ler o arquivo criptografado
        fernet = Fernet(CHAVE)
        with open(CRIPTO_FILE, "rb") as f:
            dados_criptografados = f.read()

        # Descriptografar o conteúdo
        dados_json = fernet.decrypt(dados_criptografados).decode()
        dados = json.loads(dados_json)

        print(dados)

        return dados
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

# Programa principal
if __name__ == "__main__":
    dados = carregar_dados()
    if dados:
        print(f"Usuario: {dados['credenciais']['usuario']}")
        print(f"Senha: {dados['credenciais']['senha']}")
        for loja in dados["lojas"]:
            print(f"Loja: {loja['LOJA']}, Hostname: {loja['HOSTNAME']}, DB Name: {loja['DB NAME']}")
    else:
        print("Nao foi possivel carregar os dados.")
