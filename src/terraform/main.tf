terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = ">= 0.50.0"
    }
  }
}

provider "proxmox" {
  endpoint  = var.pm_api_url
  api_token = "${var.pm_api_token_id}=${var.pm_api_token_secret}"
  insecure  = true
}

# 複数のVMを定義する変数
variable "vms" {
  description = "複数のVMの設定"
  type = map(object({
    vm_id       = number
    vm_name     = string
    storage     = string
    memory_mb   = number
    disk_gb     = number
    vm_ip       = string
    started     = optional(bool, false)  # VM毎の起動設定（デフォルト: false）
  }))
  default = {}
}

# 共通変数
variable "pm_api_url" {}
variable "pm_api_token_id" {}
variable "pm_api_token_secret" {}
variable "pm_node" {}
variable "template_id" {
  description = "テンプレートVMのID（VMID）"
  type        = number
}
variable "network_bridge" {}
variable "vm_gw" {}
variable "vm_started" {
  description = "VMを作成時に起動するかどうか"
  type        = bool
  default     = false
}

# for_eachを使用して複数のVMを作成
resource "proxmox_virtual_environment_vm" "cloudinit_vms" {
  for_each = var.vms

  name      = each.value.vm_name
  node_name = var.pm_node
  vm_id     = each.value.vm_id
  started   = each.value.started  # VM毎の設定を使用
  stop_on_destroy = true   # Terraform destroy時にVMを停止してから削除
  on_boot         = false  # ホストの起動時にVMを自動起動しない

  clone {
    vm_id = var.template_id
  }

  cpu {
    cores = 2
  }
  memory {
    dedicated = each.value.memory_mb
  }
  disk {
    datastore_id = each.value.storage
    size         = each.value.disk_gb
    interface    = "scsi0"
  }
  network_device {
    bridge = var.network_bridge
    model  = "virtio"
  }
}
