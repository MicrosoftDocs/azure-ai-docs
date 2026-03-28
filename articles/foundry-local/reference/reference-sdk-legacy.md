---
title: Foundry Local Legacy SDK Reference
titleSuffix: Foundry Local
description: Reference guide for the Foundry Local Legacy SDK.
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.author: jburchel
author: jonburchel
ms.topic: concept-article
ms.date: 01/05/2026
zone_pivot_groups: foundry-local-sdk
reviewer: maanavdalal
ms.reviewer: maanavd
ai-usage: ai-assisted
---

# Foundry Local Legacy SDK reference


> [!WARNING]
> This reference applies to earlier versions of the Foundry Local SDK that depend on the Foundry Local CLI for service management. Starting with the versions listed below, the SDK embeds the runtime directly and no longer requires the CLI. For new development, use the [current SDK reference](./reference-sdk-current.md).
>
> | Language | Package | CLI-dependent versions | Embedded versions |
> |---|---|---|---|
> | C# | Microsoft.AI.Foundry.Local | 0.3.0 and earlier | 0.8.0 and later |
> | JavaScript | foundry-local-sdk | 0.5.0 and earlier | 0.9.0 and later |
> | Python | foundry-local-sdk | 0.5.1 and earlier | 1.0.0 and later |
> | Rust | foundry-local (legacy) → foundry-local-sdk | 0.x | 1.0.0 and later |
>
> **Support for CLI-dependent versions ends 31 August 2026.**

<!-- markdownlint-disable MD044 -->

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/sdk-legacy-reference/python.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/sdk-legacy-reference/javascript.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/sdk-legacy-reference/csharp.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/sdk-legacy-reference/rust.md)]
::: zone-end

<!-- markdownlint-enable MD044 -->