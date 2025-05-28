from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI()

# Dados extraídos do PDF (poderiam ser carregados de um arquivo .json, se preferir)
dados_imoveis: Dict[str, Dict] = {
    "4969/3": {
        "id": "4969/3",
        "endereco": None,
        "locatario": "Sergio Pacheco Mendes Junior",
        "valor_aluguel": None,
        "taxa_administracao": "-544.67",
        "total_para_repasse": "5172.32",
        "pagamento_realizado": False
    },
    "548/4": {
        "id": "548/4",
        "endereco": None,
        "locatario": "Hunter Douglas do Brasil Ltda",
        "valor_aluguel": None,
        "taxa_administracao": "-280.00",
        "total_para_repasse": "2597.59",
        "pagamento_realizado": False
    },
    "15445/1": {
        "id": "15445/1",
        "endereco": None,
        "locatario": "Bárbara Letícia Arndt",
        "valor_aluguel": None,
        "taxa_administracao": "-208.00",
        "total_para_repasse": "2392.00",
        "pagamento_realizado": True
    },
    "15439/1": {
        "id": "15439/1",
        "endereco": None,
        "locatario": "Guilherme Campestrini",
        "valor_aluguel": None,
        "taxa_administracao": "-232.00",
        "total_para_repasse": "2668.00",
        "pagamento_realizado": True
    },
    "15628/1": {
        "id": "15628/1",
        "endereco": None,
        "locatario": "Janaina Rodrigues Kemper",
        "valor_aluguel": None,
        "taxa_administracao": "-248.00",
        "total_para_repasse": "2852.00",
        "pagamento_realizado": True
    }
    # Pode adicionar mais aqui se quiser
}

@app.get("/imovel/{imovel_id}")
def get_imovel(imovel_id: str):
    imovel = dados_imoveis.get(imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return imovel
