import requests

base_url = "https://mock-bg-api.onrender.com"

# Function to check the API documentation
def check_api_docs():
    response = requests.get(f"{base_url}/docs")
    return response.status_code == 200

# Function to add a new client
def add_client():
    new_client = {
        "id": 1018468,
        "identificacion": "0925035702",
        "tipoIdentificacion": "C",
        "nombres": "JUAN PEREZ",
        "direccion1": "CALLE FALSA 123",
        "telefono1": 12345678,
        "correoElectronico": "juan.perez@example.com",
        "telefonoCelular": "0987654321",
        "segmentoEstrategico": "PR",
        "calificacion": "A",
        "estado": "1",
        "sexo": "M",
        "fechaNacimiento": "1990-01-01",
        "oficial": "EWA",
        "clienteDesde": "2020-01-01",
        "clave_cajero": "5678"
    }
    response = requests.post(f"{base_url}/clientes", json=new_client)
    return response.status_code, response.json()

# Function to authenticate the user
def authenticate_user():
    credentials = {
        "identificacion": "0925035702",
        "clave_cajero": "5678"
    }
    response = requests.post(f"{base_url}/autenticar", json=credentials)
    return response.status_code, response.json()

# Function to get client details
def get_client_details():
    response = requests.get(f"{base_url}/clientes/0925035702")
    return response.status_code, response.json()

# Function to add a new movement
def add_movement():
    new_movement = {
        "secuencia": "1",
        "tipoMoneda": "USD",
        "fechaTransaccion": "2024-06-01",
        "tipoMovimiento": "N/D",
        "descripcionMovimiento": "Test Movement",
        "documento": "1234",
        "referencia": "Test Ref",
        "montoTransaccion": 100.0,
        "montoDisponible": 100.0,
        "montoConfirmar": 100.0,
        "agencia": "MATRIZ",
        "signo": "-",
        "mtcuenta": 15466141,
        "identificacion": "0925035702"
    }
    response = requests.post(f"{base_url}/movimientos", json=new_movement)
    return response.status_code, response.json()

# Function to get movements for a specific account
def get_movements():
    response = requests.get(f"{base_url}/movimientos/15466141?limit=10")
    return response.status_code, response.json()

# Function to get account details
def get_account_details():
    response = requests.get(f"{base_url}/cuentas/0925035702")
    return response.status_code, response.json()

# Run the validations
docs_available = check_api_docs()
print("API documentation available:", docs_available)

client_status_code, client_response = add_client()
print("Add client status code:", client_status_code)
print("Add client response:", client_response)

auth_status_code, auth_response = authenticate_user()
print("Authenticate user status code:", auth_status_code)
print("Authenticate user response:", auth_response)

client_details_status_code, client_details_response = get_client_details()
print("Get client details status code:", client_details_status_code)
print("Get client details response:", client_details_response)

movement_status_code, movement_response = add_movement()
print("Add movement status code:", movement_status_code)
print("Add movement response:", movement_response)

movements_status_code, movements_response = get_movements()
print("Get movements status code:", movements_status_code)
print("Get movements response:", movements_response)

account_details_status_code, account_details_response = get_account_details()
print("Get account details status code:", account_details_status_code)
print("Get account details response:", account_details_response)
