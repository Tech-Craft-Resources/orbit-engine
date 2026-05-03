"""
Seed script for LEHGO — Colombian toy/building-blocks company demo data.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_lehgo.py

Idempotent: checks for existing products before inserting.
Targets the "lehgo" organization created by initial_data.py.

Data context:
  - Products inspired by Lego themes, prices in COP
  - IVA 19% (Colombia)
  - Customers with CC (Cédula de Ciudadanía)
  - Colombian cities and phone numbers
"""

import logging
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.models import (
    Category,
    Customer,
    InventoryMovement,
    Organization,
    Product,
    Role,
    Sale,
    SaleItem,
    User,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Demo data definitions
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Ciudad",
        "description": "Sets de construcción urbana y vida cotidiana",
        "children": [
            {"name": "Policía y Rescate", "description": "Patrullas, bomberos y equipos de emergencia"},
            {"name": "Tráfico y Transporte", "description": "Buses, trenes y vehículos de ciudad"},
            {"name": "Construcción", "description": "Grúas, excavadoras y maquinaria urbana"},
        ],
    },
    {
        "name": "Técnica",
        "description": "Sets de ingeniería con mecanismos funcionales",
        "children": [
            {"name": "Autos y Motos", "description": "Réplicas detalladas de vehículos"},
            {"name": "Maquinaria Pesada", "description": "Excavadoras, volquetes y grúas técnicas"},
        ],
    },
    {
        "name": "Clásico",
        "description": "Cajas de bloques y sets creativos libres",
        "children": [
            {"name": "Cajas de Bloques", "description": "Surtidos de piezas para construcción libre"},
            {"name": "Sets Creativos", "description": "Construcciones guiadas para principiantes"},
        ],
    },
    {
        "name": "Espacial",
        "description": "Exploración del universo y tecnología futurista",
        "children": [
            {"name": "Cohetes y Naves", "description": "Cohetes, lanzaderas y naves estelares"},
            {"name": "Exploración Lunar", "description": "Rovers, bases y misiones lunares"},
        ],
    },
    {
        "name": "Fantasía",
        "description": "Mundos mágicos, medievales y de aventura",
        "children": [
            {"name": "Castillos y Dragones", "description": "Fortalezas medievales y criaturas míticas"},
            {"name": "Piratas", "description": "Barcos, islas y aventuras en alta mar"},
        ],
    },
    {
        "name": "Creadores",
        "description": "Sets 3 en 1 con múltiples formas de construcción",
        "children": [
            {"name": "3 en 1", "description": "Un set, tres modelos posibles"},
        ],
    },
    {
        "name": "Minifiguras",
        "description": "Figuras coleccionables por series temáticas",
        "children": [
            {"name": "Series Coleccionables", "description": "Personajes de edición limitada por temporada"},
        ],
    },
]

