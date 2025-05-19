---
title: "Protected material detection in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about Protected material detection and the related flags that the Azure AI Content Safety service returns.
services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: conceptual
ms.date: 01/22/2025
ms.author: pafarley
keywords: 
---


# Protected material detection

The Protected material detection APIs scan the output of large language models to identify and flag known protected material. The APIs are designed to help organizations prevent the generation of content that closely matches copyrighted text or code.

The [Protected material text API](../quickstart-protected-material.md) flags known text content (for example, song lyrics, articles, recipes, and selected web content) that might be output by large language models.

The [Protected material code API](../quickstart-protected-material-code.md) flags protected code content (from known GitHub repositories, including software libraries, source code, algorithms, and other proprietary programming content) that might be output by large language models.

[!INCLUDE [protected-material-examples](../includes/protected-material-examples.md)]

## Next step

Follow the quickstart to get started using Azure AI Content Safety to detect protected material.

> [!div class="nextstepaction"]
> [Detect protected material](../quickstart-protected-material.md)




