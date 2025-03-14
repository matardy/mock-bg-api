from fastapi import APIRouter, HTTPException
import json
from ..models.cliente import Cliente

router = APIRouter()

def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

def save_data(archivo, data):
    with open(archivo, "w") as file:
        json.dump({"data": data}, file, indent=4)

clientes = load_data("data/clientes.json")

@router.post("/clientes")
async def agregar_cliente(cliente: Cliente):
    # Verificar si el cliente ya existe
    for c in clientes:
        if c["identificacion"] == cliente.identificacion:
            raise HTTPException(status_code=400, detail="Cliente ya existe")
    clientes.append(cliente.dict())
    save_data("data/clientes.json", clientes)
    return {"message": "Cliente agregado con éxito"}

@router.get("/clientes/{identificacion}")
async def obtener_cliente(identificacion: str):
    for cliente in clientes:
        if cliente["identificacion"] == identificacion:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")