---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

* Add the [Azure AI inference package](https://aka.ms/azsdk/azure-ai-inference/java/reference) to your project:

  ```xml
  <dependency>
      <groupId>com.azure</groupId>
      <artifactId>azure-ai-inference</artifactId>
      <version>1.0.0-beta.4</version>
  </dependency>
  ```
  
* If you are using Entra ID, you also need the following package:

  ```xml
  <dependency>
      <groupId>com.azure</groupId>
      <artifactId>azure-identity</artifactId>
      <version>1.15.3</version>
  </dependency>
  ```

* Import the following namespace:
  
  ```java
  package com.azure.ai.inference.usage;
  
  import com.azure.ai.inference.EmbeddingsClient;
  import com.azure.ai.inference.EmbeddingsClientBuilder;
  import com.azure.ai.inference.ChatCompletionsClient;
  import com.azure.ai.inference.ChatCompletionsClientBuilder;
  import com.azure.ai.inference.models.EmbeddingsResult;
  import com.azure.ai.inference.models.EmbeddingItem;
  import com.azure.ai.inference.models.ChatCompletions;
  import com.azure.core.credential.AzureKeyCredential;
  import com.azure.core.util.Configuration;
  
  import java.util.ArrayList;
  import java.util.List;
  ```