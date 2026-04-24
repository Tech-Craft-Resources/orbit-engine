import csv
from datetime import UTC, date, datetime, time, timedelta
from io import BytesIO, StringIO
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentOrganization,
    CurrentUser,
    SessionDep,
    require_role,
)
from app.models import Category, DashboardExportRequest, DashboardStatsPublic, Role

router = APIRouter()


def _to_local_datetime(value: datetime, tz_name: str) -> datetime:
    target_tz = ZoneInfo(tz_name)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(target_tz)


def _to_local_iso(value: datetime, tz_name: str) -> str:
    return _to_local_datetime(value, tz_name).strftime("%Y-%m-%d %H:%M:%S")


def _to_utc_range(
    *,
    date_from: date | None,
    date_to: date | None,
    tz_name: str,
) -> tuple[datetime | None, datetime | None]:
    if date_from is None and date_to is None:
        return None, None

    tz = ZoneInfo(tz_name)
    start_utc = None
    end_utc = None

    if date_from is not None:
        start_local = datetime.combine(date_from, time.min, tzinfo=tz)
        start_utc = start_local.astimezone(UTC)

    if date_to is not None:
        end_local = datetime.combine(date_to + timedelta(days=1), time.min, tzinfo=tz)
        end_utc = end_local.astimezone(UTC)

    return start_utc, end_utc


def _build_xlsx_bytes(*, headers: list[str], rows: list[list[Any]]) -> bytes:
    output = BytesIO()
    import zipfile

    def xml_escape(value: str) -> str:
        return (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    def make_row_xml(values: list[Any], row_index: int) -> str:
        cell_xml: list[str] = []
        for col_idx, value in enumerate(values, start=1):
            cell_ref = f"{_column_name(col_idx)}{row_index}"
            if isinstance(value, (int, float)):
                cell_xml.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
            else:
                text = xml_escape("" if value is None else str(value))
                cell_xml.append(
                    f'<c r="{cell_ref}" t="inlineStr"><is><t>{text}</t></is></c>'
                )
        return f'<row r="{row_index}">{"".join(cell_xml)}</row>'

    worksheet_rows = [make_row_xml(headers, 1)]
    worksheet_rows.extend(make_row_xml(row, idx + 2) for idx, row in enumerate(rows))

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "<sheetData>"
        f"{''.join(worksheet_rows)}"
        "</sheetData>"
        "</worksheet>"
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        '<sheet name="Export" sheetId="1" r:id="rId1"/>'
        "</sheets>"
        "</workbook>"
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )

    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    return output.getvalue()


def _column_name(index: int) -> str:
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _build_inventory_export(
    *,
    session: SessionDep,
    organization_id: Any,
    payload: DashboardExportRequest,
) -> tuple[list[str], list[list[Any]]]:
    products = crud.get_products_by_organization(
        session=session,
        organization_id=organization_id,
        skip=0,
        limit=100000,
        search=payload.search,
        is_active=payload.is_active,
        category_id=payload.category_id,
        sort_by="name",
        sort_order="asc",
    )
    categories = list(
        session.exec(
            select(Category)
            .where(Category.organization_id == organization_id)
            .where(Category.deleted_at.is_(None))  # type: ignore[union-attr]
        ).all()
    )
    category_map = {str(category.id): category.name for category in categories}

    headers = [
        "SKU",
        "Producto",
        "Categoría",
        "Stock",
        "Stock mínimo",
        "Precio venta",
        "Estado",
        "Creado",
    ]
    rows: list[list[Any]] = []
    for product in products:
        rows.append(
            [
                product.sku,
                product.name,
                category_map.get(str(product.category_id), "—"),
                product.stock_quantity,
                product.stock_min,
                str(product.sale_price),
                "Activo" if product.is_active else "Inactivo",
                _to_local_iso(product.created_at, payload.timezone),
            ]
        )

    return headers, rows


