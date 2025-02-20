resource "yandex_vpc_network" "network" {
  name = "web-server-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name       = "web-server-subnet"
  zone       = var.zone
  v4_cidr_blocks = ["192.168.10.0/24"]
  network_id = yandex_vpc_network.network.id
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2404-lts-oslogin"
}

resource "yandex_compute_disk" "boot_disk" {
  name     = "web-server-boot-disk"
  type     = "network-ssd"
  image_id = data.yandex_compute_image.ubuntu.id
  size     = 10
}

resource "yandex_compute_instance" "server" {
  name        = "web-server"
  platform_id = "standard-v3"
  hostname    = "web"

  resources {
    core_fraction = 20
    cores         = 2
    memory        = 1
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot_disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

resource "local_file" "inventory" {
  content  = <<EOF
[web]
web-server ansible_host=${yandex_compute_instance.server.network_interface[0].nat_ip_address} ansible_user=ubuntu ansible_connection=ssh
EOF
  filename = "hosts"
}

output "nextcloud_url" {
  value = "http://${yandex_compute_instance.server.network_interface[0].nat_ip_address}/nextcloud"
}
