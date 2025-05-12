---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* An AI project connected to your Azure AI Services resource. You call follow the steps at [Configure Azure AI model inference service in my project](../../how-to/configure-project-connection.md) in Azure AI Foundry.

## Create a custom content filter

Follow these steps to create a custom content filter:

1. Go to [Azure AI Foundry portal](https://ai.azure.com/explore/models).

2. Select **Guardrails & controls**.

3. Select the tab **Content filters** and then select **Create content filter**.

4. Under **Basic information**, give the content filter a name.

5. Under **Connection**, select the connection to the **Azure AI Services** resource that is connected to your project.

6. Under **Input filter**, configure the filter depending on your requirements. This configuration is applied before the request reaches the model itself.

7. Under **Output filter**, configure the filter depending on your requirements. This configuration is applied after the model is executed and content is generated.

8. Select **Next**.

9. Optionally, you can associate a given deployment with the created content filter. You can change the model deployments associated at any time.

10. Once the deployment completes, the new content filter is applied to the model deployment.

[!INCLUDE [code](code.md)]

