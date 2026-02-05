---
title: Virtual network support for evaluation
titleSuffix: Microsoft Foundry
description: Configure virtual network support for evaluation workloads in Microsoft Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 01/15/2025
ms.topic: how-to
ms.service: azure-ai-foundry
monikerRange: 'foundry-classic || foundry'
---

# Virtual network support for evaluation

For network isolation purposes you can bring your own virtual network for evaluation. To learn more, see [How to configure a private link](../how-to/configure-private-link.md).

> [!NOTE]
> Evaluation data is sent to Application Insights if Application Insights is connected. Virtual network support for Application Insights and tracing isn't available. Inline datasource is not supported.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Azure AI User role to the project's Managed Identity during initial project setup.

## Virtual network region support

Bring your own virtual network for evaluation is supported in all regions except for Central India, East Asia, North Europe and Qatar Central.

## Related content

- [How to configure a private link](../how-to/configure-private-link.md)
- [Observability for generative AI applications](observability.md)
