# 🔄 run_fabric_update_ds.py - Gestión de Datasets y Conexiones

## 📋 Propósito

Este script se encarga de **configurar y mantener los datasets** de Power BI en el workspace de Fabric. Realiza dos funciones críticas: toma de control (takeover) de datasets por parte del Service Principal y configuración de conexiones a fuentes de datos.

## 🏗️ Arquitectura del Script

### 1. **Configuración y Autenticación**

```python
# Configuración desde variables de entorno
TENANT_ID = os.environ.get('FABRIC_TENANT_ID')
CLIENT_ID = os.environ.get('FABRIC_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FABRIC_CLIENT_SECRET')
AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
```

**¿Por qué OAuth2?**: Utiliza el flujo `client_credentials` para autenticación sin intervención del usuario, ideal para procesos automatizados.

### 2. **Función: `get_access_token()`**

```python
def get_access_token(client_id, client_secret, auth_url):
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }
```

**¿Qué hace?**: 
- Solicita un token de acceso a la API de Power BI
- Utiliza el scope específico para operaciones de Power BI
- El token es válido por 1 hora aproximadamente

**Manejo de Errores**:
- Valida el código de respuesta HTTP
- Lanza excepción si la autenticación falla
- Incluye el texto del error para debugging

### 3. **Función: `list_datasets_ids()`**

```python
def list_datasets_ids(workspace_id, token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
```

**¿Qué hace?**:
- Obtiene todos los datasets del workspace especificado
- Extrae únicamente los IDs para procesamiento posterior
- Utiliza la Power BI REST API v1.0

**Endpoint utilizado**: `GET /groups/{groupId}/datasets`

### 4. **Función: `serviceprincipal_takeOver()`**

```python
def serviceprincipal_takeOver(workspace_id, dataset_id, token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/Default.TakeOver"
```

**¿Qué hace?**:
- **Transfiere la propiedad** del dataset al Service Principal
- Permite que el SP pueda gestionar completamente el dataset
- Necesario para operaciones de actualización y configuración

**¿Por qué es importante?**:
- Sin takeover, el SP no puede modificar datasets creados por usuarios
- Habilita la gestión automatizada de credenciales
- Permite actualizaciones programadas sin intervención manual

**Endpoint utilizado**: `POST /groups/{groupId}/datasets/{datasetId}/Default.TakeOver`

### 5. **Función: `set_cloudConnection_to_Dataset()`**

```python
def set_cloudConnection_to_Dataset(workspace_id, dataset_id, cloud_connection_id, token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/Default.BindToGateway"
    
    payload = {  
        "gatewayObjectId": f"{dataset_id}",
        "datasourceObjectIds": [ f"{cloud_connection_id}" ]
    }
```

**¿Qué hace?**:
- **Asocia una conexión en la nube** al dataset
- Configura las credenciales para acceso a fuentes de datos
- Utiliza el endpoint de binding a gateway (aunque sea cloud connection)

**Parámetros del Payload**:
- `gatewayObjectId`: ID del gateway (en este caso, el dataset mismo)
- `datasourceObjectIds`: Array con IDs de las conexiones a usar

**Endpoint utilizado**: `POST /groups/{groupId}/datasets/{datasetId}/Default.BindToGateway`

## 🔄 Flujo de Ejecución Principal

```python
# 1. Obtener token de acceso
token = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL)

# 2. Listar todos los datasets del workspace
ds = list_datasets_ids(WORKSPACE_ID, token)

# 3. Procesar cada dataset individualmente
for dataset in ds:
    if IS_ONLY_UPDATE == "False":
        # 3a. Tomar control del dataset
        serviceprincipal_takeOver(workspace_id=WORKSPACE_ID, dataset_id=dataset, token=token)
    
    # 3b. Configurar conexión en la nube
    set_cloudConnection_to_Dataset(workspace_id=WORKSPACE_ID, dataset_id=dataset, cloud_connection_id=CLOUD_CONNECTION_ID, token=token)
```

## 🎯 Dos Modos de Operación

### **Modo Completo (`IS_ONLY_UPDATE = "False"`)**
1. ✅ Ejecuta takeover de datasets
2. ✅ Configura cloud connections
3. **Cuándo usar**: Despliegue inicial o cuando hay nuevos datasets

### **Modo Actualización (`IS_ONLY_UPDATE = "True"`)**
1. ❌ Omite takeover (ya realizado anteriormente)
2. ✅ Solo actualiza cloud connections
3. **Cuándo usar**: Actualización de credenciales o cambio de conexiones

## 📊 Variables de Entorno Utilizadas

| Variable | Propósito | Valor de Ejemplo |
|----------|-----------|------------------|
| `FABRIC_CLIENT_ID` | ID del Service Principal | `12345678-abcd-1234-efgh-123456789012` |
| `FABRIC_CLIENT_SECRET` | Secret del Service Principal | `secretValue123` |
| `FABRIC_TENANT_ID` | ID del tenant de Azure | `87654321-1234-5678-9012-210987654321` |
| `FABRIC_WORKSPACE_ID` | ID del workspace objetivo | `workspace-guid-here` |
| `FABRIC_CLOUD_CONNECTION_ID` | ID de la conexión configurada | `connection-guid-here` |
| `IS_ONLY_UPDATE` | Controla el modo de ejecución | `"True"` o `"False"` |

## 🔒 Permisos y Seguridad

### **Permisos Requeridos del Service Principal**

1. **En Azure AD**:
   - `Application.ReadWrite.All` (para gestionar aplicaciones)

2. **En Power BI**:
   - **Admin** o **Member** del workspace
   - Habilitado en configuración de administración de Power BI

3. **En Fabric**:
   - Permisos de **Contributor** o superior en el workspace

### **Consideraciones de Seguridad**

- Los secrets se almacenan de forma segura en GitHub Secrets
- Los tokens tienen tiempo de vida limitado (1 hora)
- Las operaciones se registran para auditoría
- Solo se procesan datasets del workspace especificado

## ⚠️ Manejo de Errores Comunes

### **Error 401 - No Autorizado**
```
❌ Error 401: Unauthorized
```
**Causa**: Token expirado o permisos insuficientes
**Solución**: Verificar credenciales del Service Principal

### **Error 404 - No Encontrado**
```
❌ Error 404: Dataset not found
```
**Causa**: Dataset ID incorrecto o eliminado
**Solución**: Verificar que el dataset existe en el workspace

### **Error 403 - Prohibido**
```
❌ Error 403: Forbidden
```
**Causa**: El Service Principal no tiene permisos suficientes
**Solución**: Revisar configuración de permisos en Power BI Admin

## 🔗 APIs y Documentación

- [Power BI REST API - Datasets](https://docs.microsoft.com/en-us/rest/api/power-bi/datasets)
- [Dataset Takeover](https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/take-over-in-group)
- [Gateway Binding](https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/bind-to-gateway-in-group)
- [Power BI Service Principal](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal)

---

*Este script se ejecuta **antes y después** del despliegue de artefactos para garantizar la configuración correcta de los datasets.*