# (name, sku, category_path, cost_cop, sale_price_cop, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Ciudad > Policía y Rescate
    ("Patrulla Policial Lehgo", "LEH-CIU-001", ("Ciudad", "Policía y Rescate"), 28000, 45900, 80, 15, "unit"),
    ("Camión de Bomberos", "LEH-CIU-002", ("Ciudad", "Policía y Rescate"), 65000, 99900, 45, 10, "unit"),
    ("Helicóptero de Rescate", "LEH-CIU-003", ("Ciudad", "Policía y Rescate"), 120000, 189900, 25, 5, "unit"),
    # Ciudad > Tráfico y Transporte
    ("Estación de Bus Articulado", "LEH-CIU-004", ("Ciudad", "Tráfico y Transporte"), 85000, 139900, 30, 8, "unit"),
    ("Cruce Ferroviario Eléctrico", "LEH-CIU-005", ("Ciudad", "Tráfico y Transporte"), 180000, 289900, 15, 4, "unit"),
    # Ciudad > Construcción
    ("Grúa Torre de Construcción", "LEH-CIU-006", ("Ciudad", "Construcción"), 95000, 149900, 20, 5, "unit"),
    ("Excavadora Urbana", "LEH-CIU-007", ("Ciudad", "Construcción"), 55000, 89900, 35, 8, "unit"),
    # Técnica > Autos y Motos
    ("Superdeportivo V12 Técnico", "LEH-TEC-001", ("Técnica", "Autos y Motos"), 580000, 899900, 8, 2, "unit"),
    ("Moto Café Racer Técnico", "LEH-TEC-002", ("Técnica", "Autos y Motos"), 280000, 449900, 12, 3, "unit"),
    ("Camioneta 4x4 Offroad", "LEH-TEC-003", ("Técnica", "Autos y Motos"), 380000, 599900, 10, 2, "unit"),
    # Técnica > Maquinaria Pesada
    ("Excavadora Técnica XL", "LEH-TEC-004", ("Técnica", "Maquinaria Pesada"), 450000, 699900, 8, 2, "unit"),
    ("Camión Volquete Articulado", "LEH-TEC-005", ("Técnica", "Maquinaria Pesada"), 220000, 349900, 15, 4, "unit"),
    # Clásico > Cajas de Bloques
    ("Caja Clásica 300 piezas", "LEH-CLA-001", ("Clásico", "Cajas de Bloques"), 18000, 29900, 150, 30, "unit"),
    ("Caja Clásica 900 piezas", "LEH-CLA-002", ("Clásico", "Cajas de Bloques"), 45000, 74900, 80, 20, "unit"),
    ("Mega Caja 2000 piezas", "LEH-CLA-003", ("Clásico", "Cajas de Bloques"), 90000, 149900, 40, 10, "unit"),
    # Clásico > Sets Creativos
    ("Casa de Campo Creativa", "LEH-CLA-004", ("Clásico", "Sets Creativos"), 65000, 99900, 50, 12, "unit"),
    ("Parque Comunitario", "LEH-CLA-005", ("Clásico", "Sets Creativos"), 85000, 139900, 35, 8, "unit"),
    # Espacial > Cohetes y Naves
    ("Cohete Exploratorio Lehgo", "LEH-ESP-001", ("Espacial", "Cohetes y Naves"), 95000, 149900, 30, 8, "unit"),
    ("Nave Estelar Comando", "LEH-ESP-002", ("Espacial", "Cohetes y Naves"), 220000, 349900, 18, 5, "unit"),
    ("Estación Espacial Orbital", "LEH-ESP-003", ("Espacial", "Cohetes y Naves"), 520000, 799900, 8, 2, "unit"),
    # Espacial > Exploración Lunar
    ("Rover Lunar Explorador", "LEH-ESP-004", ("Espacial", "Exploración Lunar"), 145000, 229900, 20, 5, "unit"),
    ("Base Lunar Avanzada", "LEH-ESP-005", ("Espacial", "Exploración Lunar"), 380000, 599900, 10, 3, "unit"),
    # Fantasía > Castillos y Dragones
    ("Gran Castillo Medieval", "LEH-FAN-001", ("Fantasía", "Castillos y Dragones"), 280000, 449900, 12, 3, "unit"),
    ("Torre del Dragón Rojo", "LEH-FAN-002", ("Fantasía", "Castillos y Dragones"), 180000, 289900, 20, 5, "unit"),
    ("Aldea Élfica del Bosque", "LEH-FAN-003", ("Fantasía", "Castillos y Dragones"), 420000, 649900, 8, 2, "unit"),
    # Fantasía > Piratas
    ("Galeón Pirata El Cóndor", "LEH-FAN-004", ("Fantasía", "Piratas"), 320000, 499900, 10, 3, "unit"),
    ("Isla del Tesoro Perdido", "LEH-FAN-005", ("Fantasía", "Piratas"), 145000, 229900, 18, 5, "unit"),
    # Creadores > 3 en 1
    ("Casa Giratoria 3 en 1", "LEH-CRE-001", ("Creadores", "3 en 1"), 85000, 139900, 40, 10, "unit"),
    ("Criaturas del Océano 3 en 1", "LEH-CRE-002", ("Creadores", "3 en 1"), 65000, 99900, 45, 10, "unit"),
    ("Monstruos Divertidos 3 en 1", "LEH-CRE-003", ("Creadores", "3 en 1"), 35000, 59900, 60, 15, "unit"),
    # Minifiguras > Series Coleccionables
    ("Serie 1 - Héroes Colombianos", "LEH-MIN-001", ("Minifiguras", "Series Coleccionables"), 12000, 19900, 200, 40, "unit"),
    ("Serie 2 - Deportes y Aventura", "LEH-MIN-002", ("Minifiguras", "Series Coleccionables"), 12000, 19900, 180, 40, "unit"),
    ("Serie 3 - Personajes de Fantasía", "LEH-MIN-003", ("Minifiguras", "Series Coleccionables"), 12000, 19900, 160, 40, "unit"),
    ("Pack Especial x4 Minifiguras", "LEH-MIN-004", ("Minifiguras", "Series Coleccionables"), 45000, 74900, 80, 20, "unit"),
]

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Sebastián",
        "last_name": "Rodríguez Martínez",
        "document_type": "CC",
        "document_number": "1020345678",
        "email": "sebastian.rodriguez@gmail.com",
        "phone": "+57 312 345 6789",
        "address": "Cra. 15 # 85-32, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Valentina",
        "last_name": "Gómez Herrera",
        "document_type": "CC",
        "document_number": "1032456789",
        "email": "valentina.gomez@hotmail.com",
        "phone": "+57 320 456 7890",
        "address": "Cll. 10 # 43E-21, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Andrés",
        "last_name": "Moreno Ospina",
        "document_type": "CC",
        "document_number": "94567890",
        "email": "andres.moreno@outlook.com",
        "phone": "+57 315 567 8901",
        "address": "Av. 6N # 25-41",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Camila",
        "last_name": "Torres Peña",
        "document_type": "CC",
        "document_number": "1045678901",
        "email": "camila.torres@gmail.com",
        "phone": "+57 317 678 9012",
        "address": "Cra. 53 # 76-110, Prado",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Felipe",
        "last_name": "Castro Vargas",
        "document_type": "CC",
        "document_number": "73890123",
        "email": "felipe.castro@gmail.com",
        "phone": "+57 300 789 0123",
        "address": "Cll. del Porvenir # 32-14, Manga",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Daniela",
        "last_name": "Ruiz Mendoza",
        "document_type": "CC",
        "document_number": "37012345",
        "email": "daniela.ruiz@gmail.com",
        "phone": "+57 311 890 1234",
        "address": "Cra. 27 # 51-38, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Mateo",
        "last_name": "López Arbeláez",
        "document_type": "CC",
        "document_number": "1088234567",
        "email": "mateo.lopez@gmail.com",
        "phone": "+57 321 901 2345",
        "address": "Cll. 19 # 7-45, Centro",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Sofía",
        "last_name": "Jiménez Ramos",
        "document_type": "CC",
        "document_number": "57123456",
        "email": "sofia.jimenez@outlook.com",
        "phone": "+57 318 012 3456",
        "address": "Cra. 5 # 17-25, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Santiago",
        "last_name": "Pardo Quintero",
        "document_type": "CC",
        "document_number": "1006789012",
        "email": "santiago.pardo@gmail.com",
        "phone": "+57 316 123 4567",
        "address": "Av. El Lago # 10-35",
        "city": "Villavicencio",
        "country": "Colombia",
    },
    {
        "first_name": "Isabella",
        "last_name": "Sánchez Forero",
        "document_type": "CC",
        "document_number": "1014890123",
        "email": "isabella.sanchez@gmail.com",
        "phone": "+57 313 234 5678",
        "address": "Cll. 116 # 17-83, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Juan Pablo",
        "last_name": "Reyes Aguilar",
        "document_type": "CC",
        "document_number": "71901234",
        "email": "juanpa.reyes@yahoo.com",
        "phone": "+57 314 345 6780",
        "address": "Cra. 43A # 18 Sur-115, Envigado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Laura",
        "last_name": "Bejarano Cruz",
        "document_type": "CC",
        "document_number": "52012345",
        "email": "laura.bejarano@gmail.com",
        "phone": "+57 322 456 7891",
        "address": "Cll. 45 # 3E-08, Granada",
        "city": "Cali",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "vendedor1@lehgo.com.co",
        "first_name": "Camilo",
        "last_name": "Vargas",
        "phone": "+57 310 111 1111",
    },
    {
        "email": "vendedor2@lehgo.com.co",
        "first_name": "Natalia",
        "last_name": "Ríos",
        "phone": "+57 310 222 2222",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]

