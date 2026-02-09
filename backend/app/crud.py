from typing import Any
import uuid

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    User,
    UserCreate,
    UserUpdate,
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    Category,
    CategoryCreate,
    CategoryUpdate,
    Product,
    ProductCreate,
    ProductUpdate,
    Customer,
    CustomerCreate,
    CustomerUpdate,
    InventoryMovement,
    InventoryMovementCreate,
    Role,
)


# ============================================================================
# ORGANIZATION CRUD
# ============================================================================


def create_organization(
    *, session: Session, organization_create: OrganizationCreate
) -> Organization:
    """Create a new organization"""
    db_obj = Organization.model_validate(organization_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_organization_by_id(
    *, session: Session, organization_id: uuid.UUID
) -> Organization | None:
    """Get organization by ID"""
    return session.get(Organization, organization_id)


def get_organization_by_slug(*, session: Session, slug: str) -> Organization | None:
    """Get organization by slug"""
    statement = select(Organization).where(Organization.slug == slug)
    return session.exec(statement).first()


def update_organization(
    *,
    session: Session,
    db_organization: Organization,
    organization_in: OrganizationUpdate,
) -> Organization:
    """Update an organization"""
    organization_data = organization_in.model_dump(exclude_unset=True)
    db_organization.sqlmodel_update(organization_data)
    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)
    return db_organization


# ============================================================================
# ROLE CRUD
# ============================================================================


def get_role_by_id(*, session: Session, role_id: int) -> Role | None:
    """Get role by ID"""
    return session.get(Role, role_id)


def get_role_by_name(*, session: Session, name: str) -> Role | None:
    """Get role by name"""
    statement = select(Role).where(Role.name == name)
    return session.exec(statement).first()


def get_roles(*, session: Session) -> list[Role]:
    """Get all roles"""
    statement = select(Role)
    return list(session.exec(statement).all())


# ============================================================================
# USER CRUD
# ============================================================================


