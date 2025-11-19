---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 11/19/2025
---

Set up default model deployments for your Content Understanding resource. Setting defaults creates a connection to the Foundry models you use for Content Understanding requests. Choose one of the following methods:

# [Portal](#tab/portal)

1. Go to the [Content Understanding settings page](https://contentunderstanding.ai.azure.com/settings)
2. Select the "+ Add resource" button in the upper left
3. Select the Foundry resource that you want to use and click Next, then Save
 - Make sure to leave "Enable auto-deployment for required models if no defaults are available." checked. This will ensure your resource is fully setup.

By taking these steps you will setup a connection between Content Understanding and Foundry models in your Foundry resource. 


# [REST API](#tab/rest-api)

1. Create a Foundry Model deployment of GPT-4.1 completion model and a text-embedding-3-large embedding model in your Foundry resource. For details on how to deploy these models, see [Create model deployments in Microsoft Foundry portal](/azure/ai-foundry/foundry-models/how-to/create-model-deployments?pivots=ai-foundry-portal).

2. Define default model deployments at the resource level.

   Before running the following cURL command, make the following changes to the HTTP request:
   - Replace `{endpoint}` and `{key}` with the corresponding values from your Foundry instance in the Azure portal.
   - Replace `{myGPT41Deployment}`, `{myGPT41MiniDeployment}` and `{myEmbeddingDeployment}` with your actual model deployment names from your Foundry resource.

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
