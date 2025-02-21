import shutil
import subprocess
import time
from pathlib import Path

from services.db import get_projects, add_deployment_time, delete_project
from services.email import send_message
from settings import MODULES_FILE, TERRAFORM_DIR, TEMPLATE_MODULE_DIR
from templates.terraform import MODULE_TEMPLATE, TERRAFORM_TEMPLATE, DEPLOYED_EMAIL


def generate_modules():
    has_new_project = False
    projects = get_projects()

    for project in projects:
        if Path(project["name"]).exists():
            continue
        shutil.copytree(TEMPLATE_MODULE_DIR, TERRAFORM_DIR / project["name"], dirs_exist_ok=True)
        has_new_project = True

    modules_list = "\n".join(MODULE_TEMPLATE.format(name=project["name"]) for project in projects)
    modules = TERRAFORM_TEMPLATE.format(modules=modules_list)

    with open(MODULES_FILE, "w") as file:
        file.write(modules)

    if has_new_project:
        subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR)


def deploy_project(name, email):
    try:
        add_deployment_time(name)
        if not get_projects():
            subprocess.run(["terraform", "apply", "-auto-approve", "-target=module.common"], cwd=TERRAFORM_DIR)

        subprocess.run(["terraform", "apply", "-auto-approve", f"-target=module.{name}"], cwd=TERRAFORM_DIR)
        time.sleep(30)
        subprocess.run(["ansible-playbook", "--become", "--become-user", "root", "--become-method", "sudo",
                        "-i", str(Path(name, "hosts")), "web-server.yml"],
                       cwd=TERRAFORM_DIR, env={"ANSIBLE_HOST_KEY_CHECKING": "False"})
        # send_message(f"Проект {name} успешно развернут!", DEPLOYED_EMAIL.format(name=name), email)
    except Exception as e:
        print("Fall with error", e)
        destroy_project(name)


def destroy_project(name):
    subprocess.run(["terraform", "destroy", "-auto-approve", f"-target=module.{name}"], cwd=TERRAFORM_DIR)
    shutil.rmtree(TERRAFORM_DIR / name)
    delete_project(name)
    generate_modules()

    if not get_projects():
        subprocess.run(["terraform", "destroy", "-auto-approve", "-target=module.common"], cwd=TERRAFORM_DIR)
