"""
Seed script for Frozt Bitez — tienda online colombiana de uvas congeladas acidulces.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_frozt_bitez.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - E-commerce especializado en uvas sin semilla congeladas con recubrimientos acidulces
  - Cuatro sabores individuales + combo, precios en COP tomados de froztbitez.com
  - Sales history simulates Jan–Apr 2026 (118 days)
  - Tienda online: tarjeta y transferencia son los métodos de pago principales
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
# Target organization
# ---------------------------------------------------------------------------

ORG_SLUG = "frozt-bitez"

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Uvas Congeladas Acidulces",
        "description": "Uvas sin semilla congeladas con recubrimientos acidulces de alta calidad",
        "children": [
            {
                "name": "Sabores Individuales",
                "description": "Uvas congeladas en sabores únicos — Maracumango, Limonada Cerezada, Sandía y Frutos Rojos",
            },
            {
                "name": "Combos y Promos",
                "description": "Combos con descuento y promociones especiales con envío gratis",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Products
# (name, sku, cat_leaf, price_cop, initial_stock, stock_min)
# initial_stock = stock_actual + v_ene + v_feb + v_mar + v_abr
# cost_price ≈ 50% of sale price
# ---------------------------------------------------------------------------


def _cost(price: int, pct: float = 0.50) -> int:
    return max(1, int(price * pct))


# stock = current + jan + feb + mar + apr_partial
_FB_RAW: list[tuple] = [
    # Sabores Individuales
    ("Frozt Bitez Maracumango",                              "FB-001", "Sabores Individuales", 29900, 15+30+35+38+25, 5),
    ("Frozt Bitez Limonada Cerezada",                        "FB-002", "Sabores Individuales", 29900, 12+25+30+34+22, 5),
    ("Frozt Bitez Sandía",                                   "FB-003", "Sabores Individuales", 29900, 14+28+32+36+24, 5),
    ("Frozt Bitez Frutos Rojos",                             "FB-004", "Sabores Individuales", 29900, 13+27+31+34+21, 5),
    # Combos
    ("Combo Favoritos — Maracumango + Sandía + Frutos Rojos","FB-005", "Combos y Promos",      59900,  8+15+18+20+12, 3),
]

PRODUCTS: list[tuple] = []
for name, sku, cat_leaf, price, initial_stock, stock_min in _FB_RAW:
    cost = _cost(price, 0.50)
    PRODUCTS.append((name, sku, ("Uvas Congeladas Acidulces", cat_leaf), cost, price, max(initial_stock, 1), stock_min, "unit"))

# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Valentina",
        "last_name": "Gómez Ríos",
        "document_type": "CC",
        "document_number": "1020345678",
        "email": "valentina.gomez@gmail.com",
        "phone": "+57 311 234 5678",
        "address": "Cra. 11 # 93-40, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Santiago",
        "last_name": "Vargas Ospina",
        "document_type": "CC",
        "document_number": "1032456789",
        "email": "santi.vargas@gmail.com",
        "phone": "+57 314 345 6789",
        "address": "Cll. 10 # 43E-55, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Daniela",
        "last_name": "Moreno Castro",
        "document_type": "CC",
        "document_number": "1015567890",
        "email": "daniela.moreno@hotmail.com",
        "phone": "+57 320 456 7890",
        "address": "Cra. 70 # 45-12, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Sebastián",
        "last_name": "Ruiz Herrera",
        "document_type": "CC",
        "document_number": "1143678901",
        "email": "sebas.ruiz@gmail.com",
        "phone": "+57 316 567 8901",
        "address": "Cll. 5N # 38-40, Norte",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Isabella",
        "last_name": "Torres Salcedo",
        "document_type": "CC",
        "document_number": "1006789012",
        "email": "isa.torres@gmail.com",
        "phone": "+57 312 678 9012",
        "address": "Cll. 82 # 11-37, Barrio El Prado",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Camila",
        "last_name": "Peña Lozano",
        "document_type": "CC",
        "document_number": "1018901234",
        "email": "camila.pena@gmail.com",
        "phone": "+57 318 789 0123",
        "address": "Cra. 27 # 51-33, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Mateo",
        "last_name": "López Quintero",
        "document_type": "CC",
        "document_number": "1094012345",
        "email": "mateo.lopez@outlook.com",
        "phone": "+57 317 890 1234",
        "address": "Cll. 19 # 7-12, Centro",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Laura",
        "last_name": "Martínez Díaz",
        "document_type": "CC",
        "document_number": "1019123456",
        "email": "laura.mtz@gmail.com",
        "phone": "+57 313 901 2345",
        "address": "Cll. 116 # 17-26, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Andrés",
        "last_name": "García Muñoz",
        "document_type": "CC",
        "document_number": "1065234567",
        "email": "andres.garcia@gmail.com",
        "phone": "+57 321 012 3456",
        "address": "Cra. 53 # 76-98",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Natalia",
        "last_name": "Ramírez Arango",
        "document_type": "CC",
        "document_number": "1040345678",
        "email": "nata.ramirez@gmail.com",
        "phone": "+57 315 123 4567",
        "address": "Cra. 43A # 14-24, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Julián",
        "last_name": "Castro Bermúdez",
        "document_type": "CC",
        "document_number": "1073456789",
        "email": "julian.castro@gmail.com",
        "phone": "+57 310 234 5678",
        "address": "Av. 6N # 23-40, Granada",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "María José",
        "last_name": "Sánchez Flórez",
        "document_type": "CC",
        "document_number": "1053567890",
        "email": "mj.sanchez@gmail.com",
        "phone": "+57 319 345 6789",
        "address": "Cll. 33 # 8-52, Manga",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Felipe",
        "last_name": "Ortiz Pardo",
        "document_type": "CC",
        "document_number": "1085678901",
        "email": "felipe.ortiz@gmail.com",
        "phone": "+57 304 456 7890",
        "address": "Cra. 5 # 17-40, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Sara",
        "last_name": "Jiménez Cardona",
        "document_type": "CC",
        "document_number": "1017789012",
        "email": "sara.jimenez@gmail.com",
        "phone": "+57 322 567 8901",
        "address": "Cra. 23 # 62-10, La Enea",
        "city": "Manizales",
        "country": "Colombia",
    },
    {
        "first_name": "Tomás",
        "last_name": "Cárdenas Reyes",
        "document_type": "CC",
        "document_number": "1036901234",
        "email": "tomas.cardenas@gmail.com",
        "phone": "+57 316 678 9012",
        "address": "Cll. 72 # 11-39, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Alejandra",
        "last_name": "Vega Montoya",
        "document_type": "CC",
        "document_number": "1007012345",
        "email": "ale.vega@gmail.com",
        "phone": "+57 311 789 0123",
        "address": "Cll. 10 # 32-22, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "David",
        "last_name": "Rojas Suárez",
        "document_type": "CC",
        "document_number": "1098123456",
        "email": "david.rojas@gmail.com",
        "phone": "+57 318 890 1234",
        "address": "Cra. 9 # 13-55, Centro",
        "city": "Armenia",
        "country": "Colombia",
    },
    {
        "first_name": "Sofía",
        "last_name": "Acosta Niño",
        "document_type": "CC",
        "document_number": "1024234567",
        "email": "sofia.acosta@gmail.com",
        "phone": "+57 320 901 2345",
        "address": "Cra. 15 # 118-43, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Esteban",
        "last_name": "Ríos Palacio",
        "document_type": "CC",
        "document_number": "1002345678",
        "email": "esteban.rios@gmail.com",
        "phone": "+57 313 012 3456",
        "address": "Cll. 34 # 65-10, Belén",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Manuela",
        "last_name": "Guerrero Patiño",
        "document_type": "CC",
        "document_number": "1047456789",
        "email": "manuela.guerrero@gmail.com",
        "phone": "+57 314 123 4567",
        "address": "Cra. 3 # 10-25, Bocagrande",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Juan Pablo",
        "last_name": "Herrera Molina",
        "document_type": "CC",
        "document_number": "1110567890",
        "email": "jp.herrera@gmail.com",
        "phone": "+57 312 234 5678",
        "address": "Cll. 17 # 14-30, Centro",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Valeria",
        "last_name": "Cruz Betancourt",
        "document_type": "CC",
        "document_number": "1028678901",
        "email": "valeria.cruz@gmail.com",
        "phone": "+57 317 345 6789",
        "address": "Cra. 58 # 80-45",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Nicolás",
        "last_name": "Mendoza Álvarez",
        "document_type": "CC",
        "document_number": "1083789012",
        "email": "nicolas.mendoza@gmail.com",
        "phone": "+57 319 456 7890",
        "address": "Cll. 45 # 9-18, La Soledad",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Luisa",
        "last_name": "Pineda Castaño",
        "document_type": "CC",
        "document_number": "1060901234",
        "email": "luisa.pineda@hotmail.com",
        "phone": "+57 315 567 8901",
        "address": "Av. El Poblado # 14-30, Patio Bonito",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Simón",
        "last_name": "Aguirre Toro",
        "document_type": "CC",
        "document_number": "1045012345",
        "email": "simon.aguirre@gmail.com",
        "phone": "+57 321 678 9012",
        "address": "Cra. 12 # 23-15, Centro",
        "city": "Manizales",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "fabianrincon@froztbitez.com",
        "first_name": "Fabian",
        "last_name": "Rincon",
        "phone": "+57 315 910 7649",
    },
    {
        "email": "frozt@froztbitez.com",
        "first_name": "Frozt",
        "last_name": "Bitez",
        "phone": "+57 315 910 7650",
    },
]

PAYMENT_METHODS = ["card", "transfer", "card", "transfer", "cash"]  # weighted towards online methods
IVA_RATE = Decimal("0.19")

# Sales period: Jan 1 – Apr 28, 2026
SALES_START = datetime(2026, 1, 1, tzinfo=timezone.utc)
SALES_DAYS = 118  # Jan 1 to Apr 28 inclusive


def seed(session: Session) -> None:
    """Main seed function for Frozt Bitez demo data."""

    # ── 1. Get the target organization ───────────────────────────────
    org = session.exec(
        select(Organization).where(Organization.slug == ORG_SLUG)
    ).first()
    if not org:
        logger.error(f"Organization '{ORG_SLUG}' not found. Create it first.")
        return
    org_id = org.id
    logger.info(f"Using organization: {org.name} ({org_id})")

    existing = session.exec(
        select(Product)
        .where(Product.organization_id == org_id)
        .where(Product.deleted_at.is_(None))
    ).first()
    if existing:
        logger.warning("Demo data already exists. Skipping seed.")
        return

    # ── 2. Roles ─────────────────────────────────────────────────────
    admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
    seller_role = session.exec(select(Role).where(Role.name == "seller")).first()
    if not admin_role or not seller_role:
        logger.error("Roles not found. Run migrations first.")
        return

    # ── 3. Admin user ─────────────────────────────────────────────────
    admin_user = session.exec(
        select(User)
        .where(User.organization_id == org_id)
        .where(User.role_id == admin_role.id)
        .where(User.deleted_at.is_(None))
    ).first()
    if not admin_user:
        logger.error("Admin user not found.")
        return

    # ── 4. Seller users ───────────────────────────────────────────────
    sellers: list[User] = []
    for sd in SELLER_USERS:
        existing_u = session.exec(
            select(User).where(User.email == sd["email"]).where(User.organization_id == org_id)
        ).first()
        if existing_u:
            sellers.append(existing_u)
            continue
        user = User(
            organization_id=org_id,
            role_id=seller_role.id,
            email=sd["email"],
            hashed_password=get_password_hash("seller123"),
            first_name=sd["first_name"],
            last_name=sd["last_name"],
            phone=sd["phone"],
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

    # ── 5. Categories ─────────────────────────────────────────────────
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

    # ── 6. Products ───────────────────────────────────────────────────
    product_list: list[Product] = []
    for name, sku, cat_path, cost, price, stock, stock_min, unit in PRODUCTS:
        category = (
            category_map.get(cat_path[1]) if len(cat_path) > 1 else category_map.get(cat_path[0])
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

    # ── 7. Initial inventory (Jan 1, 2026) ────────────────────────────
    for product in product_list:
        session.add(InventoryMovement(
            organization_id=org_id,
            product_id=product.id,
            user_id=admin_user.id,
            movement_type="purchase",
            quantity=product.stock_quantity,
            previous_stock=0,
            new_stock=product.stock_quantity,
            reference_type="adjustment",
            reason="Stock inicial — Inventario apertura Frozt Bitez Ene 2026",
            created_at=SALES_START - timedelta(days=1),
        ))
    session.commit()
    logger.info("Created initial inventory movements")

    # ── 8. Customers ──────────────────────────────────────────────────
    customer_list: list[Customer] = []
    for cust_data in CUSTOMERS_DATA:
        customer = Customer(organization_id=org_id, **cust_data, is_active=True)
        session.add(customer)
        customer_list.append(customer)
    session.commit()
    for c in customer_list:
        session.refresh(c)
    logger.info(f"Created {len(customer_list)} customers")

    # ── 9. Sales — Jan 1 to Apr 28, 2026 (online snack store pattern) ─
    invoice_counter = 0
    total_sales = 0

    for day_offset in range(SALES_DAYS + 1):
        day = SALES_START + timedelta(days=day_offset)
        weekday = day.weekday()

        # Online snack store: peak on Fri-Sun (impulse buys / weekend treats)
        if weekday == 6:          # Sunday
            num_sales = random.randint(4, 9)
        elif weekday == 5:        # Saturday
            num_sales = random.randint(5, 10)
        elif weekday == 4:        # Friday
            num_sales = random.randint(4, 8)
        else:                     # Mon–Thu
            num_sales = random.randint(2, 6)

        # Last day (today)
        if day_offset == SALES_DAYS:
            num_sales = random.randint(3, 7)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"FB-{invoice_counter:05d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.75 else None

            # Online orders: 1-3 items per order
            num_items = random.randint(1, 3)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(9, 22)
            sale_date = day.replace(
                hour=sale_hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
                microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = 1
                item_subtotal = prod.sale_price * qty
                subtotal += item_subtotal
                items_data.append({
                    "product_id": prod.id,
                    "product_name": prod.name,
                    "product_sku": prod.sku,
                    "quantity": qty,
                    "unit_price": prod.sale_price,
                    "subtotal": item_subtotal,
                })

            # Occasional discount for loyal customers (5% or 10%)
            discount_pct = random.choice([0, 0, 0, 5, 10]) if customer else 0
            discount = (subtotal * Decimal(str(discount_pct)) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.02 and day_offset > 0
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
                sale.cancellation_reason = random.choice([
                    "Cliente no completó el pago",
                    "Producto sin stock disponible",
                    "Error en la dirección de envío",
                    "Cliente canceló el pedido",
                    "Fallo en el procesador de pagos",
                ])
                sale.updated_at = sale.cancelled_at

            session.add(sale)
            session.flush()

            for item_data in items_data:
                session.add(SaleItem(sale_id=sale.id, **item_data, created_at=sale_date))

            if status == "completed":
                for item_data in items_data:
                    prod_obj = next(p for p in product_list if p.id == item_data["product_id"])
                    prev_stock = prod_obj.stock_quantity
                    prod_obj.stock_quantity = max(0, prod_obj.stock_quantity - item_data["quantity"])
                    session.add(InventoryMovement(
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
                    ))
                if customer:
                    customer.total_purchases += total
                    customer.purchases_count += 1
                    customer.last_purchase_at = sale_date

            total_sales += 1

    session.commit()
    logger.info(f"Created {total_sales} sales from Jan 1 to Apr 28, 2026")

    # ── 10. Restock low-inventory products ───────────────────────────
    now = datetime.now(timezone.utc)
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(20, 60)
            prev = product.stock_quantity
            product.stock_quantity += restock_qty
            session.add(InventoryMovement(
                organization_id=org_id,
                product_id=product.id,
                user_id=admin_user.id,
                movement_type="purchase",
                quantity=restock_qty,
                previous_stock=prev,
                new_stock=product.stock_quantity,
                reference_type="purchase",
                reason="Reposición de inventario Frozt Bitez",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED FROZT BITEZ COMPLETE!")
    logger.info(f"  Organización: {org.name}")
    logger.info(f"  Categorías:   {len(category_map)}")
    logger.info(f"  Productos:    {len(product_list)}")
    logger.info(f"  Clientes:     {len(customer_list)}")
    logger.info(f"  Ventas:       {total_sales}")
    logger.info(f"  Vendedores:   {len(all_sellers)}")
    logger.info("")
    logger.info("Credenciales de acceso:")
    for sd in SELLER_USERS:
        logger.info(f"  Seller: {sd['email']} / seller123")
    logger.info("=" * 60)


def main() -> None:
    random.seed(57)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
