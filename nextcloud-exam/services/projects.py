from datetime import datetime, timedelta
from uuid import uuid4

from app import scheduler
from services.db import add_project
from services.terraform import generate_modules, deploy_project, destroy_project


def create_project(name, email):
    add_project(name, email)
    generate_modules()
    scheduler.add_job(uuid4().hex, deploy_project, run_date=datetime.now(), args=[name, email])
    scheduler.add_job(uuid4().hex, destroy_project, run_date=datetime.now() + timedelta(minutes=40), args=[name])
