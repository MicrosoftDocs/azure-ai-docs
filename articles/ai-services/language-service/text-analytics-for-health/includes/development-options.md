---
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 12/19/2023
ms.author: jboback
---

To use Text Analytics for health, you submit raw unstructured text for analysis and handle the API output in your application. Analysis is performed as-is, with no additional customization to the model used on your data. There are two ways to use Text Analytics for health:


|Development option  |Description  |
|---------|---------|
|Azure AI Foundry     | Azure AI Foundry is a web-based platform that lets you use entity linking with text examples with your own data when you sign up. For more information, see the [Azure AI Foundry website](https://ai.azure.com) or [Azure AI Foundry documentation](../../../../ai-foundry/what-is-ai-foundry.md).         |
|REST API or Client library (Azure SDK)      | Integrate Text Analytics for health into your applications using the REST API, or the client library available in a variety of languages. For more information, see the [Text Analytics for health quickstart](../quickstart.md).        |
| Docker container | Use the available Docker container to [deploy this feature on-premises](../how-to/use-containers.md). These docker containers enable you to bring the service closer to your data for compliance, security, or other operational reasons. |
