---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 11/19/2025
---

Set up default model deployments for your Content Understanding resource. By setting defaults, you create a connection to the Microsoft Foundry models you use for Content Understanding requests. Choose one of the following methods:

# [Portal](#tab/portal)

1. Go to the [Content Understanding settings page](https://contentunderstanding.ai.azure.com/settings).

1. Select the **+ Add resource** button in the upper left.

1. Select the Foundry resource that you want to use and select **Next** > **Save**.

   Make sure that the **Enable autodeployment for required models if no defaults are available** checkbox is selected. This selection ensures your resource is fully set up with the required `GPT-4.1`, `GPT-4.1-mini`, and `text-embedding-3-large` models. Different prebuilt analyzers require different models.

By taking these steps, you set up a connection between Content Understanding and Foundry models in your Foundry resource.

# [REST API](#tab/rest-api)

1. In your Foundry resource, create Foundry model deployments of the `GPT-4.1`, `GPT-4.1-mini`, and `text-embedding-3-large` models. For details on how to deploy these models, see [Create model deployments in Microsoft Foundry portal](/azure/ai-foundry/foundry-models/how-to/create-model-deployments?pivots=ai-foundry-portal). Different prebuilt analyzers require different models, so you need to deploy all three.

1. Define default model deployments at the resource level. Before you run the following `cURL` command, make the following changes to the HTTP request:

   1. Replace `{endpoint}` and `{key}` with the corresponding values from your Foundry instance in the Azure portal.

   1. Replace `{myGPT41Deployment}`, `{myGPT41MiniDeployment}`, and `{myEmbeddingDeployment}` with your actual model deployment names from your Foundry resource.

   ```bash
   curl -i -X PATCH "{endpoint}/contentunderstanding/defaults?api-version=2025-11-01" \
     -H "Ocp-Apim-Subscription-Key: {key}" \
     -H "Content-Type: application/json" \
     -d '{
           "modelDeployments": {
             "gpt-4.1": "{myGPT41Deployment}",
             "gpt-4.1-mini": "{myGPT41MiniDeployment}",
             "text-embedding-3-large": "{myEmbeddingDeployment}"
           }
         }'
   ```

---