IVA_RATE = Decimal("0.19")  # Colombia IVA 19%

ORG_SLUG = "lehgo"


def seed(session: Session) -> None:
    """Main seed function for Lehgo demo data."""

    # ── 1. Get the target organization ───────────────────────────────
    org = session.exec(
        select(Organization).where(Organization.slug == ORG_SLUG)
    ).first()
    if not org:
        logger.error("Default organization not found. Run initial_data.py first.")
        return
    org_id = org.id
    logger.info(f"Using organization: {org.name} ({org_id})")

    # Check if demo data already exists
    existing_products = session.exec(
        select(Product)
        .where(Product.organization_id == org_id)
        .where(Product.deleted_at.is_(None))
    ).first()
    if existing_products:
        logger.warning(
            "Demo data already exists. Skipping seed. Delete existing data first if you want to re-seed."
        )
        return

    # ── 2. Get roles ─────────────────────────────────────────────────
    admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
    seller_role = session.exec(select(Role).where(Role.name == "seller")).first()
    if not admin_role or not seller_role:
        logger.error("Roles not found. Run migrations first.")
        return

    # ── 3. Get existing admin user ───────────────────────────────────
    admin_user = session.exec(
        select(User)
        .where(User.organization_id == org_id)
        .where(User.role_id == admin_role.id)
        .where(User.deleted_at.is_(None))
    ).first()
    if not admin_user:
        logger.error("Admin user not found.")
        return

    # ── 4. Create seller users ───────────────────────────────────────
    sellers: list[User] = []
    for seller_data in SELLER_USERS:
        existing = session.exec(
            select(User)
            .where(User.email == seller_data["email"])
            .where(User.organization_id == org_id)
        ).first()
        if existing:
            sellers.append(existing)
            continue
        user = User(
            organization_id=org_id,
            role_id=seller_role.id,
            email=seller_data["email"],
            hashed_password=get_password_hash("seller123"),
            first_name=seller_data["first_name"],
            last_name=seller_data["last_name"],
            phone=seller_data["phone"],
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        sellers.append(user)
    session.commit()
    for s in sellers:
        session.refresh(s)
    all_sellers = [admin_user] + sellers
    logger.info(f"Created {len(sellers)} seller users")

    # ── 5. Create categories ─────────────────────────────────────────
    category_map: dict[str, Category] = {}

    for cat_data in CATEGORIES:
        parent = Category(
            organization_id=org_id,
            name=cat_data["name"],
            description=cat_data["description"],
            is_active=True,
        )
        session.add(parent)
        session.flush()
        category_map[cat_data["name"]] = parent

        for child_data in cat_data.get("children", []):
            child = Category(
                organization_id=org_id,
                name=child_data["name"],
                description=child_data["description"],
                parent_id=parent.id,
                is_active=True,
            )
            session.add(child)
            session.flush()
            category_map[child_data["name"]] = child

    session.commit()
    for cat in category_map.values():
        session.refresh(cat)
    logger.info(f"Created {len(category_map)} categories")

    # ── 6. Create products ───────────────────────────────────────────
    product_list: list[Product] = []
    for name, sku, cat_path, cost, price, stock, stock_min, unit in PRODUCTS:
        category = (
            category_map.get(cat_path[1])
            if len(cat_path) > 1
            else category_map.get(cat_path[0])
        )
        product = Product(
            organization_id=org_id,
            category_id=category.id if category else None,
            name=name,
            sku=sku,
            cost_price=Decimal(str(cost)),
            sale_price=Decimal(str(price)),
            stock_quantity=stock,
            stock_min=stock_min,
            unit=unit,
            is_active=True,
        )
        session.add(product)
        product_list.append(product)

    session.commit()
    for p in product_list:
        session.refresh(p)
    logger.info(f"Created {len(product_list)} products")

    # ── 7. Create initial inventory movements (stock-in) ─────────────
    for product in product_list:
        movement = InventoryMovement(
            organization_id=org_id,
            product_id=product.id,
            user_id=admin_user.id,
            movement_type="purchase",
            quantity=product.stock_quantity,
            previous_stock=0,
            new_stock=product.stock_quantity,
            reference_type="adjustment",
            reason="Stock inicial - Inventario de apertura Lehgo",
            created_at=datetime.now(timezone.utc) - timedelta(days=35),
        )
        session.add(movement)
    session.commit()
    logger.info("Created initial inventory movements")

    # ── 8. Create customers ──────────────────────────────────────────
    customer_list: list[Customer] = []
    for cust_data in CUSTOMERS_DATA:
        customer = Customer(
            organization_id=org_id,
            **cust_data,
            is_active=True,
        )
        session.add(customer)
        customer_list.append(customer)

    session.commit()
    for c in customer_list:
        session.refresh(c)
    logger.info(f"Created {len(customer_list)} customers")

    # ── 9. Create sales over the last 30 days ────────────────────────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(30, -1, -1):
        day = now - timedelta(days=days_ago)
        is_weekend = day.weekday() >= 5
        num_sales = random.randint(1, 4) if is_weekend else random.randint(3, 8)

        if days_ago == 0:
            num_sales = random.randint(5, 8)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"FAC-{invoice_counter:06d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.7 else None

            num_items = random.randint(1, 4)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(9, 20)
            sale_minute = random.randint(0, 59)
            sale_date = day.replace(
                hour=sale_hour,
                minute=sale_minute,
                second=random.randint(0, 59),
                microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = random.randint(1, 3)
                item_subtotal = prod.sale_price * qty
                subtotal += item_subtotal
                items_data.append(
                    {
                        "product_id": prod.id,
                        "product_name": prod.name,
                        "product_sku": prod.sku,
                        "quantity": qty,
                        "unit_price": prod.sale_price,
                        "subtotal": item_subtotal,
                    }
                )

            discount = (
                subtotal * Decimal(str(random.randint(0, 10))) / Decimal("100")
            ).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.05 and days_ago > 0
            status = "cancelled" if is_cancelled else "completed"

            sale = Sale(
                organization_id=org_id,
                customer_id=customer.id if customer else None,
                user_id=seller.id,
                invoice_number=invoice_number,
                sale_date=sale_date,
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                total=total,
                payment_method=payment_method,
                status=status,
                notes=None,
                created_at=sale_date,
                updated_at=sale_date,
            )

            if is_cancelled:
                sale.cancelled_at = sale_date + timedelta(hours=random.randint(1, 4))
                sale.cancelled_by = admin_user.id
                sale.cancellation_reason = random.choice(
                    [
                        "Cliente cambió de opinión",
                        "Producto agotado",
                        "Error en el pedido",
                    ]
                )
                sale.updated_at = sale.cancelled_at

            session.add(sale)
            session.flush()

            for item_data in items_data:
                sale_item = SaleItem(
                    sale_id=sale.id,
                    **item_data,
                    created_at=sale_date,
                )
                session.add(sale_item)

            if status == "completed":
                for item_data in items_data:
                    prod_obj = next(
                        p for p in product_list if p.id == item_data["product_id"]
                    )
                    prev_stock = prod_obj.stock_quantity
                    prod_obj.stock_quantity = max(
                        0, prod_obj.stock_quantity - item_data["quantity"]
                    )
                    movement = InventoryMovement(
                        organization_id=org_id,
                        product_id=item_data["product_id"],
                        user_id=seller.id,
                        movement_type="sale",
                        quantity=-item_data["quantity"],
                        previous_stock=prev_stock,
                        new_stock=prod_obj.stock_quantity,
                        reference_id=sale.id,
                        reference_type="sale",
                        reason=f"Venta {invoice_number}",
                        created_at=sale_date,
                    )
                    session.add(movement)

                if customer:
                    customer.total_purchases += total
                    customer.purchases_count += 1
                    customer.last_purchase_at = sale_date

            total_sales += 1

    session.commit()

    for p in product_list:
        session.add(p)
    for c in customer_list:
        session.add(c)
    session.commit()

    logger.info(f"Created {total_sales} sales over the last 30 days")

    # ── 10. Restock low-inventory products ───────────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(20, 60)
            prev = product.stock_quantity
            product.stock_quantity += restock_qty
            movement = InventoryMovement(
                organization_id=org_id,
                product_id=product.id,
                user_id=admin_user.id,
                movement_type="purchase",
                quantity=restock_qty,
                previous_stock=prev,
                new_stock=product.stock_quantity,
                reference_type="purchase",
                reason="Reposición de inventario Lehgo",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            )
            session.add(movement)
            session.add(product)

    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED LEHGO COMPLETE!")
    logger.info(f"  Organización: {org.name}")
    logger.info(f"  Categorías:   {len(category_map)}")
    logger.info(f"  Productos:    {len(product_list)}")
    logger.info(f"  Clientes:     {len(customer_list)}")
    logger.info(f"  Ventas:       {total_sales}")
    logger.info(f"  Vendedores:   {len(all_sellers)} (admin + {len(sellers)} sellers)")
    logger.info("")
    logger.info("Credenciales de acceso:")
    logger.info("  Admin:    admin@example.com / changethis")
    for sd in SELLER_USERS:
        logger.info(f"  Seller:   {sd['email']} / seller123")
    logger.info("=" * 60)


def main() -> None:
    random.seed(42)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
