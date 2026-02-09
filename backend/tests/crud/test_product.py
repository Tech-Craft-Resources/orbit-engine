import uuid
from decimal import Decimal

from sqlmodel import Session

from app import crud
from app.models import ProductCreate, ProductUpdate
from tests.utils.category import create_random_category
from tests.utils.product import create_random_product
from tests.utils.user import _get_default_org_id
from tests.utils.utils import random_lower_string


def test_create_product(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    sku = f"SKU-{random_lower_string()[:16]}"
    product_in = ProductCreate(
        name="Test Product",
        sku=sku,
        description="A test product",
        cost_price=Decimal("10.00"),
        sale_price=Decimal("25.50"),
        stock_quantity=100,
        stock_min=10,
    )
    product = crud.create_product(
        session=db, product_create=product_in, organization_id=organization_id
    )
    assert product.name == "Test Product"
    assert product.sku == sku
    assert product.description == "A test product"
    assert product.cost_price == Decimal("10.00")
    assert product.sale_price == Decimal("25.50")
    assert product.stock_quantity == 100
    assert product.stock_min == 10
    assert product.organization_id == organization_id
    assert product.is_active is True
    assert product.deleted_at is None


def test_create_product_with_category(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    category = create_random_category(db, organization_id=organization_id)
    product = create_random_product(
        db, organization_id=organization_id, category_id=category.id
    )
    assert product.category_id == category.id


def test_get_product_by_id(db: Session) -> None:
    product = create_random_product(db)
    fetched = crud.get_product_by_id(
        session=db,
        product_id=product.id,
        organization_id=product.organization_id,
    )
    assert fetched
    assert fetched.id == product.id
    assert fetched.name == product.name


def test_get_product_by_id_not_found(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    fetched = crud.get_product_by_id(
        session=db,
        product_id=uuid.uuid4(),
        organization_id=organization_id,
    )
    assert fetched is None


def test_get_products_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    create_random_product(db, organization_id=organization_id)
    create_random_product(db, organization_id=organization_id)
    products = crud.get_products_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(products) >= 2


def test_count_products_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_products_by_organization(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_product_by_sku(db: Session) -> None:
    product = create_random_product(db)
    fetched = crud.get_product_by_sku(
        session=db,
        sku=product.sku,
        organization_id=product.organization_id,
    )
    assert fetched
    assert fetched.id == product.id


def test_get_low_stock_products(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    # Create a product with stock at minimum
    create_random_product(
        db, organization_id=organization_id, stock_quantity=5, stock_min=10
    )
    products = crud.get_low_stock_products(
        session=db, organization_id=organization_id
    )
    assert len(products) >= 1
    for p in products:
        assert p.stock_quantity <= p.stock_min


def test_count_low_stock_products(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_low_stock_products(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_update_product(db: Session) -> None:
    product = create_random_product(db)
    new_name = f"Updated-{random_lower_string()[:16]}"
    update_data = ProductUpdate(
        name=new_name,
        description="Updated desc",
        sale_price=Decimal("99.99"),
    )
    updated = crud.update_product(
        session=db, db_product=product, product_in=update_data
    )
    assert updated.name == new_name
    assert updated.description == "Updated desc"
    assert updated.sale_price == Decimal("99.99")


def test_adjust_product_stock(db: Session) -> None:
    product = create_random_product(db, stock_quantity=50)
    # Add stock
    adjusted = crud.adjust_product_stock(
        session=db, db_product=product, quantity=20
    )
    assert adjusted.stock_quantity == 70
    # Remove stock
    adjusted = crud.adjust_product_stock(
        session=db, db_product=adjusted, quantity=-10
    )
    assert adjusted.stock_quantity == 60


def test_soft_delete_product(db: Session) -> None:
    product = create_random_product(db)
    deleted = crud.soft_delete_product(session=db, db_product=product)
    assert deleted.deleted_at is not None
    assert deleted.is_active is False

    # Should not appear in normal queries
    fetched = crud.get_product_by_id(
        session=db,
        product_id=product.id,
        organization_id=product.organization_id,
    )
    assert fetched is None
