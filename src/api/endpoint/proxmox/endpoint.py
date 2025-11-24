import os

from fastapi import APIRouter

from src.api.endpoint.proxmox import func as fc

router = APIRouter(prefix="/proxmox", tags=["proxmox"])


@router.get("/info")
def get_proxmox_data():
    node_name = os.getenv("NODE", "togura")
    vms = fc.proxmox.nodes(node_name).qemu.get()
    vms = fc.format(vms)
    return sorted(vms, key=lambda x: x["vmid"])


@router.get("/start")
def start_vm(vmid: int):
    node_name = os.getenv("NODE", "togura")
    fc.proxmox.nodes(node_name).qemu(vmid).status.start.post()
    return {"message": f"VM {vmid} is starting."}


@router.get("/stop")
def stop_vm(vmid: int):
    node_name = os.getenv("NODE", "togura")
    fc.proxmox.nodes(node_name).qemu(vmid).status.stop.post()
    return {"message": f"VM {vmid} is stopping."}
