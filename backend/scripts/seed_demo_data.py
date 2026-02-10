"""
Seed script to populate the database with realistic demo data for presentations.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_demo_data.py

This script is idempotent: it checks for existing data before inserting.
It creates data within the "default" organization using the existing superuser.
"""

import random
import uuid
import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.models import (
    Organization,
    User,
    Role,
    Category,
    Product,
    Customer,
    Sale,
    SaleItem,
    InventoryMovement,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Demo data definitions
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Electrónica",
        "description": "Dispositivos y accesorios electrónicos",
        "children": [
            {"name": "Smartphones", "description": "Teléfonos inteligentes"},
            {"name": "Accesorios", "description": "Cargadores, cables, fundas"},
            {"name": "Audio", "description": "Audífonos y parlantes"},
        ],
    },
    {
        "name": "Ropa",
        "description": "Prendas de vestir",
        "children": [
            {"name": "Camisetas", "description": "Camisetas casuales y deportivas"},
            {"name": "Pantalones", "description": "Jeans, joggers y pantalones"},
            {"name": "Calzado", "description": "Zapatillas y zapatos"},
        ],
    },
    {
        "name": "Hogar",
        "description": "Artículos para el hogar",
        "children": [
            {"name": "Cocina", "description": "Utensilios y electrodomésticos"},
            {"name": "Decoración", "description": "Adornos y accesorios decorativos"},
        ],
    },
    {
        "name": "Alimentos",
        "description": "Productos alimenticios y bebidas",
        "children": [
            {"name": "Bebidas", "description": "Jugos, aguas y refrescos"},
            {"name": "Snacks", "description": "Galletas, chips y dulces"},
        ],
    },
]

# (name, sku, category_path, cost, sale_price, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Electrónica > Smartphones
    ("iPhone 15 128GB", "ELEC-IP15-128", ("Electrónica", "Smartphones"), 799, 999, 25, 5, "unit"),
    ("Samsung Galaxy S24", "ELEC-SGS24", ("Electrónica", "Smartphones"), 699, 899, 18, 5, "unit"),
    ("Xiaomi Redmi Note 13", "ELEC-XRN13", ("Electrónica", "Smartphones"), 199, 299, 40, 10, "unit"),
    # Electrónica > Accesorios
    ("Cargador USB-C 20W", "ELEC-CHRG20", ("Electrónica", "Accesorios"), 8, 19.99, 150, 30, "unit"),
    ("Funda Silicona Universal", "ELEC-FUND-U", ("Electrónica", "Accesorios"), 3, 12.99, 200, 50, "unit"),
    ("Cable Lightning 1m", "ELEC-CBL-LT", ("Electrónica", "Accesorios"), 4, 14.99, 120, 25, "unit"),
    # Electrónica > Audio
    ("AirPods Pro 2", "ELEC-APP2", ("Electrónica", "Audio"), 179, 249, 30, 8, "unit"),
    ("JBL Flip 6", "ELEC-JBL-F6", ("Electrónica", "Audio"), 89, 129, 20, 5, "unit"),
    ("Sony WH-1000XM5", "ELEC-SNYWH5", ("Electrónica", "Audio"), 249, 349, 12, 3, "unit"),
    # Ropa > Camisetas
    ("Camiseta Algodón Básica", "ROPA-CAM-BAS", ("Ropa", "Camisetas"), 5, 19.99, 300, 50, "unit"),
    ("Polo Deportivo Dry-Fit", "ROPA-POLO-DF", ("Ropa", "Camisetas"), 12, 34.99, 150, 30, "unit"),
    ("Camiseta Estampada Urban", "ROPA-CAM-URB", ("Ropa", "Camisetas"), 8, 24.99, 180, 40, "unit"),
    # Ropa > Pantalones
    ("Jean Slim Fit Azul", "ROPA-JEAN-SF", ("Ropa", "Pantalones"), 18, 49.99, 120, 20, "unit"),
    ("Jogger Deportivo Negro", "ROPA-JOG-NEG", ("Ropa", "Pantalones"), 14, 39.99, 100, 20, "unit"),
    # Ropa > Calzado
    ("Zapatilla Running Pro", "ROPA-ZAP-RUN", ("Ropa", "Calzado"), 45, 89.99, 60, 10, "unit"),
    ("Zapato Casual Cuero", "ROPA-ZAP-CAS", ("Ropa", "Calzado"), 35, 69.99, 40, 8, "unit"),
    # Hogar > Cocina
    ("Licuadora 600W", "HOGR-LIC-600", ("Hogar", "Cocina"), 25, 59.99, 35, 8, "unit"),
    ("Set Cuchillos x6", "HOGR-CUCH-6", ("Hogar", "Cocina"), 12, 34.99, 50, 10, "unit"),
    ("Sartén Antiadherente 28cm", "HOGR-SART28", ("Hogar", "Cocina"), 10, 29.99, 45, 10, "unit"),
    # Hogar > Decoración
    ("Lámpara LED Escritorio", "HOGR-LAMP-E", ("Hogar", "Decoración"), 15, 39.99, 40, 8, "unit"),
    ("Reloj de Pared Moderno", "HOGR-RELOJ", ("Hogar", "Decoración"), 8, 24.99, 30, 5, "unit"),
    # Alimentos > Bebidas
    ("Agua Mineral 600ml x12", "ALIM-AGUA-12", ("Alimentos", "Bebidas"), 3, 8.99, 500, 100, "pack"),
    ("Jugo de Naranja 1L", "ALIM-JUGO-NJ", ("Alimentos", "Bebidas"), 2, 5.99, 200, 50, "unit"),
    ("Gaseosa Cola 500ml", "ALIM-COLA-500", ("Alimentos", "Bebidas"), 1, 2.99, 400, 80, "unit"),
    # Alimentos > Snacks
    ("Galletas Chocolate x6", "ALIM-GALL-CH", ("Alimentos", "Snacks"), 1.5, 4.99, 250, 60, "pack"),
    ("Chips Papas Sal 150g", "ALIM-CHIP-SAL", ("Alimentos", "Snacks"), 1, 3.49, 300, 70, "unit"),
    ("Barra Cereal x10", "ALIM-BARR-10", ("Alimentos", "Snacks"), 3, 9.99, 150, 30, "pack"),
]

