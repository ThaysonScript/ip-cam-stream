from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional

from core.camera import Camera


camera = Camera()
router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "endpoint inicial sem relevancia"}


@router.get('/get/rtsp_viwer')
async def get_rtsp_viewer():
    return camera.rtsp_viewer()


@router.get("/ptz/capabilities")
async def ptz_capability_current_protocol(
    channel: int = Query(1, description="Canal PTZ (começa em 1)")
):
    return JSONResponse(content=camera.ptz_get_capability_current_protocol(
        channel=channel
    ))


@router.get("/ptz/control/basic_movement")
async def ptz_control_basic_movement(
    channel: int = Query(1, description="Canal PTZ (começa em 1)"),
    code: str = Query('Up', const=True),
    rotate_base: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento horizontal (Pan): -1.0 a 1.0"),
    rotate_lens: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento vertical (Tilt): -1.0 a 1.0"),
    zoom: float = Query(0.0, ge=-1.0, le=1.0, description="Zoom óptico: -1.0 a 1.0")
):
    return JSONResponse(content=camera.ptz_control_basic_movement(
        channel=channel,
        code=code,
        rotate_base=rotate_base,
        rotate_lens=rotate_lens,
        zoom=zoom
    ))


@router.get("/ptz/control/stop_movement")
async def ptz_control_stop_movement(
    code: str = Query('Up', const=True),
    channel: int = Query(1, description="Canal PTZ (começa em 1)"),
    rotate_base: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento horizontal (Pan): -1.0 a 1.0"),
    rotate_lens: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento vertical (Tilt): -1.0 a 1.0"),
    zoom: float = Query(0.0, ge=-1.0, le=1.0, description="Zoom óptico: -1.0 a 1.0")
):
    return JSONResponse(content=camera.ptz_control_stop_movement(
        code=code,
        channel=channel,
        rotate_base=rotate_base,
        rotate_lens=rotate_lens,
        zoom=zoom
    ))


@router.get("/ptz/control/continuosly_moving")
async def ptz_control_continuosly_moving(
    code: str = Query("Continuously", const=True),
    channel: int = Query(1, description="Canal PTZ (começa em 1)"),
    rotate_base: int = Query(0, ge=-8, le=8, description="Movimento horizontal (Pan): -8 a 8, valores além de ±4 ativam movimento contínuo"),
    rotate_lens: int = Query(0, ge=-8, le=8, description="Movimento vertical (Tilt): -8 a 8, valores além de ±4 ativam movimento contínuo"),
    zoom: int = Query(0, ge=-100, le=100, description="Zoom óptico: -100 a 100"),
    movement_time: int = Query(60, ge=1, le=3600, description="Tempo máximo em segundos até parada automática (1–3600)")
):
    return JSONResponse(content=camera.ptz_control_continuosly_moving(
        code=code,
        channel=channel,
        rotate_base=rotate_base,
        rotate_lens=rotate_lens,
        zoom=zoom,
        movement_time=movement_time
    ))
    
    
@router.get("/ptz/control/stop_continuosly_moving")
async def ptz_control_stop_continuosly_moving():
    return JSONResponse(content=camera.ptz_control_stop_continuosly_moving())


@router.get("/ptz/control/3d_positioning")
async def ptz_control_3d_positioning():
    return JSONResponse(content=camera.ptz_control_3d_positioning())


@router.get("/ptz/control/relative_movement")
async def ptz_control_relative_movement(
    rotate_base: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento horizontal (Pan): -1.0 a 1.0"),
    rotate_lens: float = Query(0.0, ge=-1.0, le=1.0, description="Movimento vertical (Tilt): -1.0 a 1.0"),
    zoom: float = Query(0.0, ge=-1.0, le=1.0, description="Zoom óptico: -1.0 a 1.0")
):
    return JSONResponse(content=camera.ptz_control_relative_movement(
        rotate_base=rotate_base,
        rotate_lens=rotate_lens,
        zoom=zoom
    ))


@router.get("/ptz/control/accurate_positioning")
async def ptz_control_accurate_positioning():
    return JSONResponse(content=camera.ptz_control_accurate_positioning())