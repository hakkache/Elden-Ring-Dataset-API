# Simple Azure App Service Deployment Script
# Run this in Azure Cloud Shell or local Azure CLI

# Variables
$resourceGroup = "rg-eldenring-api"
$location = "East US"
$appServicePlan = "asp-eldenring-api"
$webAppName = "eldenring-api-webapp"

# Create Resource Group
az group create --name $resourceGroup --location $location

# Create App Service Plan (Linux, Basic B1)
az appservice plan create `
  --name $appServicePlan `
  --resource-group $resourceGroup `
  --is-linux `
  --sku B1

# Create Web App
az webapp create `
  --resource-group $resourceGroup `
  --plan $appServicePlan `
  --name $webAppName `
  --runtime "PYTHON:3.11" `
  --deployment-source-url https://github.com/hakkache/Elden-Ring-Dataset-API.git `
  --deployment-source-branch main

# Configure App Settings
az webapp config appsettings set `
  --resource-group $resourceGroup `
  --name $webAppName `
  --settings DATA_DIR="/home/site/wwwroot/data" `
             SECRET_KEY="your-production-secret-key-change-this" `
             SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Set startup command
az webapp config set `
  --resource-group $resourceGroup `
  --name $webAppName `
  --startup-file "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Get the URL
$webAppUrl = az webapp show --resource-group $resourceGroup --name $webAppName --query "hostNames[0]" --output tsv

Write-Host "Deployment completed!"
Write-Host "Web App URL: https://$webAppUrl"
Write-Host "API Documentation: https://$webAppUrl/docs"
Write-Host ""
Write-Host "Test your API:"
Write-Host "curl -X POST 'https://$webAppUrl/token' -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=admin&password=password123'"