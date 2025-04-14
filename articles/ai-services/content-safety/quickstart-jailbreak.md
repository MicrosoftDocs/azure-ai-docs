---
title: "Quickstart: Prompt Shields "
titleSuffix: Azure AI services
description: Learn how to detect large language model input attack risks and mitigate risk with Azure AI Content Safety.
services: ai-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 10/16/2024
ms.author: pafarley
zone_pivot_groups: programming-languages-content-safety-foundry-rest
#customer intent: As a developer, I want to learn how to use Prompt Shields so that I can ensure AI-generated content is safe and compliant.
---

# Quickstart: Use Prompt Shields

In this quickstart, you use the "Prompt Shields" feature. Prompt Shields in Azure AI Content Safety are designed to safeguard generative AI systems from generating harmful or inappropriate content. These shields detect and mitigate risks associated with both User Prompt Attacks (malicious or harmful user-generated inputs) and Document Attacks (inputs containing harmful content embedded within documents). The use of "Prompt Shields" is crucial in environments where GenAI is employed, ensuring that AI outputs remain safe, compliant, and trustworthy.

The primary objectives of the "Prompt Shields" feature for GenAI applications are:

- To detect and block harmful or policy-violating user prompts that could lead to unsafe AI outputs.
- To identify and mitigate document attacks where harmful content is embedded within user-provided documents.
- To maintain the integrity, safety, and compliance of AI-generated content, preventing misuse of GenAI systems.

For more information on Prompt Shields, see the [Prompt Shields concept page](./concepts/jailbreak-detection.md). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview. 


::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-prompt-shields.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-prompt-shields.md)]

::: zone-end



## Related content

* [Prompt Shields concepts](./concepts/jailbreak-detection.md)
* Configure filters for each category and test on datasets using [Content Safety Studio](studio-quickstart.md), export the code and deploy.
