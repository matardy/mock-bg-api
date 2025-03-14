from fastapi import APIRouter, HTTPException
import json
from ..models.cuenta import Movimiento

router = APIRouter()

def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

def save_data(archivo, data):
    with open(archivo, "w") as file:
        json.dump({"data": data}, file, indent=4)

try:
    movimientos = load_data("data/movimientos.json")
except:
    movimientos = []

@router.post("/movimientos")
async def agregar_movimiento(movimiento: Movimiento):
    movimientos.append(movimiento.dict())
    save_data("data/movimientos.json", movimientos)
    return {"message": "Movimiento agregado con éxito"}

@router.get("/movimientos/{mtcuenta}")
async def obtener_movimientos_por_cuenta(mtcuenta: int, limit: int = 10):
    movimientos_cuenta = [mov for mov in movimientos if mov["mtcuenta"] == mtcuenta]
    return movimientos_cuenta[:limit]