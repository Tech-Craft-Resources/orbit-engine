import uuid

from sqlmodel import Session

from app import crud
from app.models import InventoryMovementCreate
from tests.utils.inventory_movement import create_random_movement
from tests.utils.product import create_random_product
from tests.utils.user import _get_default_org_id, create_random_user


def test_create_inventory_movement(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    product = create_random_product(db, organization_id=organization_id, stock_quantity=50)
    user = create_random_user(db, role_name="seller")
    movement_in = InventoryMovementCreate(
        product_id=product.id,
        movement_type="purchase",
        quantity=20,
        reason="Restocking",
    )
    movement = crud.create_inventory_movement(
        session=db,
        movement_create=movement_in,
        organization_id=organization_id,
        user_id=user.id,
        previous_stock=50,
        new_stock=70,
    )
    assert movement.product_id == product.id
    assert movement.user_id == user.id
    assert movement.organization_id == organization_id
    assert movement.movement_type == "purchase"
    assert movement.quantity == 20
    assert movement.previous_stock == 50
    assert movement.new_stock == 70
    assert movement.reason == "Restocking"
    assert movement.created_at is not None


def test_get_inventory_movement_by_id(db: Session) -> None:
    movement = create_random_movement(db)
    fetched = crud.get_inventory_movement_by_id(
        session=db,
        movement_id=movement.id,
        organization_id=movement.organization_id,
    )
    assert fetched
    assert fetched.id == movement.id
    assert fetched.movement_type == movement.movement_type


def test_get_inventory_movement_by_id_not_found(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    fetched = crud.get_inventory_movement_by_id(
        session=db,
        movement_id=uuid.uuid4(),
        organization_id=organization_id,
    )
    assert fetched is None


def test_get_movements_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    create_random_movement(db, organization_id=organization_id)
    create_random_movement(db, organization_id=organization_id)
    movements = crud.get_movements_by_organization(
        session=db, organization_id=organization_id
    )
    assert len(movements) >= 2


def test_count_movements_by_organization(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    count = crud.count_movements_by_organization(
        session=db, organization_id=organization_id
    )
    assert count >= 0


def test_get_movements_by_product(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    product = create_random_product(db, organization_id=organization_id, stock_quantity=100)
    create_random_movement(
        db, organization_id=organization_id, product_id=product.id, quantity=10
    )
    create_random_movement(
        db, organization_id=organization_id, product_id=product.id, quantity=-5
    )
    movements = crud.get_movements_by_product(
        session=db,
        product_id=product.id,
        organization_id=organization_id,
    )
    assert len(movements) >= 2


def test_count_movements_by_product(db: Session) -> None:
    organization_id = _get_default_org_id(db)
    product = create_random_product(db, organization_id=organization_id, stock_quantity=100)
    create_random_movement(
        db, organization_id=organization_id, product_id=product.id, quantity=5
    )
    count = crud.count_movements_by_product(
        session=db,
        product_id=product.id,
        organization_id=organization_id,
    )
    assert count >= 1


def test_movement_with_reference(db: Session) -> None:
    """Test creating a movement with reference_id and reference_type"""
    organization_id = _get_default_org_id(db)
    product = create_random_product(db, organization_id=organization_id, stock_quantity=50)
    user = create_random_user(db, role_name="seller")
    ref_id = uuid.uuid4()
    movement_in = InventoryMovementCreate(
        product_id=product.id,
        movement_type="sale",
        quantity=-5,
        reference_id=ref_id,
        reference_type="sale",
        reason="Sale #123",
    )
    movement = crud.create_inventory_movement(
        session=db,
        movement_create=movement_in,
        organization_id=organization_id,
        user_id=user.id,
        previous_stock=50,
        new_stock=45,
    )
    assert movement.reference_id == ref_id
    assert movement.reference_type == "sale"


def test_movements_ordered_by_most_recent(db: Session) -> None:
    """Movements should be returned ordered by created_at desc"""
    organization_id = _get_default_org_id(db)
    product = create_random_product(db, organization_id=organization_id, stock_quantity=100)
    m1 = create_random_movement(
        db, organization_id=organization_id, product_id=product.id, quantity=5
    )
    m2 = create_random_movement(
        db, organization_id=organization_id, product_id=product.id, quantity=10
    )
    movements = crud.get_movements_by_product(
        session=db,
        product_id=product.id,
        organization_id=organization_id,
    )
    # Most recent should be first
    assert len(movements) >= 2
    assert movements[0].created_at >= movements[1].created_at
