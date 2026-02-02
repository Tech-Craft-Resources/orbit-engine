# Configuración de Almacenamiento S3

El proyecto está configurado para usar almacenamiento compatible con S3 (MinIO en desarrollo, AWS S3 en producción).

## Desarrollo Local con MinIO

MinIO es un servidor de almacenamiento de objetos compatible con S3 que se ejecuta en Docker.

### Configuración

Las variables de entorno para desarrollo local ya están configuradas en `.env.example`:

```bash
# S3 / Object Storage (S3-compatible)
S3_ENDPOINT_URL=http://minio:9000  # URL del servidor MinIO
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=app-storage
S3_REGION=us-east-1

# MinIO (solo para desarrollo local)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

### Acceso a MinIO

Cuando ejecutes `docker compose up`, MinIO estará disponible en:

- **API (S3-compatible)**: http://minio.localhost (puerto 9000)
- **Consola Web**: http://minio-console.localhost (puerto 9001)
  - Usuario: `minioadmin`
  - Contraseña: `minioadmin`

### Crear el Bucket

El bucket no se crea automáticamente. Debes crearlo manualmente:

1. Accede a la consola web: http://minio-console.localhost
2. Ve a "Buckets" → "Create Bucket"
3. Nombre del bucket: `app-storage` (o el que hayas configurado en `S3_BUCKET_NAME`)
4. Haz clic en "Create Bucket"

Alternativamente, puedes usar el CLI de MinIO (`mc`) desde el contenedor:

```bash
docker compose exec minio mc mb local/app-storage
```

## Producción con AWS S3

Para usar AWS S3 en producción, simplemente cambia las variables de entorno:

```bash
# Deja S3_ENDPOINT_URL vacío o elimínalo para usar AWS S3
S3_ENDPOINT_URL=
S3_ACCESS_KEY_ID=tu-access-key-de-aws
S3_SECRET_ACCESS_KEY=tu-secret-key-de-aws
S3_BUCKET_NAME=tu-bucket-de-produccion
S3_REGION=us-east-1  # o tu región preferida
```

### Configurar AWS S3

1. Crea un bucket en AWS S3
2. Crea un usuario IAM con permisos para el bucket
3. Genera access keys para ese usuario
4. Configura las variables de entorno con esas credenciales

## Uso en el Backend

La configuración está disponible en `app/core/config.py`:

```python
from app.core.config import settings

# Verificar si S3 está habilitado
if settings.s3_enabled:
    # Usar boto3 para conectarse
    import boto3
    
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT_URL,  # None para AWS S3
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
    )
    
    # Subir un archivo
    s3_client.upload_file(
        'local_file.pdf',
        settings.S3_BUCKET_NAME,
        'remote_file.pdf'
    )
```

## Compatibilidad S3

La configuración es completamente compatible con S3. La única diferencia entre desarrollo y producción es la variable `S3_ENDPOINT_URL`:

- **MinIO (desarrollo)**: `S3_ENDPOINT_URL=http://minio:9000`
- **AWS S3 (producción)**: `S3_ENDPOINT_URL=` (vacío) o eliminar la variable

Todas las demás operaciones son idénticas, permitiendo usar el mismo código en ambos entornos.
