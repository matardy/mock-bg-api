from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Cargar datos desde archivos JSON
def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

# Cargamos los datos al iniciar la app
try:
    clientes = load_data("data/clientes.json")
    movimientos = load_data("data/movimientos.json")
    datos_posicionales = load_data("data/posicion_consolidada.json")
except FileNotFoundError:
    raise FileNotFoundError("Uno de los archivos JSON no se encuentra en el directorio especificado.")


try:
    clientes = load_data("data/clientes.json")  # Asegúrate de que clientes.json está en la misma carpeta que tu script
    movimientos = load_data("data/movimientos.json")
    datos_posicionales = load_data("data/posicion_consolidada.json")
except FileNotFoundError:
    raise FileNotFoundError("Uno de los archivos JSON no se encuentra en el directorio especificado.")
except json.JSONDecodeError:
    raise Exception("Error al decodificar el JSON, verifica la estructura del archivo.")

@app.get("/cuentas/{identificacion}")
async def obtener_cuentas(identificacion: str):
    cuentas_usuario = [cuenta for cuenta in datos_posicionales['cuentas'] if cuenta['identificacion'] == identificacion]
    if not cuentas_usuario:
        raise HTTPException(status_code=404, detail="No se encontraron cuentas para el usuario especificado.")
    return cuentas_usuario

@app.get("/clientes/{identificacion}")
async def obtener_cliente(identificacion: str):
    for cliente in clientes:
        if cliente['identificacion'] == identificacion:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.get("/movimientos/{mtcuenta}")
async def obtener_movimientos_por_cuenta(mtcuenta: int, limit: int = 10):
    movimientos_cuenta = [mov for mov in movimientos if mov["mtcuenta"] == mtcuenta]
    return movimientos_cuenta[:limit]

@app.get("/tarjetas/{identificacion}")
async def obtener_tarjetas(identificacion: str, ultimo_cuatro: str = None):
    tarjetas = [tarjeta for tarjeta in datos_posicionales['tarjetas'] if tarjeta['identificacion'] == identificacion]
    if ultimo_cuatro:
        tarjetas = [tarjeta for tarjeta in tarjetas if tarjeta['tarjeta'].endswith(ultimo_cuatro)]
    return tarjetas

@app.get("/seguros/{identificacion}")
async def obtener_seguros(identificacion: str):
    seguros = [seguro for seguro in datos_posicionales['seguros'] if seguro['identificacion'].strip() == identificacion]
    return seguros
