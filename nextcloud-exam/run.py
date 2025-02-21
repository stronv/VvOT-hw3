import subprocess

from app import create_app
from settings import TERRAFORM_DIR

app = create_app()

if __name__ == "__main__":
    from services.db import init_db
    init_db()
    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR)
    app.run(host="0.0.0.0", debug=True)
