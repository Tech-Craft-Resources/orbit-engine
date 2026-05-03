"""
Pruebas de carga con Locust para OrbitEngine.

Instalación:
    uv add --dev locust

Uso básico (interfaz web):
    cd backend
    uv run locust -f tests/performance/locustfile.py --host=https://api.orbitengine.lat

Uso sin interfaz (reporte en terminal):
    uv run locust -f tests/performance/locustfile.py \
        --host=https://api.orbitengine.lat \
        --headless \
        --users 8 \
        --spawn-rate 1 \
        --run-time 60s \
        --html reporte-carga.html

Luego abre http://localhost:8089 en el navegador.
"""

import itertools
import threading

from locust import HttpUser, between, task


# Lista de tokens por usuario. Pega el Bearer token de cada cuenta directamente aquí.
# El campo "name" es solo descriptivo.
# Ejemplo:
#   {"name": "Ferrallas",    "token": "eyJhbGci..."},
TOKENS = [
    {"name": "Ferrallas",    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ0MDAsInN1YiI6IjNiNTdiNmM1LWVhYTYtNDdlYi1iNDZjLTM1MWE5NTk0N2U2MiIsIm9yZ2FuaXphdGlvbl9pZCI6IjE0N2E0NzJiLWQ2N2EtNGExMi1iYzQ5LTliODM1NGQzZDI0OSIsInJvbGUiOiJhZG1pbiJ9.GMLUGXUA8YxqRyTHINfTd7lLFzZdHZuDiLcfvYvlU9k"},  # carito_16172@hotmail.com
    {"name": "Sabor Caribe", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ0MjgsInN1YiI6ImM3ZWE0OWJlLWM3MjUtNGQxNS04OTgyLWMwNWM2ZGQzNjA2NiIsIm9yZ2FuaXphdGlvbl9pZCI6ImIyNzU3OTM0LTk3YzYtNDA2ZS04ODU5LWJkYzRhNmRmM2Q4ZiIsInJvbGUiOiJhZG1pbiJ9.55dRK711lhu7H3DnaAiGvWcFr6_6ItqufAv6TJj3k1c"},  # daniel.velasco01@usa.edu.co
    {"name": "Moda Andes",   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ0NjQsInN1YiI6IjUwYTliNmU0LWIxY2EtNDc0Zi04NDYwLTMyOWU3NDI2Y2JhMCIsIm9yZ2FuaXphdGlvbl9pZCI6IjQ4NjVlZGQ3LTFkNGQtNDgyOC05NzVmLWUxOGE5NTdmYjUyYiIsInJvbGUiOiJhZG1pbiJ9.JO_t81-LzYeVe_Ptyt8OoQcdWnj4STYKOuo8kU7-SUU"},  # marior.16@hotmail.com
    {"name": "Frozt Bitez",  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ1MDcsInN1YiI6IjRlYTM2NDkzLTYxMDQtNGJlMC04MzM4LWJkNzg4YjE3Y2M0ZCIsIm9yZ2FuaXphdGlvbl9pZCI6ImQ3MjQ3OWQ5LWQyZGUtNGI0Ny04YjhjLWU2NmY4ZmU3MjJiOCIsInJvbGUiOiJhZG1pbiJ9.-KFsl58TVJN4S981EyU62HucLf3tgiE-yCZkRjFRFMY"},  # info@froztbitez.com
    {"name": "FarmaVida",    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ1MzEsInN1YiI6ImFhNjY4ZDQ3LTFmZjEtNDgyYS04ZjdiLTRhNTUyYWUzMDNiNSIsIm9yZ2FuaXphdGlvbl9pZCI6IjY3YWU3ZWE0LTMzYjYtNGE2My1hMDE4LTI5NDIyYTRkNmQzZSIsInJvbGUiOiJhZG1pbiJ9.1fLlEzvqPT4Jju13iXdU6fdKQIsBnoxmDJrv86aiFo8"},  # nicolas.rodriguez10@usa.edu.co
    {"name": "lehgo",        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ1NTMsInN1YiI6IjVkNzc0ZWFhLTQ2YzMtNDkzMi05YmM0LTJhZjZkZmM5NmM3ZiIsIm9yZ2FuaXphdGlvbl9pZCI6IjA3ODg4NThjLTdiYzctNDY1OS04ZjUwLTZmNzU1ZWUxMWFhNCIsInJvbGUiOiJhZG1pbiJ9.17_7ZvJKygSJgdGQm8E_Aappg6nStv4yhMdnME9i5kE"},  # nicolas.rodriguez2004@outlook.com
    {"name": "Miss Peggy",   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ1NzQsInN1YiI6IjE0OWMxOGY3LWU5OGYtNDM1Yi05NjlmLTAzMDA4MmMxNmJlMyIsIm9yZ2FuaXphdGlvbl9pZCI6ImY3Y2NhMTEzLTcyMDktNGQ3Zi1iYmI1LTk0N2NkZjU5MGNjOCIsInJvbGUiOiJhZG1pbiJ9.oYD8MK9aWp6FLhClA2qoWHO7t1HMS0YwmQMhbYML-2Y"},  # niquimiqui@gmail.com
    {"name": "default",      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzgzMDQ2MDAsInN1YiI6ImVhNjYwNzlhLWY0ZWYtNDU0OC1hNTRlLTBhZWY0N2Y5ZGRmMCIsIm9yZ2FuaXphdGlvbl9pZCI6ImVkNDJiZTU2LTE0MmQtNDRkNy1iMDA4LTgxMTdhZTk4NWYxNSIsInJvbGUiOiJhZG1pbiJ9.GNMZkuYbUy0aHzXS9-ovQyPPKuUgy3h5Z2htc-Uh1jk"},  # orbitengine3@gmail.com
]

API = "/api/v1"

# Iterador seguro para hilos: cada usuario virtual toma el siguiente token en orden cíclico
_token_cycle = itertools.cycle(TOKENS)
_lock = threading.Lock()


def _next_token() -> dict:
    with _lock:
        return next(_token_cycle)


class OrbitEngineUser(HttpUser):
    """
    Simula usuarios navegando por la plataforma.
    Cada usuario virtual toma un Bearer token distinto de la lista TOKENS (rotación cíclica).
    No realiza login — usa los tokens pre-configurados directamente.
    Entre cada tarea espera entre 1 y 3 segundos (comportamiento humano realista).
    """

    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Se ejecuta una vez por usuario virtual al iniciar. Asigna el token pre-configurado."""
        entry = _next_token()
        if not entry["token"]:
            raise RuntimeError(
                f"Token vacío para '{entry['name']}'. Completa los tokens en TOKENS antes de ejecutar."
            )
        self.headers = {"Authorization": f"Bearer {entry['token']}"}

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    @task(3)
    def get_dashboard_stats(self) -> None:
        """Peso 3: es la vista más visitada — se prueba con más frecuencia."""
        self.client.get(f"{API}/dashboard/stats", headers=self.headers, name="/dashboard/stats")

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------

    @task(3)
    def list_products(self) -> None:
        self.client.get(f"{API}/products/", headers=self.headers, name="/products/")

    @task(1)
    def list_low_stock(self) -> None:
        self.client.get(f"{API}/products/low-stock", headers=self.headers, name="/products/low-stock")

    # ------------------------------------------------------------------
    # Ventas
    # ------------------------------------------------------------------

    @task(2)
    def list_sales(self) -> None:
        self.client.get(f"{API}/sales/", headers=self.headers, name="/sales/")

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    @task(2)
    def list_customers(self) -> None:
        self.client.get(f"{API}/customers/", headers=self.headers, name="/customers/")

    # ------------------------------------------------------------------
    # Inventario
    # ------------------------------------------------------------------

    @task(1)
    def list_inventory_movements(self) -> None:
        self.client.get(
            f"{API}/inventory-movements/",
            headers=self.headers,
            name="/inventory-movements/",
        )

    # ------------------------------------------------------------------
    # Categorías
    # ------------------------------------------------------------------

    @task(1)
    def list_categories(self) -> None:
        self.client.get(f"{API}/categories/", headers=self.headers, name="/categories/")
