import tkinter as tk
from tkinter import messagebox
import bcrypt
import banco
from telas import secretaria, professor, aluno

def login():
    email = entrada_usuario.get()
    senha = entrada_senha.get()

    con = banco.conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()
    con.close()

    if not usuario:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return

    if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
        messagebox.showinfo("Bem-vindo", usuario['nome'])
        janela.destroy()
        if usuario['tipo'] == 'secretaria':
            secretaria.abrir(usuario)
        elif usuario['tipo'] == 'professor':
            professor.abrir(usuario)
        else:
            aluno.abrir(usuario)
    else:
        messagebox.showerror("Erro", "Senha incorreta!")

janela = tk.Tk()
janela.title("Login - Sistema de Notas")
janela.geometry("300x200")

tk.Label(janela, text="E-mail:").pack()
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()

tk.Label(janela, text="Senha:").pack()
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()

tk.Button(janela, text="Entrar", command=login).pack(pady=10)

janela.mainloop()

from telas import secretaria
import banco

# Simulando login de secretaria
usuario_logado = {
    "nome": "Secretaria",
    "tipo": "secretaria"
}

# Abre a tela principal da secretaria
secretaria.abrir(usuario_logado)

