import requests
from datetime import datetime, timedelta
import json
import time

# Cambiar a URL local para pruebas
base_url = "http://127.0.0.1:8000"

print("=== PRUEBAS DE API BANCARIA CON CITAS MÉDICAS ===\n")

# PRUEBAS DE FUNCIONALIDAD BÁSICA
def check_api_docs():
    print("\n>> Verificando documentación de la API...")
    response = requests.get(f"{base_url}/docs")
    is_available = response.status_code == 200
    print(f"API documentation available: {is_available}")
    return is_available

# PRUEBAS DE CLIENTES
def add_client():
    print("\n>> Agregando nuevo cliente...")
    new_client = {
        "id": 1018469,
        "identificacion": "0925035703",
        "tipoIdentificacion": "C",
        "nombres": "ANA MARIA LOPEZ",
        "direccion1": "AVENIDA PRINCIPAL 456",
        "telefono1": 98765432,
        "correoElectronico": "ana.lopez@example.com",
        "telefonoCelular": "0976543210",
        "segmentoEstrategico": "PR",
        "calificacion": "A",
        "estado": "1",
        "sexo": "F",
        "fechaNacimiento": "1992-05-15",
        "oficial": "EWA",
        "clienteDesde": "2018-06-20",
        "clave_cajero": "9876"
    }
    response = requests.post(f"{base_url}/clientes", json=new_client)
    print(f"Add client status code: {response.status_code}")
    print(f"Add client response: {response.json()}")
    return response.status_code, response.json()

def get_client_details(identificacion="0925035703"):
    print(f"\n>> Obteniendo detalles del cliente {identificacion}...")
    response = requests.get(f"{base_url}/clientes/{identificacion}")
    print(f"Get client details status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Client details: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error response: {response.json()}")
    return response.status_code, response.json()

def authenticate_user(identificacion="0925035703", clave="9876"):
    print(f"\n>> Autenticando usuario {identificacion}...")
    credentials = {
        "identificacion": identificacion,
        "clave_cajero": clave
    }
    response = requests.post(f"{base_url}/autenticar", json=credentials)
    print(f"Authentication status code: {response.status_code}")
    print(f"Authentication response: {response.json()}")
    return response.status_code, response.json()

# PRUEBAS DE CUENTAS Y MOVIMIENTOS
def add_account(identificacion="0925035703"):
    print(f"\n>> Agregando cuenta para cliente {identificacion}...")
    nueva_cuenta = {
        "masa": "PAS",
        "tip": "AH",
        "mtcuenta": 15466142,
        "clkRelacion": "TIT",
        "concesion": 20230515,
        "vencimiento": 0,
        "saldoTotal": 1500.50,
        "efectivo": 1500.50,
        "valorPendiente": 0,
        "porConfirmar": 0,
        "identificacion": identificacion
    }
    response = requests.post(f"{base_url}/cuentas", json=nueva_cuenta)
    print(f"Add account status code: {response.status_code}")
    print(f"Add account response: {response.json()}")
    return response.status_code, response.json()

def get_account_details(identificacion="0925035703"):
    print(f"\n>> Obteniendo cuentas del cliente {identificacion}...")
    response = requests.get(f"{base_url}/cuentas/{identificacion}")
    print(f"Get accounts status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Accounts found: {len(response.json())}")
        if len(response.json()) > 0:
            print(f"First account: {json.dumps(response.json()[0], indent=2)}")
    else:
        print(f"Error response: {response.json()}")
    return response.status_code, response.json()

def add_movement():
    print("\n>> Agregando nuevo movimiento...")
    new_movement = {
        "secuencia": "1",
        "tipoMoneda": "USD",
        "fechaTransaccion": datetime.now().strftime("%Y-%m-%d"),
        "tipoMovimiento": "N/D",
        "descripcionMovimiento": "Test Movement",
        "documento": "1234",
        "referencia": "Test Ref",
        "montoTransaccion": 100.0,
        "montoDisponible": 100.0,
        "montoConfirmar": 100.0,
        "agencia": "MATRIZ",
        "signo": "-",
        "mtcuenta": 15466142,
        "identificacion": "0925035703"
    }
    response = requests.post(f"{base_url}/movimientos", json=new_movement)
    print(f"Add movement status code: {response.status_code}")
    print(f"Add movement response: {response.json()}")
    return response.status_code, response.json()

