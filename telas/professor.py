import tkinter as tk
from tkinter import ttk, messagebox
import banco

# Função principal: abre a janela do professor
def abrir(usuario_logado):
    janela = tk.Tk()
    janela.title("Área do Professor - Sistema de Notas")
    janela.geometry("750x500")

    tk.Label(janela, text=f"Bem-vindo(a), Professor {usuario_logado['nome']}",
             font=("Arial", 14, "bold")).pack(pady=10)

    # Frame para tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10, fill="x")

    colunas = ("ID", "Aluno", "Nota Trabalho", "Nota Prova")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        tabela.column(coluna, width=150, anchor="center")

    tabela.pack(fill="x", padx=10)

    # Frame de edição de notas
    frame_editar = tk.Frame(janela)
    frame_editar.pack(pady=15)

    tk.Label(frame_editar, text="Nota Trabalho:").grid(row=0, column=0, padx=5, pady=5)
    entrada_trabalho = tk.Entry(frame_editar, width=10)
    entrada_trabalho.grid(row=0, column=1, padx=5)

    tk.Label(frame_editar, text="Nota Prova:").grid(row=0, column=2, padx=5, pady=5)
    entrada_prova = tk.Entry(frame_editar, width=10)
    entrada_prova.grid(row=0, column=3, padx=5)

    # --- Funções internas ---
    def listar_alunos():
        """Mostra todos os alunos cadastrados."""
        for item in tabela.get_children():
            tabela.delete(item)

        con = banco.conectar()
        cursor = con.cursor(dictionary=True)

        # Busca alunos e notas (se existirem)
        cursor.execute("""
            SELECT a.id, a.nome,
                   COALESCE(n.nota_trabalho, '-') AS nota_trabalho,
                   COALESCE(n.nota_prova, '-') AS nota_prova
            FROM usuarios a
            LEFT JOIN notas n ON a.id = n.aluno_id
            WHERE a.tipo = 'aluno'
            ORDER BY a.nome
        """)

        for aluno in cursor.fetchall():
            tabela.insert("", "end", values=(
                aluno["id"], aluno["nome"], aluno["nota_trabalho"], aluno["nota_prova"]
            ))

        con.close()

    def salvar_notas():
        """Insere ou atualiza notas do aluno selecionado."""
        item = tabela.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela!")
            return

        dados = tabela.item(item)["values"]
        aluno_id = dados[0]
        nota_trabalho = entrada_trabalho.get()
        nota_prova = entrada_prova.get()

        if not nota_trabalho or not nota_prova:
            messagebox.showwarning("Atenção", "Preencha as duas notas!")
            return

        try:
            con = banco.conectar()
            cursor = con.cursor()

            # Verifica se já existe nota para o aluno
            cursor.execute("SELECT id FROM notas WHERE aluno_id=%s AND professor_id=%s",
                           (aluno_id, usuario_logado["id"]))
            existente = cursor.fetchone()

            if existente:
                # Atualiza as notas
                sql = "UPDATE notas SET nota_trabalho=%s, nota_prova=%s WHERE aluno_id=%s AND professor_id=%s"
                cursor.execute(sql, (nota_trabalho, nota_prova, aluno_id, usuario_logado["id"]))
            else:
                # Insere nova nota
                sql = "INSERT INTO notas (aluno_id, professor_id, nota_trabalho, nota_prova) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (aluno_id, usuario_logado["id"], nota_trabalho, nota_prova))

            con.commit()
            con.close()
            messagebox.showinfo("Sucesso", "Notas salvas com sucesso!")
            listar_alunos()
            entrada_trabalho.delete(0, tk.END)
            entrada_prova.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar notas: {e}")

    # --- Botões ---
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Atualizar Lista", command=listar_alunos, width=15).grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Salvar Notas", command=salvar_notas, width=15).grid(row=0, column=1, padx=10)

    listar_alunos()
    janela.mainloop()
