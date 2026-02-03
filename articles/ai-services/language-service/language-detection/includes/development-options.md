---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
To use language detection, you submit raw unstructured text for analysis and handle the API output in your application. Analysis is performed as-is, with no additional customization to the model used on your data. There are three ways to use language detection:


|Development option  |Description  |
|---------|---------|
|[**Microsoft Foundry (new)**](https://ai.azure.com/) portal| Foundry (new) is a cloud-based AI platform that provides streamlined access to Foundry models, agents, and tools through Foundry projects.
|[**Foundry (classic)**](https://ai.azure.com/) portal| Foundry (classic) is a cloud-based platform that supports hub-based projects and other resource types. When you sign up, you can use your own data to detect more than 100 languages in their primary script.|
|[**REST API or Client library (Azure SDK)**](/rest/api/language/analyze-text/analyze-text/analyze-text)| Integrate language detection into your applications using the REST API, or the client library available in various languages.|
| **Docker container** | Use the available Docker container to [deploy this feature on-premises](../how-to/use-containers.md). Docker containers enable you to bring the service closer to your data for compliance, security, or other operational considerations.|
