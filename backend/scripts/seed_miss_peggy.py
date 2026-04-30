"""
Seed script for Miss Peggy — Colombian naturist store and beauty supply shop.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_miss_peggy.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - Real inventory extracted from "Inventario Miss Peggy.xlsx" (April 2026)
  - Two product lines: Naturismo (supplements, plants, solar care) and
    Belleza (hair care, dyes, wax, makeup, nail supplies)
  - Prices in COP taken directly from the Excel
  - Sales history simulates Jan–Apr 2026 (118 days), consistent with
    actual monthly volumes recorded in the spreadsheet
  - Small store: low daily volume, single units per sale
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

ORG_SLUG = "peggy"

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Naturismo",
        "description": "Suplementos, plantas medicinales y productos naturales",
        "children": [
            {"name": "Suplementos y Vitaminas", "description": "Vitaminas, minerales, proteínas y suplementos importados"},
            {"name": "Plantas y Hierbas Medicinales", "description": "Gotas, tinturas, hierbas y plantas medicinales"},
            {"name": "Protección Solar y Cuidado Naturista", "description": "Bloqueadores solares, cremas y cuidado corporal natural"},
            {"name": "Alimentos y Productos Naturales Varios", "description": "Semillas, harinas, endulzantes, propóleos y naturales varios"},
        ],
    },
    {
        "name": "Belleza",
        "description": "Productos para cabello, maquillaje, uñas y cuidado personal",
        "children": [
            {"name": "Cuidado Capilar", "description": "Shampoos, acondicionadores, mascarillas y tratamientos capilares"},
            {"name": "Tintes y Coloración", "description": "Tintes profesionales, matizantes, decolorantes y henna"},
            {"name": "Cera y Depilación", "description": "Ceras depilatoria en perlas, frasco, cremas y accesorios"},
            {"name": "Maquillaje", "description": "Base, labiales, polvos, delineadores, sombras y rubor"},
            {"name": "Uñas y Manicure", "description": "Esmaltes, bases, limas, pusher, removedor y accesorios de uñas"},
            {"name": "Accesorios de Belleza", "description": "Brochas, tijeras, cosmetiqueras y accesorios varios"},
        ],
    },
]

# ---------------------------------------------------------------------------
# Products
# (name, sku, cat_path, price_cop, initial_stock, stock_min, unit)
# cost_price is computed as ~55% of sale price (naturismo) or ~50% (belleza)
# initial_stock = stock_actual + total_historical_sales (so depletion ends at real current stock)
# ---------------------------------------------------------------------------

# Helper: price -> cost (55% naturismo, 50% belleza)
def _cost(price: int, pct: float = 0.55) -> int:
    return max(1, int(price * pct))


# ── NATURISMO ────────────────────────────────────────────────────────────────

# (name, sku, cat_leaf, price, initial_stock, stock_min)
# initial_stock = stock_actual + v_ene + v_feb + v_mar + v_abr
_NATURISMO_RAW: list[tuple] = [
    # Suplementos y Vitaminas — Healthy America
    ("Biotina",                             "MP-HA-001", "Suplementos y Vitaminas", 47000, 1+1+0+2+0,  1),
    ("B Complex with B12 x90 tablets",      "MP-HA-002", "Suplementos y Vitaminas", 42000, 1+0+0+0+0,  1),
    ("Calcio x100 sofgels",                 "MP-HA-003", "Suplementos y Vitaminas", 48000, 1+0+0+0+0,  1),
    ("Colágeno x100 softgels",              "MP-HA-004", "Suplementos y Vitaminas", 68000, 2+0+0+0+0,  1),
    ("Colágeno + Biotina x60 softgels",     "MP-HA-005", "Suplementos y Vitaminas", 68000, 1+0+2+0+0,  1),
    ("Colostrum x60 sofgels",               "MP-HA-006", "Suplementos y Vitaminas", 63000, 1+0+0+0+0,  1),
    ("Creatina x300g",                      "MP-HA-007", "Suplementos y Vitaminas", 125000, 1+1+3+0+0, 1),
    ("Garlic x100 softgels",                "MP-HA-008", "Suplementos y Vitaminas", 28000, 1+0+0+0+0,  1),
    ("Ginkgo Biloba x60 sofgels HA",        "MP-HA-009", "Suplementos y Vitaminas", 38000, 1+1+0+1+0,  1),
    ("Max for Men / Megan for Women",       "MP-HA-010", "Suplementos y Vitaminas", 76000, 2+0+0+0+0,  1),
    ("Mega Cranberry",                      "MP-HA-011", "Suplementos y Vitaminas", 70000, 1+0+0+0+0,  1),
    ("Melatonina 3mg HA",                   "MP-HA-012", "Suplementos y Vitaminas", 43000, 1+0+0+0+0,  1),
    ("Milk Thistle x90 sofgels",            "MP-HA-013", "Suplementos y Vitaminas", 70000, 1+0+1+0+1,  1),
    ("Omega 3 x60 sofgels 1360mg",          "MP-HA-014", "Suplementos y Vitaminas", 65000, 2+0+0+0+1,  1),
    ("Reswine x60",                         "MP-HA-015", "Suplementos y Vitaminas", 65000, 1+0+0+0+0,  1),
    ("Saw Palmetto HA",                     "MP-HA-016", "Suplementos y Vitaminas", 60000, 1+1+1+0+0,  1),
    ("Super Magnesium",                     "MP-HA-017", "Suplementos y Vitaminas", 80000, 2+2+1+3+2,  1),
    ("Vitamina A x100 sofgels",             "MP-HA-018", "Suplementos y Vitaminas", 40000, 1+0+1+0+0,  1),
    ("Vita C 1000mg",                       "MP-HA-019", "Suplementos y Vitaminas", 65000, 1+1+0+0+1,  1),
    ("Vitamina D3 HA",                      "MP-HA-020", "Suplementos y Vitaminas", 42000, 1+0+0+1+0,  1),
    ("Zinc Chelated",                       "MP-HA-021", "Suplementos y Vitaminas", 42000, 1+0+0+0+0,  1),
    # Suplementos — Natural Systems
    ("Ácido Hialurónico cápsulas tópicas",  "MP-NS-001", "Suplementos y Vitaminas", 1800,  92+0+4+16+8,  10),
    ("Aloe Vera y Retinol cápsulas tópicas","MP-NS-002", "Suplementos y Vitaminas", 1200,  108+1+75+31+12, 15),
    ("Balanced B x100 sofgels",             "MP-NS-003", "Suplementos y Vitaminas", 42000, 1+0+0+0+0,   1),
    ("Betacaroteno x100 sofgels",           "MP-NS-004", "Suplementos y Vitaminas", 52000, 1+0+0+1+0,   1),
    ("Biotina 10.000 mcg NS",               "MP-NS-005", "Suplementos y Vitaminas", 68000, 1+0+0+0+0,   1),
    ("Biotina 900 mcg NS",                  "MP-NS-006", "Suplementos y Vitaminas", 47000, 1+0+0+0+0,   1),
    ("Castaño de Indias x60 sofgels",       "MP-NS-007", "Suplementos y Vitaminas", 45000, 1+0+3+0+0,   1),
    ("Centella Asiática NS",                "MP-NS-008", "Suplementos y Vitaminas", 35000, 1+0+0+0+0,   1),
    ("Colágeno x60 NS",                     "MP-NS-009", "Suplementos y Vitaminas", 46000, 1+0+0+0+0,   1),
    ("Colágeno x100 NS",                    "MP-NS-010", "Suplementos y Vitaminas", 65000, 1+0+0+0+0,   1),
    ("Garlic NS",                           "MP-NS-011", "Suplementos y Vitaminas", 28000, 1+0+0+0+0,   1),
    ("Ginkgo Biloba x60 NS",                "MP-NS-012", "Suplementos y Vitaminas", 35000, 1+1+1+0+0,   1),
    ("Ginkgo Biloba x100 NS",               "MP-NS-013", "Suplementos y Vitaminas", 60000, 1+1+1+2+0,   1),
    ("Glucosamina x60 NS",                  "MP-NS-014", "Suplementos y Vitaminas", 44000, 1+0+0+1+0,   1),
    ("Glucosamina x100 NS",                 "MP-NS-015", "Suplementos y Vitaminas", 78000, 1+0+0+0+0,   1),
    ("Maca x60 sofgels",                    "MP-NS-016", "Suplementos y Vitaminas", 51000, 1+0+0+1+0,   1),
    ("Magnesium NS",                        "MP-NS-017", "Suplementos y Vitaminas", 55000, 2+1+4+0+1,   1),
    ("Melatonina 3mg NS",                   "MP-NS-018", "Suplementos y Vitaminas", 33000, 1+1+1+0+0,   1),
    ("Melatonina 5mg NS",                   "MP-NS-019", "Suplementos y Vitaminas", 50000, 1+0+2+0+0,   1),
    ("Menop Formula",                       "MP-NS-020", "Suplementos y Vitaminas", 63000, 1+0+0+0+0,   1),
    ("Omega 3 x100 sofgels NS",             "MP-NS-021", "Suplementos y Vitaminas", 61000, 2+2+4+1+1,   1),
    ("Potassium x100 sofgels",              "MP-NS-022", "Suplementos y Vitaminas", 39000, 1+0+0+0+0,   1),
    ("Probióticos x60 sofgels",             "MP-NS-023", "Suplementos y Vitaminas", 53000, 1+0+0+1+0,   1),
    ("Resveratrol NS",                      "MP-NS-024", "Suplementos y Vitaminas", 74000, 1+0+1+1+0,   1),
    ("Saw Palmetto x60 NS",                 "MP-NS-025", "Suplementos y Vitaminas", 48000, 1+0+0+0+0,   1),
    ("Soy Isoflavones",                     "MP-NS-026", "Suplementos y Vitaminas", 38000, 2+0+0+0+0,   1),
    ("Spirulina NS",                        "MP-NS-027", "Suplementos y Vitaminas", 50000, 1+0+0+0+0,   1),
    ("Vitamina C x100 NS",                  "MP-NS-028", "Suplementos y Vitaminas", 58000, 1+0+0+0+0,   1),
    ("Vitamina C x60 NS",                   "MP-NS-029", "Suplementos y Vitaminas", 43000, 1+0+0+0+1,   1),
    ("Vitamina D3 2000 NS",                 "MP-NS-030", "Suplementos y Vitaminas", 40000, 1+0+1+0+0,   1),
    ("Vitamina E 1000 x60 NS",              "MP-NS-031", "Suplementos y Vitaminas", 74000, 1+0+0+1+0,   1),
    ("Vitamina E 1000 x100 NS",             "MP-NS-032", "Suplementos y Vitaminas", 95000, 1+0+0+0+1,   1),
    ("Vitamina E 400 x60 NS",               "MP-NS-033", "Suplementos y Vitaminas", 40000, 1+0+1+0+0,   1),
    ("Zinc NS",                             "MP-NS-034", "Suplementos y Vitaminas", 47000, 1+0+0+0+0,   1),
    # Suplementos — Natural Freshly
    ("Alcachofa NF",                        "MP-NF-001", "Suplementos y Vitaminas", 26000, 1+1+0+0+1,   1),
    ("Artiflex",                            "MP-NF-002", "Suplementos y Vitaminas", 48000, 1+0+0+0+0,   1),
    ("Cloruro de Magnesio x50 cap NF",      "MP-NF-003", "Suplementos y Vitaminas", 25000, 1+1+0+1+0,   1),
    ("Colágeno Complex Caps x60",           "MP-NF-004", "Suplementos y Vitaminas", 30000, 1+0+0+1+0,   1),
    ("Complejo B NF",                       "MP-NF-005", "Suplementos y Vitaminas", 28000, 1+2+2+0+1,   1),
    ("Contorno de Ojos NF",                 "MP-NF-006", "Suplementos y Vitaminas", 35000, 1+0+0+0+0,   1),
    ("Cremas Naturales NF",                 "MP-NF-007", "Suplementos y Vitaminas", 22000, 15+1+2+1+0,  2),
    ("Esencias Freshly",                    "MP-NF-008", "Suplementos y Vitaminas", 15000, 8+4+6+6+2,   2),
    ("Freshly Pausia",                      "MP-NF-009", "Suplementos y Vitaminas", 40000, 1+0+0+0+1,   1),
    ("Fybofort",                            "MP-NF-010", "Suplementos y Vitaminas", 42000, 1+1+1+1+0,   1),
    ("Jabones Naturales NF",                "MP-NF-011", "Suplementos y Vitaminas", 11000, 13+0+1+0+1,  2),
    ("Mieltertos Pastillas",                "MP-NF-012", "Suplementos y Vitaminas", 2500,  7+4+2+3+0,   2),
    ("Omega 3 NF",                          "MP-NF-013", "Suplementos y Vitaminas", 54000, 1+0+0+0+1,   1),
    ("Propóleo y Propomielito",             "MP-NF-014", "Suplementos y Vitaminas", 22000, 1+1+1+0+1,   1),
    ("Prodefens x400g",                     "MP-NF-015", "Suplementos y Vitaminas", 42000, 1+0+0+0+0,   1),
    ("Urovital",                            "MP-NF-016", "Suplementos y Vitaminas", 42000, 1+0+0+0+0,   1),
    ("Vinagre Plus y Vinagre de Manzana",   "MP-NF-017", "Suplementos y Vitaminas", 22000, 3+5+0+0+1,   1),
    # Plantas y Hierbas — Naturfar
    ("Alcachofa x60ml Naturfar",            "MP-NTA-001", "Plantas y Hierbas Medicinales", 15000, 2+0+0+0+0,   1),
    ("Gotas Hepáticas Alcachofa Boldo x60ml","MP-NTA-002","Plantas y Hierbas Medicinales", 15000, 1+0+0+0+2,  1),
    ("Caléndula x60ml",                     "MP-NTA-003", "Plantas y Hierbas Medicinales", 15000, 1+1+0+1+0,  1),
    ("Cicalen x360ml",                      "MP-NTA-004", "Plantas y Hierbas Medicinales", 36000, 1+0+0+0+0,  1),
    ("Diente de León x60ml",                "MP-NTA-005", "Plantas y Hierbas Medicinales", 13000, 1+0+0+0+0,  1),
    ("Kadein Gotas x60ml",                  "MP-NTA-006", "Plantas y Hierbas Medicinales", 21000, 2+0+0+1+0,  1),
    ("Levadura de Cerveza tabletas",        "MP-NTA-007", "Plantas y Hierbas Medicinales", 20000, 1+1+0+0+0,  1),
    ("Manzanilla x60ml",                    "MP-NTA-008", "Plantas y Hierbas Medicinales", 15000, 1+0+0+0+0,  1),
    ("Pasiflora x60ml",                     "MP-NTA-009", "Plantas y Hierbas Medicinales", 15000, 2+1+0+0+0,  1),
    ("Valepass x60ml",                      "MP-NTA-010", "Plantas y Hierbas Medicinales", 17000, 2+0+1+1+2,  1),
    ("Valessan x60ml",                      "MP-NTA-011", "Plantas y Hierbas Medicinales", 16000, 1+0+3+0+0,  1),
    ("Vira-Vira",                           "MP-NTA-012", "Plantas y Hierbas Medicinales", 15000, 1+0+0+0+0,  1),
    # Plantas — Wilintong
    ("Acacia x40g",                         "MP-WI-001", "Plantas y Hierbas Medicinales", 3500,  6+3+10+1+6,  2),
    ("Almendras x50g",                      "MP-WI-002", "Plantas y Hierbas Medicinales", 5500,  1+0+0+0+0,   1),
    ("Avena x500g",                         "MP-WI-003", "Plantas y Hierbas Medicinales", 8000,  1+1+0+0+0,   1),
    ("Boldo x40g",                          "MP-WI-004", "Plantas y Hierbas Medicinales", 7000,  8+0+0+2+0,   2),
    ("Concha de Nácar",                     "MP-WI-005", "Plantas y Hierbas Medicinales", 5000,  5+0+0+0+0,   1),
    ("Dulces de Miel",                      "MP-WI-006", "Plantas y Hierbas Medicinales", 200,   185+22+22+34+3, 20),
    ("Flor de Jamaica x60g",                "MP-WI-007", "Plantas y Hierbas Medicinales", 9000,  3+2+2+2+3,   1),
    ("Flor de Jamaica x100g",               "MP-WI-008", "Plantas y Hierbas Medicinales", 14000, 4+1+5+3+4,   1),
    ("Linaza x250g",                        "MP-WI-009", "Plantas y Hierbas Medicinales", 7000,  7+2+0+1+0,   1),
    ("Linaza x500g",                        "MP-WI-010", "Plantas y Hierbas Medicinales", 12000, 5+0+1+1+0,   1),
    ("Moringa x100g",                       "MP-WI-011", "Plantas y Hierbas Medicinales", 9000,  4+0+1+0+1,   1),
    ("Moringa cápsulas",                    "MP-WI-012", "Plantas y Hierbas Medicinales", 35000, 2+0+0+0+0,   1),
    ("Polen x125g",                         "MP-WI-013", "Plantas y Hierbas Medicinales", 15000, 1+0+0+0+0,   1),
    ("Polen x250g",                         "MP-WI-014", "Plantas y Hierbas Medicinales", 25000, 1+0+1+0+0,   1),
    ("Pomada de Coca",                      "MP-WI-015", "Plantas y Hierbas Medicinales", 15000, 6+0+0+0+0,   1),
    ("Pomada Verde",                        "MP-WI-016", "Plantas y Hierbas Medicinales", 2500,  7+1+0+0+0,   1),
    ("Psyllium x100g",                      "MP-WI-017", "Plantas y Hierbas Medicinales", 20000, 1+0+0+0+0,   1),
    ("Psyllium x200g",                      "MP-WI-018", "Plantas y Hierbas Medicinales", 35000, 1+0+0+1+0,   1),
    ("Psyllium x400g",                      "MP-WI-019", "Plantas y Hierbas Medicinales", 58000, 1+0+0+1+0,   1),
    ("Sal Marina x500g",                    "MP-WI-020", "Plantas y Hierbas Medicinales", 2500,  7+3+0+0+0,   1),
    ("Sangre de Drago",                     "MP-WI-021", "Plantas y Hierbas Medicinales", 9000,  3+2+1+0+0,   1),
    ("Semilla de Chía x100g",               "MP-WI-022", "Plantas y Hierbas Medicinales", 8000,  4+2+0+0+0,   1),
    ("Semilla de Chía x250g",               "MP-WI-023", "Plantas y Hierbas Medicinales", 16000, 1+0+0+0+0,   1),
    ("Semilla de Chía x500g",               "MP-WI-024", "Plantas y Hierbas Medicinales", 26000, 3+0+1+0+0,   1),
    ("Sen x40g",                            "MP-WI-025", "Plantas y Hierbas Medicinales", 3000,  6+2+2+0+2,   1),
    # Protección Solar — Ledmar
    ("Bloqueador Solar Niños Ledmar",       "MP-LD-001", "Protección Solar y Cuidado Naturista", 50000, 3+0+0+0+0,   1),
    ("Contorno de Ojos Ledmar",             "MP-LD-002", "Protección Solar y Cuidado Naturista", 68000, 1+0+0+0+0,   1),
    ("Crema Corporal Arawak",               "MP-LD-003", "Protección Solar y Cuidado Naturista", 28000, 4+0+0+0+0,   1),
    ("Sobres Bloqueador Arawak",            "MP-LD-004", "Protección Solar y Cuidado Naturista", 4000,  12+0+0+0+0,  2),
    ("Sobres Bloqueador Arawak Niños",      "MP-LD-005", "Protección Solar y Cuidado Naturista", 2500,  5+1+0+0+0,   1),
    # Varios Naturales
    ("Aguaje Natural Medix",                "MP-VA-001", "Alimentos y Productos Naturales Varios", 35000, 2+3+1+1+0,  1),
    ("Alovay Aloe Vera",                    "MP-VA-002", "Alimentos y Productos Naturales Varios", 18000, 1+0+0+1+0,  1),
    ("Biocross",                            "MP-VA-003", "Alimentos y Productos Naturales Varios", 5000,  1+1+1+3+4,  1),
    ("Bronquisan Jalea",                    "MP-VA-004", "Alimentos y Productos Naturales Varios", 14000, 5+0+0+1+0,  1),
    ("Café de Brusca",                      "MP-VA-005", "Alimentos y Productos Naturales Varios", 35000, 1+0+1+0+0,  1),
    ("Citrato de Magnesio Botanitas",       "MP-VA-006", "Alimentos y Productos Naturales Varios", 60000, 2+0+0+0+0,  1),
    ("Clorofila Natural Medy",              "MP-VA-007", "Alimentos y Productos Naturales Varios", 18000, 2+0+0+0+1,  1),
    ("Colágeno Bovino x1000g 3Q",           "MP-VA-008", "Alimentos y Productos Naturales Varios", 45000, 2+0+2+0+0,  1),
    ("Colágeno Marino 3Q",                  "MP-VA-009", "Alimentos y Productos Naturales Varios", 52000, 1+0+1+0+0,  1),
    ("Coloncleanser Sabores",               "MP-VA-010", "Alimentos y Productos Naturales Varios", 28500, 4+2+4+0+1,  1),
    ("Coloncleanser Tradicional",           "MP-VA-011", "Alimentos y Productos Naturales Varios", 25500, 3+4+4+0+1,  1),
    ("Chanca Piedra Jarabe x360ml",         "MP-VA-012", "Alimentos y Productos Naturales Varios", 25000, 2+0+0+0+0,  1),
    ("Fenogreco Natural Medix",             "MP-VA-013", "Alimentos y Productos Naturales Varios", 35000, 2+1+2+2+0,  1),
    ("Irene Melo RP y Advance",             "MP-VA-014", "Alimentos y Productos Naturales Varios", 90000, 2+0+0+2+0,  1),
    ("Irene Melos Pequeño",                 "MP-VA-015", "Alimentos y Productos Naturales Varios", 57000, 3+1+0+0+1,  1),
    ("Cúrcuma Cápsulas x100",               "MP-VA-016", "Alimentos y Productos Naturales Varios", 54000, 1+0+0+1+1,  1),
    ("Marañón",                             "MP-VA-017", "Alimentos y Productos Naturales Varios", 9000,  6+0+0+0+1,  1),
    ("Megabolic",                           "MP-VA-018", "Alimentos y Productos Naturales Varios", 55000, 1+0+2+0+0,  1),
    ("Megaplex",                            "MP-VA-019", "Alimentos y Productos Naturales Varios", 75000, 2+1+1+1+0,  1),
    ("Propóleo CYM",                        "MP-VA-020", "Alimentos y Productos Naturales Varios", 15000, 2+0+0+0+1,  1),
    ("Purgante Boldex",                     "MP-VA-021", "Alimentos y Productos Naturales Varios", 25000, 6+5+1+1+0,  1),
    ("Purgante Escobita",                   "MP-VA-022", "Alimentos y Productos Naturales Varios", 14000, 3+2+2+1+0,  1),
    ("Purgante Limpiaplus",                 "MP-VA-023", "Alimentos y Productos Naturales Varios", 10000, 3+3+0+0+3,  1),
    ("Stevia Gotas",                        "MP-VA-024", "Alimentos y Productos Naturales Varios", 20000, 2+0+2+0+0,  1),
    ("Té Verde + Tarro y 3 Bailarinas",     "MP-VA-025", "Alimentos y Productos Naturales Varios", 33000, 2+3+6+3+2,  1),
    ("TNT",                                 "MP-VA-026", "Alimentos y Productos Naturales Varios", 90000, 1+0+0+0+1,  1),
    ("Ultradolor",                          "MP-VA-027", "Alimentos y Productos Naturales Varios", 26000, 1+1+1+0+2,  1),
    ("Vinagre con Madre CYM",               "MP-VA-028", "Alimentos y Productos Naturales Varios", 27000, 4+2+2+0+1,  1),
    ("Vitaminas Tópicas Gotas",             "MP-VA-029", "Alimentos y Productos Naturales Varios", 12000, 2+0+0+0+0,  1),
    ("Vitacerbin-a",                        "MP-VA-030", "Alimentos y Productos Naturales Varios", 20000, 3+4+0+0+0,  1),
    ("Vitafer L",                           "MP-VA-031", "Alimentos y Productos Naturales Varios", 40000, 2+2+3+3+1,  1),
    ("Zarzaparrilla",                       "MP-VA-032", "Alimentos y Productos Naturales Varios", 18000, 1+0+0+0+1,  1),
]

# ── BELLEZA ──────────────────────────────────────────────────────────────────

_BELLEZA_RAW: list[tuple] = [
    # Cuidado Capilar — Lehit
    ("Ampolletas de Pelo Lehit",            "MP-LH-001", "Cuidado Capilar", 5000,  38+0+15+12+7,  5),
    ("Tono a Tono / Tratamientos Lehit",    "MP-LH-002", "Cuidado Capilar", 3000,  142+22+23+31+10, 15),
    ("Shampoo en Pote x300ml Lehit",        "MP-LH-003", "Cuidado Capilar", 19500, 3+1+1+1+1,     1),
    ("Tratamiento en Frasco x300ml Lehit",  "MP-LH-004", "Cuidado Capilar", 25000, 6+0+2+0+0,     1),
    ("Tratamiento en Pote Redondo x300ml",  "MP-LH-005", "Cuidado Capilar", 26000, 1+1+0+0+0,     1),
    ("Tintes Lehit",                        "MP-LH-006", "Tintes y Coloración", 18000, 5+0+0+0+0,  1),
    # Cuidado Capilar — Lissia
    ("Aceites Capilares Lissia x115ml",     "MP-LI-001", "Cuidado Capilar", 9000,  3+1+0+0+0,     1),
    ("Aceite Ricino Lissia x27ml",          "MP-LI-002", "Cuidado Capilar", 8000,  4+0+0+0+0,     1),
    ("Cera Moldeadora Lissia",              "MP-LI-003", "Cuidado Capilar", 19000, 3+0+1+0+0,     1),
    ("Cera Moldeadora en Cojín Lissia",     "MP-LI-004", "Cuidado Capilar", 7000,  11+3+1+0+2,    2),
    ("Crema Piernas Q10 y Avena x850",      "MP-LI-005", "Cuidado Capilar", 20000, 1+0+0+2+0,     1),
    ("Crema Piernas Cannabis Q10 x410",     "MP-LI-006", "Cuidado Capilar", 13000, 2+0+2+1+0,     1),
    ("Mascarilla Biosil x260g",             "MP-LI-007", "Cuidado Capilar", 16000, 1+0+0+0+0,     1),
    ("Mascarilla Equino Res Embrión x490g", "MP-LI-008", "Cuidado Capilar", 18000, 4+0+2+0+0,     1),
    ("Mascarilla Repolarizante Cebolla x260g","MP-LI-009","Cuidado Capilar",12000, 5+1+1+0+0,     1),
    ("Mascarilla Cebolla Repolarizante x490g","MP-LI-010","Cuidado Capilar",20000, 2+1+1+0+0,     1),
    ("Mascarilla Crece Pelo Biosil x490g",  "MP-LI-011", "Cuidado Capilar", 21000, 3+1+0+0+0,     1),
    ("Shampoo Crece Pelo Lissia x850ml",    "MP-LI-012", "Cuidado Capilar", 30000, 1+0+0+0+0,     1),
    ("Shampoo y Acond Embrión Cebolla x425ml","MP-LI-013","Cuidado Capilar",12500, 4+5+2+4+0,    1),
    ("Shampoo y Acond Embrión Equino x425ml","MP-LI-014","Cuidado Capilar", 14000, 14+1+2+0+1,   2),
    ("Shampoo y Acond Biosil Equino x850ml","MP-LI-015","Cuidado Capilar",  21000, 3+0+1+1+1,     1),
    ("Shampoo Embrión de Pato x850ml Lissia","MP-LI-016","Cuidado Capilar", 22000, 7+3+0+0+1,    1),
    ("Shampoo Biosil x850 Lissia",          "MP-LI-017", "Cuidado Capilar", 22500, 4+0+0+0+2,    1),
    ("Shampoo Keratina Ácido Hialurónico x560ml","MP-LI-018","Cuidado Capilar",20000,8+1+1+0+0,  2),
    ("Shampoo y Acond Cebolla x850ml",      "MP-LI-019", "Cuidado Capilar", 21500, 2+0+0+2+1,    1),
    ("Sobre Shampoo y Tratamientos x90ml",  "MP-LI-020", "Cuidado Capilar", 3500,  5+7+5+6+4,    2),
    ("Tratamiento Repolarizador x90ml",     "MP-LI-021", "Cuidado Capilar", 4000,  25+0+3+2+0,   3),
    ("Sobres Tratamiento Keratina x90ml",   "MP-LI-022", "Cuidado Capilar", 5500,  5+2+5+5+3,    2),
    ("Sobres Tratamiento Biosil x90ml",     "MP-LI-023", "Cuidado Capilar", 6000,  20+4+4+6+7,   3),
    ("Bases Lissia Uñas de Acero",          "MP-LI-024", "Uñas y Manicure", 9500,  8+3+0+0+0,    1),
    # Cuidado Capilar — Naissant / Naturaleza y Vida
    ("Shampoo y Mascarilla Naissant x300ml","MP-NA-001", "Cuidado Capilar", 36000, 12+2+0+1+0,   1),
    ("Shampoo y Mascarilla Naissant x40ml", "MP-NA-002", "Cuidado Capilar", 6500,  47+8+9+13+3,  5),
    ("Shampoo Naturaleza y Vida",           "MP-NA-003", "Cuidado Capilar", 21000, 5+0+0+0+1,    1),
    ("Mascarilla Naturaleza y Vida",        "MP-NA-004", "Cuidado Capilar", 27000, 6+0+0+0+0,    1),
    # Cuidado Capilar — Prokpil
    ("Crema para Peinar Rizos Prokpil x300ml","MP-PK-001","Cuidado Capilar",30000, 1+2+0+2+0,    1),
    ("Gel Rizos Prokpil",                   "MP-PK-002", "Cuidado Capilar", 21000, 2+1+0+2+0,    1),
    ("Leche Pelo Adulto y Niños x250ml",    "MP-PK-003", "Cuidado Capilar", 25000, 5+1+0+0+0,    1),
    ("Leche Pelo Adulto y Niños x440ml",    "MP-PK-004", "Cuidado Capilar", 38000, 9+1+0+0+0,    1),
    ("Sobres Leche Termo Tratamientos Prokpil","MP-PK-005","Cuidado Capilar",4000, 1+3+0+0+1,    1),
    ("Tratamiento Color x150ml Prokpil",    "MP-PK-006", "Cuidado Capilar", 15000, 2+0+3+0+0,    1),
    ("Tratamiento Color x300ml Prokpil",    "MP-PK-007", "Cuidado Capilar", 30000, 12+2+0+0+0,   1),
    # Cuidado Capilar — Recamier
    ("Cera Moldeadora Recamier + Termoprotector","MP-RC-001","Cuidado Capilar",36000,9+1+0+0+0,  1),
    ("Keratina Paso 1 Recamier porcionada", "MP-RC-002", "Cuidado Capilar", 15000, 1+0+0+0+0,    1),
    ("Keratina Paso 2 Recamier porcionada", "MP-RC-003", "Cuidado Capilar", 50000, 1+0+2+3+1,    1),
    ("Keratina Paso 3 Recamier porcionada", "MP-RC-004", "Cuidado Capilar", 20000, 1+0+0+0+0,    1),
    ("Laca Media y Fuerte Recamier",        "MP-RC-005", "Cuidado Capilar", 37000, 3+1+0+0+0,    1),
    ("Shampoo Económico x1000ml Recamier",  "MP-RC-006", "Cuidado Capilar", 36000, 1+1+0+0+1,    1),
    ("Acondicionador Económico x1000ml",    "MP-RC-007", "Cuidado Capilar", 40000, 2+0+0+0+0,    1),
    ("Serum x120ml Liss Control Recamier",  "MP-RC-008", "Cuidado Capilar", 59000, 1+0+0+0+0,    1),
    ("Shampoo Fortex x300ml Recamier",      "MP-RC-009", "Cuidado Capilar", 35000, 1+0+0+0+0,    1),
    ("Shampoo InDandruff / Liss / Rizos x300ml","MP-RC-010","Cuidado Capilar",34000,2+1+0+0+0,   1),
    ("Shampoo y Acond x1000ml Recamier",    "MP-RC-011", "Cuidado Capilar", 60000, 14+0+2+0+0,   2),
    ("Shampoo y Tratamiento Vegano x1000ml","MP-RC-012", "Cuidado Capilar", 61000, 2+0+0+0+0,    1),
    # Cuidado Capilar — María Salomé
    ("Crema para Peinar x350ml M.Salomé",   "MP-MS-001", "Cuidado Capilar", 26000, 1+1+1+0+0,    1),
    ("Gel Fijador M.Salomé",                "MP-MS-002", "Cuidado Capilar", 20500, 2+3+1+1+0,    1),
    ("Loción Capilar M.Salomé",             "MP-MS-003", "Cuidado Capilar", 32000, 12+0+2+1+0,   2),
    ("Shampoo y Acond Keratin M.Salomé",    "MP-MS-004", "Cuidado Capilar", 35000, 4+0+0+1+0,    1),
    ("Shampoo y Acond Color M.Salomé",      "MP-MS-005", "Cuidado Capilar", 37000, 1+0+0+0+1,    1),
    ("Shampoo Prevención Caída M.Salomé",   "MP-MS-006", "Cuidado Capilar", 32000, 1+2+2+1+1,    1),
    # Tintes — Duvy Class
    ("Keratina Sobre Duvy",                 "MP-DC-001", "Tintes y Coloración", 3000, 5+0+0+0+0,  1),
    ("Laca Cojín Duvy",                     "MP-DC-002", "Tintes y Coloración", 10000, 1+1+0+2+1, 1),
    ("Laca Frasco Duvy",                    "MP-DC-003", "Tintes y Coloración", 20000, 2+1+1+2+0,  1),
    ("Silicona en Sobre Duvy",              "MP-DC-004", "Tintes y Coloración", 3000,  1+2+1+1+1,  1),
    ("Tintes Duvy Class",                   "MP-DC-005", "Tintes y Coloración", 11000, 64+3+1+5+0, 8),
    # Tintes — Alfaparf y Marliou
    ("Alfaparf Tinte",                      "MP-TI-001", "Tintes y Coloración", 24000, 65+4+3+2+2, 8),
    ("Blondo / Decolorante Alfaparf",       "MP-TI-002", "Tintes y Coloración", 13000, 4+1+0+0+0,  1),
    ("Color 1 Tinte Pelo",                  "MP-TI-003", "Tintes y Coloración", 6000,  29+15+17+14+11, 5),
    ("Aguas Oxigenantes",                   "MP-TI-004", "Tintes y Coloración", 3500,  91+6+2+3+2,  8),
    ("Decolorante Marliou 1000ml",          "MP-TI-005", "Tintes y Coloración", 18500, 3+0+0+0+0,  1),
    ("Blondon Marliou x20g + Shampoo x20ml","MP-TI-006", "Tintes y Coloración", 3500,  9+2+0+1+2,   1),
    ("Blondon Marliou x50g",                "MP-TI-007", "Tintes y Coloración", 8000,  23+0+1+0+0,  2),
    ("Blondon Marliou Pote x400g",          "MP-TI-008", "Tintes y Coloración", 50000, 2+0+0+0+0,  1),
    ("Henna x20g",                          "MP-TI-009", "Tintes y Coloración", 8000,  16+0+2+2+1,  2),
    ("Henna x80g",                          "MP-TI-010", "Tintes y Coloración", 23000, 10+1+1+1+0,  1),
    ("Marliou Tinte",                       "MP-TI-011", "Tintes y Coloración", 16500, 102+4+1+2+0, 10),
    ("Matizante Marliou x200ml",            "MP-TI-012", "Tintes y Coloración", 16000, 6+0+2+1+0,   1),
    ("Matizante Marliou x400ml",            "MP-TI-013", "Tintes y Coloración", 34000, 11+0+0+1+0,  1),
    ("Matizante Marliou Sobre x40ml",       "MP-TI-014", "Tintes y Coloración", 4000,  14+0+0+0+2,  2),
    ("Tinte Fantasía Marliou",              "MP-TI-015", "Tintes y Coloración", 5000,  30+0+5+4+0,   3),
    ("Guantes de Nitrilo",                  "MP-TI-016", "Tintes y Coloración", 2500,  27+1+1+2+0,   3),
    ("Shampoo x20ml Marliou",               "MP-TI-017", "Tintes y Coloración", 3000,  30+0+0+0+0,   3),
    ("Pal Plus / Never Old / Flash",        "MP-TI-018", "Tintes y Coloración", 18000, 1+0+1+1+1,    1),
    ("Tónico Flash Castaño Oscuro",         "MP-TI-019", "Tintes y Coloración", 32000, 2+0+0+0+0,    1),
    ("Tónico Flash Otros Tonos",            "MP-TI-020", "Tintes y Coloración", 30000, 1+0+1+1+1,    1),
    # Depilación — Bell Franz
    ("Aceite de Coco Grande Bell Franz",    "MP-BF-001", "Cera y Depilación", 15000, 1+1+0+0+3,    1),
    ("Aceite de Coco Pequeño Bell Franz",   "MP-BF-002", "Cera y Depilación", 10000, 2+2+1+2+1,    1),
    ("Aceite Argán Bell Franz",             "MP-BF-003", "Cera y Depilación", 18000, 1+0+0+0+1,    1),
    ("Aceite Ricino x60ml",                 "MP-BF-004", "Cera y Depilación", 6000,  1+0+1+2+1,    1),
    ("Aceites Naranja y Almendras x60ml",   "MP-BF-005", "Cera y Depilación", 6000,  4+2+2+1+1,    1),
    ("Aceites Naranja y Almendras x240ml",  "MP-BF-006", "Cera y Depilación", 15000, 5+0+0+0+0,    1),
    ("Aceites Naranja y Almendras x480ml",  "MP-BF-007", "Cera y Depilación", 23500, 2+0+0+0+1,    1),
    ("Aceite Almendras y Caléndula x980ml", "MP-BF-008", "Cera y Depilación", 40000, 2+0+0+0+0,    1),
    ("Cera Perlas Grande x250g",            "MP-BF-009", "Cera y Depilación", 26000, 2+0+0+0+0,    1),
    ("Cera Depilatoria x120g / Perlas Pequeñas","MP-BF-010","Cera y Depilación",13000,6+1+1+1+3,  1),
    ("Cera Depilatoria x240g",              "MP-BF-011", "Cera y Depilación", 20000, 2+0+0+0+0,    1),
    ("Cera Depilatoria x500g",              "MP-BF-012", "Cera y Depilación", 34000, 3+0+0+0+0,    1),
    ("Cera Depilatoria Kilo",               "MP-BF-013", "Cera y Depilación", 55000, 2+0+0+0+0,    1),
    ("Crema Depilatoria Lampiña x120g",     "MP-BF-014", "Cera y Depilación", 20000, 1+0+0+0+0,    1),
    ("Crema Depilatoria Lampiña Corporal Sobre","MP-BF-015","Cera y Depilación",6000, 2+1+1+1+1,   1),
    ("Crema Depilatoria Facial Lampiña",    "MP-BF-016", "Cera y Depilación", 6500,  1+0+0+0+0,    1),
    ("Gel Celulitis",                       "MP-BF-017", "Cera y Depilación", 18000, 2+0+1+0+0,    1),
    ("Gel Sauna",                           "MP-BF-018", "Cera y Depilación", 20000, 1+0+0+1+0,    1),
    ("Máquina Roll-On",                     "MP-BF-019", "Cera y Depilación", 65000, 1+0+0+0+0,    1),
    ("Lienzos Depilación",                  "MP-BF-020", "Cera y Depilación", 2500,  11+1+0+1+0,   2),
    ("Olla Ceradora",                       "MP-BF-021", "Cera y Depilación", 62000, 1+0+0+0+0,    1),
    ("Roll-On Depilatoria",                 "MP-BF-022", "Cera y Depilación", 20000, 3+0+0+0+0,    1),
    # Maquillaje — Engol
    ("Brochas Cejas Dobles y Ojos Engol",   "MP-EN-001", "Accesorios de Belleza", 4000, 10+0+3+1+0, 1),
    ("Brochas Varias Engol 5000",           "MP-EN-002", "Accesorios de Belleza", 5000, 5+0+0+0+0,  1),
    ("Brochas Varias Engol 6000",           "MP-EN-003", "Accesorios de Belleza", 6000, 4+0+0+1+0,  1),
    ("Brocha Individual Retráctil Sirena",  "MP-EN-004", "Accesorios de Belleza", 12000, 6+1+0+0+1, 1),
    ("Brocha Rubor Engol",                  "MP-EN-005", "Accesorios de Belleza", 15000, 4+0+0+0+0, 1),
    ("Delineador Líquido Engol",            "MP-EN-006", "Maquillaje",           10000, 1+0+0+0+0,  1),
    ("Delineador Plumón Engol Raymar Blanco","MP-EN-007","Maquillaje",           12000, 7+0+0+0+0,  1),
    ("Iluminador Líquido Engol",            "MP-EN-008", "Maquillaje",           14000, 3+0+0+0+0,  1),
    ("Lápiz Tres Pelos Cejas",              "MP-EN-009", "Maquillaje",           12000, 1+0+0+1+0,  1),
    ("Tinta para Labios Engol",             "MP-EN-010", "Maquillaje",           7000,  5+1+0+0+0,  1),
    # Maquillaje — Ushas
    ("Brillo Soda Malteada Llavero Ushas",  "MP-US-001", "Maquillaje", 12000, 3+0+0+2+1,  1),
    ("Delineador Plumón Color Neón Ushas",  "MP-US-002", "Maquillaje", 15000, 1+0+0+0+1,  1),
    ("Glitter / Sombra Líquida Ushas",      "MP-US-003", "Maquillaje", 14000, 6+0+0+1+0,  1),
    ("Labial Líquido Rood Febble",          "MP-US-004", "Maquillaje", 16000, 2+0+0+0+0,  1),
    ("Labial Líquido Shine",                "MP-US-005", "Maquillaje", 10000, 2+0+0+0+0,  1),
    ("Labial Líquido Unicornio",            "MP-US-006", "Maquillaje", 13000, 2+0+0+0+0,  1),
    ("Paleta de Sombras Paradise y Harmoni","MP-US-007", "Maquillaje", 45000, 1+0+0+0+0,  1),
    ("Paleta de Sombras Feble y Nude",      "MP-US-008", "Maquillaje", 21000, 1+0+0+0+0,  1),
    ("Rubor Ushas x2 con Brocha",           "MP-US-009", "Maquillaje", 18000, 2+0+0+0+0,  1),
    ("Set de Brochas Sirena Ushas",         "MP-US-010", "Accesorios de Belleza", 32000, 1+0+0+0+0, 1),
    # Maquillaje — Samy
    ("Agua Micelar Piel Grasa x260ml",      "MP-SA-001", "Maquillaje", 15000, 2+0+0+0+0,  1),
    ("Agua Micelar Piel Grasa x125ml",      "MP-SA-002", "Maquillaje", 10000, 2+0+0+0+0,  1),
    ("Agua Micelar Dermatológica x125ml",   "MP-SA-003", "Maquillaje", 13000, 1+0+0+0+1,  1),
    ("BB Cream Samy",                       "MP-SA-004", "Maquillaje", 16000, 3+0+2+3+1,  1),
    ("Betún para Cejas Samy",               "MP-SA-005", "Maquillaje", 10000, 12+0+1+1+0, 2),
    ("Brillo de Labios Samy",               "MP-SA-006", "Maquillaje", 7000,  1+0+1+1+0,  1),
    ("Corrector Líquido Samy",              "MP-SA-007", "Maquillaje", 17000, 7+1+1+0+1,  1),
    ("Crema Facial Hidratante Samy",        "MP-SA-008", "Maquillaje", 30000, 2+0+0+0+0,  1),
    ("Delineador Líquido Samy",             "MP-SA-009", "Maquillaje", 10000, 1+0+2+3+0,  1),
    ("Delineador Líquido Icónico Samy",     "MP-SA-010", "Maquillaje", 20000, 3+0+1+1+2,  1),
    ("Delineador Plumón Negro Mate Samy",   "MP-SA-011", "Maquillaje", 20000, 8+2+1+0+0,  1),
    ("Labiales Líquidos Mate Samy 20k",     "MP-SA-012", "Maquillaje", 20000, 1+0+0+1+0,  1),
    ("Labiales Líquidos Mate Samy 16k",     "MP-SA-013", "Maquillaje", 16000, 1+0+1+0+0,  1),
    ("Lápices Samy",                        "MP-SA-014", "Maquillaje", 3500,  70+7+5+6+8, 8),
    ("Paleta de Sombras x9 Pequeña Samy",   "MP-SA-015", "Maquillaje", 24000, 3+0+0+0+0,  1),
    ("Paleta de Sombras x9 Samy",           "MP-SA-016", "Maquillaje", 38000, 1+0+0+0+0,  1),
    ("Pestañinas Samy",                     "MP-SA-017", "Maquillaje", 9000,  17+2+1+2+1, 2),
    ("Polvos Samy 10k",                     "MP-SA-018", "Maquillaje", 10000, 7+1+1+2+0,  1),
    ("Polvos Sueltos Samy",                 "MP-SA-019", "Maquillaje", 20000, 7+1+2+0+0,  1),
    ("Rubor Redondo Samy",                  "MP-SA-020", "Maquillaje", 8000,  4+2+4+2+2,  1),
    # Maquillaje — Nailen y Maquillaje Varios
    ("Bases Líquidas Nailen",               "MP-NL-001", "Maquillaje", 13000, 4+0+0+0+2,  1),
    ("Corrector Líquido Nailen",            "MP-NL-002", "Maquillaje", 13000, 2+0+0+0+0,  1),
    ("Labial en Barra Smart",               "MP-NL-003", "Maquillaje", 14000, 5+0+1+2+0,  1),
    ("Polvos con Filtro Nailen",            "MP-NL-004", "Maquillaje", 12000, 7+0+2+1+1,  1),
    ("Polvos sin Filtro Nailen",            "MP-NL-005", "Maquillaje", 10000, 15+0+0+2+0, 2),
    ("Sombra Individual Raquel y Vogue",    "MP-NL-006", "Maquillaje", 10000, 6+0+1+0+0,  1),
    ("Aplicadores de Sombras + Cepillo",    "MP-MV-001", "Accesorios de Belleza", 500, 66+2+1+5+1, 5),
    ("Betún para Cejas x3 + Brillo Karite","MP-MV-002", "Maquillaje", 7000,  7+0+1+2+0,  1),
    ("Brillos Animalito y Bioaqua",         "MP-MV-003", "Maquillaje", 5000,  4+1+2+0+0,  1),
    ("Brillos Fresa",                       "MP-MV-004", "Maquillaje", 4000,  9+0+0+3+0,  1),
    ("Delineador Plumón Económico",         "MP-MV-005", "Maquillaje", 6000,  2+1+1+1+1,  1),
    ("Henna para Cejas",                    "MP-MV-006", "Maquillaje", 12000, 3+0+0+0+1,  1),
    ("Jabón para Cejas",                    "MP-MV-007", "Maquillaje", 8000,  6+0+1+1+0,  1),
    ("Labiales Mágicos Engol y Raymar",     "MP-MV-008", "Maquillaje", 3500,  2+1+1+2+0,  1),
    ("Lápiz Económico",                     "MP-MV-009", "Maquillaje", 2500,  34+4+2+1+2, 4),
    ("Pestañina Max Factor",                "MP-MV-010", "Maquillaje", 18000, 8+2+2+0+0,  1),
    ("Polvos Ana María",                    "MP-MV-011", "Maquillaje", 29000, 11+0+0+1+0, 1),
    ("Polvos Kaloe",                        "MP-MV-012", "Maquillaje", 15000, 3+1+1+1+1,  1),
    ("Rubor Líquido Elaya / MYK",           "MP-MV-013", "Maquillaje", 15000, 10+0+2+2+1, 1),
    ("Sombras Pequeñas",                    "MP-MV-014", "Maquillaje", 12000, 2+1+2+0+0,  1),
    ("Sombra Paleta Estrellas y Sirena",    "MP-MV-015", "Maquillaje", 25000, 1+0+0+1+0,  1),
    # Masglo y Admiss — Uñas
    ("Esmaltes Comunes y Bases Masglo",     "MP-MG-001", "Uñas y Manicure", 9500,  60+17+12+14+13, 8),
    ("Esmaltes Admiss",                     "MP-MG-002", "Uñas y Manicure", 4500,  43+10+6+12+5,   5),
    ("Bases Clinical y Antimordidas",       "MP-MG-003", "Uñas y Manicure", 15000, 5+3+1+1+1,     1),
    ("Brillo Secante Masglo",               "MP-MG-004", "Uñas y Manicure", 10000, 3+0+2+0+2,     1),
    ("Brillo Gel Masglo",                   "MP-MG-005", "Uñas y Manicure", 10500, 2+2+0+0+0,     1),
    ("Esmalte Brillo y Base Polish",        "MP-MG-006", "Uñas y Manicure", 23000, 4+0+0+1+0,     1),
    ("Cubo Pulidor",                        "MP-MG-007", "Uñas y Manicure", 6000,  4+0+1+2+1,     1),
    ("Limas Normal y Lavable",              "MP-MG-008", "Uñas y Manicure", 2500,  7+3+4+11+1,    2),
    ("Limas Grises",                        "MP-MG-009", "Uñas y Manicure", 8000,  6+3+2+0+1,     1),
    ("Removedor Vidrio x60ml",              "MP-MG-010", "Uñas y Manicure", 7500,  5+1+0+0+1,     1),
    ("Removedor con Dispensador x110ml",    "MP-MG-011", "Uñas y Manicure", 11000, 5+0+1+0+0,     1),
    ("Removedor Semipermanente",            "MP-MG-012", "Uñas y Manicure", 17000, 3+1+1+0+1,     1),
    ("Removedor Tradicional x280ml",        "MP-MG-013", "Uñas y Manicure", 15000, 1+0+0+1+0,     1),
    ("Removedor Tradicional x480ml",        "MP-MG-014", "Uñas y Manicure", 20000, 2+0+0+0+0,     1),
    ("Removedor Tradicional x950ml",        "MP-MG-015", "Uñas y Manicure", 32000, 2+0+0+0+0,     1),
    # Varios Uñas
    ("Aceite para Uñas Cosdy x60ml",        "MP-VU-001", "Uñas y Manicure", 5000,  7+0+0+0+0,     1),
    ("Cepillos para Uñas",                  "MP-VU-002", "Uñas y Manicure", 3000,  5+0+0+0+1,     1),
    ("Cortacutícula en Pasta",              "MP-VU-003", "Uñas y Manicure", 13000, 2+1+0+1+1,     1),
    ("Cortauñas Grandes",                   "MP-VU-004", "Uñas y Manicure", 4000,  2+0+2+0+1,     1),
    ("Cortauñas Pequeños",                  "MP-VU-005", "Uñas y Manicure", 2000,  4+0+0+0+1,     1),
    ("Esmaltes Semipermanentes Free Nails",  "MP-VU-006", "Uñas y Manicure", 27000, 4+2+1+0+0,    1),
    ("Lima Los Monos",                      "MP-VU-007", "Uñas y Manicure", 1500,  89+4+8+3+1,    8),
    ("Lima Pico Loro",                      "MP-VU-008", "Uñas y Manicure", 2500,  11+0+0+1+0,    1),
    ("Lima 100x180 y Lima Gruesa",          "MP-VU-009", "Uñas y Manicure", 5000,  8+0+1+0+2,     1),
    ("Limas Cuadradas Negras",              "MP-VU-010", "Uñas y Manicure", 1000,  21+0+0+0+0,    3),
    ("Palos de Naranjo x10",                "MP-VU-011", "Uñas y Manicure", 2500,  4+0+1+0+1,     1),
    ("Patecabra",                           "MP-VU-012", "Uñas y Manicure", 2000,  10+2+1+0+1,    1),
    ("Pegante Adoro",                       "MP-VU-013", "Uñas y Manicure", 4500,  14+1+3+6+1,    2),
    ("Pincel para Uñas",                    "MP-VU-014", "Uñas y Manicure", 9000,  6+0+1+0+1,     1),
    ("Pusher Semipermanente",               "MP-VU-015", "Uñas y Manicure", 10000, 1+0+0+0+0,     1),
    ("Pusher Sencillo",                     "MP-VU-016", "Uñas y Manicure", 4500,  6+4+0+0+0,     1),
    ("Removedor de Cutícula x250ml",        "MP-VU-017", "Uñas y Manicure", 11000, 3+0+0+0+0,     1),
    ("Separador de Dedos Foamy",            "MP-VU-018", "Uñas y Manicure", 1600,  3+0+0+0+0,     1),
    ("Toallas Wypall Cabello",              "MP-VU-019", "Uñas y Manicure", 1000,  20+5+17+12+9,  3),
    ("Uñas de Hierro",                      "MP-VU-020", "Uñas y Manicure", 8000,  3+1+3+0+2,     1),
    ("Uñas Postizas en Caja x24",           "MP-VU-021", "Uñas y Manicure", 20000, 1+1+1+3+0,     1),
    ("Uñas Postizas Caja Niña",             "MP-VU-022", "Uñas y Manicure", 10000, 2+1+0+1+0,     1),
    # Baja Lenguas y accesorios varios
    ("Baja Lenguas",                        "MP-AC-001", "Accesorios de Belleza", 1500, 3+0+0+0+1,  1),
    ("Cosmetiqueras",                       "MP-AC-002", "Accesorios de Belleza", 20000, 2+0+0+1+0, 1),
    ("Tijeras Pequeñas",                    "MP-AC-003", "Accesorios de Belleza", 5000, 4+0+0+0+0,  1),
    ("Vaso Recipiente para Brochas",        "MP-AC-004", "Accesorios de Belleza", 22000, 1+0+0+0+0, 1),
]

# Build combined PRODUCTS list
PRODUCTS: list[tuple] = []
for name, sku, cat_leaf, price, initial_stock, stock_min in _NATURISMO_RAW:
    cost = _cost(price, 0.55)
    PRODUCTS.append((name, sku, ("Naturismo", cat_leaf), cost, price, max(initial_stock, 1), stock_min, "unit"))
for name, sku, cat_leaf, price, initial_stock, stock_min in _BELLEZA_RAW:
    cost = _cost(price, 0.50)
    PRODUCTS.append((name, sku, ("Belleza", cat_leaf), cost, price, max(initial_stock, 1), stock_min, "unit"))

# ---------------------------------------------------------------------------
# Customers (regular clients of Miss Peggy)
# ---------------------------------------------------------------------------

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Gloria Inés",
        "last_name": "Vargas Cifuentes",
        "document_type": "CC",
        "document_number": "41345678",
        "email": "gloria.vargas@gmail.com",
        "phone": "+57 315 234 5678",
        "address": "Cra. 15 # 32-10, Barrio Popular",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Lorena",
        "last_name": "Castillo Ríos",
        "document_type": "CC",
        "document_number": "52456789",
        "email": "lorena.castillo@hotmail.com",
        "phone": "+57 311 345 6789",
        "address": "Cll. 22 # 14-30, Cedritos",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Claudia",
        "last_name": "Moreno Pardo",
        "document_type": "CC",
        "document_number": "46567890",
        "email": "claudia.moreno@gmail.com",
        "phone": "+57 318 456 7890",
        "address": "Cra. 8 # 55-20",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Patricia",
        "last_name": "Herrera Blanco",
        "document_type": "CC",
        "document_number": "39678901",
        "email": "patricia.herrera@outlook.com",
        "phone": "+57 313 567 8901",
        "address": "Cll. 45 # 7-18, Chapinero",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Beatriz Elena",
        "last_name": "Ospina García",
        "document_type": "CC",
        "document_number": "43789012",
        "email": "beatriz.ospina@gmail.com",
        "phone": "+57 320 678 9012",
        "address": "Cra. 43A # 14-30, Laureles",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "María del Carmen",
        "last_name": "Torres Suárez",
        "document_type": "CC",
        "document_number": "36901234",
        "email": "mcorres.suarez@yahoo.com",
        "phone": "+57 317 789 0123",
        "address": "Cll. 10 # 43E-45, El Poblado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Sonia",
        "last_name": "Ramírez Peña",
        "document_type": "CC",
        "document_number": "57012345",
        "email": "sonia.ramirez@gmail.com",
        "phone": "+57 316 890 1234",
        "address": "Cra. 5 # 17-30, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Adriana",
        "last_name": "López Mendoza",
        "document_type": "CC",
        "document_number": "40234567",
        "email": "adriana.lopez@gmail.com",
        "phone": "+57 321 901 2345",
        "address": "Cra. 27 # 51-15, Cabecera",
        "city": "Bucaramanga",
        "country": "Colombia",
    },
    {
        "first_name": "Yaneth",
        "last_name": "Cruz Montoya",
        "document_type": "CC",
        "document_number": "47234567",
        "email": "yaneth.cruz@gmail.com",
        "phone": "+57 314 012 3456",
        "address": "Cll. 19 # 8-25, Centro",
        "city": "Pereira",
        "country": "Colombia",
    },
    {
        "first_name": "Diana Marcela",
        "last_name": "Rojas Agudelo",
        "document_type": "CC",
        "document_number": "1098345678",
        "email": "diana.rojas@gmail.com",
        "phone": "+57 312 123 4567",
        "address": "Cra. 70 # 46-20, Belén",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Estella",
        "last_name": "Bernal Quintero",
        "document_type": "CC",
        "document_number": "30456789",
        "email": "estella.bernal@gmail.com",
        "phone": "+57 319 234 5678",
        "address": "Cll. 116 # 17-50, Usaquén",
        "city": "Bogotá",
        "country": "Colombia",
    },
    {
        "first_name": "Amparo",
        "last_name": "Cárdenas Ávila",
        "document_type": "CC",
        "document_number": "35567890",
        "email": "amparo.cardenas@hotmail.com",
        "phone": "+57 304 345 6789",
        "address": "Cra. 53 # 76-88",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Nancy",
        "last_name": "Gutiérrez Soto",
        "document_type": "CC",
        "document_number": "32678901",
        "email": "nancy.guti@gmail.com",
        "phone": "+57 318 456 7891",
        "address": "Av. 3N # 25-40, Norte",
        "city": "Cali",
        "country": "Colombia",
    },
    {
        "first_name": "Rosa",
        "last_name": "Díaz Pereira",
        "document_type": "CC",
        "document_number": "48901234",
        "email": "rosa.diaz@gmail.com",
        "phone": "+57 316 567 8902",
        "address": "Cll. 12 # 15-22",
        "city": "Armenia",
        "country": "Colombia",
    },
    {
        "first_name": "Isabel Cristina",
        "last_name": "Salcedo Flórez",
        "document_type": "CC",
        "document_number": "44012345",
        "email": "isabel.salcedo@gmail.com",
        "phone": "+57 315 678 9013",
        "address": "Cra. 9 # 13-30, Centro",
        "city": "Armenia",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "carolinaforero@misspeggy.co",
        "first_name": "Carolina",
        "last_name": "Forero",
        "phone": "+57 300 111 2222",
    },
    {
        "email": "nicolasrodriguez@misspeggy.co",
        "first_name": "Nicolas",
        "last_name": "Rodriguez",
        "phone": "+57 300 333 4444",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]
IVA_RATE = Decimal("0.19")

# Sales period: Jan 1 – Apr 28, 2026
SALES_START = datetime(2026, 1, 1, tzinfo=timezone.utc)
SALES_DAYS = 118  # Jan 1 to Apr 28 inclusive


def seed(session: Session) -> None:
    """Main seed function for Miss Peggy demo data."""

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
            reason="Stock inicial - Inventario apertura Miss Peggy Ene 2026",
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

    # ── 9. Sales — Jan 1 to Apr 28, 2026 (small store pattern) ───────
    invoice_counter = 0
    total_sales = 0

    for day_offset in range(SALES_DAYS + 1):
        day = SALES_START + timedelta(days=day_offset)
        weekday = day.weekday()

        # Small tienda naturista: moderate weekday, higher Sat, closed-ish Sun
        if weekday == 6:          # Sunday
            num_sales = random.randint(0, 2)
        elif weekday == 5:        # Saturday — beauty treatments day
            num_sales = random.randint(4, 8)
        else:                     # Mon–Fri
            num_sales = random.randint(2, 5)

        # Last day (today)
        if day_offset == SALES_DAYS:
            num_sales = random.randint(3, 6)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"MP-{invoice_counter:05d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.65 else None

            # Small shop: 1-3 items per ticket
            num_items = random.randint(1, 3)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(8, 19)
            sale_date = day.replace(
                hour=sale_hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
                microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                qty = random.randint(1, 2)
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

            # Small store: occasional small discount for loyal clients
            discount_pct = random.choice([0, 0, 0, 5, 10]) if customer else 0
            discount = (subtotal * Decimal(str(discount_pct)) / Decimal("100")).quantize(Decimal("0.01"))
            tax = ((subtotal - discount) * IVA_RATE).quantize(Decimal("0.01"))
            total = subtotal - discount + tax

            payment_method = random.choice(PAYMENT_METHODS)
            is_cancelled = random.random() < 0.03 and day_offset > 0
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
                    "Cliente no volvió a recoger el pedido",
                    "Producto no disponible",
                    "Error en el cobro",
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
    logger.info(f"Created {total_sales} sales from Jan 1 to Apr 28, 2026")

    # ── 10. Restock low-inventory products ───────────────────────────
    now = datetime.now(timezone.utc)
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(2, 15)
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
                reason="Reposición de inventario Miss Peggy",
                created_at=now - timedelta(hours=random.randint(1, 48)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED MISS PEGGY COMPLETE!")
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
