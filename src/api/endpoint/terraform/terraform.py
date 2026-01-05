from fastapi import APIRouter, HTTPException
from loguru import logger

from src.api.shema.profiles import AddProfile, DeleteProfile
from src.database.db import Database
from src.terraform.make_tfvars import TfvarsGenerator
from src.terraform.terraform import terraform_run

terraform_router = APIRouter(tags=["terraform"])
db = Database("./src/database/save.csv")
tfvars_generator = TfvarsGenerator("src/terraform/templates")


@terraform_router.post("/add")
def add_profile(profile: AddProfile):
    try:
        logger.info(profile)
        db.add(profile.get())
        db.save()
        return profile
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e))


@terraform_router.delete("/delete")
def delete_profile(profile: DeleteProfile):
    try:
        db.delete(profile.id)
        db.save()
        return profile
    except Exception as e:
        return {"error": str(e)}


@terraform_router.get("/run")
def run_profile():
    profile = db.get()
    tfvars_generator.save(profile)
    terraform_run()


@terraform_router.get("/info")
def get_info():
    return db.get()
