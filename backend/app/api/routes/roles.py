from typing import Any

from fastapi import APIRouter

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import RolesPublic, RolePublic

router = APIRouter()


@router.get("/", response_model=RolesPublic)
def list_roles(*, session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get all available roles in the system.

    Any authenticated user can see the available roles.
    """
    roles = crud.get_roles(session=session)
    return RolesPublic(data=roles, count=len(roles))
