---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

* Install the [Azure AI inference package](https://aka.ms/azsdk/azure-ai-inference/python/reference) with the following command:

    ```bash
    dotnet add package Azure.AI.Inference --prerelease
    ```
    
* If you are using Entra ID, you also need the following package:

    ```bash
    dotnet add package Azure.Identity
    ```