CUSTOMERS_DATA: list[dict] = [
    {"first_name": "Carlos", "last_name": "Mendoza", "document_type": "DNI", "document_number": "45678901", "email": "carlos.mendoza@gmail.com", "phone": "+51 987 654 321", "address": "Av. Arequipa 1234, Lima", "city": "Lima", "country": "Perú"},
    {"first_name": "María", "last_name": "García López", "document_type": "DNI", "document_number": "32145678", "email": "maria.garcia@hotmail.com", "phone": "+51 912 345 678", "address": "Jr. Cusco 567, Miraflores", "city": "Lima", "country": "Perú"},
    {"first_name": "José", "last_name": "Ramírez Torres", "document_type": "DNI", "document_number": "78901234", "email": "jose.ramirez@outlook.com", "phone": "+51 945 678 123", "address": "Calle Los Olivos 890", "city": "Arequipa", "country": "Perú"},
    {"first_name": "Ana", "last_name": "Fernández", "document_type": "DNI", "document_number": "56789012", "email": "ana.fernandez@gmail.com", "phone": "+51 923 456 789", "address": "Av. La Marina 456", "city": "Lima", "country": "Perú"},
    {"first_name": "Luis", "last_name": "Chávez Díaz", "document_type": "DNI", "document_number": "89012345", "email": "luis.chavez@yahoo.com", "phone": "+51 967 890 123", "address": "Calle Tacna 321", "city": "Trujillo", "country": "Perú"},
    {"first_name": "Rosa", "last_name": "Huamán Quispe", "document_type": "DNI", "document_number": "23456789", "email": "rosa.huaman@gmail.com", "phone": "+51 934 567 890", "address": "Av. Ejército 654", "city": "Cusco", "country": "Perú"},
    {"first_name": "Pedro", "last_name": "Silva Morales", "document_type": "DNI", "document_number": "67890123", "email": "pedro.silva@gmail.com", "phone": "+51 978 901 234", "address": "Jr. Puno 789", "city": "Lima", "country": "Perú"},
    {"first_name": "Carmen", "last_name": "López Vega", "document_type": "DNI", "document_number": "34567890", "email": "carmen.lopez@hotmail.com", "phone": "+51 956 789 012", "address": "Av. Brasil 1011", "city": "Lima", "country": "Perú"},
    {"first_name": "Distribuciones ABC", "last_name": "S.A.C.", "document_type": "RUC", "document_number": "20456789012", "email": "ventas@abc-dist.com", "phone": "+51 1 234 5678", "address": "Zona Industrial Lote 5", "city": "Callao", "country": "Perú"},
    {"first_name": "Importadora Global", "last_name": "E.I.R.L.", "document_type": "RUC", "document_number": "20567890123", "email": "contacto@importglobal.pe", "phone": "+51 1 345 6789", "address": "Av. Argentina 2500", "city": "Lima", "country": "Perú"},
    {"first_name": "Diego", "last_name": "Vargas Rojas", "document_type": "DNI", "document_number": "90123456", "email": "diego.vargas@gmail.com", "phone": "+51 989 012 345", "address": "Calle Libertad 432", "city": "Piura", "country": "Perú"},
    {"first_name": "Sofía", "last_name": "Paredes Castro", "document_type": "DNI", "document_number": "12345679", "email": "sofia.paredes@outlook.com", "phone": "+51 912 345 679", "address": "Av. Salaverry 876", "city": "Lima", "country": "Perú"},
]

