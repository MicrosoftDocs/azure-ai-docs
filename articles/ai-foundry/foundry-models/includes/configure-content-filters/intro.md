---
manager: nitinme
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 08/29/2025
ms.topic: include
---

The content filtering system integrated into Microsoft Foundry runs alongside Foundry Models. It uses an ensemble of multi-class classification models to detect four categories of harmful content (violence, hate, sexual, and self-harm) at four severity levels (safe, low, medium, and high). It offers optional binary classifiers for detecting jailbreak risk, existing text, and code in public repositories. For more information about content categories, severity levels, and the behavior of the content filtering system, see [the following article](../../concepts/content-filter.md).

The [default content filtering](../../concepts/default-safety-policies.md) configuration filters content at the medium severity threshold for all four harmful categories for both prompts and completions. Content detected at medium or high severity level is filtered out, while content detected at low or safe severity level isn't filtered.

You can configure content filters at the resource level and associate them with one or more deployments.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry](../../how-to/quickstart-github-models.md).

* A Foundry resource (formerly known as Azure AI Services resource). For more information, see [Create a Foundry resource](../../how-to/quickstart-create-resources.md).