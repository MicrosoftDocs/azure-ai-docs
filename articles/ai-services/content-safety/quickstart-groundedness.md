---
title: "Quickstart: Groundedness detection (preview)"
titleSuffix: Azure AI services
description: Learn how to detect whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users.
services: ai-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 09/16/2025
ms.author: pafarley
zone_pivot_groups: programming-languages-content-safety-foundry-rest
#customer intent: As a developer, I want to learn how to use the groundedness detection API so that I can ensure generated content is aligned with factual references.

---

# Quickstart: Use Groundedness detection (preview)

This guide shows you how to use the groundedness detection API. This feature automatically detects and corrects text that goes against the provided source documents, ensuring that the generated content is aligned with factual or intended references. Below, we explore several common scenarios to help you understand how and when to apply these features to achieve the best outcomes. 


::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-groundedness.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-groundedness.md)]

::: zone-end


## Related content

* [Groundedness detection concepts](./concepts/groundedness.md)
* Combine Groundedness detection with other LLM safety features like [Prompt Shields](./quickstart-jailbreak.md).

