import re
from datetime import datetime, timedelta

from flask import render_template, request, redirect, url_for, Blueprint

from services.db import get_project
from services.projects import create_project

deployer = Blueprint("deployer", __name__)


@deployer.route("/", methods=["GET", "POST"])
def index():
    name, email, error = "", "", ""

    if request.method == "POST":
        name_valid, email_valid = True, True

        name = request.form["name"]
        if not re.fullmatch(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$", name):
            name_valid = False

        email = request.form["email"]
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            email_valid = False

        if not name_valid and not email_valid:
            error = "Указаны некорректные имя проекта и почта"
        elif not name_valid:
            error = "Указано некорректное имя проекта"
        elif not email_valid:
            error = "Указана некорректная почта"
        elif get_project(name):
            error = "Проект с таким именем уже существует"

        if not error:
            create_project(name, email)
            return redirect(url_for("deployer.status", name=name))

    return render_template("index.html", name=name, email=email, error=error)


@deployer.route("/project-status")
def status():
    name = request.args.get("name")
    project = get_project(name)
    if not project:
        return render_template("status.html", error="Проект не найден")

    deleted_at = None
    if project["deployed_at"]:
        deleted_at = (datetime.fromisoformat(project["deployed_at"]) + timedelta(minutes=40)).strftime("%H:%M:%S %d.%m.%Y")
    return render_template("status.html", project=project, deleted_at=deleted_at)
