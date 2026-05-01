---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/01/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

> [!TIP]
> The REST API deployment path targets the Microsoft Foundry account resource directly and doesn't require a Foundry project. This makes it a good option for existing customers who deploy and manage Foundry models without a project association.

Before you run the REST examples, sign in with Azure CLI and save a management-plane bearer token as `AZURE_AI_AUTH_TOKEN`.

```bash
export AZURE_AI_AUTH_TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)
```

Deploy model router programmatically with the Azure Management REST API. The following example creates a default deployment and relies on the built-in **Balanced** routing mode and full supported model set.

```bash
curl -X PUT "https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/my-resource-group/providers/Microsoft.CognitiveServices/accounts/my-foundry-account/deployments/model-router-deployment?api-version=2025-10-01-preview" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AZURE_AI_AUTH_TOKEN" \
    -d '{
        "sku": {"name": "GlobalStandard", "capacity": 10},
        "properties": {
                "model": {"format": "OpenAI", "name": "model-router", "version": "2025-11-18"}
        }
}'
```