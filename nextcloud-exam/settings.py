from os import getenv
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PROJECTS_FILE = Path(getenv("PROJECTS_FILE", "projects.json"))

TERRAFORM_DIR = Path(getenv("TERRAFORM_DIR", "terraform"))
TEMPLATE_MODULE_DIR = TERRAFORM_DIR / "nextcloud"
MODULES_FILE = TERRAFORM_DIR / "modules.tf"

MAIL_SERVER = getenv("MAIL_SERVER", "smtp.mail.ru")
MAIL_PORT = int(getenv("MAIL_PORT", 465))
MAIL_USERNAME = getenv("MAIL_USERNAME")
MAIL_PASSWORD = getenv("MAIL_PASSWORD")
MAIL_USE_SSL = getenv("MAIL_USE_SSL", "True").lower() == "true"
MAIL_DEFAULT_SENDER = getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
