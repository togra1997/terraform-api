from fastapi import APIRouter

from src.api.endpoint.proxmox.endpoint import router as proxmox_router
from src.api.endpoint.terraform.terraform import terraform_router

router = APIRouter()
router.include_router(proxmox_router, prefix="/proxmox", tags=["proxmox"])
router.include_router(terraform_router, prefix="/terraform", tags=["terraform"])
