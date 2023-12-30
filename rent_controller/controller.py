from fastapi import APIRouter

router = APIRouter()


@router.get("/Transport")
def get_accessible_transport():

