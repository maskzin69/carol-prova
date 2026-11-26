# API de gerenciamento de tarefas

Aluno: João Pedro Fernandes Duarte

API REST desenvolvida em Python com FastAPI. Os dados ficam em memória e o cadastro exige autenticação JWT. A senha é validada por hash PBKDF2.

## Execução

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Acesse http://127.0.0.1:8000/docs para testar as rotas.

| Método | Rota | Descrição |
|---|---|---|
| POST | /login | Valida usuário e senha e retorna token JWT (200 ou 401). |
| GET | /tarefas | Lista tarefas (200). |
| POST | /tarefas | Cadastra tarefa pendente (201, 400 ou 401). |

Login de demonstração: usuário `admin`, senha `123456`. No cadastro, informe o cabeçalho `Authorization: Bearer TOKEN` e o JSON `{"titulo":"Estudar Python"}`. O token expira em uma hora. Os dados são reiniciados ao parar a API.

## Testes

```bash
python -m pytest -v
```

São seis testes: login correto, login incorreto, consulta, cadastro sem token, cadastro autenticado e título inválido. Após executar no computador, salvar a captura do terminal como `resultado_pytest.png` para entrega.
