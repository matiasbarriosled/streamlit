from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'env/utopian-honor-438417-u7-5b7f84fcfd25.json'
)
client = storage.Client(project='utopian-honor-438417-u7', credentials=credentials)

def descargar_archivo(bucket_name, archivo_name):
    try:
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(archivo_name)
        archivo_local = f"./{archivo_name}"
        blob.download_to_filename(archivo_local)
        return archivo_local
    except Exception as e:
        st.error(f"Error al descargar el archivo {archivo_name}: {e}")
        raise