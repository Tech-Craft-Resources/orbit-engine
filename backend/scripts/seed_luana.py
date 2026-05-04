"""
Seed script for Luana — emprendimiento colombiano de tejidos y manualidades artesanales.

Usage:
    cd backend && uv run python scripts/seed_luana.py

Self-contained: crea la organización "luana-handmade" y la administradora Claudia González
si no existen todavía. Idempotente: si ya hay productos en la organización, no inserta nada.

Data context:
  - Productos: bolsos, alfombras, accesorios y decoración en trapillo y macramé
  - Precios en COP, acordes a un emprendimiento artesanal pequeño
  - Sin IVA (Régimen Simple / productor artesanal no factura IVA)
  - Pagos predominantemente por transferencia (Nequi / Bancolombia), algo en efectivo
  - Ventas de bajo volumen: 1-3 por día entre semana, 0-1 los fines de semana
  - Solo una usuaria: Claudia González (admin)
  - Clientes colombianas, ciudades principales del país
"""

import logging
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlmodel import Session, select

from app.core.db import engine
from app import crud
from app.models import (
    Category,
    Customer,
    InventoryMovement,
    OrganizationCreate,
    Product,
    Role,
    Sale,
    SaleItem,
    User,
    UserCreate,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Identidad de la organización
# ---------------------------------------------------------------------------

ORG_SLUG = "luana-handmade"
ORG_NAME = "Luana"
ORG_DESCRIPTION = "Tejidos y manualidades artesanales en trapillo y materiales sostenibles"

ADMIN_EMAIL = "claudia@luana-handmade.co"
ADMIN_PASSWORD = "claudia123"
ADMIN_FIRST_NAME = "Claudia"
ADMIN_LAST_NAME = "González"
ADMIN_PHONE = "+57 312 874 5519"

# ---------------------------------------------------------------------------
# Catálogo de productos
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Bolsos en Trapillo",
        "description": "Bolsos tejidos a mano con trapillo reciclado y sostenible",
        "children": [
            {"name": "Bandoleras", "description": "Bolsos pequeños con correa cruzada"},
            {"name": "Totes", "description": "Bolsos grandes tipo tote para el día a día"},
            {"name": "Mochilas", "description": "Mochilas tejidas de uso diario"},
            {"name": "Clutches", "description": "Bolsos de mano pequeños y elegantes"},
        ],
    },
    {
        "name": "Alfombras y Tapetes",
        "description": "Alfombras y tapetes artesanales tejidos en trapillo",
        "children": [
            {"name": "Redondas", "description": "Alfombras de forma circular"},
            {"name": "Rectangulares", "description": "Alfombras de forma rectangular"},
            {"name": "Tapetes de Baño", "description": "Tapetes antideslizantes para baño"},
        ],
    },
    {
        "name": "Accesorios",
        "description": "Accesorios funcionales y decorativos tejidos en trapillo",
        "children": [
            {"name": "Cestas Organizadoras", "description": "Cestas para organizar el hogar"},
            {"name": "Posavasos", "description": "Posavasos tejidos a mano"},
        ],
    },
    {
        "name": "Decoración Hogar",
        "description": "Piezas decorativas artesanales para el hogar",
        "children": [
            {"name": "Colgantes de Pared", "description": "Colgantes decorativos en macramé y trapillo"},
            {"name": "Atrapasueños", "description": "Atrapasueños tejidos con materiales naturales"},
        ],
    },
]

