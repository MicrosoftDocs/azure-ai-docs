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
  npm install @azure/core-auth
  ```

  Alternately, you can add your dependencies to **package.json** and install with `npm rebuild`:

  __package.json__

  ```json
  {
    "name": "sample_app",
    "version": "1.0.0",
    "description": "",
    "main": "app.js",
    "dependencies": {
      "@azure-rest/ai-inference": "1.0.0-beta.6",
      "@azure/core-auth": "1.9.0"
    }
  }
  ```    
