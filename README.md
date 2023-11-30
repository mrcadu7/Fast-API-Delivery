# Fast API Delivery

## Descrição
O Fast API Delivery é um projeto de entrega de pedidos de pizza desenvolvido com o framework FastAPI. Ele fornece uma API para gerenciar pedidos de pizza, autenticação de usuários e controle de acesso.

## Instalação
1. Clone o repositório do projeto.
2. Crie um ambiente virtual para o projeto.
3. Ative o ambiente virtual.
4. Instale as dependências do projeto usando o comando `pip install -r requirements.txt`.
5. Configure o banco de dados PostgreSQL no arquivo `database.py`.
6. Execute o script `init_db.py` para criar as tabelas do banco de dados.

## Uso
1. Inicie o servidor local executando o comando `uvicorn main:app --reload`.
2. Acesse a documentação da API em `http://localhost:8000/docs` para obter detalhes sobre os endpoints disponíveis.

## Endpoints

### Autenticação

- `POST /signup`: Cria um novo usuário.
- `POST /login`: Faz login e retorna um token de acesso.

### Pedidos

- `GET /orders`: Lista todos os pedidos (apenas para administradores).
- `GET /orders/{id}`: Obtém um pedido pelo ID (apenas para administradores).
- `GET /user/orders`: Lista os pedidos do usuário logado.
- `GET /user/orders/{id}`: Obtém um pedido específico do usuário logado.
- `POST /orders`: Cria um novo pedido.
- `PATCH /order/update/{id}`: Atualiza o status de um pedido (apenas para administradores).
- `DELETE /order/delete/{id}`: Exclui um pedido (apenas para administradores).

## Contribuição
1. Faça um fork do projeto.
2. Crie uma nova branch com a sua contribuição.
3. Envie um pull request com as suas alterações.

## Licença
Este projeto possui uma licença The Unlicense. Consulte o arquivo LICENSE para mais detalhes.
