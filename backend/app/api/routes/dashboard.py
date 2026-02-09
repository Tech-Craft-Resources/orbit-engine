from typing import Any

from fastapi import APIRouter

from app import crud
from app.api.deps import (
    CurrentOrganization,
    CurrentUser,
    SessionDep,
)
from app.models import DashboardStatsPublic

router = APIRouter()


@router.get("/stats", response_model=DashboardStatsPublic)
def read_dashboard_stats(
    session: SessionDep,
    current_user: CurrentUser,
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
