---
title: Build a translation app with LangChain
titleSuffix: Foundry Local
description: Learn how to build a LangChain application using Foundry Local
keywords: Foundry Tools, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.date: 01/05/2026
ms.reviewer: eneros
ms.author: jburchel
author: jonburchel
reviewer: eneros
ms.custom:
  - build-2025
  - dev-focus
zone_pivot_groups: foundry-local-langchain
ai-usage: ai-assisted
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Build a translation app with LangChain

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article shows you how to build a translation app by using the Foundry Local SDK and [LangChain](https://www.langchain.com/langchain). Use a local model to translate text between languages.

<!-- markdownlint-disable MD044 -->
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/use-langchain/python.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/use-langchain/javascript.md)]
::: zone-end
<!-- markdownlint-enable MD044 -->

## Troubleshooting

- If you see a service connection error, restart the Foundry Local service and try again.
- The first run can take longer because Foundry Local might download the model.
- If Node.js fails with an import or top-level await error, confirm your project is configured for ES modules.

## Related content

- Explore the [LangChain documentation](https://python.langchain.com/docs/introduction) for advanced features.
- [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md)
