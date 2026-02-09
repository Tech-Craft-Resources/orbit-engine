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
    Sale,
    SaleItem,
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
# SALE CRUD
# ============================================================================


def generate_invoice_number(
    *, session: Session, organization_id: uuid.UUID
) -> str:
    """Generate the next invoice number for an organization."""
    from sqlalchemy import func

    count = session.exec(
        select(func.count())
        .select_from(Sale)
        .where(Sale.organization_id == organization_id)
    ).one()
    return f"INV-{count + 1:06d}"


def create_sale(
    *,
    session: Session,
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    customer_id: uuid.UUID | None,
    invoice_number: str,
    subtotal: Any,
    discount: Any,
    tax: Any,
    total: Any,
    payment_method: str,
    notes: str | None,
) -> Sale:
    """Create a new sale record."""
    sale = Sale(
        organization_id=organization_id,
        user_id=user_id,
        customer_id=customer_id,
        invoice_number=invoice_number,
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        total=total,
        payment_method=payment_method,
        notes=notes,
        status="completed",
    )
    session.add(sale)
    session.commit()
    session.refresh(sale)
    return sale


def create_sale_item(
    *,
    session: Session,
    sale_id: uuid.UUID,
    product_id: uuid.UUID,
    product_name: str,
    product_sku: str,
    quantity: int,
    unit_price: Any,
    subtotal: Any,
) -> SaleItem:
    """Create a sale item record."""
    item = SaleItem(
        sale_id=sale_id,
        product_id=product_id,
        product_name=product_name,
        product_sku=product_sku,
        quantity=quantity,
        unit_price=unit_price,
        subtotal=subtotal,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_sale_by_id(
    *, session: Session, sale_id: uuid.UUID, organization_id: uuid.UUID
) -> Sale | None:
    """Get a sale by ID within an organization, including items."""
    statement = (
        select(Sale)
        .where(Sale.id == sale_id)
        .where(Sale.organization_id == organization_id)
    )
    return session.exec(statement).first()


def get_sales_by_organization(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Sale]:
    """Get all sales for an organization, ordered by most recent."""
    statement = (
        select(Sale)
        .where(Sale.organization_id == organization_id)
        .order_by(Sale.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_sales_by_organization(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count sales in an organization."""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Sale)
        .where(Sale.organization_id == organization_id)
    )
    return session.exec(statement).one()


def get_sale_items(
    *, session: Session, sale_id: uuid.UUID
) -> list[SaleItem]:
    """Get all items for a sale."""
    statement = (
        select(SaleItem)
        .where(SaleItem.sale_id == sale_id)
    )
    return list(session.exec(statement).all())


def cancel_sale(
    *,
    session: Session,
    db_sale: Sale,
    cancelled_by: uuid.UUID,
    reason: str,
) -> Sale:
    """Cancel a sale."""
    from datetime import datetime, timezone

    db_sale.status = "cancelled"
    db_sale.cancelled_at = datetime.now(timezone.utc)
    db_sale.cancelled_by = cancelled_by
    db_sale.cancellation_reason = reason
    db_sale.updated_at = datetime.now(timezone.utc)
    session.add(db_sale)
    session.commit()
    session.refresh(db_sale)
    return db_sale


def get_sales_today(
    *,
    session: Session,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Sale]:
    """Get today's sales for an organization."""
    from datetime import datetime, timezone, time

    today_start = datetime.combine(
        datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc
    )
    statement = (
        select(Sale)
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .where(Sale.sale_date >= today_start)
        .order_by(Sale.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_sales_today(
    *, session: Session, organization_id: uuid.UUID
) -> int:
    """Count today's completed sales in an organization."""
    from datetime import datetime, timezone, time
    from sqlalchemy import func

    today_start = datetime.combine(
        datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc
    )
    statement = (
        select(func.count())
        .select_from(Sale)
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .where(Sale.sale_date >= today_start)
    )
    return session.exec(statement).one()


def get_sales_stats(
    *, session: Session, organization_id: uuid.UUID
) -> dict[str, Any]:
    """Get sales statistics for an organization."""
    from datetime import datetime, timezone, time
    from decimal import Decimal
    from sqlalchemy import func

    now = datetime.now(timezone.utc)
    today_start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Today stats
    today_result = session.exec(
        select(func.count(), func.coalesce(func.sum(Sale.total), 0))
        .select_from(Sale)
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .where(Sale.sale_date >= today_start)
    ).one()

    # Month stats
    month_result = session.exec(
        select(func.count(), func.coalesce(func.sum(Sale.total), 0))
        .select_from(Sale)
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .where(Sale.sale_date >= month_start)
    ).one()

    sales_today_count = today_result[0]
    sales_today_total = today_result[1]
    sales_month_count = month_result[0]
    sales_month_total = month_result[1]

    # Average ticket
    if sales_month_count > 0:
        average_ticket = Decimal(str(sales_month_total)) / sales_month_count
    else:
        average_ticket = Decimal("0")

    return {
        "sales_today_count": sales_today_count,
        "sales_today_total": Decimal(str(sales_today_total)),
        "sales_month_count": sales_month_count,
        "sales_month_total": Decimal(str(sales_month_total)),
        "average_ticket": average_ticket,
    }


def update_customer_purchase_stats(
    *,
    session: Session,
    db_customer: Customer,
    sale_total: Any,
) -> Customer:
    """Update customer's denormalized purchase stats after a sale."""
    from datetime import datetime, timezone
    from decimal import Decimal

    db_customer.total_purchases = Decimal(str(db_customer.total_purchases)) + Decimal(str(sale_total))
    db_customer.purchases_count += 1
    db_customer.last_purchase_at = datetime.now(timezone.utc)
    db_customer.updated_at = datetime.now(timezone.utc)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def revert_customer_purchase_stats(
    *,
    session: Session,
    db_customer: Customer,
    sale_total: Any,
) -> Customer:
    """Revert customer's denormalized purchase stats after a sale cancellation."""
    from datetime import datetime, timezone
    from decimal import Decimal

    db_customer.total_purchases = Decimal(str(db_customer.total_purchases)) - Decimal(str(sale_total))
    if db_customer.total_purchases < 0:
        db_customer.total_purchases = Decimal("0")
    db_customer.purchases_count = max(0, db_customer.purchases_count - 1)
    db_customer.updated_at = datetime.now(timezone.utc)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def get_sales_by_customer(
    *,
    session: Session,
    customer_id: uuid.UUID,
    organization_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Sale]:
    """Get all sales for a specific customer."""
    statement = (
        select(Sale)
        .where(Sale.customer_id == customer_id)
        .where(Sale.organization_id == organization_id)
        .order_by(Sale.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_sales_by_customer(
    *,
    session: Session,
    customer_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> int:
    """Count sales for a specific customer."""
    from sqlalchemy import func

    statement = (
        select(func.count())
        .select_from(Sale)
        .where(Sale.customer_id == customer_id)
        .where(Sale.organization_id == organization_id)
    )
    return session.exec(statement).one()


# ============================================================================
# DASHBOARD
# ============================================================================


def get_top_products(
    *,
    session: Session,
    organization_id: uuid.UUID,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Get top-selling products by quantity sold for completed sales."""
    from decimal import Decimal
    from sqlalchemy import func

    statement = (
        select(
            SaleItem.product_id,
            SaleItem.product_name,
            func.sum(SaleItem.quantity).label("quantity_sold"),
            func.sum(SaleItem.subtotal).label("revenue"),
        )
        .join(Sale, SaleItem.sale_id == Sale.id)
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .group_by(SaleItem.product_id, SaleItem.product_name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(limit)
    )
    results = session.exec(statement).all()
    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "quantity_sold": int(row[2]),
            "revenue": Decimal(str(row[3])),
        }
        for row in results
    ]


def get_sales_by_day(
    *,
    session: Session,
    organization_id: uuid.UUID,
    days: int = 30,
) -> list[dict[str, Any]]:
    """Get sales aggregated by day for the last N days, completed sales only."""
    from datetime import datetime, timedelta, timezone
    from decimal import Decimal
    from sqlalchemy import func, cast, Date

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)

    statement = (
        select(
            cast(Sale.sale_date, Date).label("date"),
            func.count().label("count"),
            func.coalesce(func.sum(Sale.total), 0).label("total"),
        )
        .where(Sale.organization_id == organization_id)
        .where(Sale.status == "completed")
        .where(Sale.sale_date >= start_date)
        .group_by(cast(Sale.sale_date, Date))
        .order_by(cast(Sale.sale_date, Date))
    )
    results = session.exec(statement).all()
    return [
        {
            "date": str(row[0]),
            "count": int(row[1]),
            "total": Decimal(str(row[2])),
        }
        for row in results
    ]


def get_dashboard_stats(
    *,
    session: Session,
    organization_id: uuid.UUID,
) -> dict[str, Any]:
    """Get unified dashboard statistics for an organization."""
    # Reuse existing functions
    sales_stats = get_sales_stats(session=session, organization_id=organization_id)
    low_stock = count_low_stock_products(session=session, organization_id=organization_id)
    top_products = get_top_products(session=session, organization_id=organization_id)
    sales_by_day = get_sales_by_day(session=session, organization_id=organization_id)

    return {
        "sales_today": {
            "count": sales_stats["sales_today_count"],
            "total": sales_stats["sales_today_total"],
        },
        "sales_month": {
            "count": sales_stats["sales_month_count"],
            "total": sales_stats["sales_month_total"],
        },
        "low_stock_count": low_stock,
        "average_ticket": sales_stats["average_ticket"],
        "top_products": top_products,
        "sales_by_day": sales_by_day,
    }


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
