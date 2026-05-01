"""
Pruebas de carga con Locust para OrbitEngine.

Instalación:
    uv add --dev locust

Uso básico (interfaz web):
    cd backend
    uv run locust -f tests/performance/locustfile.py --host=https://orbitengine.lat

Uso sin interfaz (reporte en terminal):
    uv run locust -f tests/performance/locustfile.py \
        --host=https://orbitengine.lat \
        --headless \
        --users 7 \
        --spawn-rate 1 \
        --run-time 60s

Luego abre http://localhost:8089 en el navegador.
"""

import itertools
import threading

from locust import HttpUser, between, task


# Lista de cuentas a rotar. Cada usuario virtual toma la siguiente en orden cíclico.
# Agrega o quita cuentas según necesites.
ACCOUNTS = [
    {"username": "carito_16172@hotmail.com",          "password": "orbit26-"},  # Ferrallas
    {"username": "daniel.velasco01@usa.edu.co",        "password": "orbit26)"},  # Sabor Caribe
    {"username": "marior.16@hotmail.com",              "password": "orbit26/"},  # Moda Andes
    {"username": "info@froztbitez.com",                "password": "orbit26!"},  # Frozt Bitez
    {"username": "nicolas.rodriguez10@usa.edu.co",     "password": "orbit26|"},  # FarmaVida
    {"username": "nicolas.rodriguez2004@outlook.com",  "password": "orbit26*"},  # lehgo
    {"username": "niquimiqui@gmail.com",               "password": "orbit26+"},  # Miss Peggy
    {"username": "orbitengine3@gmail.com",             "password": "Orbit26+"},  # default
]

API = "/api/v1"

# Iterador seguro para hilos: cada usuario virtual toma el siguiente par de credenciales
_account_cycle = itertools.cycle(ACCOUNTS)
_lock = threading.Lock()


def _next_account() -> dict:
    with _lock:
        return next(_account_cycle)


class OrbitEngineUser(HttpUser):
    """
    Simula usuarios navegando por la plataforma.
    Cada usuario virtual toma credenciales distintas de la lista ACCOUNTS (rotación cíclica).
    Entre cada tarea espera entre 1 y 3 segundos (comportamiento humano realista).
    """

    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Se ejecuta una vez por usuario virtual al iniciar. Toma credenciales y hace login."""
        account = _next_account()
        response = self.client.post(
            f"{API}/login/access-token",
            data=account,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Login falló ({response.status_code}): {response.text}"
            )

        token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {token}"}

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
