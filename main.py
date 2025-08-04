from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from assets import AssetEnum, AssetContractEnum
from wallet_utils import (
    create_wallet, build_and_send_transaction,
    consultar_saldo_e_endereco, saldo_assets,
    transacoes_recebidas
)

app = FastAPI()

class WalletCreateRequest(BaseModel):
    seed_phrase: Optional[List[str]] = None

class TransactionRequest(BaseModel):
    seed_phrase: List[str]
    asset: str
    recipient_address: str
    amount: int

class AddressRequest(BaseModel):
    seed_phrase: List[str]
    index: int

class SeedRequest(BaseModel):
    seed_phrase: List[str]



@app.post("/create_wallet")
def create_wallet_endpoint(data: WalletCreateRequest):
    try:
        wallet, seed = create_wallet(data.seed_phrase)
        return {"message": "Carteira criada com sucesso", "seed": seed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_transaction")
def send_transaction(data: TransactionRequest):
    try:
        wallet, _ = create_wallet(data.seed_phrase)

        # pega o asset_id correto
        asset_id = AssetContractEnum[data.asset.name]

        txid = build_and_send_transaction(wallet, asset_id, data.recipient_address, data.amount)
        return {"message": "Transação enviada", "txid": txid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/address")
def get_address(data: AddressRequest):
    try:
        address = consultar_saldo_e_endereco(data.seed_phrase, data.index)
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/saldo")
def get_balance(data: SeedRequest):
    try:
        saldo = saldo_assets(data.seed_phrase)
        return {"saldo": saldo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transacoes")
def get_received_transactions(data: SeedRequest):
    try:
        txs = transacoes_recebidas(data.seed_phrase)
        return {"transacoes_recebidas": txs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
