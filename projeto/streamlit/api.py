import requests

API_URL = "https://trabalhorpa-api.onrender.com"

def obter_chamados():
    try:
        resp = requests.get(f"{API_URL}/chamados/", timeout=10)
        resp.raise_for_status()
        return resp.json() or []
    except requests.exceptions.RequestException:
        return []

def validar_chamado_api(chamado_id: int, validar: bool = True):
    try:
        params = {"validar": str(validar).lower()}  
        resp = requests.put(
            f"{API_URL}/chamado/{chamado_id}/validar",
            params=params,
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}

def remover_chamado_por_id_api(chamado_id: int):
    try:
        resp = requests.delete(f"{API_URL}/chamado/{chamado_id}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}

def criar_chamado_api(local_subestacao: str, nome_tecnico: str, acao_tomada: str, gravidade: str, situacao_subestacao: str):
    payload = {
        "local_subestacao": local_subestacao,
        "nome_tecnico": nome_tecnico,
        "acao_tomada": acao_tomada,
        "gravidade": gravidade,
        "situacao_subestacao": situacao_subestacao
    }
    try:
        resp = requests.post(f"{API_URL}/chamado/", data=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}
