"""
Seed script for Moda Andes — Colombian mid-range fashion and accessories retailer.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_moda_andes.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - Products: women's/men's/kids' clothing, footwear, bags and accessories
  - Prices in COP, mid-range Colombian fashion pricing
  - IVA 19% (Colombia)
  - Higher sales on weekends and paydays (end/mid month)
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
# Target organization
# ---------------------------------------------------------------------------

ORG_SLUG = "moda-andes"

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Mujer",
        "description": "Ropa y moda para mujer",
        "children": [
            {"name": "Blusas y Tops", "description": "Blusas casuales, de vestir, tops y camisetas"},
            {"name": "Pantalones y Jeans", "description": "Jeans, pantalones de tela y joggers mujer"},
            {"name": "Vestidos y Faldas", "description": "Vestidos casuales, de cóctel, faldas midi y mini"},
            {"name": "Chaquetas y Abrigos", "description": "Chaquetas de jean, bomber, abrigos y suéteres"},
            {"name": "Ropa Interior y Pijamas", "description": "Conjuntos íntimos, bralettes y pijamas"},
        ],
    },
    {
        "name": "Hombre",
        "description": "Ropa y moda para hombre",
        "children": [
            {"name": "Camisas y Polos", "description": "Camisas de manga larga, corta, polos y camisetas"},
            {"name": "Pantalones Hombre", "description": "Jeans, pantalones chinos y cargo"},
            {"name": "Chaquetas Hombre", "description": "Chaquetas de jean, cortavientos y sacos"},
            {"name": "Ropa Interior Hombre", "description": "Boxes, briefs y medias"},
        ],
    },
    {
        "name": "Niños",
        "description": "Moda infantil y juvenil",
        "children": [
            {"name": "Niñas (2-14 años)", "description": "Vestidos, blusas, pantalones y conjuntos para niñas"},
            {"name": "Niños (2-14 años)", "description": "Camisetas, pantalones y conjuntos para niños"},
            {"name": "Bebé (0-24 meses)", "description": "Bodys, mameluco, conjuntos y ajuares de bebé"},
        ],
    },
    {
        "name": "Calzado",
        "description": "Zapatos, sandalias y sneakers",
        "children": [
            {"name": "Calzado Mujer", "description": "Tacones, bailarinas, botas y sneakers mujer"},
            {"name": "Calzado Hombre", "description": "Mocasines, zapatos de cuero, sneakers hombre"},
            {"name": "Calzado Niños", "description": "Zapatos escolares, tenis y sandalias infantiles"},
        ],
    },
    {
        "name": "Accesorios",
        "description": "Bolsos, cinturones, joyería y más",
        "children": [
            {"name": "Bolsos y Carteras", "description": "Bolsos de cuero, sintéticos, tote bags y clutch"},
            {"name": "Cinturones", "description": "Cinturones de cuero y textiles para hombre y mujer"},
            {"name": "Bisutería y Joyería", "description": "Aretes, collares, pulseras y anillos de moda"},
            {"name": "Gorras y Sombreros", "description": "Gorras de béisbol, snapback y sombreros"},
        ],
    },
    {
        "name": "Ropa Deportiva",
        "description": "Outfit para gym, yoga y actividades al aire libre",
        "children": [
            {"name": "Leggins y Shorts", "description": "Leggins deportivos, shorts y pantalonetas"},
            {"name": "Camisetas y Tops Deportivos", "description": "Camisetas funcionales, sports bra y tanks"},
        ],
    },
]

# (name, sku, category_path, cost_cop, sale_price_cop, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Mujer > Blusas y Tops
    ("Blusa Gasa Estampada Mujer", "MA-MU-001", ("Mujer", "Blusas y Tops"), 28000, 59900, 80, 15, "unit"),
    ("Camiseta Básica Cuello Redondo Mujer", "MA-MU-002", ("Mujer", "Blusas y Tops"), 18000, 39900, 120, 20, "unit"),
    ("Top Corto Rib Mujer", "MA-MU-003", ("Mujer", "Blusas y Tops"), 22000, 49900, 90, 15, "unit"),
    ("Blusa Off-Shoulder Mujer", "MA-MU-004", ("Mujer", "Blusas y Tops"), 32000, 69900, 60, 12, "unit"),
    ("Camisa de Lino Beige Mujer", "MA-MU-005", ("Mujer", "Blusas y Tops"), 42000, 89900, 50, 10, "unit"),
    # Mujer > Pantalones y Jeans
    ("Jean Skinny Tiro Alto Mujer", "MA-MU-006", ("Mujer", "Pantalones y Jeans"), 55000, 119900, 70, 12, "unit"),
    ("Jean Mom Fit Mujer", "MA-MU-007", ("Mujer", "Pantalones y Jeans"), 58000, 124900, 65, 12, "unit"),
    ("Pantalón Wide Leg Mujer", "MA-MU-008", ("Mujer", "Pantalones y Jeans"), 48000, 104900, 50, 10, "unit"),
    ("Jogger Cargo Mujer", "MA-MU-009", ("Mujer", "Pantalones y Jeans"), 38000, 84900, 55, 10, "unit"),
    # Mujer > Vestidos y Faldas
    ("Vestido Midi Floral Mujer", "MA-MU-010", ("Mujer", "Vestidos y Faldas"), 62000, 134900, 45, 8, "unit"),
    ("Vestido Mini Ajustado Mujer", "MA-MU-011", ("Mujer", "Vestidos y Faldas"), 55000, 119900, 40, 8, "unit"),
    ("Falda Midi Satinada Mujer", "MA-MU-012", ("Mujer", "Vestidos y Faldas"), 42000, 92900, 50, 10, "unit"),
    ("Vestido Casual Straps Mujer", "MA-MU-013", ("Mujer", "Vestidos y Faldas"), 48000, 104900, 45, 8, "unit"),
    # Mujer > Chaquetas y Abrigos
    ("Chaqueta Jean Clásica Mujer", "MA-MU-014", ("Mujer", "Chaquetas y Abrigos"), 68000, 149900, 35, 6, "unit"),
    ("Blazer Oversize Mujer", "MA-MU-015", ("Mujer", "Chaquetas y Abrigos"), 78000, 169900, 30, 6, "unit"),
    ("Suéter Tejido Cuello Alto Mujer", "MA-MU-016", ("Mujer", "Chaquetas y Abrigos"), 52000, 114900, 40, 8, "unit"),
    # Mujer > Ropa Interior
    ("Conjunto Íntimo Encaje Mujer", "MA-MU-017", ("Mujer", "Ropa Interior y Pijamas"), 35000, 74900, 60, 12, "unit"),
    ("Pijama Short Set Mujer", "MA-MU-018", ("Mujer", "Ropa Interior y Pijamas"), 45000, 99900, 50, 10, "unit"),
    # Hombre > Camisas y Polos
    ("Camisa Oxford Cuadros Hombre", "MA-HO-001", ("Hombre", "Camisas y Polos"), 52000, 114900, 60, 10, "unit"),
    ("Polo Piqué Sólido Hombre", "MA-HO-002", ("Hombre", "Camisas y Polos"), 38000, 84900, 75, 12, "unit"),
    ("Camiseta Básica Hombre x2", "MA-HO-003", ("Hombre", "Camisas y Polos"), 35000, 74900, 90, 15, "unit"),
    ("Camisa Lino Manga Corta Hombre", "MA-HO-004", ("Hombre", "Camisas y Polos"), 48000, 104900, 50, 10, "unit"),
    # Hombre > Pantalones
    ("Jean Slim Fit Oscuro Hombre", "MA-HO-005", ("Hombre", "Pantalones Hombre"), 62000, 134900, 65, 10, "unit"),
    ("Jean Straight Azul Medio Hombre", "MA-HO-006", ("Hombre", "Pantalones Hombre"), 60000, 129900, 60, 10, "unit"),
    ("Pantalón Chino Beige Hombre", "MA-HO-007", ("Hombre", "Pantalones Hombre"), 52000, 114900, 50, 8, "unit"),
    ("Pantaloneta Cargo Hombre", "MA-HO-008", ("Hombre", "Pantalones Hombre"), 35000, 74900, 55, 10, "unit"),
    # Hombre > Chaquetas
    ("Chaqueta Jean Hombre", "MA-HO-009", ("Hombre", "Chaquetas Hombre"), 72000, 154900, 30, 5, "unit"),
    ("Cortavientos Ligero Hombre", "MA-HO-010", ("Hombre", "Chaquetas Hombre"), 65000, 139900, 25, 5, "unit"),
    # Hombre > Ropa Interior
    ("Pack Boxes x3 Hombre", "MA-HO-011", ("Hombre", "Ropa Interior Hombre"), 38000, 82900, 80, 15, "unit"),
    ("Pack Medias Deportivas x6", "MA-HO-012", ("Hombre", "Ropa Interior Hombre"), 22000, 49900, 100, 20, "unit"),
    # Niños > Niñas
    ("Vestido Casual Niña 4-12 años", "MA-NI-001", ("Niños", "Niñas (2-14 años)"), 28000, 62900, 50, 10, "unit"),
    ("Conjunto Blusa+Falda Niña", "MA-NI-002", ("Niños", "Niñas (2-14 años)"), 35000, 74900, 45, 8, "unit"),
    ("Jean Niña Skinny", "MA-NI-003", ("Niños", "Niñas (2-14 años)"), 32000, 69900, 55, 10, "unit"),
    # Niños > Niños
    ("Jean Niño Straight", "MA-NI-004", ("Niños", "Niños (2-14 años)"), 30000, 64900, 55, 10, "unit"),
    ("Camiseta Gráfica Niño x2", "MA-NI-005", ("Niños", "Niños (2-14 años)"), 22000, 49900, 70, 12, "unit"),
    # Niños > Bebé
    ("Body Manga Corta Bebé x3", "MA-NI-006", ("Niños", "Bebé (0-24 meses)"), 28000, 59900, 60, 12, "unit"),
    ("Mameluco Con Pie Bebé", "MA-NI-007", ("Niños", "Bebé (0-24 meses)"), 35000, 74900, 45, 8, "unit"),
    # Calzado > Mujer
    ("Sandalias Planas Mujer T36-40", "MA-CA-001", ("Calzado", "Calzado Mujer"), 45000, 99900, 40, 8, "unit"),
    ("Botines Tacón Bloque Mujer T36-40", "MA-CA-002", ("Calzado", "Calzado Mujer"), 95000, 199900, 25, 5, "unit"),
    ("Sneakers Casuales Mujer T36-40", "MA-CA-003", ("Calzado", "Calzado Mujer"), 75000, 159900, 35, 6, "unit"),
    # Calzado > Hombre
    ("Mocasines Hombre T40-44", "MA-CA-004", ("Calzado", "Calzado Hombre"), 85000, 179900, 25, 5, "unit"),
    ("Sneakers Hombre T40-44", "MA-CA-005", ("Calzado", "Calzado Hombre"), 80000, 169900, 30, 6, "unit"),
    # Calzado > Niños
    ("Tenis Escolares Niño T26-34", "MA-CA-006", ("Calzado", "Calzado Niños"), 48000, 104900, 35, 7, "unit"),
    # Accesorios > Bolsos y Carteras
    ("Bolso Tote Cuero Sintético Mujer", "MA-AC-001", ("Accesorios", "Bolsos y Carteras"), 55000, 119900, 35, 7, "unit"),
    ("Cartera Crossbody Mini Mujer", "MA-AC-002", ("Accesorios", "Bolsos y Carteras"), 42000, 92900, 40, 8, "unit"),
    ("Mochila Casual Unisex", "MA-AC-003", ("Accesorios", "Bolsos y Carteras"), 65000, 139900, 30, 6, "unit"),
    # Accesorios > Cinturones
    ("Cinturón Cuero Sintético Hombre", "MA-AC-004", ("Accesorios", "Cinturones"), 22000, 49900, 50, 10, "unit"),
    ("Cinturón Trenzado Mujer", "MA-AC-005", ("Accesorios", "Cinturones"), 18000, 39900, 55, 10, "unit"),
    # Accesorios > Bisutería y Joyería
    ("Set Aretes Mujer x3 pares", "MA-AC-006", ("Accesorios", "Bisutería y Joyería"), 15000, 34900, 80, 15, "unit"),
    ("Collar Choker Mujer", "MA-AC-007", ("Accesorios", "Bisutería y Joyería"), 12000, 27900, 70, 12, "unit"),
    ("Pulsera Minimalista Mujer", "MA-AC-008", ("Accesorios", "Bisutería y Joyería"), 10000, 22900, 90, 15, "unit"),
    # Accesorios > Gorras y Sombreros
    ("Gorra Snapback Unisex", "MA-AC-009", ("Accesorios", "Gorras y Sombreros"), 18000, 39900, 55, 10, "unit"),
    ("Sombrero Bucket Unisex", "MA-AC-010", ("Accesorios", "Gorras y Sombreros"), 22000, 49900, 45, 8, "unit"),
    # Ropa Deportiva > Leggins y Shorts
    ("Leggins Deportivo Tiro Alto Mujer", "MA-RD-001", ("Ropa Deportiva", "Leggins y Shorts"), 38000, 84900, 70, 12, "unit"),
    ("Short Deportivo Mujer", "MA-RD-002", ("Ropa Deportiva", "Leggins y Shorts"), 28000, 62900, 60, 10, "unit"),
    ("Pantaloneta Deportiva Hombre", "MA-RD-003", ("Ropa Deportiva", "Leggins y Shorts"), 25000, 54900, 60, 10, "unit"),
    # Ropa Deportiva > Tops Deportivos
    ("Sports Bra Seamless Mujer", "MA-RD-004", ("Ropa Deportiva", "Camisetas y Tops Deportivos"), 32000, 72900, 65, 12, "unit"),
    ("Camiseta Funcional Dry-Fit Hombre", "MA-RD-005", ("Ropa Deportiva", "Camisetas y Tops Deportivos"), 28000, 62900, 60, 10, "unit"),
]

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Valentina",
        "last_name": "Arango Giraldo",
        "document_type": "CC",
        "document_number": "1037456789",
        "email": "vale.arango@gmail.com",
        "phone": "+57 320 234 5678",
        "address": "Cra. 43A # 7-50, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Andrea",
        "last_name": "Ospina Velásquez",
        "document_type": "CC",
        "document_number": "1040567890",
        "email": "andrea.ospina@hotmail.com",
        "phone": "+57 315 345 6789",
        "address": "Cll. 10 # 38-25, El Tesoro",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Camila",
        "last_name": "Rodríguez Reyes",
        "document_type": "CC",
        "document_number": "1020678901",
        "email": "cami.rodriguez@gmail.com",
        "phone": "+57 313 456 7890",
        "address": "Cra. 15 # 93-10, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Sofía",
        "last_name": "Pardo Méndez",
        "document_type": "CC",
        "document_number": "1014789012",
        "email": "sofia.pardo@gmail.com",
        "phone": "+57 317 567 8901",
        "address": "Cll. 116 # 17-80, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Laura",
        "last_name": "Morales Blanco",
        "document_type": "CC",
        "document_number": "1028901234",
        "email": "lauramorales@outlook.com",
        "phone": "+57 321 678 9012",
        "address": "Cra. 5 # 15-30, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Isabella",
        "last_name": "Soto Barrera",
        "document_type": "CC",
        "document_number": "1045012345",
        "email": "isabella.soto@gmail.com",
        "phone": "+57 311 789 0123",
        "address": "Cll. 85 # 12-30, Zona Rosa",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Daniela",
        "last_name": "Herrera López",
        "document_type": "CC",
        "document_number": "1006234567",
        "email": "dani.herrera@gmail.com",
        "phone": "+57 318 890 1234",
        "address": "Av. El Lago # 5-20",
        "city": "Villavicencio",
        "country": "Colombia",
    },
    {
        "first_name": "Manuela",
        "last_name": "Castaño Ríos",
        "document_type": "CC",
        "document_number": "1088123456",
        "email": "manuela.castano@gmail.com",
        "phone": "+57 316 901 2345",
        "address": "Cll. 19 # 8-32, Centro",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Juliana",
        "last_name": "Betancur Salcedo",
        "document_type": "CC",
        "document_number": "1098234567",
        "email": "juli.betancur@yahoo.com",
        "phone": "+57 314 012 3456",
        "address": "Cra. 70 # 44A-30, Belén",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Natalia",
        "last_name": "Guerrero Montoya",
        "document_type": "CC",
        "document_number": "1032345678",
        "email": "nata.guerrero@gmail.com",
        "phone": "+57 312 123 4567",
        "address": "Cra. 27 # 50-45, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Sebastián",
        "last_name": "Ruiz Palomino",
        "document_type": "CC",
        "document_number": "1000456789",
        "email": "sebas.ruiz@gmail.com",
        "phone": "+57 320 234 5679",
        "address": "Cll. 93B # 11-54, Chico",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Mateo",
        "last_name": "González Vera",
        "document_type": "CC",
        "document_number": "1007567890",
        "email": "mateo.gv@gmail.com",
        "phone": "+57 301 345 6780",
        "address": "Cra. 43A # 25-10, Envigado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Felipe",
        "last_name": "Navarro Suárez",
        "document_type": "CC",
        "document_number": "1002678901",
        "email": "felipe.navarro@outlook.com",
        "phone": "+57 319 456 7891",
        "address": "Cll. 10 # 43D-15",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Paula",
        "last_name": "Martínez Agudelo",
        "document_type": "CC",
        "document_number": "1047890123",
        "email": "paula.martinez@gmail.com",
        "phone": "+57 322 567 8902",
        "address": "Cra. 53 # 76-88",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "María José",
        "last_name": "Valencia Cano",
        "document_type": "CC",
        "document_number": "1094901234",
        "email": "mjose.valencia@gmail.com",
        "phone": "+57 315 678 9013",
        "address": "Cll. 12 # 15-30, La Isabela",
        "city": "Armenia",
        "country": "Colombia",
    },
    {
        "first_name": "Alejandra",
        "last_name": "Zapata Ocampo",
        "document_type": "CC",
        "document_number": "43012345",
        "email": "ale.zapata@gmail.com",
        "phone": "+57 304 789 0125",
        "address": "Cra. 65 # 34-20, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Carolina",
        "last_name": "Pineda Rojas",
        "document_type": "CC",
        "document_number": "52234567",
        "email": "carolina.pineda@hotmail.com",
        "phone": "+57 311 890 1236",
        "address": "Cll. 44 # 3A-20, Granada",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Lorena",
        "last_name": "Barón Peñaloza",
        "document_type": "CC",
        "document_number": "37123456",
        "email": "lorena.baron@gmail.com",
        "phone": "+57 318 901 2347",
        "address": "Cra. 27A # 51-12",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "vendedor1@modaandes.co",
        "first_name": "Valeria",
        "last_name": "Rincón",
        "phone": "+57 310 777 8888",
    },
    {
        "email": "vendedor2@modaandes.co",
        "first_name": "Sergio",
        "last_name": "Mendoza",
        "phone": "+57 310 888 9999",
    },
    {
        "email": "vendedor3@modaandes.co",
        "first_name": "Tatiana",
        "last_name": "Gómez",
        "phone": "+57 310 999 0000",
    },
    {
        "email": "vendedor4@modaandes.co",
        "first_name": "Julián",
        "last_name": "Cárdenas",
        "phone": "+57 310 000 1111",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]
IVA_RATE = Decimal("0.19")


def seed(session: Session) -> None:
    """Main seed function for Moda Andes demo data."""

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

    # ── 7. Initial inventory ──────────────────────────────────────────
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
            reason="Stock inicial - Apertura Moda Andes",
            created_at=datetime.now(timezone.utc) - timedelta(days=60),
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

    # ── 9. Sales — 60 days, heavier on weekends and paydays ──────────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(60, -1, -1):
        day = now - timedelta(days=days_ago)
        is_weekend = day.weekday() >= 5
        day_of_month = day.day
        is_payday = day_of_month in (1, 2, 3, 15, 16, 17)

        if is_weekend and is_payday:
            num_sales = random.randint(10, 18)
        elif is_weekend:
            num_sales = random.randint(6, 12)
        elif is_payday:
            num_sales = random.randint(5, 10)
        else:
            num_sales = random.randint(2, 6)
        if days_ago == 0:
            num_sales = random.randint(8, 14)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"MA-{invoice_counter:06d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.75 else None

            num_items = random.randint(1, 4)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(10, 21)
            sale_minute = random.randint(0, 59)
            sale_date = day.replace(
                hour=sale_hour, minute=sale_minute,
                second=random.randint(0, 59), microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = random.randint(1, 3)
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

            # Fashion stores: more discounts, especially on weekends
            max_discount = 15 if is_weekend else 10
            discount = (subtotal * Decimal(str(random.randint(0, max_discount))) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.06 and days_ago > 0
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
                sale.cancelled_at = sale_date + timedelta(hours=random.randint(1, 48))
                sale.cancelled_by = admin_user.id
                sale.cancellation_reason = random.choice([
                    "Cambio por talla incorrecta",
                    "Cliente devolvió mercancía",
                    "Defecto en el producto",
                    "Cliente cambió de opinión",
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
    logger.info(f"Created {total_sales} sales over 60 days")

    # ── 10. Restock ───────────────────────────────────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(25, 80)
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
                reason="Reposición de inventario Moda Andes",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED MODA ANDES COMPLETE!")
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
    random.seed(13)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
