# Azure Deployment Script for Elden Ring API
# Run this in Azure Cloud Shell or local Azure CLI

# Variables
$resourceGroup = "rg-eldenring-api"
$location = "East US"
$acrName = "acreldenringapi"
$containerAppName = "eldenring-api"
$environmentName = "env-eldenring-api"

# Login to Azure
az login

# Create Resource Group
az group create --name $resourceGroup --location $location

# Create Azure Container Registry
az acr create --resource-group $resourceGroup --name $acrName --sku Basic --admin-enabled true

# Get ACR credentials for GitHub secrets
az acr credential show --name $acrName

# Create Container Apps Environment
az containerapp env create `
  --name $environmentName `
  --resource-group $resourceGroup `
  --location $location

# Create Container App
az containerapp create `
  --name $containerAppName `
  --resource-group $resourceGroup `
  --environment $environmentName `
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest `
  --target-port 8000 `
  --ingress external `
  --env-vars "DATA_DIR=/app/data" "SECRET_KEY=your-production-secret-key"

Write-Host "Azure resources created successfully!"
Write-Host "Resource Group: $resourceGroup"
Write-Host "Container Registry: $acrName.azurecr.io"
Write-Host "Container App: $containerAppName"

Write-Host "`nNext steps:"
Write-Host "1. Add these secrets to your GitHub repository:"
Write-Host "   - ACR_LOGIN_SERVER: $acrName.azurecr.io"
Write-Host "   - ACR_NAME: $acrName"
Write-Host "   - ACR_USERNAME: (from az acr credential show output)"
Write-Host "   - ACR_PASSWORD: (from az acr credential show output)"
Write-Host "   - AZURE_RG: $resourceGroup"
Write-Host "   - API_SECRET_KEY: (generate a strong secret key)"
Write-Host "2. Push to GitHub to trigger deployment"