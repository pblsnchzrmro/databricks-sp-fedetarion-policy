# Databricks SP Federation Policy

Herramienta de línea de comandos para intercambiar un JWT emitido por GitHub por un token de acceso de Databricks utilizando el flujo **OAuth Token Exchange**. Después del anje opcionalmente se valida el token contra el endpoint SCIM `Me` para verificar que la federación está configurada correctamente.

## Requisitos previos

- Python 3.8 o superior.
- Dependencias de Python: [`requests`](https://pypi.org/project/requests/).
- Acceso a un *Service Principal* de Databricks configurado para federación con el workspace de Databricks.

## Instalación

1. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   Si no cuentas con un `requirements.txt`, instala directamente `requests`:
   ```bash
   pip install requests
   ```

## Configuración

El script busca por defecto un archivo `config.json` en el directorio raíz del proyecto. Debe contener los siguientes campos:

```json
{
  "databricks_host": "https://<tu-workspace>.azuredatabricks/cloud.databricks.net",
  "databricks_client_id": "<client-id-del-service-principal>",
  "jwt": "<jwt-federado-generado-por-azure-ad>"
}
```

- `databricks_host`: URL base del workspace de Databricks (sin la barra final).
- `databricks_client_id`: Identificador del *Service Principal* configurado en Databricks.
- `jwt`: Token JWT emitido por Azure AD usando las políticas de federación.

Si deseas utilizar otro nombre o ubicación para el archivo de configuración, ajusta la llamada a `load_config` en [`src/main.py`](src/main.py) para que reciba la ruta deseada.

## Uso

Ejecuta el script principal:

```bash
python src/main.py
```

Durante la ejecución verás en consola:

1. La solicitud de intercambio de tokens hacia `/oidc/v1/token` con el estado HTTP resultante.
2. La respuesta JSON devuelta por Databricks. Si existe un `access_token`, se imprimirá un mensaje confirmando la obtención exitosa.
3. Una validación opcional contra el endpoint SCIM `/api/2.0/preview/scim/v2/Me`. El contenido de la respuesta te permitirá confirmar que el token tiene los permisos esperados.

Si el intercambio falla (p.ej. por credenciales incorrectas) el script finalizará con un mensaje de error y un código de salida distinto de cero.

## Resolución de problemas

- **401 Unauthorized**: Comprueba que el JWT sea válido y que el `client_id` coincida con el registrado en Databricks.
- **400 Bad Request**: Asegúrate de que los parámetros enviados en `config.json` tengan el formato correcto y que la URL del workspace sea accesible.
- **Errores de red**: Verifica la conectividad hacia `https://<tu-workspace>.azuredatabricks.net` y revisa reglas de firewall o proxies.

## Desarrollo

El código fuente principal se encuentra en [`src/main.py`](src/main.py). Está estructurado en funciones pequeñas para facilitar modificaciones como:

- Cambiar la carga de configuración para soportar múltiples entornos.
- Añadir registros adicionales o integrar con herramientas de observabilidad.
- Sustituir la validación SCIM por otras comprobaciones según tus necesidades.

## IMPORTANTE

Solo ejecutar el workflow de all.yml para pruebas, ya que expone un token jwt emitido por github.
