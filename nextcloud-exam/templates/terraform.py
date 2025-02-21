TERRAFORM_TEMPLATE = """module "common" {{
  source = "./common"
  zone   = var.zone
}}

{modules}
"""

MODULE_TEMPLATE = """module "{name}" {{
  source        = "./{name}"
  name          = "{name}"
  subnet_id     = module.common.subnet_id
  boot_disk_id  = module.common.boot_disk_id
  dns_zone_id   = module.common.dns_zone_id
  dns_zone_name = module.common.dns_zone_name
}}
"""

DEPLOYED_EMAIL = """<b>Проект {name} был развернут и доступен по адресу https://{name}.vvot37.itiscl.ru/</b>

Для создания административного аккаунта используйте следующие данные:
- Учётная запись базы данных: <b>dbuser</b>
- Пароль базы данных: <b>dbpassword</b>
- Имя базы данных: <b>dbnextcloud</b>
- Хост базы данных: <b>localhost:5432</b>
"""