def _build_customers_export(
    *,
    session: SessionDep,
    organization_id: Any,
    payload: DashboardExportRequest,
) -> tuple[list[str], list[list[Any]]]:
    customers = crud.get_customers_by_organization(
        session=session,
        organization_id=organization_id,
        skip=0,
        limit=100000,
        search=payload.search,
        is_active=payload.is_active,
        sort_by="first_name",
        sort_order="asc",
    )

    headers = [
        "Documento",
        "Nombre",
        "Email",
        "Teléfono",
        "Compras",
        "Total comprado",
        "Estado",
        "Creado",
    ]
    rows: list[list[Any]] = []
    for customer in customers:
        rows.append(
            [
                f"{customer.document_type} {customer.document_number}",
                f"{customer.first_name} {customer.last_name}",
                customer.email or "",
                customer.phone or "",
                customer.purchases_count,
                str(customer.total_purchases),
                "Activo" if customer.is_active else "Inactivo",
                _to_local_iso(customer.created_at, payload.timezone),
            ]
        )

    return headers, rows


def _build_sales_export(
    *,
    session: SessionDep,
    organization_id: Any,
    payload: DashboardExportRequest,
) -> tuple[list[str], list[list[Any]]]:
    sales = crud.get_sales_by_organization(
        session=session,
        organization_id=organization_id,
        skip=0,
        limit=100000,
        search=payload.search,
        status=payload.status,
        payment_method=payload.payment_method,
        sort_by="sale_date",
        sort_order="desc",
    )

    start_utc, end_utc = _to_utc_range(
        date_from=payload.date_from,
        date_to=payload.date_to,
        tz_name=payload.timezone,
    )
    if start_utc is not None:
        sales = [sale for sale in sales if sale.sale_date >= start_utc]
    if end_utc is not None:
        sales = [sale for sale in sales if sale.sale_date < end_utc]

    headers = [
        "Factura",
        "Fecha",
        "Total",
        "Método pago",
        "Estado",
        "Items",
        "Cliente ID",
    ]
    rows: list[list[Any]] = []
    for sale in sales:
        rows.append(
            [
                sale.invoice_number,
                _to_local_iso(sale.sale_date, payload.timezone),
                str(sale.total),
                sale.payment_method,
                sale.status,
                len(sale.items),
                str(sale.customer_id) if sale.customer_id else "",
            ]
        )

    return headers, rows


@router.get("/stats", response_model=DashboardStatsPublic)
def read_dashboard_stats(
    session: SessionDep,
    _current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    """
    Get dashboard statistics for the current organization.

    Any authenticated user can view dashboard stats.
    Returns sales today/month, low stock count, average ticket,
    top products, and sales by day.
    """
    return crud.get_dashboard_stats(
        session=session, organization_id=current_organization
    )


@router.post(
    "/export-excel",
    dependencies=[Depends(require_role("admin", "contador"))],
)
def export_dashboard_excel(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    payload: DashboardExportRequest,
) -> StreamingResponse:
    """Export dashboard datasets in Excel format (all filtered rows)."""
    role = session.get(Role, current_user.role_id)
    if not role:
        raise HTTPException(status_code=500, detail="User role not found")

    if role.name not in {"admin", "contador"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    try:
        ZoneInfo(payload.timezone)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail="Invalid timezone") from exc

    builders = {
        "inventory": _build_inventory_export,
        "customers": _build_customers_export,
        "sales": _build_sales_export,
    }

    builder = builders.get(payload.dataset)
    if builder is None:
        raise HTTPException(status_code=400, detail="Invalid dataset")

    headers, rows = builder(
        session=session,
        organization_id=current_organization,
        payload=payload,
    )

    if rows:
        content = _build_xlsx_bytes(headers=headers, rows=rows)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        suffix = "xlsx"
    else:
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(headers)
        content = csv_buffer.getvalue().encode("utf-8")
        media_type = "text/csv"
        suffix = "csv"

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    filename = f"{payload.dataset}-export-{timestamp}.{suffix}"

    return StreamingResponse(
        BytesIO(content),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