def get_movements(mtcuenta=15466142):
    print(f"\n>> Obteniendo movimientos de la cuenta {mtcuenta}...")
    response = requests.get(f"{base_url}/movimientos/{mtcuenta}?limit=5")
    print(f"Get movements status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Movements found: {len(response.json())}")
        if len(response.json()) > 0:
            print(f"Latest movement: {json.dumps(response.json()[0], indent=2)}")
    return response.status_code, response.json()

# PRUEBAS DE CITAS MÉDICAS
def list_doctors():
    print("\n>> Listando doctores disponibles...")
    response = requests.get(f"{base_url}/doctores")
    print(f"List doctors status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Doctors found: {len(response.json())}")
        if len(response.json()) > 0:
            for doctor in response.json()[:2]:  # Mostrar solo los primeros 2 doctores
                print(f"- {doctor['nombre']} ({doctor['especialidad']})")
    return response.status_code, response.json()

def check_availability():
    print("\n>> Consultando disponibilidad de citas...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    filtros = {
        "fecha": tomorrow
    }
    response = requests.post(f"{base_url}/disponibilidad", json=filtros)
    print(f"Check availability status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Available slots found: {len(response.json())}")
        if len(response.json()) > 0:
            first_slot = response.json()[0]
            print(f"Example slot: {first_slot['doctor']} on {first_slot['fecha']} at {first_slot['hora_inicio']}")
            return response.status_code, response.json(), first_slot
    return response.status_code, response.json(), None

def schedule_appointment(identificacion="0925035703", slot=None):
    print(f"\n>> Agendando cita para el paciente {identificacion}...")
    
    if not slot:
        print("No se encontró disponibilidad para agendar una cita.")
        return None, None
    
    nueva_cita = {
        "paciente_id": identificacion,
        "doctor_id": slot["doctor_id"],
        "fecha": slot["fecha"],
        "hora": slot["hora_inicio"],
        "motivo": "Consulta de rutina"
    }
    
    response = requests.post(f"{base_url}/citas", json=nueva_cita)
    print(f"Schedule appointment status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Appointment scheduled: {json.dumps(response.json(), indent=2)}")
        return response.status_code, response.json()
    else:
        print(f"Error response: {response.json()}")
        return response.status_code, response.json()

def get_patient_appointments(identificacion="0925035703"):
    print(f"\n>> Consultando citas del paciente {identificacion}...")
    response = requests.get(f"{base_url}/citas/paciente/{identificacion}")
    print(f"Get appointments status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Appointments found: {len(response.json())}")
        if len(response.json()) > 0:
            print(f"First appointment: {json.dumps(response.json()[0], indent=2)}")
            return response.status_code, response.json(), response.json()[0]["id"] if len(response.json()) > 0 else None
    return response.status_code, response.json(), None

def get_appointment_details(cita_id):
    print(f"\n>> Obteniendo detalles de la cita {cita_id}...")
    response = requests.get(f"{base_url}/citas/{cita_id}")
    print(f"Get appointment details status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Appointment details: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error response: {response.json()}")
    return response.status_code, response.json()

def cancel_appointment(cita_id):
    print(f"\n>> Cancelando cita {cita_id}...")
    response = requests.put(f"{base_url}/citas/{cita_id}/cancelar")
    print(f"Cancel appointment status code: {response.status_code}")
    print(f"Cancel appointment response: {response.json()}")
    return response.status_code, response.json()

# EJECUCIÓN DE PRUEBAS
print("1. PRUEBAS BÁSICAS")
check_api_docs()

print("\n2. PRUEBAS DE CLIENTES")
add_client()
get_client_details("0925035703")
authenticate_user()

print("\n3. PRUEBAS DE CUENTAS Y MOVIMIENTOS")
add_account()
get_account_details()
add_movement()
get_movements()

print("\n4. PRUEBAS DE CITAS MÉDICAS")
doctors_status, doctors_data = list_doctors()
availability_status, availability_data, available_slot = check_availability()

if available_slot:
    appointment_status, appointment_data = schedule_appointment(slot=available_slot)
    time.sleep(1)  # Pequeño retraso para asegurar que la cita esté guardada
    
    patient_appts_status, patient_appts_data, appointment_id = get_patient_appointments()
    
    if appointment_id:
        get_appointment_details(appointment_id)
        cancel_appointment(appointment_id)
        # Verificar que la cita se canceló correctamente
        time.sleep(1)
        get_appointment_details(appointment_id)

print("\n=== PRUEBAS COMPLETADAS ===")