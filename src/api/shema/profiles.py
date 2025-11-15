from pydantic import BaseModel


class AddProfile(BaseModel):
    profile: str
    vm_id: int
    name: str
    storage: str
    memory: int
    disk: int
    ip: str
    started: bool

    def get(self) -> dict:
        return {
            "profile": self.profile,
            "vm_id": self.vm_id,
            "name": self.name,
            "storage": self.storage,
            "memory": self.memory,
            "disk": self.disk,
            "ip": self.ip,
            "started": self.started,
        }


class DeleteProfile(BaseModel):
    id: int