SELLER_USERS: list[dict] = [
    {"email": "vendedor1@orbitengine.com", "first_name": "Juan", "last_name": "Pérez", "phone": "+51 911 111 111"},
    {"email": "vendedor2@orbitengine.com", "first_name": "Lucía", "last_name": "Torres", "phone": "+51 922 222 222"},
]

PAYMENT_METHODS = ["cash", "card", "transfer"]


def seed(session: Session) -> None:
    """Main seed function."""

    # ── 1. Get the default organization ──────────────────────────────
    org = session.exec(
        select(Organization).where(Organization.slug == "default")
    ).first()
    if not org:
        logger.error("Default organization not found. Run initial_data.py first.")
        return
    org_id = org.id
    logger.info(f"Using organization: {org.name} ({org_id})")

    # Check if data already exists
    existing_products = session.exec(
        select(Product).where(Product.organization_id == org_id).where(Product.deleted_at.is_(None))
    ).first()
    if existing_products:
        logger.warning("Demo data already exists. Skipping seed. Delete existing data first if you want to re-seed.")
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
    category_map: dict[str, Category] = {}  # "Parent/Child" -> Category

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
        # cat_path is ("Parent", "Child")
        category = category_map.get(cat_path[1]) if len(cat_path) > 1 else category_map.get(cat_path[0])
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
            reason="Stock inicial - Inventario de apertura",
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

    # Generate between 3-8 sales per day for the last 30 days
    for days_ago in range(30, -1, -1):
        day = now - timedelta(days=days_ago)
        # More sales on weekdays, fewer on weekends
        is_weekend = day.weekday() >= 5
        num_sales = random.randint(1, 4) if is_weekend else random.randint(3, 8)

        # Today should have a decent number of sales for the demo
        if days_ago == 0:
            num_sales = random.randint(5, 8)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"INV-{invoice_counter:06d}"

            # Pick a random seller
            seller = random.choice(all_sellers)

            # 70% chance of having an associated customer
            customer = random.choice(customer_list) if random.random() < 0.7 else None

            # Pick 1-5 random products for this sale
            num_items = random.randint(1, 5)
            sale_products = random.sample(
                product_list, min(num_items, len(product_list))
            )

            # Random time during business hours (8am - 8pm)
            sale_hour = random.randint(8, 20)
            sale_minute = random.randint(0, 59)
            sale_date = day.replace(
                hour=sale_hour, minute=sale_minute, second=random.randint(0, 59),
                microsecond=0,
            )

            # Build sale items
            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = random.randint(1, 4)
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

            # Random discount (0-10% of subtotal)
            discount = (subtotal * Decimal(str(random.randint(0, 10))) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * Decimal("0.18")).quantize(Decimal("0.01"))  # 18% IGV
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)

            # Occasional cancelled sale (5%)
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
                sale.cancellation_reason = random.choice([
                    "Cliente cambió de opinión",
                    "Producto defectuoso",
                    "Error en la orden",
                ])

            session.add(sale)
            session.flush()

            # Create sale items
            for item_data in items_data:
                sale_item = SaleItem(
                    sale_id=sale.id,
                    **item_data,
                    created_at=sale_date,
                )
                session.add(sale_item)

            # Create inventory movements for completed sales
            if status == "completed":
                for item_data in items_data:
                    prod_obj = next(p for p in product_list if p.id == item_data["product_id"])
                    prev_stock = prod_obj.stock_quantity
                    prod_obj.stock_quantity = max(0, prod_obj.stock_quantity - item_data["quantity"])
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

                # Update customer purchase stats
                if customer:
                    customer.total_purchases += total
                    customer.purchases_count += 1
                    customer.last_purchase_at = sale_date

            total_sales += 1

    session.commit()

    # Refresh product stock (they were modified in-memory)
    for p in product_list:
        session.add(p)
    for c in customer_list:
        session.add(c)
    session.commit()

    logger.info(f"Created {total_sales} sales over the last 30 days")

    # ── 10. Add some recent restocking movements ─────────────────────
    # Simulate restocking for products with low stock
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(20, 80)
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
                reason="Reposición de inventario",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            )
            session.add(movement)
            session.add(product)

    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED COMPLETE!")
    logger.info(f"  Organization: {org.name}")
    logger.info(f"  Categories:   {len(category_map)}")
    logger.info(f"  Products:     {len(product_list)}")
    logger.info(f"  Customers:    {len(customer_list)}")
    logger.info(f"  Sales:        {total_sales}")
    logger.info(f"  Sellers:      {len(all_sellers)} (admin + {len(sellers)} sellers)")
    logger.info("")
    logger.info("Login credentials:")
    logger.info(f"  Admin:    admin@example.com / changethis")
    for sd in SELLER_USERS:
        logger.info(f"  Seller:   {sd['email']} / seller123")
    logger.info("=" * 60)


def main() -> None:
    random.seed(42)  # Reproducible results
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
