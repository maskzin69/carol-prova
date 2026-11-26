import os
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, Body, Header, HTTPException

app = FastAPI(title='API de Tarefas')
CHAVE = os.getenv('JWT_SECRET') or secrets.token_hex(32)
SALT = b'atividade-tarefas'

def hash_senha(senha):
    return hashlib.pbkdf2_hmac('sha256', senha.encode(), SALT, 100000)

SENHA_HASH = hash_senha('123456')
tarefas = [{'id': 1, 'titulo': 'Organizar atividades', 'situacao': 'pendente'}]

@app.post('/login')
def login(dados: dict = Body(..., examples=[{'usuario': 'admin', 'senha': '123456'}])):
    senha = dados.get('senha')
    if dados.get('usuario') != 'admin' or not isinstance(senha, str) or not hmac.compare_digest(hash_senha(senha), SENHA_HASH):
        raise HTTPException(401, 'Credenciais inválidas')
    token = jwt.encode({'sub': 'admin', 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, CHAVE, algorithm='HS256')
    return {'access_token': token}

@app.get('/tarefas')
def consultar():
    return tarefas

@app.post('/tarefas', status_code=201)
def cadastrar(dados: dict = Body(default={}, examples=[{'titulo': 'Estudar Python'}]), authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(401, 'Token obrigatório')
    try:
        payload = jwt.decode(authorization[7:], CHAVE, algorithms=['HS256'], options={'require': ['exp', 'sub']})
        if payload['sub'] != 'admin':
            raise jwt.InvalidTokenError()
    except jwt.InvalidTokenError:
        raise HTTPException(401, 'Token inválido')
    titulo = dados.get('titulo')
    if not isinstance(titulo, str) or not titulo.strip():
        raise HTTPException(400, 'Título obrigatório')
    tarefa = {'id': max((t['id'] for t in tarefas), default=0) + 1, 'titulo': titulo.strip(), 'situacao': 'pendente'}
    tarefas.append(tarefa)
    return tarefa
