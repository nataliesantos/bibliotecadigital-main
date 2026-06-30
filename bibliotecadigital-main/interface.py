import tkinter as tk
from tkinter import messagebox
from main import biblioteca, carregar_dados, salvar_dados

# função de listar
def clique_listar():
    if len(biblioteca) == 0:
        messagebox.showinfo("Acervo", "Nenhum livro cadastrado no momento!")
        return

    janela_lista = tk.Toplevel(janela)
    janela_lista.title("Livros Cadastrados")
    janela_lista.geometry("400x400")
    janela_lista.configure(bg="#FFF8E7")

    lbl_titulo = tk.Label(janela_lista, text="📚 Livros no Acervo", font=("Comic Sans MS", 14, "bold"), bg="#FFF8E7", fg="#005088")
    lbl_titulo.pack(pady=10)

    caixa_texto = tk.Text(janela_lista, font=("Comic Sans MS", 10), bg="white", fg="#334155", wrap="word")
    caixa_texto.pack(padx=15, pady=15, fill="both", expand=True)

    for livro in biblioteca.values():
        status_txt = "Disponível" if livro["Status"] == 0 else "Emprestado"
        texto_livro = (
            f"📖 Código: {livro['Código']}\n"
            f"Título: {livro['Título']}\n"
            f"Autor: {livro['Autor']}\n"
            f"Gênero: {livro['Gênero']}\n"
            f"Status: {status_txt}\n"
            f"{'-'*40}\n"
        )
        caixa_texto.insert(tk.END, texto_livro)
    
    caixa_texto.config(state=tk.DISABLED)

# CADASTRAR
def clique_cadastrar():
    janela_cad = tk.Toplevel(janela)
    janela_cad.title("Novo Cadastro 📝")
    janela_cad.geometry("350x450")
    janela_cad.configure(bg="#FFF8E7")

    def salvar_novo_livro():
        try:
            cod = int(ent_cod.get())
            if cod in biblioteca:
                messagebox.showerror("Erro", "Este código já existe!")
                return

            titulo = ent_titulo.get().strip()
            autor = ent_autor.get().strip()
            genero = ent_genero.get().strip()
            ano = int(ent_ano.get())
            status = int(ent_status.get())

            if status not in [0, 1]:
                messagebox.showwarning("Atenção", "o Status deve ser 0 ou 1!")
                return

            livro = {
                "Código": cod, "Título": titulo, "Autor": autor,
                "Gênero": genero, "Ano de publicação": ano, "Status": status
            }

            biblioteca[cod] = livro
            salvar_dados()
            
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso")
            janela_cad.destroy()

        except ValueError:
            messagebox.showerror("Erro", "Código, Ano e Status precisam ser números!")

    tk.Label(janela_cad, text="Cadastro de Livro", font=("Comic Sans MS", 14, "bold"), bg="#FFF8E7", fg="#005088").pack(pady=10)
    tk.Label(janela_cad, text="Código:", bg="#FFF8E7").pack()
    ent_cod = tk.Entry(janela_cad); ent_cod.pack()
    tk.Label(janela_cad, text="Título:", bg="#FFF8E7").pack()
    ent_titulo = tk.Entry(janela_cad, width=30); ent_titulo.pack()
    tk.Label(janela_cad, text="Autor:", bg="#FFF8E7").pack()
    ent_autor = tk.Entry(janela_cad, width=30); ent_autor.pack()
    tk.Label(janela_cad, text="Gênero:", bg="#FFF8E7").pack()
    ent_genero = tk.Entry(janela_cad, width=30); ent_genero.pack()
    tk.Label(janela_cad, text="Ano de publicação:", bg="#FFF8E7").pack()
    ent_ano = tk.Entry(janela_cad); ent_ano.pack()
    tk.Label(janela_cad, text="Status (0-Disp / 1-Emp):", bg="#FFF8E7").pack()
    ent_status = tk.Entry(janela_cad); ent_status.pack()

    btn_salvar = tk.Button(janela_cad, text="✨ Salvar Livro", font=("Comic Sans MS", 10, "bold"), bg="#11CAA0", fg="white", command=salvar_novo_livro, pady=5)
    btn_salvar.pack(pady=20)

# função de remover
def clique_remover():
    if len(biblioteca) == 0:
        messagebox.showinfo("Acervo", "Nenhum livro cadastrado para remover!")
        return

    janela_rem = tk.Toplevel(janela)
    janela_rem.title("Remover Livro ❌")
    janela_rem.geometry("300x200")
    janela_rem.configure(bg="#FFF8E7")

    def confirmar_remocao():
        try:
            cod = int(ent_cod_rem.get())
            if cod in biblioteca:
                titulo_livro = biblioteca[cod]["Título"]
                del biblioteca[cod]
                salvar_dados()
                messagebox.showinfo("Sucesso", f"O livro '{titulo_livro}' foi removido!")
                janela_rem.destroy()
            else:
                messagebox.showerror("Erro", "Livro não encontrado!")
        except ValueError:
            messagebox.showerror("Erro", "Digite um código válido!")

    tk.Label(janela_rem, text="Digite o código do livro:", font=("Comic Sans MS", 11), bg="#FFF8E7").pack(pady=20)
    ent_cod_rem = tk.Entry(janela_rem, font=("Comic Sans MS", 10), width=15); ent_cod_rem.pack(pady=5)
    btn_confirma_rem = tk.Button(janela_rem, text="❌ Apagar Livro", font=("Comic Sans MS", 10, "bold"), bg="#e11d48", fg="white", command=confirmar_remocao, pady=3)
    btn_confirma_rem.pack(pady=20)