# (nombre, sku, (cat_padre, cat_hijo), costo, precio_venta, stock, stock_min, unidad)
PRODUCTS: list[tuple] = [
    # Bolsos en Trapillo > Bandoleras
    (
        "Bolso Bandolera Terracota",
        "LUA-BOL-BAN-TC",
        ("Bolsos en Trapillo", "Bandoleras"),
        80000, 185000, 5, 2, "unit",
    ),
    (
        "Bolso Bandolera Mostaza",
        "LUA-BOL-BAN-MS",
        ("Bolsos en Trapillo", "Bandoleras"),
        85000, 195000, 4, 2, "unit",
    ),
    # Bolsos en Trapillo > Totes
    (
        "Bolso Tote Beige Natural",
        "LUA-BOL-TOT-BG",
        ("Bolsos en Trapillo", "Totes"),
        92000, 215000, 6, 2, "unit",
    ),
    (
        "Bolso Tote Verde Oliva",
        "LUA-BOL-TOT-VO",
        ("Bolsos en Trapillo", "Totes"),
        95000, 220000, 5, 2, "unit",
    ),
    # Bolsos en Trapillo > Mochilas
    (
        "Mochila Trapillo Crudo",
        "LUA-BOL-MOC-CR",
        ("Bolsos en Trapillo", "Mochilas"),
        115000, 260000, 4, 1, "unit",
    ),
    (
        "Mochila Trapillo Gris Perla",
        "LUA-BOL-MOC-GP",
        ("Bolsos en Trapillo", "Mochilas"),
        110000, 248000, 3, 1, "unit",
    ),
    # Bolsos en Trapillo > Clutches
    (
        "Clutch Trapillo Rosa Palo",
        "LUA-BOL-CLU-RP",
        ("Bolsos en Trapillo", "Clutches"),
        45000, 108000, 8, 3, "unit",
    ),
    # Alfombras y Tapetes > Redondas
    (
        "Alfombra Redonda 80cm Crudo",
        "LUA-ALF-RED-80",
        ("Alfombras y Tapetes", "Redondas"),
        120000, 278000, 4, 1, "unit",
    ),
    (
        "Alfombra Redonda 1m Terracota",
        "LUA-ALF-RED-100",
        ("Alfombras y Tapetes", "Redondas"),
        152000, 345000, 3, 1, "unit",
    ),
    # Alfombras y Tapetes > Rectangulares
    (
        "Alfombra Rectangular 1.2m Gris",
        "LUA-ALF-REC-120",
        ("Alfombras y Tapetes", "Rectangulares"),
        182000, 415000, 2, 1, "unit",
    ),
    (
        "Alfombra Rectangular 1.5m Beige",
        "LUA-ALF-REC-150",
        ("Alfombras y Tapetes", "Rectangulares"),
        225000, 495000, 2, 1, "unit",
    ),
    # Alfombras y Tapetes > Tapetes de Baño
    (
        "Tapete de Baño Verde Salvia",
        "LUA-ALF-TBA-VS",
        ("Alfombras y Tapetes", "Tapetes de Baño"),
        55000, 128000, 8, 3, "unit",
    ),
    (
        "Tapete de Baño Mostaza",
        "LUA-ALF-TBA-MS",
        ("Alfombras y Tapetes", "Tapetes de Baño"),
        52000, 122000, 9, 3, "unit",
    ),
    # Accesorios > Cestas Organizadoras
    (
        "Cesta Organizadora S Beige",
        "LUA-ACC-CES-S",
        ("Accesorios", "Cestas Organizadoras"),
        22000, 55000, 12, 4, "unit",
    ),
    (
        "Cesta Organizadora M Terracota",
        "LUA-ACC-CES-M",
        ("Accesorios", "Cestas Organizadoras"),
        30000, 72000, 10, 3, "unit",
    ),
    # Accesorios > Posavasos
    (
        "Posavasos Trapillo x4",
        "LUA-ACC-POS-4",
        ("Accesorios", "Posavasos"),
        12000, 32000, 15, 5, "set",
    ),
    # Decoración Hogar > Colgantes de Pared
    (
        "Colgante de Pared Macramé Natural",
        "LUA-DEC-COL-MN",
        ("Decoración Hogar", "Colgantes de Pared"),
        36000, 85000, 7, 2, "unit",
    ),
    # Decoración Hogar > Atrapasueños
    (
        "Atrapasueños Trapillo Grande",
        "LUA-DEC-ATR-G",
        ("Decoración Hogar", "Atrapasueños"),
        28000, 68000, 9, 3, "unit",
    ),
]

