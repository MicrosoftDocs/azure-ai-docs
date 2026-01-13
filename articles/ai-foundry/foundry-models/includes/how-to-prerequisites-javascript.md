---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

* Install the [Azure Inference library for JavaScript](https://aka.ms/azsdk/azure-ai-inference/javascript/reference) with the following command:

  ```bash
  npm install @azure-rest/ai-inference
  npm install @azure/core-auth
  npm install @azure/identity
  ```

  If you are using Node.js, you can configure the dependencies in **package.json**:

  __package.json__

  ```json
  {
    "name": "main_app",
    "version": "1.0.0",
    "description": "",
    "main": "app.js",
    "type": "module",
    "dependencies": {
      "@azure-rest/ai-inference": "1.0.0-beta.6",
      "@azure/core-auth": "1.9.0",
      "@azure/core-sse": "2.2.0",
      "@azure/identity": "4.8.0"
    }
  }
  ```

* Import the following:

  ```javascript
  import ModelClient from "@azure-rest/ai-inference";
  import { isUnexpected } from "@azure-rest/ai-inference";
  import { createSseStream } from "@azure/core-sse";
  import { AzureKeyCredential } from "@azure/core-auth";
  import { DefaultAzureCredential } from "@azure/identity";
  ```
