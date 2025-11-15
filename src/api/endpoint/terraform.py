from fastapi import APIRouter

from src.api.shema.profiles import AddProfile, DeleteProfile
from src.db import Database
from src.terraform.make_tfvars import TfvarsGenerator

router = APIRouter(prefix="/terraform")
db = Database("db/save.csv")
tfvars_generator = TfvarsGenerator("src/terraform/templates")


@router.post("/add")
def add_profile(profile: AddProfile):
    try:
        print(profile)
        db.add(profile.get())
        db.save()
        return profile
    except Exception as e:
        return {"error": str(e)}


@router.delete("/delete")
def delete_profile(profile: DeleteProfile):
    try:
        db.delete(profile.id)
        db.save()
        return profile
    except Exception as e:
        return {"error": str(e)}


@router.get("/run")
def run_profile():
    profile = db.get()
    output_path = "output"
    tfvars_generator.save(output_path, profile)
