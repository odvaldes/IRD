import requests
import os
import tempfile

def descargar_archivo_desde_github(repo_url, archivo_path, token=None):
    """
    Descarga un archivo desde un repositorio público o privado de GitHub.

    Parámetros:
    - repo_url: URL base del repositorio (por ejemplo, https://github.com/usuario/repositorio)
    - archivo_path: ruta del archivo dentro del repositorio (por ejemplo, data/capas/capa.kmz)
    - token: token de autenticación (si es repositorio privado)

    Retorna:
    - ruta temporal del archivo descargado
    """
    try:
        # Extraer datos del repositorio
        repo_url = repo_url.rstrip('/')
        user_repo = "/".join(repo_url.split("/")[-2:])
        raw_url = f"https://raw.githubusercontent.com/{user_repo}/main/{archivo_path}"

        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        response = requests.get(raw_url, headers=headers)

        if response.status_code == 200:
            tmp_dir = tempfile.mkdtemp()
            archivo_local = os.path.join(tmp_dir, os.path.basename(archivo_path))
            with open(archivo_local, 'wb') as f:
                f.write(response.content)
            return archivo_local
        else:
            raise Exception(f"Error al descargar archivo: {response.status_code} - {response.text}")

    except Exception as e:
        raise RuntimeError(f"No se pudo descargar el archivo desde GitHub: {e}")