# ---------------------------------------------------------------------------
# Clientes (clientas habituales de emprendimiento artesanal colombiano)
# ---------------------------------------------------------------------------

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Valentina",
        "last_name": "Ospina Rueda",
        "document_type": "CC",
        "document_number": "1019847236",
        "email": "valentina.ospina@gmail.com",
        "phone": "+57 310 482 3917",
        "address": "Calle 85 #15-32, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Carolina",
        "last_name": "Herrera Díaz",
        "document_type": "CC",
        "document_number": "43812564",
        "email": "carolina.herrera.d@hotmail.com",
        "phone": "+57 314 739 2048",
        "address": "Carrera 43 #12-20, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Mariana",
        "last_name": "Castro Vélez",
        "document_type": "CC",
        "document_number": "1088291047",
        "email": "mariana.castro@outlook.com",
        "phone": "+57 311 628 4753",
        "address": "Cra 23 #48-10, Versalles",
        "city": "Manizales",
        "country": "Colombia",
    },
    {
        "first_name": "Alejandra",
        "last_name": "Moreno Patiño",
        "document_type": "CC",
        "document_number": "1052384917",
        "email": "alejandra.moreno.p@gmail.com",
        "phone": "+57 316 940 5182",
        "address": "Av. 6N #23-45, Granada",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Isabella",
        "last_name": "Restrepo Gómez",
        "document_type": "CC",
        "document_number": "1037482916",
        "email": "isabella.restrepo@gmail.com",
        "phone": "+57 313 857 6294",
        "address": "Calle 10 #32-80, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Daniela",
        "last_name": "Vargas Suárez",
        "document_type": "CC",
        "document_number": "1015638294",
        "email": "daniela.vargas.s@gmail.com",
        "phone": "+57 318 263 7410",
        "address": "Calle 127 #7-55, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Sofía",
        "last_name": "Jiménez Acosta",
        "document_type": "CC",
        "document_number": "1094728365",
        "email": "sofia.jimenez.a@yahoo.com",
        "phone": "+57 315 184 9036",
        "address": "Cra 36 #55-20, Cabecera del Llano",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Natalia",
        "last_name": "Rodríguez Peña",
        "document_type": "CC",
        "document_number": "1001847362",
        "email": "natalia.rodriguez.p@gmail.com",
        "phone": "+57 312 507 8193",
        "address": "Transversal 82 #47-62, Fontibón",
        "city": "Bogotá",
        "country": "Colombia",
    },
]


