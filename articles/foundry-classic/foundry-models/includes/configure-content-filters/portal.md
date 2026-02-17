---
manager: nitinme
author: msakande
ms.author: mopeakande
ms.reviewer: yinchang
reviewer: ychang-msft
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 08/29/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* An AI project connected to your Foundry Tools resource. You can follow the steps at [Configure Microsoft Foundry Models service in my project](../../how-to/configure-project-connection.md) in Foundry.

## Create a custom content filter

Follow these steps to create a custom content filter:

1. Go to the [Foundry portal](https://ai.azure.com/explore/models).

1. Select **Guardrails & controls** from the left pane.

1. Select the **Content filters** tab, then select **Create content filter**.

1. On the **Basic information** page, enter a name for the content filter.

1. For **Connection**, select the connection to the **Foundry Tools** resource that is connected to your project.

1. Select **Next** to go to the **Input filter** page.

1. Configure the input filter depending on your requirements. This configuration is applied before the request reaches the model itself.

1. Select **Next** to go to the **Output filter** page.

1. Configure the output filter depending on your requirements. This configuration is applied after the model is executed and content is generated.

1. Select **Next** to go to the **Connection** page.

1. On this page, you have the option to associate model deployments with the created content filter. You can change the associated model deployments at any time.

1. Select **Next** to review the filter settings. Then, select **Create filter**.

1. When the deployment completes, the new content filter is applied to the model deployment.

[!INCLUDE [code](code.md)]

