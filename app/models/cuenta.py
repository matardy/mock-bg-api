from pydantic import BaseModel

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

class Observaciones(BaseModel):
    identificacion: str
    tag: str
    observacion: str