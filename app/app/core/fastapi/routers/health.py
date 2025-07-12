from fastapi import APIRouter
from app.core.fastapi.models.base_models import HealthResponse

router = APIRouter()

@router.get("/")
async def health_check():
    # return {"status" : "up"}
    return HealthResponse(status="up")

@router.get("/healthz")
async def health_check():
    # return {"status" : "up"}
    return HealthResponse(status="up")
    
@router.get("/sexy")
async def health_check():
    # return {"status" : "up"}
    return HealthResponse(status="up")

@router.get("/test")
async def health_check():
    # return {"status" : "up"}
    return HealthResponse(status="up")

@router.get("/skata")
async def health_check():
    # return {"status" : "up"}
    return HealthResponse(status="sta moutra mou !!")