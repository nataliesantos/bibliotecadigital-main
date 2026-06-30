# Projeto: Sistema de Cadastro de Biblioteca
# Feito por: Melissa Galdino e Natalie Santos

import json

# Dicionário que servirá como banco de dados temporário na memória
biblioteca = {}

#salva as informações da memória para arquivo json
def salvar_dados():
    with open("dados.json", "w", encoding="utf-8") as a:
        json.dump(biblioteca, a, indent=4, ensure_ascii=False)

#carrega todos os dados salvos do arquio para a memória
def carregar_dados():
    global biblioteca
    try:
        with open("dados.json", "r", encoding="utf-8") as a:
            dados = json.load(a)
            biblioteca = {int(k): v for k, v in dados.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        biblioteca = {}

def listar():
    if len(biblioteca) == 0:
        print("Nenhum livro cadastrado.")
    else:
        print("\nLista de livros cadastrados")
    for livro in biblioteca.values():
        print(f"Código: {livro['Código']}")
        print(f"Título: {livro['Título']}")
        print(f"Autor: {livro['Autor']}")
        print(f"Gênero: {livro['Gênero']}")
        print(f"Ano de publicação: {livro['Ano de publicação']}")
        print(f"Status: {livro['Status']}\n")

def cadastrar():
    try:
        cod = int(input('Código: '))
        if cod in biblioteca:
            print("Infelizmente já existe um livro cadastrado com esse código!")
            return
            
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        genero = input("Gênero: ").strip()
        ano_pub = int(input("Ano de publicação: "))
        status = int(input("Status (0 - Disponível / 1 - Emprestado): "))
        
        if status not in [0, 1]:
            print("Erro: Status inválido! Deve ser 0 ou 1.")
            return

    except ValueError:
        print("Valor inválido! O código, ano de publicação e status devem ser numeros.")
        return

    livro = {
        "Código": cod,
        "Título": titulo,
        "Autor": autor,
        "Gênero": genero,
        "Ano de publicação": ano_pub,
        "Status": status
    }

    biblioteca[cod] = livro
    salvar_dados()
    print("Cadastrado com sucesso!")

def remover():
    try:
        cod = int(input("Digite o código do livro que deseja remover: "))
    except ValueError:
        print("Código inválido.")
        return

    if cod in biblioteca:
        del biblioteca[cod]
        print("Livro removido com sucesso!")
        salvar_dados()
    else:
        print("Livro não encontrado.")

def emprestar():
    try:
        cod = int(input("Digite o código do livro que deseja emprestar: "))
    except ValueError:
        print("Código inválido.")
        return
    
    if cod in biblioteca:
        biblioteca[cod]["Status"] = 1
        print("Livro emprestado com sucesso!")
        salvar_dados()
    else:
        print("Livro não encontrado.")

def devolver():
    try:
        cod = int(input("Digite o código do livro que deseja devolver: "))
    except ValueError:
        print("Código inválido.")
        return
    
    if cod in biblioteca:
        biblioteca[cod]["Status"] = 0
        print("Livro devolvido com sucesso!")
        salvar_dados()
    else:
        print("Livro não encontrado.")

def buscar_e_filtrar():
    if len(biblioteca) == 0:
        print("Nenhum livro cadastrado para buscar.")
        return

    print("\n***** Buscar ou Filtrar *****")
    print("1 - Buscar título")
    print("2 - Buscar autor")
    print("3 - Filtrar livros disponíveis")
    print("4 - Filtrar livros emprestados\n")

    try: 
        op = int(input("Escolha o tipo de busca: "))
    except ValueError:
        print("Código inválido.")
        return
    
    if op == 1:
        titulo = input("Digite o *título*: ").lower()
        for livro in biblioteca.values():
            if titulo in livro["Título"].lower():
                print(f"\nLivro encontrado!")
                print(f"Código: {livro['Código']} - Título: {livro['Título']} - Autor: {livro['Autor']}")
                print(f"Ano: {livro['Ano de publicação']} - Status: {livro['Status']}")
                
    elif op == 2:
        autor = input("Digite o nome do autor: ").lower()
        for livro in biblioteca.values():
            if autor in livro["Autor"].lower():
                print(f"\nLivro encontrado!")
                print(f"Código: {livro['Código']} - Título: {livro['Título']} - Autor: {livro['Autor']}")
                print(f"Gênero: {livro['Gênero']} - Ano: {livro['Ano de publicação']} - Status: {livro['Status']}")
                
    elif op == 3:
        print("\n*** Livros Disponíveis! ***")
        for livro in biblioteca.values():
            if livro["Status"] == 0:
                print(f"Código: {livro['Código']} - Título: {livro['Título']}")
    
    elif op == 4:
        print("\n*** Livros Emprestados! ***")
        for livro in biblioteca.values():
            if livro['Status'] == 1:
                print(f"Código: {livro['Código']} - Título: {livro['Título']}")

def exportar_relatorio():
    if len(biblioteca) == 0:
        print("Nenhum livro cadastrado para exportar.")
        return

    total_livros = len(biblioteca)
    disponiveis = 0
    emprestados = 0
    
    for livro in biblioteca.values():
        if livro["Status"] == 0:
            disponiveis += 1
        else:
            emprestados += 1

    contagem = {}
    for livro in biblioteca.values():
        g = livro["Gênero"]
        if g != "": 
            if g in contagem:
                contagem[g] += 1
            else:
                contagem[g] = 1

    comum = "Nenhum"
    maior_qtd = 0
    for g, qtd in contagem.items():
        if qtd > maior_qtd:
            maior_qtd = qtd
            comum = g

    try:
        with open("relatorio.txt", "w", encoding="utf-8") as f:
            f.write("*** Relatório da Biblioteca ***\n\n")
            f.write(f"Total de Livros Cadastrados: {total_livros}\n")
            f.write(f"Livros Disponíveis: {disponiveis}\n")
            f.write(f"Livros Emprestados: {emprestados}\n")
            f.write(f"Gênero mais frequente: {comum}\n\n")

            f.write("LISTA COMPLETA DOS LIVROS:\n\n")
            for livro in biblioteca.values():
                status_txt = "Disponível" if livro["Status"] == 0 else "Emprestado"
                f.write(f"Código: {livro['Código']}\n")
                f.write(f"Título: {livro['Título']}\n") 
                f.write(f"Autor: {livro['Autor']}\n") 
                f.write(f"Gênero: {livro['Gênero']}\n")
                f.write(f"Ano: {livro['Ano de publicação']}\n")
                f.write(f"Status: {status_txt}\n")
        
        print("Relatório gerado e salvo com sucesso em 'relatorio.txt'!")
        
    except IOError:
        print("Infelizmente Não foi possível gravar o arquivo de relatório.")
# o menu de opções que aparecem no terminal
def exibir_menu():
    while True:
        print("""\nBem vindo(a) a Biblioteca!

        Selecione umas dos opções a seguir:
        1 - Listar
        2 - Cadastrar
        3 - Remover
        4 - Emprestar
        5 - Devolver
        6 - Buscar/Filtrar
        7 - Exportar Relatório(.txt)
        8 - Sair 
        """)
        try:
            op = int(input("Opção: "))
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas números.")
            continue

        if op == 1:
            listar()
        elif op == 2:
            cadastrar()
        elif op == 3:
            remover()
        elif op == 4:
            emprestar()
        elif op == 5:
            devolver()
        elif op == 6:
            buscar_e_filtrar()
        elif op == 7:
            exportar_relatorio()
        elif op == 8:
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")

#para não atrapalhar a interface
if __name__ == "__main__":
    carregar_dados()
    exibir_menu()