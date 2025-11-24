import os
import re  # 正規表現モジュールをインポート
from urllib.parse import urlparse

from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI

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

proxmox = ProxmoxAPI(
    host,
    user=user,
    token_name=token_name,
    token_value=os.getenv("API_TOKEN_SECRET"),
    port=port,
    verify_ssl=False,
)


def get_vm_ip(vmid: int) -> str:
    """
    指定した VMID の IPv4 アドレスを取得する。
    """
    proxmox = ProxmoxAPI(
        host,
        user=user,
        token_name=token_name,
        token_value=os.getenv("API_TOKEN_SECRET"),
        port=port,
        verify_ssl=False,
    )
    node_name = os.getenv("NODE", "togura")

    # VM のネットワーク情報を取得
    vm_status = (
        proxmox.nodes(node_name).qemu(vmid).agent("network-get-interfaces").get()
    )

    ip_addresses = []
    ipv4_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")  # IPv4 の正規表現
    for interface in vm_status.get("result", []):
        for ip_info in interface.get("ip-addresses", []):
            ip_address = ip_info.get("ip-address")
            if (
                ip_address
                and ip_address != "127.0.0.1"
                and ipv4_pattern.match(ip_address)
                and not ip_address.startswith("172.")
            ):
                ip_addresses.append(ip_address)

    if not ip_addresses:
        return {"message": f"No IPv4 address found for VM {vmid}."}

    return ip_addresses[0]


def format(vms: dict) -> list[dict]:
    returns = []
    for vm in vms:
        vmid = vm.get("vmid", "")

        if vmid not in [1000]:
            name = vm.get("name", "")
            status = vm.get("status", "")
            try:
                ip = get_vm_ip(vmid)
            except Exception:
                ip = "vm is not running"

            returns.append({"name": name, "vmid": vmid, "status": status, "ip": ip})

    return returns
