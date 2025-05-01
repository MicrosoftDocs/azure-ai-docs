---
title: Securely store access credentials
titleSuffix: Azure Data Science Virtual Machine 
description: Learn how to securely store access credentials on the Data Science Virtual Machine. You'll learn how to use managed service identities and Azure Key Vault to store access credentials.
keywords: deep learning, AI, data science tools, data science virtual machine, geospatial analytics, team data science process
services: machine-learning
ms.service: azure-data-science-virtual-machines
ms.custom: devx-track-azurecli, devx-track-python

author: fbsolo-ms1
ms.author: franksolomon 
ms.topic: conceptual
ms.reviewer: vijetaj
ms.date: 04/16/2024
---

# Store access credentials securely on an Azure Data Science Virtual Machine

Cloud application code often contains credentials to authenticate to cloud services. Management and security of these credentials is a well-known challenge as we build cloud applications. Ideally, credentials should never appear on developer workstations. We should never check in credentials to source control.

The [managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview) feature helps solve the problem. It gives Azure services an automatically managed identity in Microsoft Entra ID. You can use this identity to authenticate to any service that supports Microsoft Entra authentication. Additionally, this identity avoids placement of any embedded credentials in your code.

To secure credentials, use Windows Installer (MSI) in combination with [Azure Key Vault](/azure/key-vault/). Azure Key Vault is a managed Azure service that securely stores secrets and cryptographic keys. You can access a key vault by using the managed identity and then retrieve the authorized secrets and cryptographic keys from the key vault.

The documentation about Key Vault and managed identities for Azure resources forms a comprehensive resource for in-depth information about these services. This article walks through the basic use of MSI and Key Vault on the Data Science Virtual Machine (DSVM) to access Azure resources.

## Create a managed identity on the DSVM

```azurecli-interactive
# Prerequisite: You already created a Data Science VM in the usual way.

# Create an identity principal for the VM.
az vm assign-identity -g <Resource Group Name> -n <Name of the VM>
# Get the principal ID of the DSVM.
az resource list -n <Name of the VM> --query [*].identity.principalId --out tsv
```

## Assign Key Vault access permissions to a VM principal

```azurecli-interactive
# Prerequisite: You already created an empty Key Vault resource on Azure through use of the Azure portal or Azure CLI.

# Assign only get and set permissions but not the capability to list the keys.
az keyvault set-policy --object-id <Principal ID of the DSVM from previous step> --name <Key Vault Name> -g <Resource Group of Key Vault>  --secret-permissions get set
```

## Access a secret in the key vault from the DSVM

```bash
# Get the access token for the VM.
x=`curl http://localhost:50342/oauth2/token --data "resource=https://vault.azure.net" -H Metadata:true`
token=`echo $x | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])"`

# Access the key vault by using the access token.
curl https://<Vault Name>.vault.azure.net/secrets/SQLPasswd?api-version=2016-10-01 -H "Authorization: Bearer $token"
```

## Access storage keys from the DSVM

```bash
# Prerequisite: You granted your VMs MSI access to use storage account access keys, based on instructions at https://learn.microsoft.com/azure/active-directory/managed-service-identity/tutorial-linux-vm-access-storage. This article describes the process in more detail.

y=`curl http://localhost:50342/oauth2/token --data "resource=https://management.azure.com/" -H Metadata:true`
ytoken=`echo $y | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])"`
curl https://management.azure.com/subscriptions/<SubscriptionID>/resourceGroups/<ResourceGroup of Storage account>/providers/Microsoft.Storage/storageAccounts/<Storage Account Name>/listKeys?api-version=2016-12-01 --request POST -d "" -H "Authorization: Bearer $ytoken"

# Now you can access the data in the storage account from the retrieved storage account keys.
```

## Access the key vault from Python

```python
from azure.keyvault import KeyVaultClient
from msrestazure.azure_active_directory import MSIAuthentication

"""MSI Authentication example."""

# Get credentials.
credentials = MSIAuthentication(
    resource='https://vault.azure.net'
)

# Create a Key Vault client.
key_vault_client = KeyVaultClient(
    credentials
)

key_vault_uri = "https://<key Vault Name>.vault.azure.net/"

secret = key_vault_client.get_secret(
    key_vault_uri,  # Your key vault URL.
    # The name of your secret that already exists in the key vault.
    "SQLPasswd",
    ""              # The version of the secret; empty string for latest.
)
print("My secret value is {}".format(secret.value))
```

## Access the key vault from Azure CLI

```azurecli-interactive
# With managed identities for Azure resources set up on the DSVM, users on the DSVM can use Azure CLI to perform the authorized functions. The following commands enable access to the key vault from Azure CLI, without a required Azure account login.
# Prerequisites: MSI is already set up on the DSVM, as indicated earlier. Specific permissions, like accessing storage account keys, reading specific secrets, and writing new secrets, are provided to the MSI.

# Authenticate to Azure CLI without a required Azure account. 
az login --msi

# Retrieve a secret from the key vault. 
az keyvault secret show --vault-name <Vault Name> --name SQLPasswd

# Create a new secret in the key vault.
az keyvault secret set --name MySecret --vault-name <Vault Name> --value "Helloworld"

# List access keys for the storage account.
az storage account keys list -g <Storage Account Resource Group> -n <Storage Account Name>
```