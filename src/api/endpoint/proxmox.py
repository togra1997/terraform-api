import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi import APIRouter
from proxmoxer import ProxmoxAPI

router = APIRouter(prefix="/proxmox", tags=["proxmox"])
load_dotenv()

# API_TOKEN_IDを分割（"user@realm!tokenname"）
api_token_id = os.getenv("API_TOKEN_ID", "")
if not api_token_id or "!" not in api_token_id:
    raise RuntimeError("API_TOKEN_ID must be set as 'user@realm!tokenname' in .env")
user, token_name = api_token_id.split("!", 1)


# PROXMOX_URL をパースして host/port を取得
proxmox_url = os.getenv("PROXMOX_URL", "")
parsed = urlparse(proxmox_url)
host = parsed.hostname
port = parsed.port or 8006


def get_vm_status(proxmox: ProxmoxAPI, vmid: int, node: str | None = None) -> dict:
    """
    指定した VMID の現在の電源状態などを取得する。
    戻り値の例: {'status': 'running', 'uptime': 1234, ...}
    """
    return proxmox.nodes(node).qemu(vmid).status.current.get()


@router.get("/info")
def get_proxmox_data():
    proxmox = ProxmoxAPI(
        host,
        user=user,
        token_name=token_name,
        token_value=os.getenv("API_TOKEN_SECRET"),
        port=port,
        verify_ssl=False,
    )
    node_name = os.getenv("NODE", "togura")
    vms = proxmox.nodes(node_name).qemu.get()
    return sorted(vms, key=lambda x: x["vmid"])
