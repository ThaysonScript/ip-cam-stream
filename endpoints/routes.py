from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from core.camera import Camera

camera = Camera()

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello from root endpoint"}


@router.get("/ptz/control")
async def ptz_control(
    rotate_base: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento horizontal (Pan): -1.0 a 1.0"),
    rotate_lens: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento vertical (Tilt): -1.0 a 1.0"),
    zoom: float = Query(0.0, ge=-1.0, le=1.0, description="Zoom óptico: -1.0 a 1.0")
):
    response = camera.ptz_relative_movement(
        rotate_base=rotate_base,
        rotate_lens=rotate_lens,
        zoom=zoom
    )
    return JSONResponse(content=response)