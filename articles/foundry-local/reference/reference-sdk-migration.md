---
title: Foundry Local SDK Migration Guide
titleSuffix: Foundry Local
description: Migration guide for updating from Foundry Local SDK legacy version to the current version.
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.author: jburchel
author: jonburchel
ms.topic: concept-article
ms.date: 01/05/2026
zone_pivot_groups: foundry-local-sdk-vnext
reviewer: maanavdalal
ms.reviewer: maanavd
ai-usage: ai-assisted
---

# Foundry Local SDK migration guide

This guide provides instructions for migrating your code from the legacy version of the Foundry Local SDK to the current version. The new SDK removes the dependency on the Foundry Local CLI and therefore allows you to ship your applications without requiring your users to install the CLI or set up a local Foundry environment. The new SDK also includes improvements to the API for better usability and performance.

<!-- markdownlint-disable MD044 -->

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/sdk-migration-guide/javascript.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/sdk-migration-guide/csharp.md)]
::: zone-end

<!-- markdownlint-enable MD044 -->