---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/28/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

> [!TIP]
> The REST API deployment path targets the Microsoft Foundry account resource directly and doesn't require a Foundry project. This makes it a good option for existing customers who deploy and manage Foundry models without a project association.

Deploy model router programmatically with the Azure Management REST API. The following example deploys model router with a routing mode and a custom model subset in a single request.

> [!NOTE]
> The deployment request body uses `format`, `name`, and `version` for the model router itself and for each model in the routing subset. Find the correct values for each model in the [Supported models](#supported-models) table.

```bash
curl -X PUT "https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/my-resource-group/providers/Microsoft.CognitiveServices/accounts/my-foundry-account/deployments/model-router-deployment?api-version=2025-10-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_AI_AUTH_TOKEN" \
  -d '{
    "sku": {"name": "GlobalStandard", "capacity": 10},
    "properties": {
        "model": {"format": "OpenAI", "name": "model-router", "version": "2025-11-18"},
        "routing": {
            "mode": "balanced",
            "models": [
                {"format": "OpenAI", "name": "gpt-4.1", "version": "2025-04-14"},
                {"format": "OpenAI", "name": "gpt-5.2-chat", "version": "2025-12-11"},
                {"format": "Meta", "name": "Llama-4-Maverick-17B-128E-Instruct-FP8", "version": "1"}
            ]
        }
    }
}'
```

> [!TIP]
> For the full runnable sample and other deployment options (routing mode only, model subset only), see the [Model Router REST samples](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/REST/model-router/deploy-model-router-all-configs.sh) in the foundry-samples repository.

> [!IMPORTANT]
> If you include Anthropic Claude models in the `routing.models` array, you must first deploy them to the same Foundry account with a matching SKU. Otherwise the request fails with an `InvalidResourceProperties` error. Deploy Claude models from the Foundry model catalog before you reference them in a model router deployment. See [Deploy and use Claude models](/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude).
