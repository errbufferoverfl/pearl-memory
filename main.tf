# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.0.0"
    }
  }
}

variable "name" {
  type = string
  default = "pearl-memory"
  description = "The name you want to use to name services and regions."
}

variable "region" {
  type = string
  default = "australiaeast"
  description = "The region you want all the resources configured in."
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = format("rg-%s-prod-001", var.name)
  location = var.region
}

resource "azurerm_cognitive_account" "az-speech-cog" {
  name                = format("cog-%s-speech-prod-001", var.name)
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "SpeechServices"
  // If you already have a S0 service configured you'll need to set this to S1
  sku_name = "F0"
}

resource "azurerm_cognitive_account" "az-translate-cog" {
  name                = format("cog-%s-translator-prod-001", var.name)
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "TextTranslation"
  // If you already have a F0 service configured you'll need to set this to S1
  sku_name = "F0"
}

// Bing.Search.v7 APIs haven't been correctly migrated for Terraform use yet
// so you will need to manually create this asset.
// See for more info: https://github.com/terraform-providers/terraform-provider-azurerm/issues/9102
//resource "azurerm_cognitive_account" "az-search-cog" {
//  name                = format("cog-%s-search-prod-001", var.name)
//  location            = "global"
//  resource_group_name = azurerm_resource_group.rg.name
//  kind                = "Bing.Search.v7"
//  sku_name = "F0"
//}
output "az-speech-cog-key" {
  value       = azurerm_cognitive_account.az-speech-cog.primary_access_key
  description = "The access key for accessing the Speech Cognitive Service."
  sensitive   = true
}

output "az-translate-cog-key" {
  value       = azurerm_cognitive_account.az-translate-cog.primary_access_key
  description = "The access key for accessing the Translate Cognitive Service."
  sensitive   = true
}

