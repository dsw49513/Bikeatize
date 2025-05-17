from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"message": "API is working!"}