def seed(session: Session) -> None:
    """Función principal de seed para Luana."""

    # ── 1. Bootstrap: organización ────────────────────────────────────
    org = crud.get_organization_by_slug(session=session, slug=ORG_SLUG)
    if not org:
        org_in = OrganizationCreate(
            name=ORG_NAME,
            slug=ORG_SLUG,
            description=ORG_DESCRIPTION,
        )
        org = crud.create_organization(session=session, organization_create=org_in)
        logger.info(f"Organización creada: {org.name} ({org.id})")
    else:
        logger.info(f"Organización encontrada: {org.name} ({org.id})")
    org_id = org.id

    # ── 2. Verificar si ya hay datos ──────────────────────────────────
    existing_products = session.exec(
        select(Product)
        .where(Product.organization_id == org_id)
        .where(Product.deleted_at.is_(None))
    ).first()
    if existing_products:
        logger.warning(
            "Los datos de demo ya existen. Saltando seed. Elimina los datos existentes si quieres re-sembrar."
        )
        return

    # ── 3. Roles ──────────────────────────────────────────────────────
    admin_role = crud.get_role_by_name(session=session, name="admin")
    if not admin_role:
        logger.error("Rol 'admin' no encontrado. Ejecuta las migraciones primero.")
        return

    # ── 4. Bootstrap: admin Claudia González ──────────────────────────
    admin_user = crud.get_user_by_email(
        session=session, email=ADMIN_EMAIL, organization_id=org_id
    )
    if not admin_user:
        user_in = UserCreate(
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME,
            phone=ADMIN_PHONE,
            role_id=admin_role.id,
        )
        admin_user = crud.create_user(
            session=session, user_create=user_in, organization_id=org_id
        )
        admin_user.is_verified = True
        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)
        logger.info(f"Admin creada: {admin_user.first_name} {admin_user.last_name}")
    else:
        logger.info(f"Admin encontrada: {admin_user.first_name} {admin_user.last_name}")

    all_sellers = [admin_user]

    # ── 5. Categorías ─────────────────────────────────────────────────
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
    logger.info(f"Categorías creadas: {len(category_map)}")

    # ── 6. Productos ──────────────────────────────────────────────────
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
    logger.info(f"Productos creados: {len(product_list)}")

    # ── 7. Movimientos iniciales de inventario (apertura) ─────────────
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
            reason="Stock inicial - Inventario de apertura Luana",
            created_at=datetime.now(timezone.utc) - timedelta(days=35),
        )
        session.add(movement)
    session.commit()
    logger.info("Movimientos iniciales de inventario creados")

    # ── 8. Clientes ───────────────────────────────────────────────────
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
    logger.info(f"Clientes creados: {len(customer_list)}")

    # ── 9. Ventas (últimos 30 días, escala artesanal) ─────────────────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(30, -1, -1):
        day = now - timedelta(days=days_ago)
        is_weekend = day.weekday() >= 5
        num_sales = random.randint(0, 1) if is_weekend else random.randint(1, 3)

        if days_ago == 0:
            num_sales = random.randint(1, 2)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"LUA-{invoice_counter:06d}"

            seller = random.choice(all_sellers)

            # 90 % de ventas tienen cliente asociado (clientas conocidas)
            customer = random.choice(customer_list) if random.random() < 0.9 else None

            # 1-2 productos por venta (piezas artesanales, no se compran en cantidad)
            num_items = random.randint(1, 2)
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
                qty = 1  # artesanías: siempre una unidad por referencia
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

            # Descuentos pequeños (0-5 %) — amistad, cliente recurrente, etc.
            discount = (
                subtotal * Decimal(str(random.randint(0, 5))) / Decimal("100")
            ).quantize(Decimal("0.01"))
            # Sin IVA: emprendimiento artesanal en Régimen Simple
            tax = Decimal("0.00")
            total = subtotal - discount

            # 70 % transferencia (Nequi / Bancolombia), 30 % efectivo
            payment_method = random.choices(
                ["transfer", "cash"], weights=[70, 30], k=1
            )[0]

            # 2 % de ventas canceladas (muy pocas)
            is_cancelled = random.random() < 0.02 and days_ago > 0
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
                sale.cancelled_at = sale_date + timedelta(hours=random.randint(1, 6))
                sale.cancelled_by = admin_user.id
                sale.cancellation_reason = random.choice(
                    [
                        "Cliente cambió de opinión",
                        "Producto reservado para otra clienta",
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

    logger.info(f"Ventas creadas: {total_sales} (últimos 30 días)")

    # ── 10. Reposición de productos con stock bajo ────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            # Luana produce en pequeñas tandas: 3-8 unidades por reposición
            restock_qty = random.randint(3, 8)
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
                reason="Nueva tanda artesanal — reposición de inventario",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            )
            session.add(movement)
            session.add(product)

    session.commit()
    logger.info("Reposición de inventario finalizada")

    logger.info("=" * 60)
    logger.info("SEED LUANA COMPLETO!")
    logger.info(f"  Organización: {org.name} (slug: {ORG_SLUG})")
    logger.info(f"  Categorías:   {len(category_map)}")
    logger.info(f"  Productos:    {len(product_list)}")
    logger.info(f"  Clientes:     {len(customer_list)}")
    logger.info(f"  Ventas:       {total_sales}")
    logger.info("")
    logger.info("Credenciales de acceso:")
    logger.info(f"  Email:        {ADMIN_EMAIL}")
    logger.info(f"  Contraseña:   {ADMIN_PASSWORD}")
    logger.info("=" * 60)


def main() -> None:
    random.seed(42)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
