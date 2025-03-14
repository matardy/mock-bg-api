from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, clientes, cuentas, movimientos, citas
from .db.init_db import init_db

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos
@app.on_event("startup")
async def startup_event():
    init_db()

# Incluir las rutas
app.include_router(auth.router, tags=["Autenticación"])
app.include_router(clientes.router, tags=["Clientes"])
app.include_router(cuentas.router, tags=["Cuentas"])
app.include_router(movimientos.router, tags=["Movimientos"])
app.include_router(citas.router, tags=["Citas Médicas"])

@app.get("/docs")
async def get_docs():
    return {"message": "API documentation available"}

@app.get("/")
async def root():
    return {"message": "API Mock Bancaria con Citas Médicas"}