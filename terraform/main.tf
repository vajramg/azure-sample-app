terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "my-rg"
    storage_account_name = "my1988vg"
    container_name       = "mycontainer"
    key                  = "terraform.tfstate"
  }

}


provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

module "aks" {
  source              = "./modules/aks"
  resource_group_name = var.resource_group_name
  location            = var.location
  subscription_id     = var.subscription_id
}


module "acr" {
  source              = "./modules/acr"
  resource_group_name = var.resource_group_name
  location            = var.location
  subscription_id     = var.subscription_id
}

resource "azurerm_role_assignment" "role" {
  principal_id                     = module.aks.kubelet_object_id
  scope                            = module.acr.acr_id
  skip_service_principal_aad_check = true
  role_definition_name             = "AcrPull"
}

module "keyvault" {
  source              = "./modules/keyvault"
  resource_group_name = var.resource_group_name
  location            = var.location
  subscription_id     = var.subscription_id
}
