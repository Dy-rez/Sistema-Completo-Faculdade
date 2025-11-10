import tkinter as tk
from tkinter import ttk, messagebox
import banco
import bcrypt

# Função que abre a janela principal da Secretaria
def abrir(usuario_logado):
    janela = tk.Tk()
    janela.title("Área da Secretaria - Sistema de Notas")
    janela.geometry("700x500")

    # Label de boas-vindas
    tk.Label(janela, text=f"Bem-vindo(a), {usuario_logado['nome']}!",
             font=("Arial", 14, "bold")).pack(pady=10)

    # Frame para o formulário de cadastro
    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    # Campos do formulário
    tk.Label(frame_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entrada_nome = tk.Entry(frame_form, width=30)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
    entrada_cpf = tk.Entry(frame_form, width=30)
    entrada_cpf.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    entrada_email = tk.Entry(frame_form, width=30)
    entrada_email.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Senha:").grid(row=3, column=0, padx=5, pady=5)
    entrada_senha = tk.Entry(frame_form, show="*", width=30)
    entrada_senha.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Tipo:").grid(row=4, column=0, padx=5, pady=5)
    combo_tipo = ttk.Combobox(frame_form, values=["secretaria", "professor", "aluno"], state="readonly", width=27)
    combo_tipo.grid(row=4, column=1, padx=5, pady=5)

    # --- Funções internas ---
    def cadastrar():
        nome = entrada_nome.get()
        cpf = entrada_cpf.get()
        email = entrada_email.get()
        senha = entrada_senha.get()
        tipo = combo_tipo.get()

        if not nome or not cpf or not email or not senha or not tipo:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        # Criptografa a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            con = banco.conectar()
            cursor = con.cursor()
            sql = "INSERT INTO usuarios (cpf, nome, email, senha, tipo) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (cpf, nome, email, senha_hash, tipo))
            con.commit()
            con.close()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            listar()  # Atualiza a tabela
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")

    def limpar_campos():
        entrada_nome.delete(0, tk.END)
        entrada_cpf.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)
        combo_tipo.set('')

    def listar():
        for item in tabela.get_children():
            tabela.delete(item)

        con = banco.conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, tipo FROM usuarios ORDER BY id ASC")
        for usuario in cursor.fetchall():
            tabela.insert("", "end", values=(usuario["id"], usuario["nome"], usuario["email"], usuario["tipo"]))
        con.close()

    def excluir():
        item_selecionado = tabela.focus()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir!")
            return
        dados = tabela.item(item_selecionado)["values"]
        usuario_id = dados[0]

        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este usuário?")
        if confirmar:
            con = banco.conectar()
            cursor = con.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            con.commit()
            con.close()
            listar()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")

    # --- Botões ---
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar, width=15).grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Excluir", command=excluir, width=15).grid(row=0, column=1, padx=10)
    tk.Button(frame_botoes, text="Atualizar Lista", command=listar, width=15).grid(row=0, column=2, padx=10)

    # --- Tabela de listagem ---
    colunas = ("ID", "Nome", "Email", "Tipo")
    tabela = ttk.Treeview(janela, columns=colunas, show="headings")
    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        tabela.column(coluna, width=150)
    tabela.pack(pady=20, fill="x")

    listar()  # Preenche a tabela ao abrir
    janela.mainloop()
