from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar datos desde archivos JSON
def load_data(archivo):
    with open(archivo, "r") as file:
        return json.load(file)["data"]

# Guardar datos en archivos JSON
def save_data(archivo, data):
    with open(archivo, "w") as file:
        json.dump({"data": data}, file, indent=4)

# Cargamos los datos al iniciar la app
try:
    clientes = load_data("data/clientes.json")
    movimientos = load_data("data/movimientos.json")
    datos_posicionales = load_data("data/posicion_consolidada.json")
except FileNotFoundError:
    raise FileNotFoundError("Uno de los archivos JSON no se encuentra en el directorio especificado.")
except json.JSONDecodeError:
    raise Exception("Error al decodificar el JSON, verifica la estructura del archivo.")

class Cliente(BaseModel):
    id: int
    identificacion: str
    tipoIdentificacion: str
    nombres: str
    direccion1: str
    telefono1: int
    correoElectronico: str
    telefonoCelular: str
    segmentoEstrategico: str
    calificacion: str
    estado: str
    sexo: str
    fechaNacimiento: str
    oficial: str
    clienteDesde: str
    clave_cajero: str  # Nueva propiedad para la clave del cajero

class Movimiento(BaseModel):
    secuencia: str
    tipoMoneda: str
    fechaTransaccion: str
    tipoMovimiento: str
    descripcionMovimiento: str
    documento: str
    referencia: str
    montoTransaccion: float
    montoDisponible: float
    montoConfirmar: float
    agencia: str
    signo: str
    mtcuenta: int
    identificacion: str

class Tarjeta(BaseModel):
    cuentas: int
    tarjeta: str
    principalAdicional: str
    identificacion: str
    fchExpiracion: str
    fchApertura: str
    tarjetas: int
    cupo: float
    disponible: float

class Seguro(BaseModel):
    identificacion: str
    descripcionTipo: str
    numeroPoliza: str
    valorAsegurado: float
    fechaVigencia: str
    fechaContratacion: str
    fechaVencimiento: str
    primaTotal: float
    descripcionTipoPlazo: str
    primaMensual: float
    estado: str
    descripcionEstado: str

class Cuenta(BaseModel):
    masa: str
    tip: str
    mtcuenta: int
    clkRelacion: str
    concesion: int
    vencimiento: int
    saldoTotal: float
    efectivo: float
    valorPendiente: float
    porConfirmar: float
    identificacion: str

class Autenticacion(BaseModel):
    identificacion: str
    clave_cajero: str

class Observaciones(BaseModel):
    identificacion: str
    tag: str
    observacion: str

@app.post("/clientes")
async def agregar_cliente(cliente: Cliente):
    # Verificar si el cliente ya existe
    for c in clientes:
        if c["identificacion"] == cliente.identificacion:
            raise HTTPException(status_code=400, detail="Cliente ya existe")
    clientes.append(cliente.dict())
    save_data("data/clientes.json", clientes)
    return {"message": "Cliente agregado con éxito"}

@app.post("/movimientos")
async def agregar_movimiento(movimiento: Movimiento):
    movimientos.append(movimiento.dict())
    save_data("data/movimientos.json", movimientos)
    return {"message": "Movimiento agregado con éxito"}

@app.post("/tarjetas")
async def agregar_tarjeta(tarjeta: Tarjeta):
    datos_posicionales['tarjetas'].append(tarjeta.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Tarjeta agregada con éxito"}

@app.post("/seguros")
async def agregar_seguro(seguro: Seguro):
    datos_posicionales['seguros'].append(seguro.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Seguro agregado con éxito"}

@app.post("/cuentas")
async def agregar_cuenta(cuenta: Cuenta):
    datos_posicionales['cuentas'].append(cuenta.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Cuenta agregada con éxito"}

@app.post("/observaciones")
async def agregar_observacion(observacion: Observaciones):
    datos_posicionales['observaciones'].append(observacion.dict())
    save_data("data/posicion_consolidada.json", datos_posicionales)
    return {"message": "Observación agregada con éxito"}

@app.post("/autenticar")
async def autenticar_usuario(autenticacion: Autenticacion):
    for cliente in clientes:
        if cliente["identificacion"] == autenticacion.identificacion and cliente.get("clave_cajero") == autenticacion.clave_cajero:
            return {"autenticado": True}
    return {"autenticado": False}

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

@app.get("/observaciones/{identificacion}")
async def obtener_observaciones(identificacion: str):
    observaciones = [obs for obs in datos_posicionales['observaciones'] if obs['identificacion'].strip() == identificacion]
    return observaciones