from fastapi import APIRouter

from src.api.shema.profiles import AddProfile, DeleteProfile
from src.databaes.db import Database
from src.terraform.make_tfvars import TfvarsGenerator
from src.terraform.terraform import terraform_run

router = APIRouter(prefix="/terraform")
db = Database("./src/database/save.csv")
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
    tfvars_generator.save(profile)
    terraform_run()


@router.get("/info")
def get_info():
    return db.get()
