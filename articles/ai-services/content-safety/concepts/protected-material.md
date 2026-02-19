---
title: "Protected material detection in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about Protected material detection and the related flags that the Azure AI Content Safety service returns.
services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 09/02/2025
ms.author: pafarley
keywords: 
---


# Protected material detection

The Protected material detection APIs scan the output of large language models to identify and flag known protected material. These APIs help organizations prevent the generation of content that closely matches copyrighted text or code.

The [Protected material text API](../quickstart-protected-material.md) flags any known text content that large language models output, such as song lyrics, articles, recipes, and selected web content.

The [Protected material code API](../quickstart-protected-material-code.md) flags protected code content that large language models might output. This content comes from known GitHub repositories and includes software libraries, source code, algorithms, and other proprietary programming content.

[!INCLUDE [protected-material-examples](../includes/protected-material-examples.md)]

## Next step

To detect protected material, follow the quickstart to get started using Azure AI Content Safety.

> [!div class="nextstepaction"]
> [Detect protected material](../quickstart-protected-material.md)




