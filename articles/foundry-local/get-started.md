---
title: "Get started with Foundry Local"
titleSuffix: Foundry Local
description: "Build your first on-device AI application with the Foundry Local SDK."
ms.date: 03/27/2026
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.reviewer: samkemp
ms.author: jburchel
author: jonburchel
reviewer: samuel100
ms.custom:
  - build-2025
  - build-aifnd
  - peer-review-program
  - dev-focus
keywords:
  - Foundry Local
  - on-device AI
  - local inference
zone_pivot_groups: foundry-local-sdk
ai-usage: ai-assisted
# customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Get started with Foundry Local

In this quickstart, you create a console application that downloads a local AI model, generates a streaming chat response, and unloads the model. Everything runs on your device with no cloud dependency or Azure subscription.


::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](./includes/native-chat-completions/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](./includes/native-chat-completions/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](./includes/native-chat-completions/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](./includes/native-chat-completions/rust.md)]
::: zone-end

## Related content

- [What is Foundry Local?](what-is-foundry-local.md)
- [Use chat completions via REST server](how-to/how-to-integrate-with-inference-sdks.md)
- [Foundry Local CLI reference](reference/reference-cli.md)