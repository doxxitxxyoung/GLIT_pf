from fastapi import APIRouter
from starlette.responses import JSONResponse


router = APIRouter()

@router.post('/glit_predict')
def glit_predict(request: dict):
    return JSONResponse(request)
