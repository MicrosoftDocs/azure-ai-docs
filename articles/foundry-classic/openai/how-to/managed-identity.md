---
title: "How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication (classic)"
description: "Authenticate to Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID by using your developer identity or a managed identity (classic)."
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to 
ms.date: 08/04/2026
author: alvinashcraft
ms.author: aashcraft
recommendations: false
ms.custom:
  - devx-track-azurecli
  - doc-kit-assisted
ai-usage: ai-assisted
---

# How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Microsoft Entra ID lets you call your Azure OpenAI resource without storing an API key in your application. Instead of a key, your code requests a short-lived access token for an identity that you grant a role on the resource. This article shows you how to authenticate two ways: as yourself during local development, and as a managed identity when your app runs in Azure.

## Entra ID authentication compared to managed identities

These two terms are often used interchangeably, but they describe different things.

**Microsoft Entra ID** is the identity platform. Every token-based call to Azure OpenAI goes through it, no matter which identity you use.

**A managed identity** is one kind of Entra identity. Azure creates it, assigns it to an Azure resource such as a virtual machine or web app, and rotates its credentials for you. There's no secret for you to store or rotate.

The identity you authenticate with depends on where your code runs:

| Identity | Where it's used | Secret to manage |
| --- | --- | --- |
| **Your developer account** | Your local machine, after you run `az login` | None. The Azure CLI holds the session. |
| **System-assigned managed identity** | An Azure resource, tied to that resource's lifecycle | None. Azure manages it. |
| **User-assigned managed identity** | Multiple Azure resources that share one identity | None. Azure manages it. |
| **Service principal** | CI/CD pipelines and non-Azure hosts | A client secret or certificate that you rotate |

Use a system-assigned managed identity when a single resource needs access. Use a user-assigned managed identity when several resources need the same access, or when you want to grant the role before you create the resource that uses it.

You don't have to write different code for each of these. The `DefaultAzureCredential` class in the Azure Identity library tries a chain of credentials in order and uses the first one it finds. On your laptop, it picks up your `az login` session. On an Azure host, it picks up the managed identity. That's why the same sample works in both places, and it's why this article covers both.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

- An Azure OpenAI resource with a [custom subdomain name](../../../ai-services/cognitive-services-custom-subdomains.md). You need a custom subdomain for Microsoft Entra ID authentication.

- A model deployed to your resource.

- Azure CLI - [Installation Guide](/cli/azure/install-azure-cli)

- Python 3.8 or later, with the following packages installed:

    ```console
    pip install openai azure-identity
    ```

## Assign a role

Role assignments control who can call your resource. Assign yourself either the [Cognitive Services OpenAI User](role-based-access-control.md#cognitive-services-openai-user) or [Cognitive Services OpenAI Contributor](role-based-access-control.md#cognitive-services-openai-contributor) role on the Azure OpenAI resource. Either role lets you make inference API calls with your own identity instead of a key.

Assign the same role to your app's managed identity later, when you deploy to Azure.

> [!IMPORTANT]
> Role assignments can take up to five minutes to take effect. If you get a `403` error right after you assign a role, wait and try again before you troubleshoot anything else.

## Authenticate from your development machine

On your local machine, `DefaultAzureCredential` uses your Azure CLI session. Sign in first. You might need to sign in again if your session is idle for too long.

```azurecli
az login
```

If you belong to more than one tenant, sign in to the tenant that holds your Azure OpenAI resource:

```azurecli
az login --tenant YOUR-TENANT-ID
```

Now call your model. This sample requests a token, then sends a chat completions request.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

response = client.chat.completions.create(
    model="gpt-4o",  # Use your deployment name, which might differ from the model name.
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure services support this too?"}
    ]
)

print(response.choices[0].message.content)
```

### Why the sample passes a token to `api_key`

The `api_key` parameter looks out of place in a keyless sample, and it's the most common point of confusion in this workflow. Here's what's happening.

The `api_key` parameter accepts either a string or a callable. When you pass the `token_provider` callable, the client invokes it before each request to get a current Microsoft Entra access token, then sends that token as a bearer token in the `Authorization` header. No API key is created, stored, or transmitted. The parameter keeps the name `api_key` for compatibility with the OpenAI client library, which uses one parameter for both authentication styles.

The `get_bearer_token_provider` function handles token caching and refresh for you, so you don't need to track token expiry yourself.

### Verify your access

To confirm the role assignment works before you run any code, request a token and call the API directly. This method also provides the clearest way to see the `Authorization` header that the client library sets for you.

```bash
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken --output tsv)

curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Authenticate from an Azure-hosted app by using a managed identity

When your code runs on an Azure virtual machine, web app, function app, container app, or virtual machine scale set, use a managed identity instead of your developer account. Your app never stores a credential, and Azure rotates the identity for you.

### Enable and assign the identity

1. Enable a managed identity on the Azure resource that hosts your app. For a virtual machine, see the quickstart for your preferred tool: [Azure portal](/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm), [Azure PowerShell](/azure/active-directory/managed-identities-azure-resources/qs-configure-powershell-windows-vm), [Azure CLI](/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm), [Azure Resource Manager template](/azure/active-directory/managed-identities-azure-resources/qs-configure-template-windows-vm), or [Azure Resource Manager client libraries](/azure/active-directory/managed-identities-azure-resources/qs-configure-sdk-windows-vm).

1. Assign the managed identity the **Cognitive Services OpenAI User** role on your Azure OpenAI resource, the same way you did for your own account in [Assign a role](#assign-a-role).

### Use a system-assigned managed identity

If the host has only a system-assigned managed identity, the sample from [Authenticate from your development machine](#authenticate-from-your-development-machine) works without any changes. `DefaultAzureCredential` finds the managed identity automatically when it runs in Azure.

### Use a user-assigned managed identity

A host can have several identities assigned to it, so you have to say which one to use. Pass the client ID of the user-assigned managed identity:

```python
from openai import OpenAI
from azure.identity import ManagedIdentityCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    ManagedIdentityCredential(client_id="YOUR-USER-ASSIGNED-CLIENT-ID"),
    "https://ai.azure.com/.default",
)

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
```

To keep using `DefaultAzureCredential` so the same code still runs locally, set the `AZURE_CLIENT_ID` environment variable on the Azure host to the client ID of the user-assigned managed identity. `DefaultAzureCredential` reads that variable and selects the matching identity.

For more information, see [Managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview).

## Call the control plane API

The previous examples call the *data plane*, which is where you run inference. Management operations, such as listing the models available in a region, use the *control plane*. The control plane is a different API with a different token audience: `https://management.azure.com/.default` instead of `https://ai.azure.com/.default`. A token issued for one audience doesn't work with the other.

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

Control plane calls need a role that grants management permissions, such as **Cognitive Services Contributor**. The inference roles in [Assign a role](#assign-a-role) don't grant control plane access.

## Troubleshoot authentication errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` | The resource doesn't have a custom subdomain, so it can't accept Entra tokens. | Configure a [custom subdomain](../../../ai-services/cognitive-services-custom-subdomains.md) and use the `https://YOUR-RESOURCE-NAME.openai.azure.com` endpoint rather than the regional endpoint. |
| `403 Forbidden` or `PermissionDenied` | The identity has no role on the resource, or the assignment hasn't propagated. | Confirm the role assignment is on the Azure OpenAI resource, then wait up to five minutes and retry. |
| `DefaultAzureCredential failed to retrieve a token` | You aren't signed in locally, or you're signed in to the wrong tenant. | Run `az login --tenant YOUR-TENANT-ID`. |
| Works locally, fails after you deploy | The managed identity isn't enabled, or the role was assigned to your user account rather than the identity. | Enable the managed identity on the host and assign it the role. |
| Works locally, fails in Azure with a user-assigned identity | The host has multiple identities and none was specified. | Pass the client ID, or set `AZURE_CLIENT_ID` on the host. |
| `404 Not Found` on a valid endpoint | The `model` value doesn't match a deployment name. | Use your deployment name, which can differ from the model name. |

## Related content

- [Role-based access control for Azure OpenAI](role-based-access-control.md)
- [Custom subdomain names for Azure AI services](../../../ai-services/cognitive-services-custom-subdomains.md)
- [Managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview)
- [DefaultAzureCredential in the Azure Identity library for Python](/python/api/overview/azure/identity-readme#defaultazurecredential)
