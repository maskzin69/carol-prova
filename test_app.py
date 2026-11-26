import pytest
from fastapi.testclient import TestClient
from app import app, tarefas

client = TestClient(app)

@pytest.fixture(autouse=True)
def restaurar_tarefas():
    original = tarefas.copy()
    yield
    tarefas[:] = original

def autenticar():
    resposta = client.post('/login', json={'usuario': 'admin', 'senha': '123456'})
    return {'Authorization': 'Bearer ' + resposta.json()['access_token']}

def test_login_correto():
    resposta = client.post('/login', json={'usuario': 'admin', 'senha': '123456'})
    assert resposta.status_code == 200
    assert resposta.json()['access_token']

def test_login_incorreto():
    resposta = client.post('/login', json={'usuario': 'admin', 'senha': 'errada'})
    assert resposta.status_code == 401
    assert 'access_token' not in resposta.json()

def test_consulta():
    resposta = client.get('/tarefas')
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

def test_sem_token():
    antes = len(tarefas)
    resposta = client.post('/tarefas', json={'titulo': 'Ler'})
    assert resposta.status_code == 401
    assert len(tarefas) == antes

def test_com_token():
    ids = {t['id'] for t in tarefas}
    resposta = client.post('/tarefas', json={'titulo': 'Ler'}, headers=autenticar())
    assert resposta.status_code == 201
    tarefa = resposta.json()
    assert tarefa['titulo'] == 'Ler'
    assert tarefa['situacao'] == 'pendente'
    assert tarefa['id'] not in ids
    assert tarefa in tarefas

def test_titulo_vazio():
    antes = len(tarefas)
    headers = autenticar()
    for dados in ({'titulo': ''}, {'titulo': '   '}, {}):
        resposta = client.post('/tarefas', json=dados, headers=headers)
        assert resposta.status_code == 400
        assert len(tarefas) == antes
