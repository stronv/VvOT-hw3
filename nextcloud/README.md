# Nextcloud

## Требования для запуска

* [Terraform](https://www.terraform.io/) 
* [Ansible](https://docs.ansible.com/)

## Запуск проекта

1. Инициализировать терраформа — `terraform init` 
2. Поднять инфраструктуру с виртуальной машиной — `terraform apply`
3. Установить Nextcloud на виртуальную машину — `ansible-playbook --become --become-user root --become-method sudo -i hosts web-server.yml`
