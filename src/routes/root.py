from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Root"])
async def get_root():
  return {
    "name": "EmailAnalyst",
    "status": "It works!",
  }