from fastapi import APIRouter, HTTPException
import json
from ..models.cuenta import Cuenta, Tarjeta, Seguro, Observaciones

router = APIRouter()

def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

def save_data(archivo, data):
    with open(archivo, "w") as file:
        json.dump({"data": data}, file, indent=4)

try:
    datos_posicionales = load_data("data/posicion_consolidada.json")
except:
    datos_posicionales = {"cuentas": [], "tarjetas": [], "seguros": [], "observaciones": []}

@router.post("/cuentas")
async def agregar_cuenta(cuenta: Cuenta):
    datos_posicionales["cuentas"].append(cuenta.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Cuenta agregada con éxito"}

@router.get("/cuentas/{identificacion}")
async def obtener_cuentas(identificacion: str):
    cuentas_usuario = [cuenta for cuenta in datos_posicionales["cuentas"] if cuenta["identificacion"] == identificacion]
    if not cuentas_usuario:
        raise HTTPException(status_code=404, detail="No se encontraron cuentas para el usuario especificado.")
    return cuentas_usuario

@router.post("/tarjetas")
async def agregar_tarjeta(tarjeta: Tarjeta):
    datos_posicionales["tarjetas"].append(tarjeta.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Tarjeta agregada con éxito"}

@router.get("/tarjetas/{identificacion}")
async def obtener_tarjetas(identificacion: str, ultimo_cuatro: str = None):
    tarjetas = [tarjeta for tarjeta in datos_posicionales["tarjetas"] if tarjeta["identificacion"] == identificacion]
    if ultimo_cuatro:
        tarjetas = [tarjeta for tarjeta in tarjetas if tarjeta["tarjeta"].endswith(ultimo_cuatro)]
    return tarjetas

@router.post("/seguros")
async def agregar_seguro(seguro: Seguro):
    datos_posicionales["seguros"].append(seguro.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Seguro agregado con éxito"}

@router.get("/seguros/{identificacion}")
async def obtener_seguros(identificacion: str):
    seguros = [seguro for seguro in datos_posicionales["seguros"] if seguro["identificacion"].strip() == identificacion]
    return seguros

@router.post("/observaciones")
async def agregar_observacion(observacion: Observaciones):
    datos_posicionales["observaciones"].append(observacion.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Observación agregada con éxito"}

@router.get("/observaciones/{identificacion}")
async def obtener_observaciones(identificacion: str):
    observaciones = [obs for obs in datos_posicionales["observaciones"] if obs["identificacion"].strip() == identificacion]
    return observaciones