def create_user(
    *, session: Session, user_create: UserCreate, organization_id: uuid.UUID
) -> User:
    """Create a new user within an organization"""
    db_obj = User.model_validate(
        user_create,
        update={
            "hashed_password": get_password_hash(user_create.password),
            "organization_id": organization_id,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    """Update a user"""
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
        del user_data["password"]
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(
    *, session: Session, email: str, organization_id: uuid.UUID | None = None
) -> User | None:
    """
    Get user by email.
    If organization_id is provided, search within that organization only.
    """
    statement = select(User).where(User.email == email).where(User.deleted_at.is_(None))
    if organization_id:
        statement = statement.where(User.organization_id == organization_id)
    return session.exec(statement).first()


def get_user_by_id(
    *, session: Session, user_id: uuid.UUID, organization_id: uuid.UUID | None = None
) -> User | None:
    """
    Get user by ID.
    If organization_id is provided, ensure the user belongs to that organization.
    """
    statement = select(User).where(User.id == user_id).where(User.deleted_at.is_(None))
    if organization_id:
        statement = statement.where(User.organization_id == organization_id)
    return session.exec(statement).first()


def get_users_by_organization(
    *, session: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[User]:
    """Get all users for an organization"""
    statement = (
        select(User)
        .where(User.organization_id == organization_id)
        .where(User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_users_by_organization(*, session: Session, organization_id: uuid.UUID) -> int:
    """Count users in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(User)
        .where(User.organization_id == organization_id)
        .where(User.deleted_at.is_(None))
    )
    return session.exec(statement).one()


# ============================================================================
# CATEGORY CRUD
# ============================================================================


def create_category(
    *, session: Session, category_create: CategoryCreate, organization_id: uuid.UUID
) -> Category:
    """Create a new category within an organization"""
    db_obj = Category.model_validate(
        category_create,
        update={"organization_id": organization_id},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_category_by_id(
    *, session: Session, category_id: uuid.UUID, organization_id: uuid.UUID
) -> Category | None:
    """Get a category by ID within an organization"""
    statement = (
        select(Category)
        .where(Category.id == category_id)
        .where(Category.organization_id == organization_id)
        .where(Category.deleted_at.is_(None))
    )
    return session.exec(statement).first()


def get_categories_by_organization(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Category]:
    """Get all categories for an organization"""
    statement = (
        select(Category)
        .where(Category.organization_id == organization_id)
        .where(Category.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_categories_by_organization(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count categories in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Category)
        .where(Category.organization_id == organization_id)
        .where(Category.deleted_at.is_(None))
    )
    return session.exec(statement).one()


def get_category_by_name(
    *,
    session: Session,
    name: str,
    organization_id: uuid.UUID,
    parent_id: uuid.UUID | None = None,
) -> Category | None:
    """Get a category by name within an organization and parent"""
    statement = (
        select(Category)
        .where(Category.name == name)
        .where(Category.organization_id == organization_id)
        .where(Category.deleted_at.is_(None))
    )
    if parent_id is not None:
        statement = statement.where(Category.parent_id == parent_id)
    else:
        statement = statement.where(Category.parent_id.is_(None))
    return session.exec(statement).first()


def update_category(
    *, session: Session, db_category: Category, category_in: CategoryUpdate
) -> Category:
    """Update a category"""
    from datetime import datetime, timezone

    category_data = category_in.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    db_category.updated_at = datetime.now(timezone.utc)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def soft_delete_category(*, session: Session, db_category: Category) -> Category:
    """Soft delete a category"""
    from datetime import datetime, timezone

    db_category.deleted_at = datetime.now(timezone.utc)
    db_category.is_active = False
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


# ============================================================================
# PRODUCT CRUD
# ============================================================================


def create_product(
    *, session: Session, product_create: ProductCreate, organization_id: uuid.UUID
) -> Product:
    """Create a new product within an organization"""
    db_obj = Product.model_validate(
        product_create,
        update={"organization_id": organization_id},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_product_by_id(
    *, session: Session, product_id: uuid.UUID, organization_id: uuid.UUID
) -> Product | None:
    """Get a product by ID within an organization"""
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
    )
    return session.exec(statement).first()


def get_products_by_organization(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Product]:
    """Get all products for an organization"""
    statement = (
        select(Product)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_products_by_organization(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count products in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Product)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
    )
    return session.exec(statement).one()


def get_product_by_sku(
    *, session: Session, sku: str, organization_id: uuid.UUID
) -> Product | None:
    """Get a product by SKU within an organization"""
    statement = (
        select(Product)
        .where(Product.sku == sku)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
    )
    return session.exec(statement).first()


def get_low_stock_products(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Product]:
    """Get products where stock_quantity <= stock_min"""
    statement = (
        select(Product)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
        .where(Product.stock_quantity <= Product.stock_min)
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_low_stock_products(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count products where stock_quantity <= stock_min"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Product)
        .where(Product.organization_id == organization_id)
        .where(Product.deleted_at.is_(None))
        .where(Product.stock_quantity <= Product.stock_min)
    )
    return session.exec(statement).one()


def update_product(
    *, session: Session, db_product: Product, product_in: ProductUpdate
) -> Product:
    """Update a product"""
    from datetime import datetime, timezone

    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    db_product.updated_at = datetime.now(timezone.utc)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def adjust_product_stock(
    *, session: Session, db_product: Product, quantity: int
) -> Product:
    """Adjust product stock by a given quantity (positive or negative)"""
    from datetime import datetime, timezone

    db_product.stock_quantity += quantity
    db_product.updated_at = datetime.now(timezone.utc)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def soft_delete_product(*, session: Session, db_product: Product) -> Product:
    """Soft delete a product"""
    from datetime import datetime, timezone

    db_product.deleted_at = datetime.now(timezone.utc)
    db_product.is_active = False
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


# ============================================================================
# CUSTOMER CRUD
# ============================================================================


def create_customer(
    *, session: Session, customer_create: CustomerCreate, organization_id: uuid.UUID
) -> Customer:
    """Create a new customer within an organization"""
    db_obj = Customer.model_validate(
        customer_create,
        update={"organization_id": organization_id},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_customer_by_id(
    *, session: Session, customer_id: uuid.UUID, organization_id: uuid.UUID
) -> Customer | None:
    """Get a customer by ID within an organization"""
    statement = (
        select(Customer)
        .where(Customer.id == customer_id)
        .where(Customer.organization_id == organization_id)
        .where(Customer.deleted_at.is_(None))
    )
    return session.exec(statement).first()


def get_customers_by_organization(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Customer]:
    """Get all customers for an organization"""
    statement = (
        select(Customer)
        .where(Customer.organization_id == organization_id)
        .where(Customer.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_customers_by_organization(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count customers in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Customer)
        .where(Customer.organization_id == organization_id)
        .where(Customer.deleted_at.is_(None))
    )
    return session.exec(statement).one()


def get_customer_by_document(
    *, session: Session, document_number: str, organization_id: uuid.UUID
) -> Customer | None:
    """Get a customer by document number within an organization"""
    statement = (
        select(Customer)
        .where(Customer.document_number == document_number)
        .where(Customer.organization_id == organization_id)
        .where(Customer.deleted_at.is_(None))
    )
    return session.exec(statement).first()


def update_customer(
    *, session: Session, db_customer: Customer, customer_in: CustomerUpdate
) -> Customer:
    """Update a customer"""
    from datetime import datetime, timezone

    customer_data = customer_in.model_dump(exclude_unset=True)
    db_customer.sqlmodel_update(customer_data)
    db_customer.updated_at = datetime.now(timezone.utc)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def soft_delete_customer(*, session: Session, db_customer: Customer) -> Customer:
    """Soft delete a customer"""
    from datetime import datetime, timezone

    db_customer.deleted_at = datetime.now(timezone.utc)
    db_customer.is_active = False
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


# ============================================================================
# INVENTORY MOVEMENT CRUD
# ============================================================================


def create_inventory_movement(
    *,
    session: Session,
    movement_create: InventoryMovementCreate,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    previous_stock: int,
    new_stock: int,
) -> InventoryMovement:
    """Create a new inventory movement record"""
    db_obj = InventoryMovement.model_validate(
        movement_create,
        update={
            "organization_id": organization_id,
            "user_id": user_id,
            "previous_stock": previous_stock,
            "new_stock": new_stock,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_inventory_movement_by_id(
    *, session: Session, movement_id: uuid.UUID, organization_id: uuid.UUID
) -> InventoryMovement | None:
    """Get an inventory movement by ID within an organization"""
    statement = (
        select(InventoryMovement)
        .where(InventoryMovement.id == movement_id)
        .where(InventoryMovement.organization_id == organization_id)
    )
    return session.exec(statement).first()


def get_movements_by_organization(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[InventoryMovement]:
    """Get all inventory movements for an organization, ordered by most recent"""
    statement = (
        select(InventoryMovement)
        .where(InventoryMovement.organization_id == organization_id)
        .order_by(InventoryMovement.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_movements_by_organization(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count inventory movements in an organization"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(InventoryMovement)
        .where(InventoryMovement.organization_id == organization_id)
    )
    return session.exec(statement).one()


def get_movements_by_product(
    *,
    session: Session,
    product_id: uuid.UUID,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[InventoryMovement]:
    """Get all inventory movements for a specific product"""
    statement = (
        select(InventoryMovement)
        .where(InventoryMovement.product_id == product_id)
        .where(InventoryMovement.organization_id == organization_id)
        .order_by(InventoryMovement.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_movements_by_product(
    *,
    session: Session,
    product_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> int:
    """Count inventory movements for a specific product"""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(InventoryMovement)
        .where(InventoryMovement.product_id == product_id)
        .where(InventoryMovement.organization_id == organization_id)
    )
    return session.exec(statement).one()


# ============================================================================
# AUTHENTICATION
# ============================================================================

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(
    *,
    session: Session,
    email: str,
    password: str,
    organization_id: uuid.UUID | None = None,
) -> User | None:
    """
    Authenticate a user by email and password.
    If organization_id is provided, search within that organization only.
    """
    db_user = get_user_by_email(
        session=session, email=email, organization_id=organization_id
    )
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
