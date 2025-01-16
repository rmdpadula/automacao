import tkinter as tk
from tkinter import scrolledtext
import os
import shutil
import ctypes
import sys
import winreg

# Verificar se o programa esta rodando como administrador
def verificar_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
    print(teste)

# Funcao para limpar pastas temporarias
def limpar_temporarios(log_terminal):
    try:
        log_terminal.insert(tk.END, "Iniciando limpeza de pastas temporarias...\n")
        log_terminal.see(tk.END)
        
        temp_dirs = [
            os.getenv("TEMP"),  # %temp%
            os.getenv("WINDIR") + "\\Temp",  # C:\Windows\Temp
            os.getenv("WINDIR") + "\\Prefetch"  # C:\Windows\Prefetch
        ]

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                log_terminal.insert(tk.END, f"Limpando: {temp_dir}\n")
                log_terminal.see(tk.END)
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)  # Remove arquivos ou links
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)  # Remove diretorios
                    except PermissionError:
                        log_terminal.insert(tk.END, f"Nao foi possivel remover {item_path}: Acesso negado.\n")
                    except OSError as e:
                        log_terminal.insert(tk.END, f"Nao foi possivel remover {item_path}: {e.strerror}.\n")
                    except Exception as e:
                        log_terminal.insert(tk.END, f"Erro ao remover {item_path}: {e}\n")
                    log_terminal.see(tk.END)

        log_terminal.insert(tk.END, "Limpeza concluida com sucesso!\n")
        log_terminal.see(tk.END)
    except Exception as e:
        log_terminal.insert(tk.END, f"Erro ao limpar pastas: {e}\n")
        log_terminal.see(tk.END)

# Funcao para apagar registros no Windows Registry
def apagar_registros(log_terminal):
    try:
        log_terminal.insert(tk.END, "Iniciando exclusao de registros no Windows Registry...\n")
        log_terminal.see(tk.END)

        registros = [
            r"Software\Linx Sistemas\LinxPOS\Venda",
            r"Software\Linx Sistemas\LinxPOS\Log",
            r"Software\Linx Sistemas\LinxPOS\Log OMS",
            r"Software\Linx Sistemas\LinxPOS\Log OMS\Troca",
            r"Software\Linx Sistemas\LinxPOS\LogCancelSale",
            r"Software\Linx Sistemas\LinxPOS\LogMRE-S",
            r"Software\Linx Sistemas\LinxPOS-e\Venda",
            r"Software\Linx Sistemas\LinxPOS-e\Log",
            r"Software\Linx Sistemas\LinxPOS-e\Log OMS",
            r"Software\Linx Sistemas\LinxPOS-e\Log OMS\Troca",
            r"Software\Linx Sistemas\LinxPOS-e\LogCancelSale",
            r"Software\Linx Sistemas\LinxPOS-e\LogMRE-S"
        ]

        for registro in registros:
            try:
                chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registro, 0, winreg.KEY_SET_VALUE)
                log_terminal.insert(tk.END, f"Limpando valores em: {registro}\n")
                i = 0
                while True:
                    try:
                        valor = winreg.EnumValue(chave, i)
                        winreg.DeleteValue(chave, valor[0])  # Apagar valor
                        log_terminal.insert(tk.END, f"Valor '{valor[0]}' removido com sucesso.\n")
                    except OSError:
                        break
                    except Exception as e:
                        log_terminal.insert(tk.END, f"Erro ao remover valor: {e}\n")
                    i += 1
                winreg.CloseKey(chave)
            except FileNotFoundError:
                log_terminal.insert(tk.END, f"Registro nao encontrado: {registro}\n")
            except Exception as e:
                log_terminal.insert(tk.END, f"Erro ao acessar registro {registro}: {e}\n")
            log_terminal.see(tk.END)

        log_terminal.insert(tk.END, "Exclusao de registros concluida com sucesso!\n")
        log_terminal.see(tk.END)
    except Exception as e:
        log_terminal.insert(tk.END, f"Erro ao apagar registros: {e}\n")
        log_terminal.see(tk.END)

# Interface grafica
def criar_interface():
    janela = tk.Tk()
    janela.title("Automacao de Tarefas")

    # Tornar a janela fixa (desativar redimensionamento)
    janela.resizable(False, False)

    # Adicionando um icone ao programa
    try:
        janela.iconbitmap("favicon.ico")  # Substitua "icone.ico" pelo caminho do seu arquivo de icone
    except Exception as e:
        print(f"Erro ao carregar o icone: {e}")

    # Adicionando o banner
    try:
        banner = tk.PhotoImage(file="logo-netlogic.png")  # Substitua "banner.png" pelo caminho do seu arquivo de banner
        banner_label = tk.Label(janela, image=banner)
        banner_label.pack(side=tk.TOP, fill=tk.X)
    except Exception as e:
        print(f"Erro ao carregar o banner: {e}")

    # Frame principal
    frame_principal = tk.Frame(janela)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Frame dos botoes
    frame_botoes = tk.Frame(frame_principal)
    frame_botoes.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    btn_limpar_temp = tk.Button(frame_botoes, text="Limpar Pastas Temporarias", 
                                 command=lambda: limpar_temporarios(log_terminal), width=25)
    btn_limpar_temp.pack(pady=5)

    btn_apagar_registros = tk.Button(frame_botoes, text="Apagar Registros no Registro", 
                                      command=lambda: apagar_registros(log_terminal), width=25)
    btn_apagar_registros.pack(pady=5)

    btn_encerrar = tk.Button(frame_botoes, text="Encerrar", command=janela.quit, width=25)
    btn_encerrar.pack(pady=5)

    # Frame do terminal
    frame_terminal = tk.Frame(frame_principal)
    frame_terminal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    log_terminal = scrolledtext.ScrolledText(frame_terminal, width=50, height=20, state='normal')
    log_terminal.pack(fill=tk.BOTH, expand=True)
    log_terminal.insert(tk.END, "Programa iniciado...\n")
    log_terminal.see(tk.END)

    # Definir o tamanho fixo da janela
    janela.geometry("800x500")
    janela.mainloop()

# Execucao do programa
if __name__ == "__main__":
    if not verificar_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        criar_interface()
