import json
from datetime import datetime

from settings import PROJECTS_FILE


def init_db():
    with open(PROJECTS_FILE, "w") as db:
        json.dump({
            "projects": [],
        }, db)


def add_project(name, email):
    with open(PROJECTS_FILE, "r") as db:
        data = json.load(db)

    data["projects"].append({
        "name": name,
        "email": email,
        "deployed_at": None,
    })

    with open(PROJECTS_FILE, "w") as db:
        json.dump(data, db)


def delete_project(name):
    with open(PROJECTS_FILE, "r") as db:
        data = json.load(db)

    for project in data["projects"]:
        if project["name"] == name:
            data["projects"].remove(project)
            break

    with open(PROJECTS_FILE, "w") as db:
        json.dump(data, db)


def get_project(name):
    with open(PROJECTS_FILE, "r") as db:
        data = json.load(db)

    for project in data["projects"]:
        if project["name"] == name:
            return project

    return None


def get_projects():
    with open(PROJECTS_FILE, "r") as db:
        data = json.load(db)

    return data["projects"]


def add_deployment_time(name):
    with open(PROJECTS_FILE, "r") as db:
        data = json.load(db)

    for project in data["projects"]:
        if project["name"] == name:
            project["deployed_at"] = datetime.now().isoformat()
            break

    with open(PROJECTS_FILE, "w") as db:
        json.dump(data, db)
