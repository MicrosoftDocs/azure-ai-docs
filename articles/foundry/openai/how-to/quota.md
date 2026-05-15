---
title: "Manage Azure OpenAI in Microsoft Foundry Models quota"
description: "Learn how to use Azure OpenAI to control your deployments rate limits."
author: alvinashcraft
ms.reviewer: shiyingfu
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 05/04/2026
ms.author: aashcraft
ms.custom: classic-and-new

#CustomerIntent: As a developer or AI practitioner, I want to understand how to manage Azure OpenAI deployment quotas in Microsoft Foundry so that I can control rate limits for my models.
---

# Manage Azure OpenAI in Microsoft Foundry Models quota

[!INCLUDE [quota 1](../includes/quota-1.md)]

## View and request quotas in Foundry portal

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../../includes/fdp-project-name.md)]s in the same subscription.

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
 
1. Projects help organize your work. The project you're working on appears in the upper-left corner. If you want to create a new project, select the project name, then **Create new project**.

1. Select **Operate** from the upper-right navigation.

1. Select **Quota** from the left pane to land on the **Quota** pane. The quota view has two tabs:

    - **Token per minute** — View and manage token-per-minute (TPM) quota allocations for standard deployments.
    - **Provisioned throughput unit** — View and manage provisioned throughput unit (PTU) allocations for provisioned deployments, including capacity estimation tools.

1. Select any of the deployments in the list to open its details pane on the right side. The details pane shows the deployment's current quota allocation, usage, and affiliated deployments.

1. On the deployment's details pane, go to the **Affiliated deployments using shared quota** section. Select the pencil icon in the **Actions** column of the table to edit quota allocation for the deployment and free up unused quota or increase allocation as needed.

1. Select the **Request quota** button in the upper-right corner to request increases in quota for the standard deployment type.

> [!NOTE]
> After you edit a quota allocation or submit a request, allow up to 15 minutes for changes to propagate. Refresh the **Quota** page to verify the updated allocation.

## Programmatically check quota and capacity

In addition to the [Foundry portal](https://ai.azure.com/resource/quota), you can use two Azure Resource Manager REST APIs to programmatically check your subscription's quota consumption and available model capacity.

### Choose the right API

| | **Usages API** | **Model Capacities API** |
|---|---|---|
| **Question it answers** | How much of my quota have I consumed vs. my limit? | How much deployable capacity is available for a specific model? |
| **Scope** | Subscription + location | Subscription (all locations at once) |
| **Input** | Location only | Model name, version, and format |
| **Returns** | Every quota line in that region — current usage and limit | Available capacity per location and deployment type for one model |
| **Typical use case** | Monitor consumption, trigger alerts when approaching limits | Pre-check capacity before creating or scaling a deployment |
| **API reference** | [Usages - List](/rest/api/aiservices/accountmanagement/usages/list) | [Model Capacities - List](/rest/api/aiservices/accountmanagement/model-capacities/list) |

Use the **Usages API** when you need a ledger view of what you've consumed and what's left. Use the **Model Capacities API** when you want to know where you _can_ deploy a model and how much capacity is available in each location.

> [!NOTE]
> Both APIs return information for all models associated with your subscription, including [retired models](../concepts/model-retirements.md) that are no longer available for new deployments.

### Usages API

The Usages API returns every quota line for a given region, including your current consumption (`currentValue`) and assigned limit.

**Request**:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/usages?api-version=2024-10-01
```

**Example — check quota usage in East US**:

# [Python](#tab/python)

```python
import requests
import json
from azure.identity import DefaultAzureCredential

subscription_id = "<your-subscription-id>"
location = "eastus"

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
headers = {"Authorization": f"Bearer {token.token}"}

url = (
    f"https://management.azure.com/subscriptions/{subscription_id}"
    f"/providers/Microsoft.CognitiveServices/locations/{location}/usages"
    f"?api-version=2024-10-01"
)

response = requests.get(url, headers=headers)
usages = response.json()

# Show quota lines that have a non-zero limit
for item in usages["value"]:
    if item["limit"] > 0:
        print(f"{item['name']['localizedValue']}: {item['currentValue']}/{item['limit']}")
```

# [Bash](#tab/bash)

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
LOCATION="eastus"

az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.CognitiveServices/locations/$LOCATION/usages?api-version=2024-10-01"
```

# [Sample output](#tab/output)

```json
{
  "value": [
    {
      "name": {
        "value": "OpenAI.Standard.gpt-4o",
        "localizedValue": "Tokens Per Minute (thousands) - gpt-4o"
      },
      "currentValue": 0,
      "limit": 150,
      "unit": "Count"
    }
  ]
}
```

---

**Key fields**:

| Field | Description |
|---|---|
| `name.value` | Quota name in the format `{Provider}.{DeploymentType}.{Model}` |
| `name.localizedValue` | Human-readable description including the unit |
| `currentValue` | How much of this quota is currently consumed by deployments |
| `limit` | Your subscription's quota limit for this model and deployment type |

### Model Capacities API

The Model Capacities API returns the available deployment capacity for a specific model across all locations and deployment types in your subscription.

**Request**:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/modelCapacities?api-version=2024-10-01&modelFormat={format}&modelName={name}&modelVersion={version}
```

**Example — check where gpt-4o capacity is available**:

# [Python](#tab/python)

```python
import requests
import json
from azure.identity import DefaultAzureCredential

subscription_id = "<your-subscription-id>"
model_name = "gpt-4o"
model_version = "2024-08-06"

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
headers = {"Authorization": f"Bearer {token.token}"}

url = (
    f"https://management.azure.com/subscriptions/{subscription_id}"
    f"/providers/Microsoft.CognitiveServices/modelCapacities"
    f"?api-version=2024-10-01"
    f"&modelFormat=OpenAI&modelName={model_name}&modelVersion={model_version}"
)

response = requests.get(url, headers=headers)
capacities = response.json()

# Show locations with available capacity for Standard deployments
for item in capacities["value"]:
    props = item["properties"]
    if props["availableCapacity"] > 0 and "Standard" in props["skuName"]:
        print(f"{item['location']} ({props['skuName']}): {props['availableCapacity']} available")
```

# [Bash](#tab/bash)

```bash
SUBSCRIPTION_ID="<your-subscription-id>"

az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.CognitiveServices/modelCapacities?api-version=2024-10-01&modelFormat=OpenAI&modelName=gpt-4o&modelVersion=2024-08-06"
```

# [Sample output](#tab/output)

```json
{
  "value": [
    {
      "location": "eastus",
      "properties": {
        "model": {
          "name": "gpt-4o",
          "format": "OpenAI",
          "version": "2024-08-06"
        },
        "skuName": "Standard",
        "availableCapacity": 150,
        "availableFinetuneCapacity": 0
      }
    }
  ]
}
```

---

**Key fields**:

| Field | Description |
|---|---|
| `location` | Azure region |
| `properties.skuName` | Deployment type (Standard, GlobalStandard, DataZoneStandard, ProvisionedManaged, etc.) |
| `properties.availableCapacity` | Capacity units available in your subscription for this model, location, and deployment type |
| `properties.availableFinetuneCapacity` | Fine-tuning capacity available (when applicable) |

[!INCLUDE [quota 2](../includes/quota-2.md)]
