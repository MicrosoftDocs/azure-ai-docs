---
title: "Quickstart: Detect prompt attacks with Prompt Shields"
titleSuffix: Azure AI services
description: Learn how to detect large language model input attack risks and mitigate risk with Azure AI Content Safety.
services: ai-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 01/30/2026
ms.author: pafarley
ms.custom: dev-focus
ai-usage: ai-assisted
zone_pivot_groups: programming-languages-content-safety-foundry-rest
#customer intent: As a developer, I want to learn how to use Prompt Shields so that I can ensure AI-generated content is safe and compliant.
---

# Quickstart: Detect prompt attacks with Prompt Shields

In this quickstart, you use Prompt Shields to detect potential security threats in user inputs and documents.

Prompt Shields in Azure AI Content Safety detects both User Prompt Attacks (malicious inputs) and Document Attacks (harmful content embedded in documents). For a comprehensive background on Prompt Shields capabilities and objectives, see the [Prompt Shields concept page](./concepts/jailbreak-detection.md). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview.

## Quick example

Here's what a basic Prompt Shields API call looks like:

```bash
curl --location --request POST '<endpoint>/contentsafety/text:shieldPrompt?api-version=2024-09-01' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "userPrompt": "Your input text here",
  "documents": ["Document text to analyze"]
}'
```

Expected response:
```json
{
  "userPromptAnalysis": { "attackDetected": true },
  "documentsAnalysis": [{ "attackDetected": false }]
}
```

Choose your preferred implementation approach below:

::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-prompt-shields.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-prompt-shields.md)]

::: zone-end

## Next steps

Now that you've completed the basic Prompt Shields setup, explore these advanced scenarios:

* **Production integration**: See complete code examples in the [Azure AI Content Safety samples repository](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentsafety/azure-ai-contentsafety/samples)
* **Configure custom thresholds**: Learn how to adjust detection sensitivity in [Content Safety Studio](https://contentsafety.cognitive.azure.com)
* **Batch processing**: Process multiple inputs efficiently using the batch analysis capabilities
* **Integration patterns**: Implement Prompt Shields in your AI application workflow

## Related content

* [Prompt Shields concepts](./concepts/jailbreak-detection.md)
* Configure filters for each category and test on datasets using [Content Safety Studio](https://contentsafety.cognitive.azure.com), export the code and deploy.
