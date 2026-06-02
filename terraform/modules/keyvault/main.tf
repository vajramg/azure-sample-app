data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "vault" {
  name                        = "myvault1988"
  location                    = var.location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false




  sku_name = "standard"
access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id

    object_id = "a93a20fd-6971-4774-bef4-678b5ccdedb8"

    secret_permissions = [
      "Get",
      "List"
    ]
  }
}
