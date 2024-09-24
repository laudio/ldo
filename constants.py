import os

# Constants for repository paths
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
LAUDIO_SCRIPTS_DIR = os.path.join(BASE_DIR, "laudio-scripts")
DOCKER_COMPOSE_DIR = os.path.join(BASE_DIR, "laudio-scripts", "docker", "development")
CORE_DIR = os.path.join(BASE_DIR, "core")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
DB_DIR = os.path.join(BASE_DIR, "db")
DOCKER_DIR = os.path.join(BASE_DIR, "docker")
LISS_DIR = os.path.join(BASE_DIR, "liss")

SQLCMD = "sqlcmd"
DB_HOST = "localhost"
DB_PORT = "1433"

USER = os.environ.get("USER")
