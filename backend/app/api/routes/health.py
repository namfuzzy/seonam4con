from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
