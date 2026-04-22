---
title: Foundry Local Legacy SDK Reference
titleSuffix: Foundry Local
description: Reference guide for the Foundry Local Legacy SDK.
ms.service: microsoft-foundry
ms.subservice: foundry-local
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
> This reference applies to earlier versions of the Foundry Local SDK that depend on the Foundry Local CLI for service management. 
>
> **For new development, use the [current SDK reference](./reference-sdk-current.md)**.
>
> The following table shows the SDK versions where there was a dependency on the CLI:
>
> | Language | Package | CLI-dependent versions |
> |---|---|---|
> | C# | Microsoft.AI.Foundry.Local | 0.3.0 and earlier | 
> | JavaScript | foundry-local-sdk | 0.5.0 and earlier |
> | Python | foundry-local-sdk | 0.5.1 and earlier |
> | Rust | foundry-local / foundry-local-sdk | 0.x |
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