import requests

API_URL = "https://trabalhorpa-api.onrender.com/"

def obter_chamados():
    response = requests.get(f"{API_URL}/chamados/")
    if response.status_code == 200:
        return response.json()
    return []

def validar_chamado_api(chamado_id: int, validar: bool):
    response = requests.put(f"{API_URL}/chamado/{chamado_id}/validar", json={"validar": validar})
    return response.json()

def remover_chamado_por_id_api(chamado_id: int):
    response = requests.delete(f"{API_URL}/chamado/{chamado_id}")
    return response.json()

def criar_chamado_api(local_subestacao: str, nome_tecnico: str, acao_tomada: str, gravidade: str, situacao_subestacao: str):
    payload = {
        "local_subestacao": local_subestacao,
        "nome_tecnico": nome_tecnico,
        "acao_tomada": acao_tomada,
        "gravidade": gravidade,
        "situacao_subestacao": situacao_subestacao
    }
    response = requests.post(f"{API_URL}/chamado/", data=payload)
    return response.json()
