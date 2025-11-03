---
title: Use Native Chat Completions
titleSuffix: Foundry Local
description: This article provides instructions on how to leverage native chat completions API in Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 10/01/2025
zone_pivot_groups: foundry-local-sdk-v2
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---
    
# Use Foundry Local native chat completions API

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local has a native chat completions API that allows you to use the inference capabilities without needing to rely on the optional Web Server or separate SDKs (such as the OpenAI chat completions API). This article shows you how to use the native chat completions API in Foundry Local.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/native-chat-completions/csharp.md)]
::: zone-end

## Related content

- [Integrate Foundry Local with 3rd party SDKs](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)