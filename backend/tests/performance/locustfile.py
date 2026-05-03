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

Modo de estrés máximo (romper el servidor):
    uv run locust -f tests/performance/locustfile.py \
        --host=https://api.orbitengine.lat \
        --headless \
        --users 50 \
        --spawn-rate 5 \
        --run-time 120s \
        --html reporte-estres.html

Luego abre http://localhost:8089 en el navegador.

Clases de usuario:
  OrbitEngineUser  — lector normal con paginación extrema  (peso 3)
  SellerUser       — crea ventas e inventario reales        (peso 2)
  SpammerUser      — martilla endpoints de agregación       (peso 1)
"""

import itertools
import random
import threading
import uuid

from locust import HttpUser, between, constant, task


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

_account_cycle = itertools.cycle(ACCOUNTS)
_lock = threading.Lock()


def _next_account() -> dict:
    with _lock:
        return next(_account_cycle)


def _login(client, account: dict) -> dict:
    """Realiza login y devuelve los headers de autorización."""
    response = client.post(
        f"{API}/login/access-token",
        data=account,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Login falló ({response.status_code}): {response.text}"
        )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Clase 1: Lector agresivo con paginación extrema
# ---------------------------------------------------------------------------

class OrbitEngineUser(HttpUser):
    """
    Simula usuarios reales navegando la plataforma.
    Prueba paginación extrema, búsquedas, filtros y ordenamiento.
    Peso 3: la mayoría del tráfico.
    """

    weight = 3
    wait_time = between(0.5, 1.5)

    def on_start(self) -> None:
        account = _next_account()
        self.headers = _login(self.client, account)

    # Dashboard

    @task(4)
    def get_dashboard_stats(self) -> None:
        self.client.get(f"{API}/dashboard/stats", headers=self.headers, name="/dashboard/stats")

    # Productos — variaciones de búsqueda y paginación

    @task(3)
    def list_products(self) -> None:
        self.client.get(f"{API}/products/?limit=100&skip=0", headers=self.headers, name="/products/ [p1]")

    @task(2)
    def list_products_page2(self) -> None:
        self.client.get(f"{API}/products/?limit=100&skip=100", headers=self.headers, name="/products/ [p2]")

    @task(2)
    def search_products(self) -> None:
        term = random.choice(["a", "pro", "cam", "res", "bo", "sal", "med", "azu"])
        self.client.get(
            f"{API}/products/?search={term}&limit=100",
            headers=self.headers,
            name="/products/?search=*",
        )

    @task(1)
    def list_products_sorted(self) -> None:
        col = random.choice(["name", "sale_price", "stock_quantity", "created_at"])
        order = random.choice(["asc", "desc"])
        self.client.get(
            f"{API}/products/?sort_by={col}&sort_order={order}&limit=100",
            headers=self.headers,
            name="/products/?sort=*",
        )

    @task(1)
    def list_low_stock(self) -> None:
        self.client.get(f"{API}/products/low-stock", headers=self.headers, name="/products/low-stock")

    # Ventas

    @task(3)
    def list_sales(self) -> None:
        self.client.get(f"{API}/sales/?limit=100", headers=self.headers, name="/sales/ [p1]")

    @task(1)
    def list_sales_filtered(self) -> None:
        status = random.choice(["completed", "cancelled"])
        self.client.get(
            f"{API}/sales/?status={status}&limit=100",
            headers=self.headers,
            name="/sales/?status=*",
        )

    @task(1)
    def list_sales_stats(self) -> None:
        self.client.get(f"{API}/sales/stats", headers=self.headers, name="/sales/stats")

    @task(1)
    def list_sales_today(self) -> None:
        self.client.get(f"{API}/sales/today", headers=self.headers, name="/sales/today")

    # Clientes

    @task(2)
    def list_customers(self) -> None:
        self.client.get(f"{API}/customers/?limit=100", headers=self.headers, name="/customers/ [p1]")

    @task(1)
    def search_customers(self) -> None:
        term = random.choice(["an", "ma", "jo", "car", "ro", "lu"])
        self.client.get(
            f"{API}/customers/?search={term}&limit=100",
            headers=self.headers,
            name="/customers/?search=*",
        )

    # Inventario y categorías

    @task(1)
    def list_inventory_movements(self) -> None:
        self.client.get(
            f"{API}/inventory-movements/?limit=100",
            headers=self.headers,
            name="/inventory-movements/",
        )

    @task(1)
    def list_categories(self) -> None:
        self.client.get(f"{API}/categories/", headers=self.headers, name="/categories/")


# ---------------------------------------------------------------------------
# Clase 2: Vendedor que crea ventas reales e inventario
# ---------------------------------------------------------------------------

class SellerUser(HttpUser):
    """
    Simula un vendedor activo: crea ventas con productos reales,
    ajusta stock y registra movimientos de inventario.
    Las ventas usan productos reales obtenidos al inicio,
    con cantidades de 1 unidad para no agotar stock.
    Peso 2.
    """

    weight = 2
    wait_time = between(1, 2)

    product_ids: list[str]
    customer_ids: list[str]

    def on_start(self) -> None:
        account = _next_account()
        self.headers = _login(self.client, account)

        # Cargar productos reales
        resp = self.client.get(
            f"{API}/products/?limit=50&is_active=true",
            headers=self.headers,
            name="/products/ [setup]",
        )
        products = resp.json().get("data", []) if resp.status_code == 200 else []
        # Solo productos con stock suficiente (≥ 2 unidades)
        self.product_ids = [
            p["id"] for p in products if p.get("stock_quantity", 0) >= 2
        ]

        # Cargar clientes reales
        resp = self.client.get(
            f"{API}/customers/?limit=50",
            headers=self.headers,
            name="/customers/ [setup]",
        )
        customers = resp.json().get("data", []) if resp.status_code == 200 else []
        self.customer_ids = [c["id"] for c in customers]

    @task(4)
    def create_sale(self) -> None:
        if not self.product_ids:
            return
        product_id = random.choice(self.product_ids)
        payload: dict = {
            "items": [{"product_id": product_id, "quantity": 1}],
            "payment_method": random.choice(["cash", "card", "transfer"]),
            "discount": 0,
            "tax": 0,
            "notes": "Prueba de carga Locust",
        }
        if self.customer_ids and random.random() > 0.4:
            payload["customer_id"] = random.choice(self.customer_ids)

        self.client.post(
            f"{API}/sales/",
            json=payload,
            headers=self.headers,
            name="POST /sales/",
        )

    @task(2)
    def adjust_stock(self) -> None:
        if not self.product_ids:
            return
        product_id = random.choice(self.product_ids)
        self.client.post(
            f"{API}/products/{product_id}/adjust-stock",
            json={"quantity": random.choice([5, 10, 20, 50]), "reason": "Reposición Locust"},
            headers=self.headers,
            name="POST /products/{id}/adjust-stock",
        )

    @task(1)
    def read_product_movements(self) -> None:
        if not self.product_ids:
            return
        product_id = random.choice(self.product_ids)
        self.client.get(
            f"{API}/products/{product_id}/movements",
            headers=self.headers,
            name="GET /products/{id}/movements",
        )

    @task(1)
    def list_sales(self) -> None:
        self.client.get(f"{API}/sales/?limit=100", headers=self.headers, name="/sales/ [seller]")


# ---------------------------------------------------------------------------
# Clase 3: Spammer — sin espera, martilla endpoints de agregación
# ---------------------------------------------------------------------------

class SpammerUser(HttpUser):
    """
    Dispara peticiones sin pausa a los endpoints más costosos (agregaciones y stats).
    El objetivo es saturar la DB y revelar cuellos de botella bajo presión extrema.
    Peso 1.
    """

    weight = 1
    wait_time = constant(0)

    def on_start(self) -> None:
        account = _next_account()
        self.headers = _login(self.client, account)

    @task(5)
    def spam_dashboard(self) -> None:
        self.client.get(f"{API}/dashboard/stats", headers=self.headers, name="/dashboard/stats [spam]")

    @task(3)
    def spam_sales_stats(self) -> None:
        self.client.get(f"{API}/sales/stats", headers=self.headers, name="/sales/stats [spam]")

    @task(3)
    def spam_low_stock(self) -> None:
        self.client.get(f"{API}/products/low-stock", headers=self.headers, name="/products/low-stock [spam]")

    @task(2)
    def spam_products_large_page(self) -> None:
        skip = random.randint(0, 500)
        self.client.get(
            f"{API}/products/?limit=500&skip={skip}",
            headers=self.headers,
            name="/products/?limit=500 [spam]",
        )

    @task(2)
    def spam_sales_large_page(self) -> None:
        skip = random.randint(0, 500)
        self.client.get(
            f"{API}/sales/?limit=500&skip={skip}",
            headers=self.headers,
            name="/sales/?limit=500 [spam]",
        )

    @task(1)
    def spam_random_uuid(self) -> None:
        """Peticiones a IDs inexistentes — prueba el path de error 404."""
        fake_id = str(uuid.uuid4())
        endpoint = random.choice([
            f"{API}/products/{fake_id}",
            f"{API}/sales/{fake_id}",
            f"{API}/customers/{fake_id}",
        ])
        self.client.get(endpoint, headers=self.headers, name="GET /{resource}/{bad-uuid}")
