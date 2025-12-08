---
title: How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication
titleSuffix: Azure OpenAI
description: Provides guidance on how to set managed identity with Microsoft Entra ID
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to 
ms.date: 11/26/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom: devx-track-azurecli
---

# How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

More complex security scenarios require Azure role-based access control (Azure RBAC). This document covers how to authenticate to your Azure OpenAI resource using Microsoft Entra ID.

In the following sections, you'll use the Azure CLI to sign in, and obtain a bearer token to call the OpenAI resource. If you get stuck, links are provided in each section with all available options for each command in Azure Cloud Shell/Azure CLI.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

- [Custom subdomain names are required to enable features like Microsoft Entra ID for authentication.](
../../../ai-services/cognitive-services-custom-subdomains.md)

- Azure CLI - [Installation Guide](/cli/azure/install-azure-cli)
- The following Python libraries: os, requests, json, openai, azure-identity

## Assign role

Assign yourself either the [Cognitive Services OpenAI User](role-based-access-control.md#cognitive-services-openai-user) or [Cognitive Services OpenAI Contributor](role-based-access-control.md#cognitive-services-openai-contributor) role to allow you to use your account to make Azure OpenAI inference API calls rather than having to use key-based auth. After you make this change it can take up to 5 minutes before the change takes effect.

## Sign into the Azure CLI

To sign-in to the Azure CLI, run the following command and complete the sign-in. You might need to do it again if your session has been idle for too long.

```azurecli
az login
```

## Chat Completions

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider
)

response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure services support this too?"}
    ]
)

print(response.choices[0].message.content)
```

## Querying Azure OpenAI with the control plane API

```python
import requests
import json
from azure.identity import DefaultAzureCredential

region = "eastus"
token_credential = DefaultAzureCredential()
subscriptionId = "{YOUR-SUBSCRIPTION-ID}" 


token = token_credential.get_token('https://management.azure.com/.default')
headers = {'Authorization': 'Bearer ' + token.token}

url = f"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{region}/models?api-version=2023-05-01"

response = requests.get(url, headers=headers)

data = json.loads(response.text)

print(json.dumps(data, indent=4))
```

## Authorize access to managed identities

OpenAI supports Microsoft Entra authentication with [managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview). Managed identities for Azure resources can authorize access to Azure OpenAI resources using Microsoft Entra credentials from applications running in Azure virtual machines (VMs), function apps, virtual machine scale sets, and other services. By using managed identities for Azure resources together with Microsoft Entra authentication, you can avoid storing credentials with your applications that run in the cloud.  

## Enable managed identities on a VM

Before you can use managed identities for Azure resources to authorize access to Azure OpenAI resources from your VM, you must enable managed identities for Azure resources on the VM. To learn how to enable managed identities for Azure Resources, see:

- [Azure portal](/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm)
- [Azure PowerShell](/azure/active-directory/managed-identities-azure-resources/qs-configure-powershell-windows-vm)
- [Azure CLI](/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm)
- [Azure Resource Manager template](/azure/active-directory/managed-identities-azure-resources/qs-configure-template-windows-vm)
- [Azure Resource Manager client libraries](/azure/active-directory/managed-identities-azure-resources/qs-configure-sdk-windows-vm)

For more information about managed identities, see [Managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview).
