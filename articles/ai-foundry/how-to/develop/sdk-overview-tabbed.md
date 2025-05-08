---
title: How to get started with Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides an overview of the Azure AI Foundry SDK and how to get started using it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 05/07/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
# customer intent: I want to learn how to use the Azure AI Foundry SDK to build AI applications on Azure.
---

# Azure AI Foundry SDK client libraries

The Azure AI Foundry SDK is a comprehensive toolchain designed to simplify the development of AI applications on Azure. It enables developers to:

- Access popular models from various model providers through a single interface
- Easily combine together models, data, and AI services to build AI-powered applications
- Evaluate, debug, and improve application quality & safety across development, testing, and production environments

The Azure AI Foundry SDK is a set of client libraries and services designed to work together. 

## Prerequisites

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* [Create a project](../create-projects.md) if you don't have one already.
* Sign in with the Azure CLI using the same account that you use to access your AI Project:

    ```bash
    az login
    ```

## Unified Projects client library

The Azure AI Foundry Projects client library is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.


To install the project client library:

# [C++](#tab/cpp)

Install info

# [C#](#tab/csharp)

Install info

# [Go](#tab/go)

Install info

# [Java](#tab/java)

Install info

# [JavaScript](#tab/javascript)

Install info

# [Objective-C](#tab/objectivec)

Install info

# [Python](#tab/python)

```bash
pip install azure-ai-projects azure-ai-identity
```

[Swift](#tab/swift)

Install info

---

Create a project client in code:

# [C++](#tab/cpp)

Client info

# [C#](#tab/csharp)

Client info

# [Go](#tab/go)

Client info

# [Java](#tab/java)

Client info

# [JavaScript](#tab/javascript)

Client info

# [Objective-C](#tab/objectivec)

Client info

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient.from_connection_string(
  endpoint="your_project_endpoint",
  credential=DefaultAzureCredential())
```

# [Swift](#tab/swift)

Client info

---

**Copy** the the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value above.


Using the project endpoint, you can:
 - [Use Foundry Model](../../quickstarts/get-started-code.md), including Azure OpenAI
 - [Use Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
 - [Run evaluations in the cloud](../../../ai-services/openai/how-to/evaluations?context=/azure/ai-foundry/context/context)
 - [Enable tracing for your app](../../concepts/trace.md) 
 - Retrieve endpoints and keys for external resource connections

## Azure AI Services client libraries

To use Azure AI services, you can use the following client libraries with the endpoints listed on the project homepage.

# [C++](#tab/cpp)

[!INCLUDE [C++ include](../../includes/sdk/cpp.md)]

# [C#](#tab/csharp)

[!INCLUDE [C# include](../../includes/sdk/csharp.md)]

# [Go](#tab/go)

[!INCLUDE [Go include](../../includes/sdk/go.md)]

# [Java](#tab/java)

[!INCLUDE [Java include](../../includes/sdk/java.md)]

# [JavaScript](#tab/javascript)

[!INCLUDE [JavaScript include](../../includes/sdk/javascript.md)]

# [Objective-C](#tab/objectivec)

[!INCLUDE [ObjectiveC include](../../includes/sdk/objective-c.md)]

# [Python](#tab/python)

[!INCLUDE [Python include](./../../includes/sdk/python.md)]

# [Swift](#tab/swift)

[!INCLUDE [Swift include](../../includes/sdk/swift.md)]

---

Next step
[Get started with Azure AI Foundry](../../quickstarts/get-started-code.md)