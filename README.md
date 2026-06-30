# Sistema de Gerenciamento de Biblioteca Digital 

Esse projeto foi criado por Melissa Galdino e Natalie Santos para a disciplina de Programação I da UFRPE. É uma apicação feita com python para gerenciar o acervo de uma biblioteca de forma simples e eficiente. 

##  Autoras:
*Melissa Galdino: Responsável pela primeira versão do código e manipulação de arquivos.
*Natalie Santos: Responsável pela interface, pelos comentários e segunda versão do código.

## Funcionalidades do Sistema

O sistema conta com um menu interativo com as seguintes operações:
1. **Listar Livros**: Exibe na tela todos os livros salvos no acervo atualmente.
2. **Cadastrar Novo Livro**: Permite a inserção de novos títulos e coleta dados como Código, Título, Autor, Gênero, Ano e Status.
3. **Remover Livro**: Exclui um registro do acervo pelo seu código identificador.
4. **Emprestar Livro**: Altera o status do livro para "Emprestado" (representado pelo valor `1`).
5. **Devolver Livro**: Altera o status do livro para "Disponível" (representado pelo valor `0`).
6. **Buscar e Filtrar**: Permite buscar livros por título ou autor específico, além de filtrar o acervo mostrando apenas os disponíveis ou apenas os emprestados.
7. **Exportar Relatório**: Gera um arquivo de texto externo (`relatorio.txt`) contendo estatísticas gerais (total de livros, quantos estão emprestados, gênero mais frequente e a listagem completa).
8. **Sair**: Encerra a execução do programa com segurança.

---

# o que foi utilizado?

* **Python 3**: Linguagem base utilizada para construir toda a lógica do sistema.
* **JSON (JavaScript Object Notation)**: Utilizado para criar um banco de dados local (`dados.json`), garantindo que as informações não sejam perdidas quando o programa for fechado (Persistência de Dados).
* **Biblioteca OS**: Utilizada para interagir com o terminal do sistema operacional e limpar a tela a cada ação, tornando a interface visual mais limpa para o usuário.

---

# como os dados são salvos?

Os dados dos livros são guardados no formato de dicionários dentro do Python e sincronizados automaticamente com o arquivo `dados.json`. 
O sistema conta com tratamento de erros (`try/except`), garantindo que entradas inválidas (como digitar letras onde deveriam ser números) não quebrem a execução do programa.