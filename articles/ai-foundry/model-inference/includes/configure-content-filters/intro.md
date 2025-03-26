---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
---

[!INCLUDE [Feature preview](../../../includes/feature-preview.md)]

The content filtering system integrated into Azure AI Services runs alongside the core models. It uses an ensemble of multi-class classification models to detect four categories of harmful content (violence, hate, sexual, and self-harm) at four severity levels respectively (safe, low, medium, and high). It offers optional binary classifiers for detecting jailbreak risk, existing text, and code in public repositories. Learn more about content categories, severity levels, and the behavior of the content filtering system [in the following article](../../concepts/content-filter.md)

The [default content filtering](../../concepts/default-safety-policies.md) configuration is set to filter at the medium severity threshold for all four content harms categories for both prompts and completions. Hence, content detected at severity level medium or high is filtered, while content detected at severity level low or safe isn't filtered.

Content filters can be configured at the resource level and associated with one or more deployments.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you are using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI model inference](../../how-to/quickstart-github-models.md) if it's your case.

* An Azure AI services resource. For more information, see [Create an Azure AI Services resource](../../../../ai-services/multi-service-resource.md??context=/azure/ai-services/model-inference/context/context).