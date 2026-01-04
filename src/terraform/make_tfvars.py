import os
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from src.utils.load_env import load_env


@dataclass
class TfvarsGenerator:
    template_folder_path: Path | str
    template_file_name: Path | str = "template.tfvars.j2"
    output_file_name: Path | str = "terraform.tfvars"

    def _read_template(self) -> Template:
        # テンプレートディレクトリを指定
        template_dir = Environment(loader=FileSystemLoader(self.template_folder_path))
        # テンプレートファイルを読み込む
        self.template = template_dir.get_template(self.template_file_name)

    @load_env
    def _render_template(self, profiles: list):
        proxmox_url = os.getenv("PROXMOX_URL")
        api_token_id = os.getenv("API_TOKEN_ID")
        api_token_secret = os.getenv("API_TOKEN_SECRET")
        node = os.getenv("NODE")
        template_id = os.getenv("TEMPLATE_ID")
        network_bridge = os.getenv("NETWORK_BRIDGE")
        vm_gw = os.getenv("VM_GW")

        # データを埋め込んでレンダリング
        output = self.template.render(
            proxmox_url=proxmox_url,
            api_token_id=api_token_id,
            api_token_secret=api_token_secret,
            node=node,
            template_id=template_id,
            network_bridge=network_bridge,
            vm_gw=vm_gw,
            profiles=profiles,
        )
        self.output = output

    def save(self, profiles: list, output_folder: Path | str = Path("./src/terraform")):
        if not isinstance(output_folder, Path):
            output_folder = Path(output_folder)
        self._read_template()
        self._render_template(profiles)
        if not output_folder.exists():
            output_folder.mkdir(parents=True, exist_ok=True)
        with open(output_folder / "terraform.tfvars", "w") as f:
            f.write(self.output)


if __name__ == "__main__":
    generator = TfvarsGenerator("templates")
    generator.save(
        profiles=[
            {
                "profile": "minecraft",
                "vm_id": 150,
                "name": "minecraft",
                "storage": "local-lvm",
                "memory": 16384,
                "disk": 500,
                "started": False,
            },
        ],
        output_folder=Path("."),
    )