# emprestar e devolver
def mudar_status_livro(novo_status):
    if len(biblioteca) == 0:
        messagebox.showinfo("Acervo 📖", "Nenhum livro cadastrado no sistema!")
        return

    janela_status = tk.Toplevel(janela)
    janela_status.title("Alterar Status 📖")
    janela_status.geometry("300x200")
    janela_status.configure(bg="#FFF8E7")

    def aplicar_mudanca():
        try:
            cod = int(ent_cod_st.get())
            if cod in biblioteca:
                status_atual = biblioteca[cod]["Status"]

                # Validação inteligente para Empréstimo
                if novo_status == 1 and status_atual == 1:
                    messagebox.showwarning("Aviso!", "Livro indisponível, pois está emprestado! Aguarde a devolução.")
                    return
                
                # Validação inteligente para Devolução
                if novo_status == 0 and status_atual == 0:
                    messagebox.showinfo("Aviso", "Este livro já está disponível no acervo!")
                    return

                # Salva a alteração se passar nos testes
                biblioteca[cod]["Status"] = novo_status
                salvar_dados()
                
                acao = "emprestado" if novo_status == 1 else "devolvido"
                messagebox.showinfo("Sucesso 🎉", f"Livro {acao} com sucesso!")
                janela_status.destroy()
            else:
                messagebox.showerror("Erro", "Livro não encontrado com esse código!")
        except ValueError:
            messagebox.showerror("Erro", "Digite um código válido!")

    tk.Label(janela_status, text="Digite o código do livro:", font=("Comic Sans MS", 11), bg="#FFF8E7").pack(pady=20)
    ent_cod_st = tk.Entry(janela_status, font=("Comic Sans MS", 10), width=15); ent_cod_st.pack(pady=5)
    btn_acao = tk.Button(janela_status, text="Confirmar", font=("Comic Sans MS", 10, "bold"), bg="#005088", fg="white", command=aplicar_mudanca, pady=3)
    btn_acao.pack(pady=20)


#Janela principal e botões
janela = tk.Tk()
janela.title("Sistema de Biblioteca - UFRPE")
janela.geometry("450x550")        
janela.configure(bg="#FFF8E7")     

# Chamar o carregar_dado IMEDIATAMENTE depois da a criação da janela corrige a persistência
carregar_dados() 

titulo = tk.Label(janela, text="Biblioteca Digital 📚", font=("Comic Sans MS", 20, "bold"), bg="#FFF8E7", fg="#005088")
titulo.pack(pady=20)

subtitulo = tk.Label(janela, text="Selecione uma das opções abaixo:", font=("Comic Sans MS", 12), bg="#FFF8E7", fg="#334155")
subtitulo.pack(pady=5)

# lista organizada e ainhada dos botoes principais
btn_listar = tk.Button(janela, text="📚 Listar Livros", font=("Comic Sans MS", 11), bg="#11CAA0", fg="white", width=25, bd=0, pady=5, command=clique_listar)
btn_listar.pack(pady=6)

btn_cadastrar = tk.Button(janela, text="📝 Cadastrar Novo Livro", font=("Comic Sans MS", 11), bg="#005088", fg="white", width=25, bd=0, pady=5, command=clique_cadastrar)
btn_cadastrar.pack(pady=6)

btn_remover = tk.Button(janela, text="❌ Remover Livro", font=("Comic Sans MS", 11), bg="#e11d48", fg="white", width=25, bd=0, pady=5, command=clique_remover)
btn_remover.pack(pady=6)

btn_emprestar = tk.Button(janela, text="🤝 Emprestar Livro", font=("Comic Sans MS", 11), bg="#f59e0b", fg="white", width=25, bd=0, pady=5, command=lambda: mudar_status_livro(1))
btn_emprestar.pack(pady=6)

btn_devolver = tk.Button(janela, text="🔄 Devolver Livro", font=("Comic Sans MS", 11), bg="#10b981", fg="white", width=25, bd=0, pady=5, command=lambda: mudar_status_livro(0))
btn_devolver.pack(pady=6)

btn_sair = tk.Button(janela, text="🚪 Sair", font=("Comic Sans MS", 11), bg="#64748b", fg="white", width=25, bd=0, pady=5, command=janela.quit)
btn_sair.pack(pady=20)

janela.mainloop()