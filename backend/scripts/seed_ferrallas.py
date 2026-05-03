"""
Seed script for Ferrallas del Norte — Colombian hardware / construction-supply store.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_ferrallas.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - Products: hand tools, power tools, plumbing, electrical, paint, fasteners,
    safety equipment, construction materials
  - Prices in COP, margins typical for Colombian ferreterías
  - IVA 19% (Colombia)
  - Customers: contractors, construction companies, individuals
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

ORG_SLUG = "ferrallas-del-norte"

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Herramientas Manuales",
        "description": "Martillos, destornilladores, llaves y herramientas de mano",
        "children": [
            {"name": "Martillos y Mazos", "description": "Martillos de carpintero, mazos de goma y demolición"},
            {"name": "Destornilladores y Puntas", "description": "Sets de destornilladores planos, Phillips y Torx"},
            {"name": "Llaves y Raches", "description": "Llaves fijas, ajustables, mixtas y sets de raches"},
            {"name": "Alicates y Pinzas", "description": "Alicates universales, de punta, corte y presión"},
            {"name": "Sierras y Serruchos", "description": "Sierras para madera, metal y multiuso"},
            {"name": "Medición y Trazado", "description": "Metros, niveles, escuadras y plomadas"},
        ],
    },
    {
        "name": "Herramientas Eléctricas",
        "description": "Taladros, pulidoras, sierras eléctricas y accesorios",
        "children": [
            {"name": "Taladros y Atornilladores", "description": "Taladros percutores, de impacto y atornilladores inalámbricos"},
            {"name": "Pulidoras y Esmeriladoras", "description": "Pulidoras angulares de 4½\" y 7\""},
            {"name": "Sierras Eléctricas", "description": "Sierras circulares, caladora y sable"},
            {"name": "Lijadoras y Fresadoras", "description": "Lijadoras orbitales, de banda y fresadoras"},
        ],
    },
    {
        "name": "Plomería",
        "description": "Tubería, accesorios, válvulas y sanitarios",
        "children": [
            {"name": "Tubería PVC y CPVC", "description": "Tubos para presión, desagüe y sanitario"},
            {"name": "Accesorios y Uniones", "description": "Codos, tees, reducciones y uniones"},
            {"name": "Válvulas y Llaves", "description": "Válvulas de bola, compuerta y llaves de paso"},
            {"name": "Pegantes y Sellantes", "description": "Pegante PVC, teflón, silicona y aditivos"},
        ],
    },
    {
        "name": "Electricidad",
        "description": "Cable, conduit, tomas, interruptores y tableros",
        "children": [
            {"name": "Cables y Alambres", "description": "Cable THHN, dúplex, encauchetado por metro y rollo"},
            {"name": "Conduit y Accesorios", "description": "Conduit EMT, PVC flexible y cajas de paso"},
            {"name": "Tomas e Interruptores", "description": "Tomas sencillas, dobles, interruptores y placas"},
            {"name": "Tableros y Breakers", "description": "Tableros monofásicos, trifásicos y breakers"},
            {"name": "Iluminación", "description": "Bombillos LED, tubos fluorescentes y luminarias"},
        ],
    },
    {
        "name": "Pinturas y Acabados",
        "description": "Pinturas, estuco, impermeabilizantes y accesorios",
        "children": [
            {"name": "Pinturas de Interior", "description": "Pinturas vinílicas y esmaltes para interiores"},
            {"name": "Pinturas de Exterior", "description": "Pinturas para fachada e impermeabilizantes"},
            {"name": "Estuco y Pañete", "description": "Estucos plásticos, acrílicos y pañetes"},
            {"name": "Accesorios de Pintura", "description": "Rodillos, brochas, bandejas y lijas"},
        ],
    },
    {
        "name": "Fijación y Tornillería",
        "description": "Tornillos, puntillas, anclajes y adhesivos",
        "children": [
            {"name": "Tornillos y Pernos", "description": "Tornillos para madera, drywall, máquina y pernos"},
            {"name": "Puntillas y Grapas", "description": "Puntillas lisas, corrugadas y grapas"},
            {"name": "Anclajes y Taquetes", "description": "Taquetes plásticos, expansivos y químicos"},
            {"name": "Adhesivos y Pegantes", "description": "Colbón, epóxico, pegamento de contacto"},
        ],
    },
    {
        "name": "Seguridad Industrial",
        "description": "EPP, señalización y equipos de protección personal",
        "children": [
            {"name": "Protección de Cabeza", "description": "Cascos de seguridad por categorías"},
            {"name": "Protección Visual y Auditiva", "description": "Gafas, monogafas y tapa oídos"},
            {"name": "Protección de Manos y Pies", "description": "Guantes de carnaza, vaqueta, nitrilo y botas"},
            {"name": "Señalización", "description": "Cintas de peligro, conos y señales de seguridad"},
        ],
    },
    {
        "name": "Construcción",
        "description": "Cemento, mortero, varilla y materiales básicos",
        "children": [
            {"name": "Cementos y Morteros", "description": "Cemento gris, blanco, mortero y aditivos"},
            {"name": "Mallas y Varillas", "description": "Varilla corrugada, malla electrosoldada y alambre"},
        ],
    },
]

# (name, sku, category_path, cost_cop, sale_price_cop, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Herramientas Manuales > Martillos y Mazos
    ("Martillo Carpintero 16oz", "FDN-HM-001", ("Herramientas Manuales", "Martillos y Mazos"), 22000, 38900, 60, 10, "unit"),
    ("Martillo Demoledor 3lb", "FDN-HM-002", ("Herramientas Manuales", "Martillos y Mazos"), 55000, 89900, 30, 6, "unit"),
    ("Mazo de Goma 1kg", "FDN-HM-003", ("Herramientas Manuales", "Martillos y Mazos"), 18000, 31900, 45, 8, "unit"),
    # Herramientas Manuales > Destornilladores y Puntas
    ("Set Destornilladores x6 Stanley", "FDN-HD-001", ("Herramientas Manuales", "Destornilladores y Puntas"), 38000, 62900, 50, 10, "unit"),
    ("Destornillador Plano 1/4\"x6\"", "FDN-HD-002", ("Herramientas Manuales", "Destornilladores y Puntas"), 8000, 14900, 80, 15, "unit"),
    ("Set Puntas Torx 30pzs", "FDN-HD-003", ("Herramientas Manuales", "Destornilladores y Puntas"), 22000, 38900, 40, 8, "unit"),
    # Herramientas Manuales > Llaves y Raches
    ("Llave Ajustable 12\"", "FDN-HL-001", ("Herramientas Manuales", "Llaves y Raches"), 35000, 59900, 40, 8, "unit"),
    ("Set Llaves Mixtas 8-19mm x8", "FDN-HL-002", ("Herramientas Manuales", "Llaves y Raches"), 65000, 109900, 25, 5, "unit"),
    ("Set Rache 1/2\" 26pzs", "FDN-HL-003", ("Herramientas Manuales", "Llaves y Raches"), 120000, 199900, 20, 4, "unit"),
    # Herramientas Manuales > Alicates y Pinzas
    ("Alicate Universal 8\"", "FDN-HA-001", ("Herramientas Manuales", "Alicates y Pinzas"), 22000, 38900, 55, 10, "unit"),
    ("Alicate de Corte 7\"", "FDN-HA-002", ("Herramientas Manuales", "Alicates y Pinzas"), 18000, 31900, 50, 10, "unit"),
    ("Pinza Prensadora 10\"", "FDN-HA-003", ("Herramientas Manuales", "Alicates y Pinzas"), 28000, 48900, 35, 8, "unit"),
    # Herramientas Manuales > Sierras y Serruchos
    ("Serrucho 22\" Madera", "FDN-HS-001", ("Herramientas Manuales", "Sierras y Serruchos"), 28000, 48900, 30, 6, "unit"),
    ("Sierra Hacksaw Marco Metálico", "FDN-HS-002", ("Herramientas Manuales", "Sierras y Serruchos"), 32000, 54900, 35, 7, "unit"),
    # Herramientas Manuales > Medición y Trazado
    ("Metro Flexómetro 5m Stanley", "FDN-HME-001", ("Herramientas Manuales", "Medición y Trazado"), 18000, 31900, 70, 15, "unit"),
    ("Nivel Aluminio 60cm", "FDN-HME-002", ("Herramientas Manuales", "Medición y Trazado"), 35000, 59900, 30, 6, "unit"),
    ("Escuadra Carpintero 12\"", "FDN-HME-003", ("Herramientas Manuales", "Medición y Trazado"), 22000, 38900, 35, 7, "unit"),
    # Herramientas Eléctricas > Taladros y Atornilladores
    ("Taladro Percutor 1/2\" 750W Bosch", "FDN-HE-001", ("Herramientas Eléctricas", "Taladros y Atornilladores"), 280000, 449900, 15, 3, "unit"),
    ("Taladro Inalámbrico 20V Dewalt", "FDN-HE-002", ("Herramientas Eléctricas", "Taladros y Atornilladores"), 480000, 749900, 10, 2, "unit"),
    ("Atornillador Inalámbrico 12V", "FDN-HE-003", ("Herramientas Eléctricas", "Taladros y Atornilladores"), 180000, 289900, 18, 4, "unit"),
    # Herramientas Eléctricas > Pulidoras y Esmeriladoras
    ("Pulidora Angular 4.5\" 800W", "FDN-HE-004", ("Herramientas Eléctricas", "Pulidoras y Esmeriladoras"), 120000, 199900, 20, 4, "unit"),
    ("Pulidora Angular 7\" 2200W", "FDN-HE-005", ("Herramientas Eléctricas", "Pulidoras y Esmeriladoras"), 280000, 449900, 10, 2, "unit"),
    # Herramientas Eléctricas > Sierras Eléctricas
    ("Sierra Circular 7.25\" 1200W", "FDN-HE-006", ("Herramientas Eléctricas", "Sierras Eléctricas"), 320000, 499900, 8, 2, "unit"),
    ("Sierra Caladora 650W", "FDN-HE-007", ("Herramientas Eléctricas", "Sierras Eléctricas"), 220000, 349900, 10, 2, "unit"),
    # Plomería > Tubería PVC y CPVC
    ("Tubo PVC 1/2\" Presión x6m", "FDN-PL-001", ("Plomería", "Tubería PVC y CPVC"), 8500, 14900, 200, 40, "unit"),
    ("Tubo PVC 1\" Presión x6m", "FDN-PL-002", ("Plomería", "Tubería PVC y CPVC"), 16000, 27900, 150, 30, "unit"),
    ("Tubo PVC 2\" Sanitario x6m", "FDN-PL-003", ("Plomería", "Tubería PVC y CPVC"), 22000, 38900, 120, 25, "unit"),
    ("Tubo PVC 4\" Sanitario x6m", "FDN-PL-004", ("Plomería", "Tubería PVC y CPVC"), 48000, 79900, 80, 15, "unit"),
    # Plomería > Accesorios y Uniones
    ("Codo 90° PVC 1/2\"", "FDN-PL-005", ("Plomería", "Accesorios y Uniones"), 800, 1900, 500, 100, "unit"),
    ("Tee PVC 1/2\"", "FDN-PL-006", ("Plomería", "Accesorios y Uniones"), 1000, 2200, 400, 80, "unit"),
    ("Unión PVC 1\" Roscada", "FDN-PL-007", ("Plomería", "Accesorios y Uniones"), 1800, 3900, 300, 60, "unit"),
    # Plomería > Válvulas y Llaves
    ("Válvula Bola PVC 1/2\"", "FDN-PL-008", ("Plomería", "Válvulas y Llaves"), 8000, 14900, 100, 20, "unit"),
    ("Válvula Bola PVC 1\"", "FDN-PL-009", ("Plomería", "Válvulas y Llaves"), 14000, 24900, 80, 15, "unit"),
    # Plomería > Pegantes y Sellantes
    ("Pegante PVC 1/32 Galón", "FDN-PL-010", ("Plomería", "Pegantes y Sellantes"), 18000, 31900, 80, 15, "unit"),
    ("Cinta Teflón Rollo x12m", "FDN-PL-011", ("Plomería", "Pegantes y Sellantes"), 2500, 4900, 200, 40, "unit"),
    ("Silicona Transparente 280ml", "FDN-PL-012", ("Plomería", "Pegantes y Sellantes"), 12000, 21900, 100, 20, "unit"),
    # Electricidad > Cables y Alambres
    ("Cable THHN #12 x100m Rojo", "FDN-EL-001", ("Electricidad", "Cables y Alambres"), 85000, 139900, 50, 10, "unit"),
    ("Cable THHN #10 x100m Negro", "FDN-EL-002", ("Electricidad", "Cables y Alambres"), 130000, 209900, 35, 7, "unit"),
    ("Cable Dúplex 2x12 x100m", "FDN-EL-003", ("Electricidad", "Cables y Alambres"), 160000, 259900, 30, 6, "unit"),
    # Electricidad > Tomas e Interruptores
    ("Toma Sencilla 15A LEVITON", "FDN-EL-004", ("Electricidad", "Tomas e Interruptores"), 8000, 14900, 150, 30, "unit"),
    ("Interruptor Sencillo 15A", "FDN-EL-005", ("Electricidad", "Tomas e Interruptores"), 7000, 13900, 150, 30, "unit"),
    ("Toma Doble USB+110V", "FDN-EL-006", ("Electricidad", "Tomas e Interruptores"), 22000, 38900, 80, 15, "unit"),
    # Electricidad > Tableros y Breakers
    ("Tablero 4 Circuitos Monofásico", "FDN-EL-007", ("Electricidad", "Tableros y Breakers"), 45000, 74900, 20, 4, "unit"),
    ("Breaker 1x20A SQUARE D", "FDN-EL-008", ("Electricidad", "Tableros y Breakers"), 18000, 31900, 80, 15, "unit"),
    ("Breaker 2x30A SQUARE D", "FDN-EL-009", ("Electricidad", "Tableros y Breakers"), 35000, 59900, 40, 8, "unit"),
    # Pinturas y Acabados > Pinturas de Interior
    ("Pintura Vinílica Blanco Galón", "FDN-PT-001", ("Pinturas y Acabados", "Pinturas de Interior"), 28000, 48900, 80, 15, "unit"),
    ("Pintura Vinílica Color Galón", "FDN-PT-002", ("Pinturas y Acabados", "Pinturas de Interior"), 32000, 54900, 60, 12, "unit"),
    ("Esmalte Brillante Blanco Galón", "FDN-PT-003", ("Pinturas y Acabados", "Pinturas de Interior"), 38000, 64900, 50, 10, "unit"),
    # Pinturas y Acabados > Pinturas de Exterior
    ("Pintura Fachada Blanca Galón", "FDN-PT-004", ("Pinturas y Acabados", "Pinturas de Exterior"), 42000, 71900, 60, 12, "unit"),
    ("Impermeabilizante Acrílico Galón", "FDN-PT-005", ("Pinturas y Acabados", "Pinturas de Exterior"), 55000, 89900, 40, 8, "unit"),
    # Pinturas y Acabados > Accesorios de Pintura
    ("Rodillo Lana 9\" con Marco", "FDN-PT-006", ("Pinturas y Acabados", "Accesorios de Pintura"), 12000, 21900, 80, 15, "unit"),
    ("Brocha Cerda Natur 3\"", "FDN-PT-007", ("Pinturas y Acabados", "Accesorios de Pintura"), 8000, 14900, 100, 20, "unit"),
    ("Lija Grano 120 Pliego", "FDN-PT-008", ("Pinturas y Acabados", "Accesorios de Pintura"), 1500, 3200, 300, 60, "unit"),
    # Fijación y Tornillería > Tornillos y Pernos
    ("Tornillo Madera 8x2\" Caja x100", "FDN-FJ-001", ("Fijación y Tornillería", "Tornillos y Pernos"), 8000, 14900, 150, 30, "unit"),
    ("Tornillo Drywall 6x1\" Caja x250", "FDN-FJ-002", ("Fijación y Tornillería", "Tornillos y Pernos"), 12000, 21900, 120, 25, "unit"),
    ("Perno Hexagonal M10x50 Caja x50", "FDN-FJ-003", ("Fijación y Tornillería", "Tornillos y Pernos"), 18000, 31900, 80, 15, "unit"),
    # Fijación y Tornillería > Anclajes y Taquetes
    ("Taquete Plástico 5/16\" x100", "FDN-FJ-004", ("Fijación y Tornillería", "Anclajes y Taquetes"), 6000, 11900, 200, 40, "unit"),
    ("Anclaje Expansivo 3/8\"x3\" x50", "FDN-FJ-005", ("Fijación y Tornillería", "Anclajes y Taquetes"), 22000, 38900, 80, 15, "unit"),
    # Seguridad Industrial > Protección de Cabeza
    ("Casco Seguridad Blanco Tipo II", "FDN-SI-001", ("Seguridad Industrial", "Protección de Cabeza"), 18000, 31900, 50, 10, "unit"),
    ("Casco Seguridad con Matraca", "FDN-SI-002", ("Seguridad Industrial", "Protección de Cabeza"), 28000, 48900, 30, 6, "unit"),
    # Seguridad Industrial > Protección Visual y Auditiva
    ("Gafas de Seguridad Transparente", "FDN-SI-003", ("Seguridad Industrial", "Protección Visual y Auditiva"), 5500, 10900, 100, 20, "unit"),
    ("Tapa Oídos Espuma x2 NRR30", "FDN-SI-004", ("Seguridad Industrial", "Protección Visual y Auditiva"), 3000, 6900, 150, 30, "unit"),
    # Seguridad Industrial > Protección de Manos y Pies
    ("Guantes Carnaza Palma Reforzada", "FDN-SI-005", ("Seguridad Industrial", "Protección de Manos y Pies"), 12000, 21900, 80, 15, "unit"),
    ("Guantes Nitrilo Caja x100 M", "FDN-SI-006", ("Seguridad Industrial", "Protección de Manos y Pies"), 35000, 59900, 50, 10, "unit"),
    ("Botas Seguridad Punta Acero T42", "FDN-SI-007", ("Seguridad Industrial", "Protección de Manos y Pies"), 85000, 139900, 20, 4, "unit"),
    # Construcción > Cementos y Morteros
    ("Cemento Gris Argos 50kg", "FDN-CO-001", ("Construcción", "Cementos y Morteros"), 32000, 52900, 200, 50, "unit"),
    ("Mortero Pega Bloque x25kg", "FDN-CO-002", ("Construcción", "Cementos y Morteros"), 18000, 31900, 150, 30, "unit"),
    ("Aditivo Impermeabilizante 1kg", "FDN-CO-003", ("Construcción", "Cementos y Morteros"), 12000, 21900, 80, 15, "unit"),
    # Construcción > Mallas y Varillas
    ("Varilla Corrugada 3/8\" x6m", "FDN-CO-004", ("Construcción", "Mallas y Varillas"), 18000, 29900, 200, 40, "unit"),
    ("Varilla Corrugada 1/2\" x6m", "FDN-CO-005", ("Construcción", "Mallas y Varillas"), 28000, 46900, 150, 30, "unit"),
    ("Malla Electrosoldada 6\"x6\" 2x6m", "FDN-CO-006", ("Construcción", "Mallas y Varillas"), 55000, 89900, 80, 15, "unit"),
]

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Hernán",
        "last_name": "Ospina Castillo",
        "document_type": "CC",
        "document_number": "79345612",
        "email": "hernan.ospina@construccionesospina.com",
        "phone": "+57 310 234 5678",
        "address": "Cra. 30 # 12-45, Barrio Restrepo",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Constructora",
        "last_name": "Andes SAS",
        "document_type": "NIT",
        "document_number": "900234567-1",
        "email": "compras@constructoraandes.co",
        "phone": "+57 604 456 7890",
        "address": "Cll. 50 # 35-20, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Jorge",
        "last_name": "Ramírez Pinto",
        "document_type": "CC",
        "document_number": "16456789",
        "email": "jorge.ramirez@gmail.com",
        "phone": "+57 315 345 6789",
        "address": "Av. 3N # 22-15",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Ferretería",
        "last_name": "El Clavo SAS",
        "document_type": "NIT",
        "document_number": "800567890-2",
        "email": "ventas@ferreteriadelclavo.com",
        "phone": "+57 575 567 8901",
        "address": "Cra. 5 # 25-10, Centro",
        "city": "Manizales",
        "country": "Colombia",
    },
    {
        "first_name": "Ricardo",
        "last_name": "Suárez Moreno",
        "document_type": "CC",
        "document_number": "91678901",
        "email": "ricardosuarez@hotmail.com",
        "phone": "+57 317 456 7890",
        "address": "Cll. 35 # 28-60, Provenza",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Consorcio",
        "last_name": "Norte Infraestructura",
        "document_type": "NIT",
        "document_number": "901345678-3",
        "email": "licitaciones@norteinfra.co",
        "phone": "+57 575 678 9012",
        "address": "Cra. 9 # 15-40, La Floresta",
        "city": "Cúcuta",
        "country": "Colombia",
    },
    {
        "first_name": "Mauricio",
        "last_name": "Torres Varela",
        "document_type": "CC",
        "document_number": "13789012",
        "email": "mauricio.torres@gmail.com",
        "phone": "+57 311 789 0123",
        "address": "Cll. 5 # 15-22",
        "city": "Cúcuta",
        "country": "Colombia",
    },
    {
        "first_name": "Eléctricos",
        "last_name": "Potencia del Norte SAS",
        "document_type": "NIT",
        "document_number": "901456789-1",
        "email": "compras@potencianorte.com",
        "phone": "+57 310 890 1234",
        "address": "Zona Industrial Cra. 22 # 8-15",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Claudia",
        "last_name": "Mendoza Ríos",
        "document_type": "CC",
        "document_number": "38901234",
        "email": "claudia.mendoza@gmail.com",
        "phone": "+57 320 901 2345",
        "address": "Cra. 27B # 40-12, Bello Horizonte",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Constructora",
        "last_name": "Pacífico Verde Ltda",
        "document_type": "NIT",
        "document_number": "891234567-2",
        "email": "contabilidad@pacificoverde.co",
        "phone": "+57 602 012 3456",
        "address": "Av. Simón Bolívar # 34-80",
        "city": "Pasto",
        "country": "Colombia",
    },
    {
        "first_name": "Alejandro",
        "last_name": "Gutierrez Peña",
        "document_type": "CC",
        "document_number": "1094012345",
        "email": "alejandro.gp@gmail.com",
        "phone": "+57 316 012 3456",
        "address": "Cll. 12 # 5-30, Centro",
        "city": "Armenia",
        "country": "Colombia",
    },
    {
        "first_name": "Isabel",
        "last_name": "Navarro Cruz",
        "document_type": "CC",
        "document_number": "46123456",
        "email": "isabel.navarro@outlook.com",
        "phone": "+57 321 123 4567",
        "address": "Cra. 8 # 22-18, Villa del Rosario",
        "city": "Cúcuta",
        "country": "Colombia",
    },
    {
        "first_name": "Plomeros",
        "last_name": "Asociados del Eje SAS",
        "document_type": "NIT",
        "document_number": "901567890-4",
        "email": "pedidos@plomeroseje.co",
        "phone": "+57 312 234 5679",
        "address": "Cll. 19 # 9-44, El Centro",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Carlos",
        "last_name": "Salinas Hurtado",
        "document_type": "CC",
        "document_number": "6234567",
        "email": "csalinas.hurtado@yahoo.com",
        "phone": "+57 314 345 6782",
        "address": "Cra. 15 # 30-08, Chipre",
        "city": "Manizales",
        "country": "Colombia",
    },
    {
        "first_name": "Urbanizadora",
        "last_name": "Casas del Caribe SA",
        "document_type": "NIT",
        "document_number": "860345678-3",
        "email": "compras@casasdelcaribe.co",
        "phone": "+57 605 456 7895",
        "address": "Cll. 72 # 57-43, El Prado",
        "city": "Barranquilla",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "vendedor1@ferrallasdelnorte.co",
        "first_name": "Jhonatan",
        "last_name": "Quintero",
        "phone": "+57 310 111 2222",
    },
    {
        "email": "vendedor2@ferrallasdelnorte.co",
        "first_name": "Paola",
        "last_name": "Castañeda",
        "phone": "+57 310 333 4444",
    },
    {
        "email": "vendedor3@ferrallasdelnorte.co",
        "first_name": "Eduardo",
        "last_name": "Serna",
        "phone": "+57 310 555 6666",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]
IVA_RATE = Decimal("0.19")


def seed(session: Session) -> None:
    """Main seed function for Ferrallas del Norte demo data."""

    # ── 1. Get the target organization ───────────────────────────────
    org = session.exec(
        select(Organization).where(Organization.slug == ORG_SLUG)
    ).first()
    if not org:
        logger.error(f"Organization '{ORG_SLUG}' not found. Create it first.")
        return
    org_id = org.id
    logger.info(f"Using organization: {org.name} ({org_id})")

    # Idempotency check
    existing = session.exec(
        select(Product)
        .where(Product.organization_id == org_id)
        .where(Product.deleted_at.is_(None))
    ).first()
    if existing:
        logger.warning("Demo data already exists. Skipping seed.")
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

    # ── 7. Initial inventory movements ───────────────────────────────
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
            reason="Stock inicial - Inventario de apertura Ferrallas del Norte",
            created_at=datetime.now(timezone.utc) - timedelta(days=40),
        ))
    session.commit()
    logger.info("Created initial inventory movements")

    # ── 8. Create customers ──────────────────────────────────────────
    customer_list: list[Customer] = []
    for cust_data in CUSTOMERS_DATA:
        customer = Customer(organization_id=org_id, **cust_data, is_active=True)
        session.add(customer)
        customer_list.append(customer)
    session.commit()
    for c in customer_list:
        session.refresh(c)
    logger.info(f"Created {len(customer_list)} customers")

    # ── 9. Create sales — 45 days, heavier Mon–Sat ───────────────────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(45, -1, -1):
        day = now - timedelta(days=days_ago)
        is_sunday = day.weekday() == 6
        is_saturday = day.weekday() == 5
        if is_sunday:
            num_sales = random.randint(1, 3)
        elif is_saturday:
            num_sales = random.randint(4, 9)
        else:
            num_sales = random.randint(5, 12)
        if days_ago == 0:
            num_sales = random.randint(6, 10)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"FDN-{invoice_counter:06d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.65 else None

            # Ferreterías: many items per sale, higher quantities for fasteners/plumbing
            num_items = random.randint(1, 6)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(7, 18)
            sale_minute = random.randint(0, 59)
            sale_date = day.replace(
                hour=sale_hour, minute=sale_minute,
                second=random.randint(0, 59), microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = random.randint(1, 10)
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

            discount = (subtotal * Decimal(str(random.randint(0, 8))) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.04 and days_ago > 0
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
                    "Cliente cambió de opinión",
                    "Producto sin stock",
                    "Error en el pedido",
                    "Cliente solicitó cambio de referencia",
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

    # ── 10. Restock low-inventory products ───────────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(30, 100)
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
                reason="Reposición de inventario Ferrallas del Norte",
                created_at=now - timedelta(hours=random.randint(1, 72)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED FERRALLAS DEL NORTE COMPLETE!")
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
    random.seed(7)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
