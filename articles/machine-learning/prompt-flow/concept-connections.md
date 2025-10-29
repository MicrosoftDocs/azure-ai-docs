---
title: Connections in Azure Machine Learning prompt flow
titleSuffix: Azure Machine Learning
description: Learn about how in Azure Machine Learning prompt flow, you can utilize connections to effectively manage credentials or secrets for APIs and data sources.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.custom:
  - ignite-2023
ms.topic: concept-article
author: lgayhardt
ms.author: lagayhar
ms.reviewer: keli19
ms.date: 06/26/2024
ms.update-cycle: 365-days
---

# Connections in prompt flow

In Azure Machine Learning prompt flow, you can utilize connections to effectively manage credentials or secrets for APIs and data sources.

## Connections

Connections in prompt flow play a crucial role in establishing connections to remote APIs or data sources. They encapsulate essential information such as endpoints and secrets, ensuring secure and reliable communication.

In the Azure Machine Learning workspace, connections can be configured to be shared across the entire workspace or limited to the creator. Secrets associated with connections are securely persisted in the corresponding Azure Key Vault, adhering to robust security and compliance standards.

Prompt flow provides various prebuilt connections, including Azure OpenAI, OpenAI, and Azure Content Safety. These prebuilt connections enable seamless integration with these resources within the built-in tools. Additionally, users have the flexibility to create custom connection types using key-value pairs, empowering them to tailor the connections to their specific requirements, particularly in Python tools.

| Connection type                                              | Built-in tools                  |
| ------------------------------------------------------------ | ------------------------------- |
| [Azure OpenAI](https://azure.microsoft.com/products/cognitive-services/openai-service) | LLM or Python                   |
| [OpenAI](https://openai.com/)                               | LLM or Python                   |
| [Azure Content Safety](https://aka.ms/acs-doc)               | Content Safety (Text) or Python |
| [Azure AI Search](https://azure.microsoft.com/products/search) (formerly Cognitive Search) | Vector DB Lookup or Python      |
| [Serp](https://serpapi.com/)                                 | Serp API or Python              |
| [Custom](./tools-reference/python-tool.md#use-a-custom-connection-in-python)                                                       | Python                          |

By leveraging connections in prompt flow, users can easily establish and manage connections to external APIs and data sources, facilitating efficient data exchange and interaction within their AI applications.

## Next steps

- [Get started with prompt flow](get-started-prompt-flow.md)
- [Consume custom connection in Python Tool](./tools-reference/python-tool.md#use-a-custom-connection-in-python)
