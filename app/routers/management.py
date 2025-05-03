from fastapi import APIRouter, status

router = APIRouter()


@router.get("/healthz", status_code=status.HTTP_200_OK)
def healthz():
    return {"status": "OK"}


@router.get("/ready", status_code=status.HTTP_200_OK)
def ready():
    return {"status": "OK"}
