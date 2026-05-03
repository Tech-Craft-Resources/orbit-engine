"""
Seed script for Sabor Caribe — Colombian food distributor / wholesale market.

Usage (via Docker Compose):
    docker compose exec backend python scripts/seed_sabor_caribe.py

Idempotent: checks for existing products before inserting.
Target org slug is defined by ORG_SLUG below.

Data context:
  - Products: meats, dairy, grains, beverages, snacks, condiments and fresh produce
  - Prices in COP, wholesale/retail food pricing
  - IVA 0% on most food (exento), 5% on snacks/sugary beverages
  - Higher sales on Fri–Sat; restaurants/tiendas buy Mon–Wed
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

ORG_SLUG = "sabor-caribe"

# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {
        "name": "Carnes y Proteínas",
        "description": "Carnes frescas, embutidos y proteínas de origen animal",
        "children": [
            {"name": "Carnes Rojas", "description": "Res, cerdo y cordero frescos y en cortes"},
            {"name": "Pollo y Aves", "description": "Pollo entero, presas y productos avícolas"},
            {"name": "Embutidos y Fríos", "description": "Salchichas, jamón, chorizo y tocineta"},
            {"name": "Pescados y Mariscos", "description": "Pescado fresco, filetes, camarones y calamares"},
        ],
    },
    {
        "name": "Lácteos y Huevos",
        "description": "Leches, quesos, derivados lácteos y huevos",
        "children": [
            {"name": "Leches y Cremas", "description": "Leche entera, descremada, en polvo y cremas de leche"},
            {"name": "Quesos y Mantequillas", "description": "Quesos frescos, maduros, margarina y mantequilla"},
            {"name": "Yogur y Postres", "description": "Yogures naturales, con frutas y postres de leche"},
            {"name": "Huevos", "description": "Huevos AA, A y jumbo por cubeta y docena"},
        ],
    },
    {
        "name": "Granos y Cereales",
        "description": "Arroz, leguminosas, harinas y cereales para el hogar",
        "children": [
            {"name": "Arroz", "description": "Arroz blanco, integral, de grano largo y paella"},
            {"name": "Leguminosas", "description": "Fríjol, lenteja, garbanzo, arveja y maíz"},
            {"name": "Harinas y Masas", "description": "Harina de trigo, maíz, yuca y mezclas"},
            {"name": "Pasta y Sémola", "description": "Pastas largas, cortas y fideos"},
        ],
    },
    {
        "name": "Frutas y Verduras",
        "description": "Producción fresca de la región Caribe y nacional",
        "children": [
            {"name": "Frutas Frescas", "description": "Mango, piña, papaya, maracuyá y frutas de temporada"},
            {"name": "Verduras y Hortalizas", "description": "Tomate, cebolla, pimentón, zanahoria y más"},
            {"name": "Tubérculos y Plátanos", "description": "Papa, yuca, ñame, plátano verde y maduro"},
        ],
    },
    {
        "name": "Bebidas",
        "description": "Jugos, refrescos, aguas y bebidas calientes",
        "children": [
            {"name": "Jugos y Néctares", "description": "Jugos en caja, botella y néctares de fruta"},
            {"name": "Gaseosas y Refrescos", "description": "Gaseosas en litro y personal, aguas saborizadas"},
            {"name": "Aguas", "description": "Agua embotellada en botellín, 600ml y galón"},
            {"name": "Bebidas Calientes", "description": "Café, té, avena y chocolate en polvo"},
        ],
    },
    {
        "name": "Aceites y Grasas",
        "description": "Aceites vegetales, mantecas y aliños",
        "children": [
            {"name": "Aceites Vegetales", "description": "Aceite de palma, girasol, canola y oliva"},
            {"name": "Mantecas y Shortenings", "description": "Manteca vegetal y animal para repostería"},
        ],
    },
    {
        "name": "Condimentos y Salsas",
        "description": "Especias, aliños, salsas y aderezos",
        "children": [
            {"name": "Salsas y Aderezos", "description": "Kétchup, mayonesa, mostaza y salsas especiales"},
            {"name": "Especias y Aliños", "description": "Comino, ajo, achiote, curcuma y mezclas"},
            {"name": "Caldos y Sazonadores", "description": "Caldos en cubos, en polvo y sazonadores líquidos"},
        ],
    },
    {
        "name": "Snacks y Confitería",
        "description": "Mecato, pasabocas, dulces y confites colombianos",
        "children": [
            {"name": "Mecato Colombiano", "description": "Papas, chicharrón, pandequeso y empanadas empacadas"},
            {"name": "Dulces y Confites", "description": "Caramelos, chocolatinas, gomas y chicles"},
            {"name": "Galletas y Ponqués", "description": "Galletas dulces, saladas, ponqués y torticas"},
        ],
    },
    {
        "name": "Aseo y Limpieza",
        "description": "Productos de limpieza del hogar y aseo personal básico",
        "children": [
            {"name": "Limpieza del Hogar", "description": "Detergente, jabón en barra, limpiapisos y desengrasante"},
            {"name": "Aseo Personal Básico", "description": "Jabón de baño, shampoo económico y papel higiénico"},
        ],
    },
]

# (name, sku, category_path, cost_cop, sale_price_cop, stock, stock_min, unit)
PRODUCTS: list[tuple] = [
    # Carnes > Carnes Rojas
    ("Carne Molida de Res x500g", "SC-CA-001", ("Carnes y Proteínas", "Carnes Rojas"), 8500, 15900, 150, 30, "unit"),
    ("Posta Negra de Res x1kg", "SC-CA-002", ("Carnes y Proteínas", "Carnes Rojas"), 15000, 28900, 80, 15, "unit"),
    ("Costilla de Cerdo x1kg", "SC-CA-003", ("Carnes y Proteínas", "Carnes Rojas"), 11000, 21900, 80, 15, "unit"),
    ("Paleta de Cerdo x1kg", "SC-CA-004", ("Carnes y Proteínas", "Carnes Rojas"), 10000, 19900, 70, 12, "unit"),
    # Carnes > Pollo y Aves
    ("Pechuga de Pollo x1kg", "SC-CA-005", ("Carnes y Proteínas", "Pollo y Aves"), 9500, 18900, 150, 30, "unit"),
    ("Pierna Muslo Pollo x1kg", "SC-CA-006", ("Carnes y Proteínas", "Pollo y Aves"), 7500, 14900, 150, 30, "unit"),
    ("Pollo Entero Limpio x1.8kg", "SC-CA-007", ("Carnes y Proteínas", "Pollo y Aves"), 17000, 32900, 80, 15, "unit"),
    # Carnes > Embutidos
    ("Salchichas Zenú x500g", "SC-CA-008", ("Carnes y Proteínas", "Embutidos y Fríos"), 7500, 14900, 120, 25, "unit"),
    ("Jamón Cocido Zenú x250g", "SC-CA-009", ("Carnes y Proteínas", "Embutidos y Fríos"), 6500, 12900, 100, 20, "unit"),
    ("Chorizo Santarrosano x500g", "SC-CA-010", ("Carnes y Proteínas", "Embutidos y Fríos"), 9000, 17900, 80, 15, "unit"),
    ("Tocineta Ahumada x200g", "SC-CA-011", ("Carnes y Proteínas", "Embutidos y Fríos"), 8500, 16900, 60, 12, "unit"),
    # Carnes > Pescado
    ("Filete de Tilapia x500g", "SC-CA-012", ("Carnes y Proteínas", "Pescados y Mariscos"), 9000, 17900, 80, 15, "unit"),
    ("Camarón Pelado x250g", "SC-CA-013", ("Carnes y Proteínas", "Pescados y Mariscos"), 18000, 34900, 50, 10, "unit"),
    # Lácteos > Leches
    ("Leche Entera Alquería x1L", "SC-LA-001", ("Lácteos y Huevos", "Leches y Cremas"), 2800, 5900, 400, 80, "unit"),
    ("Leche Entera Alquería x1/2L", "SC-LA-002", ("Lácteos y Huevos", "Leches y Cremas"), 1500, 3200, 300, 60, "unit"),
    ("Leche en Polvo Klim x200g", "SC-LA-003", ("Lácteos y Huevos", "Leches y Cremas"), 8500, 15900, 100, 20, "unit"),
    ("Crema de Leche Alpina x250ml", "SC-LA-004", ("Lácteos y Huevos", "Leches y Cremas"), 3500, 6900, 150, 30, "unit"),
    # Lácteos > Quesos
    ("Queso Costeño x500g", "SC-LA-005", ("Lácteos y Huevos", "Quesos y Mantequillas"), 8500, 16900, 80, 15, "unit"),
    ("Queso Mozzarella x250g", "SC-LA-006", ("Lácteos y Huevos", "Quesos y Mantequillas"), 7000, 13900, 80, 15, "unit"),
    ("Mantequilla Con Sal x500g", "SC-LA-007", ("Lácteos y Huevos", "Quesos y Mantequillas"), 7500, 14900, 80, 15, "unit"),
    # Lácteos > Yogur
    ("Yogur Natural Alpina x1kg", "SC-LA-008", ("Lácteos y Huevos", "Yogur y Postres"), 5500, 10900, 100, 20, "unit"),
    ("Yogur Griego Danone x125g", "SC-LA-009", ("Lácteos y Huevos", "Yogur y Postres"), 4000, 7900, 80, 15, "unit"),
    # Lácteos > Huevos
    ("Huevos AA x12 und", "SC-LA-010", ("Lácteos y Huevos", "Huevos"), 6000, 11900, 200, 40, "unit"),
    ("Huevos AA Cubeta x30 und", "SC-LA-011", ("Lácteos y Huevos", "Huevos"), 14500, 28900, 100, 20, "unit"),
    # Granos > Arroz
    ("Arroz Blanco Diana x500g", "SC-GR-001", ("Granos y Cereales", "Arroz"), 2500, 5200, 500, 100, "unit"),
    ("Arroz Blanco Diana x2kg", "SC-GR-002", ("Granos y Cereales", "Arroz"), 9500, 18900, 300, 60, "unit"),
    ("Arroz Integral x1kg", "SC-GR-003", ("Granos y Cereales", "Arroz"), 4500, 8900, 150, 30, "unit"),
    # Granos > Leguminosas
    ("Fríjol Bolo Rojo x500g", "SC-GR-004", ("Granos y Cereales", "Leguminosas"), 3000, 5900, 300, 60, "unit"),
    ("Lenteja x500g", "SC-GR-005", ("Granos y Cereales", "Leguminosas"), 2800, 5500, 250, 50, "unit"),
    ("Garbanzo x500g", "SC-GR-006", ("Granos y Cereales", "Leguminosas"), 3200, 6500, 200, 40, "unit"),
    # Granos > Harinas
    ("Harina de Trigo Haz de Oros x1kg", "SC-GR-007", ("Granos y Cereales", "Harinas y Masas"), 3000, 5900, 300, 60, "unit"),
    ("Harina de Maíz Maseca x1kg", "SC-GR-008", ("Granos y Cereales", "Harinas y Masas"), 3500, 6900, 200, 40, "unit"),
    # Granos > Pastas
    ("Pasta Espagueti Doria x250g", "SC-GR-009", ("Granos y Cereales", "Pasta y Sémola"), 1800, 3900, 400, 80, "unit"),
    ("Pasta Codito Doria x250g", "SC-GR-010", ("Granos y Cereales", "Pasta y Sémola"), 1800, 3900, 350, 70, "unit"),
    # Frutas > Frescas
    ("Mango Tommy x1kg", "SC-FV-001", ("Frutas y Verduras", "Frutas Frescas"), 2000, 4900, 200, 40, "unit"),
    ("Piña x1 unidad (~2kg)", "SC-FV-002", ("Frutas y Verduras", "Frutas Frescas"), 3500, 7900, 150, 30, "unit"),
    ("Maracuyá x1kg", "SC-FV-003", ("Frutas y Verduras", "Frutas Frescas"), 3000, 6500, 100, 20, "unit"),
    # Frutas > Verduras
    ("Tomate Chonto x1kg", "SC-FV-004", ("Frutas y Verduras", "Verduras y Hortalizas"), 2500, 5500, 250, 50, "unit"),
    ("Cebolla Cabezona Blanca x1kg", "SC-FV-005", ("Frutas y Verduras", "Verduras y Hortalizas"), 2000, 4500, 250, 50, "unit"),
    ("Pimentón Rojo x1kg", "SC-FV-006", ("Frutas y Verduras", "Verduras y Hortalizas"), 3500, 7500, 150, 30, "unit"),
    # Frutas > Tubérculos
    ("Papa Pastusa x5kg", "SC-FV-007", ("Frutas y Verduras", "Tubérculos y Plátanos"), 5500, 10900, 200, 40, "unit"),
    ("Plátano Verde x1kg", "SC-FV-008", ("Frutas y Verduras", "Tubérculos y Plátanos"), 1800, 3900, 300, 60, "unit"),
    ("Yuca x1kg", "SC-FV-009", ("Frutas y Verduras", "Tubérculos y Plátanos"), 1500, 3200, 250, 50, "unit"),
    # Bebidas > Jugos
    ("Jugo Hit Mango x1L Tetra", "SC-BE-001", ("Bebidas", "Jugos y Néctares"), 3000, 5900, 200, 40, "unit"),
    ("Jugo Del Valle Naranja x237ml", "SC-BE-002", ("Bebidas", "Jugos y Néctares"), 1500, 3200, 300, 60, "unit"),
    # Bebidas > Gaseosas
    ("Coca-Cola x1.5L", "SC-BE-003", ("Bebidas", "Gaseosas y Refrescos"), 3500, 7200, 200, 40, "unit"),
    ("Colombiana x300ml", "SC-BE-004", ("Bebidas", "Gaseosas y Refrescos"), 1200, 2500, 400, 80, "unit"),
    # Bebidas > Aguas
    ("Agua Brisa x600ml", "SC-BE-005", ("Bebidas", "Aguas"), 900, 1900, 500, 100, "unit"),
    ("Agua Manantial x1.5L", "SC-BE-006", ("Bebidas", "Aguas"), 1500, 3200, 300, 60, "unit"),
    # Bebidas > Calientes
    ("Café Colcafé x100g", "SC-BE-007", ("Bebidas", "Bebidas Calientes"), 5500, 10900, 150, 30, "unit"),
    ("Chocolate Luker Bloque x500g", "SC-BE-008", ("Bebidas", "Bebidas Calientes"), 8500, 16900, 100, 20, "unit"),
    # Aceites
    ("Aceite Girasol Gourmet x1L", "SC-AC-001", ("Aceites y Grasas", "Aceites Vegetales"), 8000, 15900, 150, 30, "unit"),
    ("Aceite de Palma La Palmera x3L", "SC-AC-002", ("Aceites y Grasas", "Aceites Vegetales"), 18000, 34900, 100, 20, "unit"),
    # Condimentos > Salsas
    ("Kétchup Fruco x400g", "SC-CO-001", ("Condimentos y Salsas", "Salsas y Aderezos"), 5500, 10900, 150, 30, "unit"),
    ("Mayonesa Real x250g", "SC-CO-002", ("Condimentos y Salsas", "Salsas y Aderezos"), 5000, 9900, 150, 30, "unit"),
    # Condimentos > Especias
    ("Comino Molido La Torre x100g", "SC-CO-003", ("Condimentos y Salsas", "Especias y Aliños"), 2500, 5500, 200, 40, "unit"),
    ("Achiote en Pasta x100g", "SC-CO-004", ("Condimentos y Salsas", "Especias y Aliños"), 2000, 4500, 200, 40, "unit"),
    # Condimentos > Caldos
    ("Caldo Maggi Gallina x40g", "SC-CO-005", ("Condimentos y Salsas", "Caldos y Sazonadores"), 3000, 6200, 250, 50, "unit"),
    ("Sazonador Knorr Suiza x200g", "SC-CO-006", ("Condimentos y Salsas", "Caldos y Sazonadores"), 5000, 9900, 200, 40, "unit"),
    # Snacks > Mecato
    ("Papas Margarita x220g", "SC-SN-001", ("Snacks y Confitería", "Mecato Colombiano"), 4500, 8900, 200, 40, "unit"),
    ("Chicharrón Gustositos x80g", "SC-SN-002", ("Snacks y Confitería", "Mecato Colombiano"), 2500, 5500, 250, 50, "unit"),
    # Snacks > Dulces
    ("Chocolatina Jet x16g x12", "SC-SN-003", ("Snacks y Confitería", "Dulces y Confites"), 5500, 10900, 150, 30, "unit"),
    ("Gomitas Haribo x100g", "SC-SN-004", ("Snacks y Confitería", "Dulces y Confites"), 3500, 6900, 120, 25, "unit"),
    # Snacks > Galletas
    ("Galletas Festival x388g", "SC-SN-005", ("Snacks y Confitería", "Galletas y Ponqués"), 5500, 10900, 150, 30, "unit"),
    ("Galletas Saltinas x318g", "SC-SN-006", ("Snacks y Confitería", "Galletas y Ponqués"), 4500, 8900, 180, 35, "unit"),
    # Aseo > Hogar
    ("Detergente Ariel x1kg", "SC-AS-001", ("Aseo y Limpieza", "Limpieza del Hogar"), 8000, 15900, 200, 40, "unit"),
    ("Jabón Fab en Barra x300g", "SC-AS-002", ("Aseo y Limpieza", "Limpieza del Hogar"), 3000, 5900, 250, 50, "unit"),
    ("Limpiapisos Fabuloso x1L", "SC-AS-003", ("Aseo y Limpieza", "Limpieza del Hogar"), 4500, 8900, 200, 40, "unit"),
    # Aseo > Personal
    ("Papel Higiénico Scott x4 rollos", "SC-AS-004", ("Aseo y Limpieza", "Aseo Personal Básico"), 4500, 8900, 300, 60, "unit"),
    ("Jabón de Baño Protex x100g", "SC-AS-005", ("Aseo y Limpieza", "Aseo Personal Básico"), 2500, 5200, 300, 60, "unit"),
]

CUSTOMERS_DATA: list[dict] = [
    {
        "first_name": "Restaurante El Sabor",
        "last_name": "Costeño SAS",
        "document_type": "NIT",
        "document_number": "900789012-1",
        "email": "compras@elsaborcoste.co",
        "phone": "+57 605 234 5678",
        "address": "Cll. 72 # 44-60",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Tienda Doña",
        "last_name": "Carmen E.U.",
        "document_type": "NIT",
        "document_number": "27345678-0",
        "email": "tiendadonacarmen@gmail.com",
        "phone": "+57 318 345 6789",
        "address": "Cra. 18 # 22-05, Villa Campestre",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "José Manuel",
        "last_name": "Peñaloza Arce",
        "document_type": "CC",
        "document_number": "8901234",
        "email": "jose.penaloza@gmail.com",
        "phone": "+57 315 456 7890",
        "address": "Cll. 18 # 7-40, Barrio España",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Supermercado",
        "last_name": "La Cosecha SAS",
        "document_type": "NIT",
        "document_number": "901234890-2",
        "email": "mercadeofruver@lacosecha.co",
        "phone": "+57 604 567 8901",
        "address": "Cra. 45 # 30-20, El Prado",
        "city": "Medellín",
        "country": "Colombia",
    },
    {
        "first_name": "Adriana",
        "last_name": "Ríos Palomino",
        "document_type": "CC",
        "document_number": "32456789",
        "email": "adriana.rios@yahoo.com",
        "phone": "+57 311 678 9012",
        "address": "Cra. 5 # 12-30, Centro",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Hotel",
        "last_name": "Brisa Marina SAS",
        "document_type": "NIT",
        "document_number": "800234567-3",
        "email": "alimentos@brisamarina.co",
        "phone": "+57 575 789 0123",
        "address": "Cra. 2 # 11-26, El Rodadero",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Marco Antonio",
        "last_name": "Fuentes Brito",
        "document_type": "CC",
        "document_number": "73567890",
        "email": "marco.fuentes@gmail.com",
        "phone": "+57 317 890 1234",
        "address": "Cll. del Guerrero # 5-30, Getsemaní",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Cafetería y Restaurante",
        "last_name": "El Palenque SAS",
        "document_type": "NIT",
        "document_number": "901567012-1",
        "email": "pedidos@elpalenque.co",
        "phone": "+57 310 901 2345",
        "address": "Cra. 5 # 8-22, Bocagrande",
        "city": "Cartagena",
        "country": "Colombia",
    },
    {
        "first_name": "Leonor",
        "last_name": "Castro Iguarán",
        "document_type": "CC",
        "document_number": "36789012",
        "email": "leonor.castro@gmail.com",
        "phone": "+57 314 012 3457",
        "address": "Cll. 23 # 7-15, Mamatoco",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Club Deportivo",
        "last_name": "Caribe Fútbol",
        "document_type": "NIT",
        "document_number": "901890123-2",
        "email": "logistica@caribefutbol.co",
        "phone": "+57 316 123 4568",
        "address": "Estadio Romelio Martínez Cra. 47",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Yolima",
        "last_name": "Vargas Herrera",
        "document_type": "CC",
        "document_number": "49901234",
        "email": "yolima.vargas@gmail.com",
        "phone": "+57 320 234 5680",
        "address": "Cll. 29 # 3-40",
        "city": "Valledupar",
        "country": "Colombia",
    },
    {
        "first_name": "Rodrigo",
        "last_name": "Díaz Cueto",
        "document_type": "CC",
        "document_number": "84012345",
        "email": "rodrigo.diaz@hotmail.com",
        "phone": "+57 312 345 6781",
        "address": "Cra. 10 # 20-35",
        "city": "Montería",
        "country": "Colombia",
    },
    {
        "first_name": "Panadería y Pastelería",
        "last_name": "La Macarena SAS",
        "document_type": "NIT",
        "document_number": "901012345-3",
        "email": "insumos@lamacarena.co",
        "phone": "+57 318 456 7893",
        "address": "Cll. 84 # 48B-30, Altamira",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Esperanza",
        "last_name": "Herrera Donado",
        "document_type": "CC",
        "document_number": "27234567",
        "email": "espe.herrera@gmail.com",
        "phone": "+57 316 567 8906",
        "address": "Cra. 44 # 12-18, Olaya",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Finca y Distribuidora",
        "last_name": "Los Mangos SAS",
        "document_type": "NIT",
        "document_number": "900456123-4",
        "email": "ventas@losmangos.co",
        "phone": "+57 575 678 9015",
        "address": "Zona Rural vía Ciénaga km 3",
        "city": "Santa Marta",
        "country": "Colombia",
    },
    {
        "first_name": "Pedro",
        "last_name": "Guzmán Petro",
        "document_type": "CC",
        "document_number": "77345678",
        "email": "pedro.guzman@gmail.com",
        "phone": "+57 313 789 0127",
        "address": "Cll. 30 # 5-15, Centro",
        "city": "Montería",
        "country": "Colombia",
    },
    {
        "first_name": "Distribuidora",
        "last_name": "Tropical Granos Ltda.",
        "document_type": "NIT",
        "document_number": "801890456-5",
        "email": "pedidos@tropicalgranos.co",
        "phone": "+57 605 890 1238",
        "address": "Central de Abastos Bodega 45",
        "city": "Barranquilla",
        "country": "Colombia",
    },
    {
        "first_name": "Blanca",
        "last_name": "Estrada Soto",
        "document_type": "CC",
        "document_number": "39456789",
        "email": "blanca.estrada@gmail.com",
        "phone": "+57 318 901 2349",
        "address": "Cra. 26 # 15-30",
        "city": "Valledupar",
        "country": "Colombia",
    },
]

SELLER_USERS: list[dict] = [
    {
        "email": "vendedor1@saborcaribe.co",
        "first_name": "Eibar",
        "last_name": "Alvarado",
        "phone": "+57 310 222 3333",
    },
    {
        "email": "vendedor2@saborcaribe.co",
        "first_name": "Rosa",
        "last_name": "Gamboa",
        "phone": "+57 310 333 4444",
    },
    {
        "email": "vendedor3@saborcaribe.co",
        "first_name": "Luis",
        "last_name": "Madera",
        "phone": "+57 310 444 5555",
    },
    {
        "email": "vendedor4@saborcaribe.co",
        "first_name": "Mariana",
        "last_name": "Palomino",
        "phone": "+57 310 555 6677",
    },
]

PAYMENT_METHODS = ["cash", "card", "transfer"]
IVA_RATE = Decimal("0.19")


def seed(session: Session) -> None:
    """Main seed function for Sabor Caribe demo data."""

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
            reason="Stock inicial - Apertura Sabor Caribe",
            created_at=datetime.now(timezone.utc) - timedelta(days=30),
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

    # ── 9. Sales — 30 days, heavy Fri-Sat and early week (B2B) ───────
    now = datetime.now(timezone.utc)
    invoice_counter = 0
    total_sales = 0

    for days_ago in range(30, -1, -1):
        day = now - timedelta(days=days_ago)
        weekday = day.weekday()
        # Mon/Tue: restaurants restock (heavy), Wed: medium, Thu: low,
        # Fri/Sat: retail peak, Sun: low
        sales_by_day = {0: (6, 12), 1: (5, 10), 2: (4, 8),
                        3: (3, 6),  4: (5, 9),  5: (8, 15), 6: (2, 5)}
        lo, hi = sales_by_day[weekday]
        num_sales = random.randint(lo, hi)
        if days_ago == 0:
            num_sales = random.randint(8, 14)

        for _ in range(num_sales):
            invoice_counter += 1
            invoice_number = f"SC-{invoice_counter:06d}"

            seller = random.choice(all_sellers)
            customer = random.choice(customer_list) if random.random() < 0.70 else None

            # Food: high volume, many items
            num_items = random.randint(2, 8)
            sale_products = random.sample(product_list, min(num_items, len(product_list)))

            sale_hour = random.randint(6, 19)
            sale_minute = random.randint(0, 59)
            sale_date = day.replace(
                hour=sale_hour, minute=sale_minute,
                second=random.randint(0, 59), microsecond=0,
            )

            subtotal = Decimal("0")
            items_data: list[dict] = []
            for prod in sale_products:
                # Food distributors sell in higher quantities
                qty = random.randint(1, 12)
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

            # Food wholesale: small discounts for B2B clients
            is_business_customer = (
                customer is not None and
                ("SAS" in customer.last_name or "Ltda" in customer.last_name or
                 "Distribuidora" in customer.first_name or "Restaurante" in customer.first_name)
            )
            max_disc = 8 if is_business_customer else 3
            discount = (subtotal * Decimal(str(random.randint(0, max_disc))) / Decimal("100")).quantize(Decimal("0.01"))
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
                sale.cancelled_at = sale_date + timedelta(hours=random.randint(1, 5))
                sale.cancelled_by = admin_user.id
                sale.cancellation_reason = random.choice([
                    "Producto sin stock",
                    "Pedido duplicado del cliente",
                    "Producto en mal estado",
                    "Cliente canceló el pedido",
                    "Error en la cantidad solicitada",
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
    logger.info(f"Created {total_sales} sales over 30 days")

    # ── 10. Restock ───────────────────────────────────────────────────
    for product in product_list:
        session.refresh(product)
        if product.stock_quantity <= product.stock_min:
            restock_qty = random.randint(100, 300)
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
                reason="Reposición de inventario Sabor Caribe",
                created_at=now - timedelta(hours=random.randint(1, 24)),
            ))
            session.add(product)
    session.commit()
    logger.info("Restocked low-inventory products")

    logger.info("=" * 60)
    logger.info("SEED SABOR CARIBE COMPLETE!")
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
    random.seed(37)
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    main()
