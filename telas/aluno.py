import tkinter as tk
from tkinter import ttk, messagebox
import banco

# Função principal: abre a janela da área do aluno
def abrir(usuario_logado):
    janela = tk.Tk()
    janela.title("Área do Aluno - Sistema de Notas")
    janela.geometry("700x500")

    # Saudação inicial
    tk.Label(
        janela,
        text=f"Bem-vindo(a), {usuario_logado['nome']}!",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    # Frame da tabela de notas
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=20, fill="x")

    # Define as colunas da Treeview (tabela)
    colunas = ("Disciplina", "Nota Trabalho", "Nota Prova", "Média", "Situação")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    # Configura cabeçalhos e largura das colunas
    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        tabela.column(coluna, width=120, anchor="center")

    tabela.pack(fill="x", padx=10)

    # Função para buscar notas do aluno no banco
    def carregar_notas():
        for item in tabela.get_children():
            tabela.delete(item)

        con = banco.conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                d.nome AS disciplina,
                n.nota_trabalho,
                n.nota_prova
            FROM notas n
            JOIN usuarios p ON n.professor_id = p.id
            LEFT JOIN disciplinas d ON d.id = 1  -- pode adaptar se tiver várias disciplinas
            WHERE n.aluno_id = %s
        """, (usuario_logado["id"],))

        notas = cursor.fetchall()
        con.close()

        if not notas:
            messagebox.showinfo("Informação", "Suas notas ainda não foram lançadas.")
            return

        for nota in notas:
            nota_trabalho = nota["nota_trabalho"] if nota["nota_trabalho"] is not None else 0
            nota_prova = nota["nota_prova"] if nota["nota_prova"] is not None else 0
            media = round(float(nota_trabalho) + float(nota_prova), 2)

            if media >= 6:
                situacao = "Aprovado"
            else:
                situacao = "Reprovado"

            tabela.insert("", "end", values=(
                nota["disciplina"],
                nota_trabalho,
                nota_prova,
                media,
                situacao
            ))

    # Botão para atualizar notas
    tk.Button(janela, text="Atualizar Notas", command=carregar_notas, width=20).pack(pady=10)

    carregar_notas()  # Carrega automaticamente ao abrir
    janela.mainloop()
