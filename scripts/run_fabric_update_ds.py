import requests
import os

# ⚙️ CONFIGURACIÓN
TENANT_ID     = os.environ.get('FABRIC_TENANT_ID')
CLIENT_ID     = os.environ.get('FABRIC_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FABRIC_CLIENT_SECRET')
AUTH_URL      = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
WORKSPACE_ID  = os.environ.get('FABRIC_WORKSPACE_ID') 
CLOUD_CONNECTION_ID = os.environ.get('FABRIC_CLOUD_CONNECTION_ID') 
IS_ONLY_UPDATE = os.environ.get('IS_ONLY_UPDATE')  

def get_access_token(client_id, client_secret, auth_url):
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(auth_url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error obteniendo token: {response.text}")

def list_datasets_ids(workspace_id, token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        datasets = response.json().get("value", [])  # lista de datasets
        ids = [ds["id"] for ds in datasets]        
        return ids
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []
      
def serviceprincipal_takeOver(workspace_id, dataset_id, token):
    # Dataset Take Over
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/Default.TakeOver"
    
    # Cabeceras con autenticación
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Enviar la petición POST
    response = requests.post(url, headers=headers)

    # Ver respuesta
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Take Over realizado al dataset: {dataset_id}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

def set_cloudConnection_to_Dataset(workspace_id, dataset_id, cloud_connection_id, token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/Default.BindToGateway"
    
    # Cabeceras con autenticación
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Payload con los detalles del shortcut
    payload = {  
                "gatewayObjectId": f"{dataset_id}",
                "datasourceObjectIds": [ f"{cloud_connection_id}" ]
            }

    # Enviar la petición POST
    response = requests.post(url, json=payload, headers=headers)

    # Ver respuesta
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Cloud Connections establecidos en: {dataset_id}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

# Obtenemos el token inicial
print(CLIENT_ID, CLIENT_SECRET,AUTH_URL)
token = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL) 

# En base al Workspace, obtenemos los datasets
ds = list_datasets_ids(WORKSPACE_ID, token)

for dataset in ds:
    print(f"⚙️ Procesando dataset ID: {dataset}")
    if IS_ONLY_UPDATE == "False": # Evitamos una llamada si es solo actualización del Cloud Connection.
        # Establecemos el Service Principal como propietario del dataset. 
        serviceprincipal_takeOver(workspace_id=WORKSPACE_ID, dataset_id=dataset, token=token)
    
    # Asociamos el Cloud Connection al dataset
    set_cloudConnection_to_Dataset(workspace_id=WORKSPACE_ID, dataset_id=dataset, cloud_connection_id=CLOUD_CONNECTION_ID, token=token)
