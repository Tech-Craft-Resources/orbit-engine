import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr, field_validator
from sqlalchemy import Column, DateTime, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from collections.abc import Sequence


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================================
# ORGANIZATION MODELS
# ============================================================================


class OrganizationBase(SQLModel):
    name: str = Field(max_length=255)
    slug: str = Field(max_length=100, index=True)
    description: str | None = Field(default=None)
    logo_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format: lowercase, alphanumeric and hyphens only"""
        import re

        if not re.match(r"^[a-z0-9-]{3,50}$", v):
            raise ValueError(
                "Slug must be 3-50 characters, lowercase letters, numbers and hyphens only"
            )
        return v


class Organization(OrganizationBase, table=True):
    __tablename__ = "organizations"
    __table_args__ = (
        Index("idx_organizations_slug", "slug", unique=True),
        Index("idx_organizations_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    users: list["User"] = Relationship(back_populates="organization")
    categories: list["Category"] = Relationship(back_populates="organization")
    products: list["Product"] = Relationship(back_populates="organization")
    customers: list["Customer"] = Relationship(back_populates="organization")
    inventory_movements: list["InventoryMovement"] = Relationship(back_populates="organization")
    sales: list["Sale"] = Relationship(back_populates="organization")


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class OrganizationPublic(OrganizationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ============================================================================
# ROLE MODELS
# ============================================================================


class RoleBase(SQLModel):
    name: str = Field(max_length=50, index=True)
    description: str | None = None
    permissions: list[str] = Field(default_factory=list, sa_column=Column(JSONB))  # type: ignore


class Role(RoleBase, table=True):
    __tablename__ = "roles"
    __table_args__ = (Index("idx_roles_name", "name", unique=True),)

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    users: list["User"] = Relationship(back_populates="role")


class RolePublic(RoleBase):
    id: int
    created_at: datetime


class RolesPublic(SQLModel):
    data: list[RolePublic]
    count: int


# ============================================================================
# CATEGORY MODELS
# ============================================================================


class CategoryBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None)
    parent_id: uuid.UUID | None = Field(default=None, foreign_key="categories.id")
    is_active: bool = Field(default=True)


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "name",
            "parent_id",
            name="uq_categories_organization_name_parent",
        ),
        Index("idx_categories_organization_id", "organization_id"),
        Index("idx_categories_parent_id", "parent_id"),
        Index("idx_categories_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="categories")
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    children: list["Category"] = Relationship(back_populates="parent")
    products: list["Product"] = Relationship(back_populates="category")


class CategoryCreate(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None)
    parent_id: uuid.UUID | None = None


class CategoryUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    parent_id: uuid.UUID | None = None
    is_active: bool | None = None


class CategoryPublic(CategoryBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int


# ============================================================================
# PRODUCT MODELS
# ============================================================================


class ProductBase(SQLModel):
    name: str = Field(max_length=255)
    sku: str = Field(max_length=100)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None, max_length=500)
    cost_price: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    sale_price: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    stock_quantity: int = Field(default=0)
    stock_min: int = Field(default=0)
    stock_max: int | None = Field(default=None)
    unit: str = Field(default="unit", max_length=50)
    barcode: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class Product(ProductBase, table=True):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "sku",
            name="uq_products_organization_sku",
        ),
        Index("idx_products_organization_id", "organization_id"),
        Index("idx_products_category_id", "category_id"),
        Index("idx_products_is_active", "is_active"),
        Index("idx_products_sku", "sku"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    category_id: uuid.UUID | None = Field(
        default=None, foreign_key="categories.id", index=True
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="products")
    category: Optional["Category"] = Relationship(back_populates="products")
    inventory_movements: list["InventoryMovement"] = Relationship(back_populates="product")
    sale_items: list["SaleItem"] = Relationship(back_populates="product")


class ProductCreate(SQLModel):
    name: str = Field(max_length=255)
    sku: str = Field(max_length=100)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None, max_length=500)
    category_id: uuid.UUID | None = None
    cost_price: Decimal = Field(default=Decimal("0"))
    sale_price: Decimal = Field(default=Decimal("0"))
    stock_quantity: int = Field(default=0)
    stock_min: int = Field(default=0)
    stock_max: int | None = None
    unit: str = Field(default="unit", max_length=50)
    barcode: str | None = Field(default=None, max_length=100)

    @field_validator("cost_price", "sale_price")
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Price must be non-negative")
        return v

    @field_validator("stock_quantity", "stock_min")
    @classmethod
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Stock values must be non-negative")
        return v


class ProductUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    sku: str | None = Field(default=None, max_length=100)
    description: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
    category_id: uuid.UUID | None = None
    cost_price: Decimal | None = None
    sale_price: Decimal | None = None
    stock_quantity: int | None = None
    stock_min: int | None = None
    stock_max: int | None = None
    unit: str | None = Field(default=None, max_length=50)
    barcode: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None

    @field_validator("cost_price", "sale_price")
    @classmethod
    def validate_price(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v < 0:
            raise ValueError("Price must be non-negative")
        return v

    @field_validator("stock_quantity", "stock_min")
    @classmethod
    def validate_stock(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("Stock values must be non-negative")
        return v


class StockAdjustment(SQLModel):
    """Schema for manual stock adjustment."""
    quantity: int  # Can be positive (add) or negative (subtract)
    reason: str = Field(max_length=500)


class ProductPublic(ProductBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    category_id: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


# ============================================================================
# INVENTORY MOVEMENT MODELS
# ============================================================================


class InventoryMovementBase(SQLModel):
    movement_type: str = Field(max_length=50)  # sale, purchase, adjustment, return
    quantity: int  # positive = in, negative = out
    previous_stock: int
    new_stock: int
    reference_id: uuid.UUID | None = Field(default=None)
    reference_type: str | None = Field(default=None, max_length=50)  # sale, purchase, adjustment
    reason: str | None = Field(default=None)


class InventoryMovement(InventoryMovementBase, table=True):
    __tablename__ = "inventory_movements"
    __table_args__ = (
        Index("idx_inventory_movements_organization_id", "organization_id"),
        Index("idx_inventory_movements_product_id", "product_id"),
        Index("idx_inventory_movements_user_id", "user_id"),
        Index("idx_inventory_movements_movement_type", "movement_type"),
        Index("idx_inventory_movements_created_at", "created_at"),
        Index(
            "idx_inventory_movements_reference",
            "reference_type",
            "reference_id",
        ),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="inventory_movements")
    product: "Product" = Relationship(back_populates="inventory_movements")
    user: "User" = Relationship(back_populates="inventory_movements")


class InventoryMovementCreate(SQLModel):
    """Schema for creating an inventory movement."""
    product_id: uuid.UUID
    movement_type: str = Field(max_length=50)
    quantity: int
    reference_id: uuid.UUID | None = None
    reference_type: str | None = Field(default=None, max_length=50)
    reason: str | None = None


class InventoryMovementPublic(InventoryMovementBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    product_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class InventoryMovementsPublic(SQLModel):
    data: list[InventoryMovementPublic]
    count: int


# ============================================================================
# CUSTOMER MODELS
# ============================================================================


class CustomerBase(SQLModel):
    document_type: str = Field(max_length=50)  # DNI, RUC, Pasaporte, Otro
    document_number: str = Field(max_length=50)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None)
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None)
    is_active: bool = Field(default=True)


class Customer(CustomerBase, table=True):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "document_number",
            name="uq_customers_organization_document",
        ),
        Index("idx_customers_organization_id", "organization_id"),
        Index("idx_customers_email", "email"),
        Index("idx_customers_phone", "phone"),
        Index("idx_customers_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    total_purchases: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    purchases_count: int = Field(default=0)
    last_purchase_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="customers")
    sales: list["Sale"] = Relationship(back_populates="customer")


class CustomerCreate(SQLModel):
    document_type: str = Field(max_length=50)
    document_number: str = Field(max_length=50)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None)
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None)


class CustomerUpdate(SQLModel):
    document_type: str | None = Field(default=None, max_length=50)
    document_number: str | None = Field(default=None, max_length=50)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = None
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    is_active: bool | None = None


class CustomerPublic(CustomerBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    total_purchases: Decimal
    purchases_count: int
    last_purchase_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class CustomersPublic(SQLModel):
    data: list[CustomerPublic]
    count: int


# ============================================================================
# SALE MODELS
# ============================================================================


class SaleBase(SQLModel):
    invoice_number: str = Field(max_length=100)
    sale_date: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    subtotal: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    discount: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    tax: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    total: Decimal = Field(
        default=Decimal("0"),
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    payment_method: str = Field(default="cash", max_length=50)  # cash, card, transfer, other
    status: str = Field(default="completed", max_length=50)  # completed, cancelled, pending
    notes: str | None = Field(default=None)


class Sale(SaleBase, table=True):
    __tablename__ = "sales"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "invoice_number",
            name="uq_sales_organization_invoice_number",
        ),
        Index("idx_sales_organization_id", "organization_id"),
        Index("idx_sales_customer_id", "customer_id"),
        Index("idx_sales_user_id", "user_id"),
        Index("idx_sales_status", "status"),
        Index("idx_sales_sale_date", "sale_date"),
        Index("idx_sales_invoice_number", "invoice_number"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    customer_id: uuid.UUID | None = Field(
        default=None, foreign_key="customers.id", index=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    cancelled_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    cancelled_by: uuid.UUID | None = Field(
        default=None, foreign_key="users.id"
    )
    cancellation_reason: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="sales")
    customer: Optional["Customer"] = Relationship(back_populates="sales")
    items: list["SaleItem"] = Relationship(back_populates="sale")
    user: "User" = Relationship(
        back_populates="sales",
        sa_relationship_kwargs={"foreign_keys": "[Sale.user_id]"},
    )


class SaleItemBase(SQLModel):
    product_name: str = Field(max_length=255)
    product_sku: str = Field(max_length=100)
    quantity: int
    unit_price: Decimal = Field(
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )
    subtotal: Decimal = Field(
        sa_column=Column(Numeric(precision=12, scale=2), nullable=False),
    )


class SaleItem(SaleItemBase, table=True):
    __tablename__ = "sale_items"
    __table_args__ = (
        Index("idx_sale_items_sale_id", "sale_id"),
        Index("idx_sale_items_product_id", "product_id"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sale_id: uuid.UUID = Field(foreign_key="sales.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id", index=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    sale: "Sale" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="sale_items")


class SaleItemCreate(SQLModel):
    """Schema for creating a sale item within a sale."""
    product_id: uuid.UUID
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than zero")
        return v


class SaleCreate(SQLModel):
    """Schema for creating a sale."""
    customer_id: uuid.UUID | None = None
    payment_method: str = Field(default="cash", max_length=50)
    discount: Decimal = Field(default=Decimal("0"))
    tax: Decimal = Field(default=Decimal("0"))
    notes: str | None = None
    items: list[SaleItemCreate]

    @field_validator("discount", "tax")
    @classmethod
    def validate_non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v

    @field_validator("items")
    @classmethod
    def validate_items_not_empty(cls, v: list[SaleItemCreate]) -> list[SaleItemCreate]:
        if not v:
            raise ValueError("A sale must have at least one item")
        return v


class SaleItemPublic(SaleItemBase):
    id: uuid.UUID
    sale_id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime


class SalePublic(SQLModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    invoice_number: str
    customer_id: uuid.UUID | None = None
    user_id: uuid.UUID
    sale_date: datetime
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal
    payment_method: str
    status: str
    notes: str | None = None
    cancelled_at: datetime | None = None
    cancelled_by: uuid.UUID | None = None
    cancellation_reason: str | None = None
    items: list[SaleItemPublic] = []
    created_at: datetime
    updated_at: datetime


class SalesPublic(SQLModel):
    data: list[SalePublic]
    count: int


class SaleCancelRequest(SQLModel):
    """Schema for cancelling a sale."""
    reason: str = Field(max_length=500)


class SaleStatsPublic(SQLModel):
    """Schema for sales statistics."""
    sales_today_count: int
    sales_today_total: Decimal
    sales_month_count: int
    sales_month_total: Decimal
    average_ticket: Decimal


# ============================================================================
# DASHBOARD MODELS
# ============================================================================


class SalesTodayStats(SQLModel):
    """Sales stats for today."""
    count: int
    total: Decimal


class SalesMonthStats(SQLModel):
    """Sales stats for current month."""
    count: int
    total: Decimal


class TopProductItem(SQLModel):
    """A top-selling product in dashboard stats."""
    product_id: uuid.UUID
    product_name: str
    quantity_sold: int
    revenue: Decimal


class SalesByDayItem(SQLModel):
    """Sales aggregated by day."""
    date: str
    count: int
    total: Decimal


class DashboardStatsPublic(SQLModel):
    """Unified dashboard statistics response."""
    sales_today: SalesTodayStats
    sales_month: SalesMonthStats
    low_stock_count: int
    average_ticket: Decimal
    top_products: list[TopProductItem]
    sales_by_day: list[SalesByDayItem]


# ============================================================================
# USER MODELS
# ============================================================================


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255, index=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "email",
            name="uq_users_organization_email",
        ),
        Index("idx_users_organization_id", "organization_id"),
        Index("idx_users_role_id", "role_id"),
        Index("idx_users_is_active", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True)
    role_id: int = Field(foreign_key="roles.id", index=True)
    hashed_password: str = Field(max_length=255)
    last_login_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    failed_login_attempts: int = Field(default=0)
    locked_until: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    # Relationships
    organization: Organization = Relationship(back_populates="users")
    role: Role = Relationship(back_populates="users")
    inventory_movements: list["InventoryMovement"] = Relationship(back_populates="user")
    sales: list["Sale"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "[Sale.user_id]"},
    )


class UserCreate(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    role_id: int


class UserRegister(SQLModel):
    """Schema for user registration during organization signup"""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=50)


class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None
    role_id: int | None = None


class UserUpdateMe(SQLModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserPublic(UserBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    role_id: int
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserPublicWithRelations(UserPublic):
    """User with organization and role included"""

    organization: OrganizationPublic
    role: RolePublic


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# ============================================================================
# ORGANIZATION SIGNUP
# ============================================================================


class OrganizationSignup(SQLModel):
    """Schema for creating a new organization with admin user"""

    # Organization data
    organization_name: str = Field(max_length=255)
    organization_slug: str = Field(max_length=100)
    organization_description: str | None = None

    # Admin user data
    admin_email: EmailStr = Field(max_length=255)
    admin_password: str = Field(min_length=8, max_length=128)
    admin_first_name: str = Field(max_length=100)
    admin_last_name: str = Field(max_length=100)
    admin_phone: str | None = Field(default=None, max_length=50)

    @field_validator("organization_slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format"""
        import re

        if not re.match(r"^[a-z0-9-]{3,50}$", v):
            raise ValueError(
                "Slug must be 3-50 characters, lowercase letters, numbers and hyphens only"
            )
        return v


# ============================================================================
# AUTHENTICATION MODELS
# ============================================================================


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str  # User ID
    organization_id: str  # Organization ID
    role: str  # Role name


class LoginResponse(Token):
    """Response after successful login with user data"""

    user: UserPublicWithRelations


# ============================================================================
# GENERIC MODELS
# ============================================================================


class Message(SQLModel):
    message: str


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
