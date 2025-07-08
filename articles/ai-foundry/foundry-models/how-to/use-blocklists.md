---
title: Use blocklists in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to create custom blocklists in Azure AI Foundry portal as part of your content filtering configurations.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 05/31/2025
ms.author: pafarley
author: PatrickFarley
---

# How to use blocklists with Foundry Models in Azure AI Foundry services

The configurable content filters are sufficient for most content moderation needs. However, you might need to create custom blocklists in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) as part of your content filtering configurations in order to filter terms specific to your use case. This article illustrates how to create custom blocklists as part of your content filters in [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

## Prerequisites

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](../../model-inference/how-to/quickstart-github-models.md) if it's your case.

* An Azure AI Foundry services resource. For more information, see [Create an Azure AI Foundry Services resource](../../../ai-services/multi-service-resource.md?context=/azure/ai-services/model-inference/context/context).

* An Azure AI Foundry project [connected to your Azure AI Foundry services resource](../../model-inference/how-to/configure-project-connection.md).

* A model deployment. See [Add and configure models to Azure AI Foundry services](../../model-inference/how-to/create-model-deployments.md) for adding models to your resource.

    > [!NOTE]
    > Blocklist (preview) is only supported for Azure OpenAI models.

[!INCLUDE [use-blocklists](../../includes/use-blocklists.md)]

## Next steps

* [Configure content filtering](../../model-inference/how-to/configure-content-filters.md)
