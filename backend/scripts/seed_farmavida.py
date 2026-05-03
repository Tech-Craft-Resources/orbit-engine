"""
Seed script for FarmaVida — Colombian independent pharmacy / droguería chain.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_farmavida.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - Products: OTC medications, vitamins, personal care, baby products,
    dermocosmetics and medical devices
  - Prices in COP, typical Colombian pharmacy pricing
  - IVA 0% on most medications (exento), 19% on personal care
  - Higher sales Mon–Fri, moderate on weekends
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

ORG_SLUG = "farmavida"

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Medicamentos OTC",
        "description": "Medicamentos de venta libre sin prescripción médica",
        "children": [
            {"name": "Analgésicos y Antipiréticos", "description": "Acetaminofén, ibuprofeno, aspirina y similares"},
            {"name": "Antigripales y Descongestivos", "description": "Medicamentos para gripa, tos y resfriado"},
            {"name": "Digestivos y Antiácidos", "description": "Antiácidos, antiespasmódicos y protectores gástricos"},
            {"name": "Antiinflamatorios Tópicos", "description": "Cremas, geles y parches antiinflamatorios"},
            {"name": "Antialérgicos", "description": "Antihistamínicos y descongestionantes nasales"},
            {"name": "Vitaminas y Suplementos", "description": "Multivitamínicos, minerales y suplementos nutricionales"},
        ],
    },
    {
        "name": "Cuidado Personal",
        "description": "Productos de higiene y cuidado corporal diario",
        "children": [
            {"name": "Higiene Oral", "description": "Cremas dentales, enjuagues y cepillos"},
            {"name": "Higiene Corporal", "description": "Jabones, desodorantes, talcos y cremas corporales"},
            {"name": "Higiene Capilar", "description": "Shampoo medicado, acondicionadores y tratamientos"},
            {"name": "Protección Solar", "description": "Bloqueadores y protectores solares faciales y corporales"},
        ],
    },
    {
        "name": "Dermocosmética",
        "description": "Cuidado de la piel con enfoque dermatológico",
        "children": [
            {"name": "Hidratación Facial", "description": "Cremas hidratantes, sérums y contornos de ojos"},
            {"name": "Tratamientos Especializados", "description": "Productos para acné, manchas y antienvejecimiento"},
            {"name": "Limpieza Facial", "description": "Desmaquillantes, tónicos y exfoliantes suaves"},
        ],
    },
    {
        "name": "Bebé y Maternidad",
        "description": "Cuidado especializado para bebés y madres gestantes",
        "children": [
            {"name": "Higiene del Bebé", "description": "Jabones, cremas, talcos y aceites para bebé"},
            {"name": "Alimentación del Bebé", "description": "Leches de fórmula, cereales y complementos"},
            {"name": "Accesorios Bebé", "description": "Termómetros, chupetes y accesorios de higiene"},
        ],
    },
    {
        "name": "Dispositivos Médicos",
        "description": "Equipos de medición y primeros auxilios",
        "children": [
            {"name": "Medición y Diagnóstico", "description": "Tensiómetros, glucómetros y oxímetros"},
            {"name": "Primeros Auxilios", "description": "Gasas, vendas, antisépticos y botiquín"},
            {"name": "Ortopedia Básica", "description": "Rodilleras, tobilleras, muñequeras y fajas"},
        ],
    },
    {
        "name": "Salud Sexual y Reproductiva",
        "description": "Anticonceptivos y productos de planificación familiar",
        "children": [
            {"name": "Anticonceptivos", "description": "Condones y métodos de barrera disponibles sin fórmula"},
        ],
    },
]

# (name, sku, category_path, cost_cop, sale_price_cop, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Medicamentos OTC > Analgésicos
    ("Acetaminofén 500mg x100 tabs", "FV-OTC-001", ("Medicamentos OTC", "Analgésicos y Antipiréticos"), 4500, 8900, 300, 60, "unit"),
    ("Acetaminofén 1g x30 tabs", "FV-OTC-002", ("Medicamentos OTC", "Analgésicos y Antipiréticos"), 5500, 10900, 250, 50, "unit"),
    ("Ibuprofeno 400mg x30 tabs", "FV-OTC-003", ("Medicamentos OTC", "Analgésicos y Antipiréticos"), 5000, 9900, 200, 40, "unit"),
    ("Dolex Extra Fuerte x24 tabs", "FV-OTC-004", ("Medicamentos OTC", "Analgésicos y Antipiréticos"), 8000, 15900, 150, 30, "unit"),
    ("Aspirina 100mg x30 tabs", "FV-OTC-005", ("Medicamentos OTC", "Analgésicos y Antipiréticos"), 4000, 7900, 200, 40, "unit"),
    # Medicamentos OTC > Antigripales
    ("Alka Seltzer Plus x10 sobres", "FV-OTC-006", ("Medicamentos OTC", "Antigripales y Descongestivos"), 12000, 22900, 120, 25, "unit"),
    ("Ambroxol Jarabe 30mg/5ml x120ml", "FV-OTC-007", ("Medicamentos OTC", "Antigripales y Descongestivos"), 8500, 16900, 100, 20, "unit"),
    ("Loratadina 10mg x30 tabs", "FV-OTC-008", ("Medicamentos OTC", "Antigripales y Descongestivos"), 6000, 11900, 150, 30, "unit"),
    ("DayQuil x16 caps", "FV-OTC-009", ("Medicamentos OTC", "Antigripales y Descongestivos"), 18000, 34900, 80, 15, "unit"),
    # Medicamentos OTC > Digestivos
    ("Omeprazol 20mg x30 caps", "FV-OTC-010", ("Medicamentos OTC", "Digestivos y Antiácidos"), 12000, 22900, 200, 40, "unit"),
    ("Mylanta Plus Suspensión 240ml", "FV-OTC-011", ("Medicamentos OTC", "Digestivos y Antiácidos"), 14000, 26900, 100, 20, "unit"),
    ("Sal de Frutas x200g", "FV-OTC-012", ("Medicamentos OTC", "Digestivos y Antiácidos"), 8000, 15900, 120, 25, "unit"),
    ("Buscapina Compositum x20 tabs", "FV-OTC-013", ("Medicamentos OTC", "Digestivos y Antiácidos"), 15000, 28900, 100, 20, "unit"),
    # Medicamentos OTC > Antiinflamatorios Tópicos
    ("Voltaren Gel 1% x50g", "FV-OTC-014", ("Medicamentos OTC", "Antiinflamatorios Tópicos"), 22000, 41900, 80, 15, "unit"),
    ("Bengay Crema Muscular 50g", "FV-OTC-015", ("Medicamentos OTC", "Antiinflamatorios Tópicos"), 16000, 30900, 70, 12, "unit"),
    # Medicamentos OTC > Antialérgicos
    ("Cetirizina 10mg x30 tabs", "FV-OTC-016", ("Medicamentos OTC", "Antialérgicos"), 7000, 13900, 150, 30, "unit"),
    ("Claritin 10mg x15 tabs", "FV-OTC-017", ("Medicamentos OTC", "Antialérgicos"), 25000, 47900, 80, 15, "unit"),
    # Medicamentos OTC > Vitaminas
    ("Centrum Adultos x30 tabs", "FV-OTC-018", ("Medicamentos OTC", "Vitaminas y Suplementos"), 28000, 52900, 100, 20, "unit"),
    ("Vitamina C 1g x30 efervescentes", "FV-OTC-019", ("Medicamentos OTC", "Vitaminas y Suplementos"), 14000, 26900, 150, 30, "unit"),
    ("Vitamina D3 1000UI x60 caps", "FV-OTC-020", ("Medicamentos OTC", "Vitaminas y Suplementos"), 18000, 34900, 100, 20, "unit"),
    ("Omega 3 1000mg x60 perlas", "FV-OTC-021", ("Medicamentos OTC", "Vitaminas y Suplementos"), 22000, 41900, 80, 15, "unit"),
    ("Zinc 50mg x60 tabs", "FV-OTC-022", ("Medicamentos OTC", "Vitaminas y Suplementos"), 12000, 22900, 100, 20, "unit"),
    # Cuidado Personal > Higiene Oral
    ("Colgate Total 12 x130g", "FV-CP-001", ("Cuidado Personal", "Higiene Oral"), 8000, 15900, 200, 40, "unit"),
    ("Sensodyne Rapid Relief x90g", "FV-CP-002", ("Cuidado Personal", "Higiene Oral"), 14000, 26900, 120, 25, "unit"),
    ("Listerine Cool Mint 500ml", "FV-CP-003", ("Cuidado Personal", "Higiene Oral"), 16000, 30900, 100, 20, "unit"),
    ("Cepillo Oral-B Soft x2", "FV-CP-004", ("Cuidado Personal", "Higiene Oral"), 12000, 22900, 150, 30, "unit"),
    # Cuidado Personal > Higiene Corporal
    ("Dove Original Crema x400ml", "FV-CP-005", ("Cuidado Personal", "Higiene Corporal"), 12000, 22900, 150, 30, "unit"),
    ("Rexona Men Clinical 150ml", "FV-CP-006", ("Cuidado Personal", "Higiene Corporal"), 18000, 34900, 120, 25, "unit"),
    ("Johnson Crema Corporal x400ml", "FV-CP-007", ("Cuidado Personal", "Higiene Corporal"), 16000, 30900, 100, 20, "unit"),
    ("Alcohol Antiséptico 70° x500ml", "FV-CP-008", ("Cuidado Personal", "Higiene Corporal"), 5500, 10900, 200, 40, "unit"),
    # Cuidado Personal > Higiene Capilar
    ("Head & Shoulders Clásico x375ml", "FV-CP-009", ("Cuidado Personal", "Higiene Capilar"), 18000, 34900, 80, 15, "unit"),
    ("Pantene Reparación x400ml", "FV-CP-010", ("Cuidado Personal", "Higiene Capilar"), 16000, 30900, 80, 15, "unit"),
    # Cuidado Personal > Protección Solar
    ("Coppertone Sport SPF50 x150ml", "FV-CP-011", ("Cuidado Personal", "Protección Solar"), 28000, 52900, 60, 12, "unit"),
    ("Isdin Fotoprotector Fusion SPF50 50ml", "FV-CP-012", ("Cuidado Personal", "Protección Solar"), 55000, 99900, 35, 7, "unit"),
    # Dermocosmética > Hidratación Facial
    ("Cetaphil Crema Hidratante x250g", "FV-DC-001", ("Dermocosmética", "Hidratación Facial"), 35000, 65900, 50, 10, "unit"),
    ("Neutrogena Hydro Boost x50ml", "FV-DC-002", ("Dermocosmética", "Hidratación Facial"), 55000, 99900, 40, 8, "unit"),
    ("La Roche Posay Effaclar x40ml", "FV-DC-003", ("Dermocosmética", "Tratamientos Especializados"), 68000, 124900, 30, 6, "unit"),
    ("Vichy Normaderm Anti-Acné x50ml", "FV-DC-004", ("Dermocosmética", "Tratamientos Especializados"), 62000, 114900, 30, 6, "unit"),
    ("Micellar Water Garnier 400ml", "FV-DC-005", ("Dermocosmética", "Limpieza Facial"), 22000, 41900, 60, 12, "unit"),
    # Bebé > Higiene del Bebé
    ("Johnson Shampoo Bebé x400ml", "FV-BE-001", ("Bebé y Maternidad", "Higiene del Bebé"), 16000, 30900, 80, 15, "unit"),
    ("Crema Antipañalitis Pañalene x125g", "FV-BE-002", ("Bebé y Maternidad", "Higiene del Bebé"), 14000, 26900, 80, 15, "unit"),
    ("Aceite de Bebé Johnson x200ml", "FV-BE-003", ("Bebé y Maternidad", "Higiene del Bebé"), 14000, 26900, 70, 12, "unit"),
    ("Toallitas Húmedas Pequeñín x80", "FV-BE-004", ("Bebé y Maternidad", "Higiene del Bebé"), 12000, 22900, 100, 20, "unit"),
    # Bebé > Alimentación
    ("Nan ProExpert 1 Lata x400g", "FV-BE-005", ("Bebé y Maternidad", "Alimentación del Bebé"), 55000, 99900, 40, 8, "unit"),
    ("Cerelac Arroz x500g", "FV-BE-006", ("Bebé y Maternidad", "Alimentación del Bebé"), 28000, 52900, 50, 10, "unit"),
    # Bebé > Accesorios
    ("Termómetro Digital Infrarojo Bebé", "FV-BE-007", ("Bebé y Maternidad", "Accesorios Bebé"), 35000, 64900, 25, 5, "unit"),
    # Dispositivos > Medición
    ("Tensiómetro Digital de Brazo Omron", "FV-DM-001", ("Dispositivos Médicos", "Medición y Diagnóstico"), 95000, 174900, 15, 3, "unit"),
    ("Oxímetro de Pulso Digital", "FV-DM-002", ("Dispositivos Médicos", "Medición y Diagnóstico"), 28000, 52900, 25, 5, "unit"),
    ("Glucómetro Kit Accu-Chek Active", "FV-DM-003", ("Dispositivos Médicos", "Medición y Diagnóstico"), 55000, 99900, 15, 3, "unit"),
    ("Termómetro Oral Digital", "FV-DM-004", ("Dispositivos Médicos", "Medición y Diagnóstico"), 15000, 28900, 40, 8, "unit"),
    # Dispositivos > Primeros Auxilios
    ("Botiquín Básico 30 artículos", "FV-DM-005", ("Dispositivos Médicos", "Primeros Auxilios"), 35000, 64900, 20, 4, "unit"),
    ("Gasa Estéril 10x10 x10 unidades", "FV-DM-006", ("Dispositivos Médicos", "Primeros Auxilios"), 4500, 8900, 150, 30, "unit"),
    ("Venda Elástica 5cm x5m", "FV-DM-007", ("Dispositivos Médicos", "Primeros Auxilios"), 5000, 9900, 120, 25, "unit"),
    ("Isodine Espuma 60ml", "FV-DM-008", ("Dispositivos Médicos", "Primeros Auxilios"), 10000, 18900, 100, 20, "unit"),
    # Dispositivos > Ortopedia
    ("Rodillera Elástica Talla M", "FV-DM-009", ("Dispositivos Médicos", "Ortopedia Básica"), 22000, 41900, 30, 6, "unit"),
    ("Tobillera Semirrígida Talla M", "FV-DM-010", ("Dispositivos Médicos", "Ortopedia Básica"), 28000, 52900, 25, 5, "unit"),
    ("Faja Lumbar Elástica Talla M", "FV-DM-011", ("Dispositivos Médicos", "Ortopedia Básica"), 38000, 71900, 20, 4, "unit"),
    # Salud Sexual
    ("Condones Durex Natural x12", "FV-SS-001", ("Salud Sexual y Reproductiva", "Anticonceptivos"), 22000, 41900, 80, 15, "unit"),
    ("Condones Trojan Ultra Thin x3", "FV-SS-002", ("Salud Sexual y Reproductiva", "Anticonceptivos"), 9000, 17900, 100, 20, "unit"),
]

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "María Elena",
        "last_name": "Torres Pineda",
        "document_type": "CC",
        "document_number": "41345678",
        "email": "melena.torres@gmail.com",
        "phone": "+57 315 234 5678",
        "address": "Cll. 45 # 12-30, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Roberto",
        "last_name": "Jiménez Palomino",
        "document_type": "CC",
        "document_number": "79456789",
        "email": "r.jimenez@hotmail.com",
        "phone": "+57 301 345 6789",
        "address": "Cra. 30 # 22-18, Barrio Américas",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Lucía",
        "last_name": "Martínez Arenas",
        "document_type": "CC",
        "document_number": "52567890",
        "email": "lucia.martinez@outlook.com",
        "phone": "+57 318 456 7890",
        "address": "Cll. 10 # 43E-30, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Carlos Humberto",
        "last_name": "Vélez Cárdenas",
        "document_type": "CC",
        "document_number": "98678901",
        "email": "ch.velez@gmail.com",
        "phone": "+57 313 567 8901",
        "address": "Cra. 70 # 45-20, Belén",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Claudia Patricia",
        "last_name": "Moreno Bolaños",
        "document_type": "CC",
        "document_number": "34789012",
        "email": "cp.moreno@gmail.com",
        "phone": "+57 317 678 9012",
        "address": "Av. 3N # 24-55, Norte",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Estela",
        "last_name": "Gutiérrez Suárez",
        "document_type": "CC",
        "document_number": "38901234",
        "email": "estela.guti@yahoo.com",
        "phone": "+57 311 789 0123",
        "address": "Cra. 27 # 50-12, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Jhon",
        "last_name": "Ospina Varela",
        "document_type": "CC",
        "document_number": "1004012345",
        "email": "jhon.ospina@gmail.com",
        "phone": "+57 316 890 1234",
        "address": "Cll. 19 # 7-30, La Circunvalar",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Beatriz",
        "last_name": "Cano Restrepo",
        "document_type": "CC",
        "document_number": "43234567",
        "email": "beatriz.cano@gmail.com",
        "phone": "+57 320 901 2345",
        "address": "Cra. 80 # 30-55, Robledo",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Andrés Felipe",
        "last_name": "Peña Cifuentes",
        "document_type": "CC",
        "document_number": "1025345678",
        "email": "afelipe.pena@gmail.com",
        "phone": "+57 314 012 3456",
        "address": "Cll. 116 # 17-43, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Rosa María",
        "last_name": "Aguilar Mosquera",
        "document_type": "CC",
        "document_number": "30456789",
        "email": "rosamaria.am@gmail.com",
        "phone": "+57 312 123 4567",
        "address": "Cll. 5 # 25-40",
        "city": "Quibdó",
        "country": "Colombia",
    },
    {
        "first_name": "Nicolás",
        "last_name": "Salcedo Flórez",
        "document_type": "CC",
        "document_number": "1090567890",
        "email": "nicolas.salcedo@gmail.com",
        "phone": "+57 300 234 5679",
        "address": "Cra. 9 # 13-40, Centro",
        "city": "Armenia",
        "country": "Colombia",
    },
    {
        "first_name": "Amparo",
        "last_name": "Rodríguez Ávila",
        "document_type": "CC",
        "document_number": "46678901",
        "email": "amparo.rdz@hotmail.com",
        "phone": "+57 321 345 6780",
        "address": "Cra. 5 # 17-18, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Germán",
        "last_name": "Bernal Lozano",
        "document_type": "CC",
        "document_number": "72789012",
        "email": "german.bernal@gmail.com",
        "phone": "+57 319 456 7892",
        "address": "Cll. del Arsenal # 8-10, Manga",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Susana",
        "last_name": "Hoyos Londoño",
        "document_type": "CC",
        "document_number": "43901234",
        "email": "susana.hoyos@gmail.com",
        "phone": "+57 304 567 8903",
        "address": "Cra. 43A # 18 Sur-50, Envigado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Patricia",
        "last_name": "Durán Castro",
        "document_type": "CC",
        "document_number": "36012345",
        "email": "patricia.duran@gmail.com",
        "phone": "+57 318 678 9014",
        "address": "Cll. 18 # 5-30, Centro Histórico",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Fabio",
        "last_name": "Montoya Ríos",
        "document_type": "CC",
        "document_number": "71234567",
        "email": "fabio.montoya@outlook.com",
        "phone": "+57 315 789 0125",
        "address": "Cll. 50 # 80-44, Los Colores",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Adriana",
        "last_name": "Rueda Bermúdez",
        "document_type": "CC",
        "document_number": "40234567",
        "email": "adriana.rueda@gmail.com",
        "phone": "+57 311 890 1237",
        "address": "Cra. 15 # 88-10, Teusaquillo",
        "city": "Bogotá",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "vendedor1@farmavida.co",
        "first_name": "Marcela",
        "last_name": "Giraldo",
        "phone": "+57 310 444 5555",
    },
    {
        "email": "vendedor2@farmavida.co",
        "first_name": "Jesús",
        "last_name": "Herrera",
        "phone": "+57 310 555 6666",
    },
    {
        "email": "vendedor3@farmavida.co",
        "first_name": "Diana",
        "last_name": "Suárez",
        "phone": "+57 310 666 7777",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]
IVA_RATE = Decimal("0.19")


def seed(session: Session) -> None:
    """Main seed function for FarmaVida demo data."""

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
            reason="Stock inicial - Apertura FarmaVida",
            created_at=datetime.now(timezone.utc) - timedelta(days=45),
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

    # ── 9. Sales — 45 days, steady Mon–Fri with weekend dip ──────────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(45, -1, -1):
        day = now - timedelta(days=days_ago)
        is_weekend = day.weekday() >= 5
        if is_weekend:
            num_sales = random.randint(4, 8)
        else:
            num_sales = random.randint(8, 16)
        if days_ago == 0:
            num_sales = random.randint(10, 15)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"FV-{invoice_counter:06d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.60 else None

            # Pharmacies: typically 1-3 items per visit
            num_items = random.randint(1, 4)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(7, 21)
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

            # Pharmacies: low discount rates
            discount = (subtotal * Decimal(str(random.randint(0, 5))) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.03 and days_ago > 0
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
                sale.cancelled_at = sale_date + timedelta(hours=random.randint(1, 3))
                sale.cancelled_by = admin_user.id
                sale.cancellation_reason = random.choice([
                    "Producto vencido devuelto",
                    "Dispensación incorrecta",
                    "Cliente no encontró el producto",
                    "Error en el cobro",
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
    logger.info(f"Created {total_sales} sales over 45 days")

    # ── 10. Restock ───────────────────────────────────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(50, 150)
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
                reason="Reposición de inventario FarmaVida",
                created_at=now - timedelta(hours=random.randint(1, 36)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED FARMAVIDA COMPLETE!")
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
    random.seed(21)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
