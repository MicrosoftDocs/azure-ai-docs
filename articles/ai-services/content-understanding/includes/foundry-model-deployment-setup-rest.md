---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-content-understanding-foundry-tools
ms.topic: include
ms.date: 07/16/2026
ai-usage: ai-assisted
---

[!INCLUDE [preview-notice](preview-notice.md)]

By default, use GA API version `2025-11-01`. Use `2026-06-01-preview` only when you need preview features.

1. In your Foundry resource, deploy the models required by your analyzers. For the current list, see [Supported generative models](../service-limits.md#supported-generative-models). For deployment instructions, see [Create model deployments in Microsoft Foundry portal](/azure/ai-foundry/foundry-models/how-to/create-model-deployments?pivots=ai-foundry-portal).

1. Define default model deployments at the resource level. Before you run the following `cURL` command, make the following changes to the HTTP request:

   1. Replace `{endpoint}` and `{key}` with the corresponding values from your Foundry instance in the Azure portal.

   1. Replace `api-version=2025-11-01` with `api-version=2026-06-01-preview` to use preview features. For the full preview feature list, see [What's new in Azure AI Content Understanding](../whats-new.md).

   1. Replace `{completionModelName}` and `{embeddingModelName}` with supported model names.

   1. Replace `{completionDeploymentName}` and `{embeddingDeploymentName}` with your model deployment names.



   ```bash
   curl -i -X PATCH "{endpoint}/contentunderstanding/defaults?api-version=2026-06-01-preview" \
     -H "Ocp-Apim-Subscription-Key: {key}" \
     -H "Content-Type: application/json" \
     -d '{
           "modelDeployments": {
             "{completionModelName}": "{completionDeploymentName}",
             "{embeddingModelName}": "{embeddingDeploymentName}"
           }
         }'
   ```
