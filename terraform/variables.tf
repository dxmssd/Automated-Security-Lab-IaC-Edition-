variable "admin_username" {
  description = "Admin User VM"
  type = string
  default = "azureuser"
}

variable "admin_password" {
  description = "password vm"
  type = string
  sensitive = true #prevents the value from being printed in logs
}
