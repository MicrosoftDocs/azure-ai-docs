---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

* Install the [Azure Inference library for JavaScript](https://aka.ms/azsdk/azure-ai-inference/javascript/reference) with the following command:

  ```bash
  npm install @azure-rest/ai-inference
  ```

* Import the following modules:

    ```javascript
    import ModelClient, { isUnexpected } from "@azure-rest/ai-inference";
    import { AzureKeyCredential } from "@azure/core-auth";
    import { DefaultAzureCredential } from "@azure/identity";
    import { createRestError } from "@azure-rest/core-client";
    ```
    
