---
title: How to send requests to orchestration workflow
titleSuffix: Foundry Tools
description: Learn about sending requests for orchestration workflow.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.devlang: csharp
# ms.devlang: csharp, python
ms.custom: language-service-clu
---
# Query deployment for intent predictions

After the deployment is added successfully, you can query the deployment for intent and entities predictions from your utterance based on the model you assigned to the deployment.
You can query the deployment programmatically [Prediction API](https://aka.ms/ct-runtime-swagger) or through the [Client libraries (Azure SDK)](#use-the-client-libraries-azure-sdk).

## Test deployed model

First you need to get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

### Query your model

[!INCLUDE [Query model](../includes/rest-api/query-model.md)]

# [Client libraries (Azure SDK)](#tab/azure-sdk)

First you need to get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

### Use the client libraries (Azure SDK)

You can also use the client libraries provided by the Azure SDK to send requests to your model.

> [!NOTE]
> The client library for conversational language understanding is only available for:
> * .NET
> * Python

1. Go to your resource overview page in the [Azure portal](https://portal.azure.com/#home)

1. From the menu on the left side, select **Keys and Endpoint**. Use endpoint for the API requests and you will need the key for `Ocp-Apim-Subscription-Key` header.

    :::image type="content" source="../../custom-text-classification/media/get-endpoint-azure.png" alt-text="Screenshot showing how to get the Azure endpoint." lightbox="../../custom-text-classification/media/get-endpoint-azure.png":::

1. Download and install the client library package for your language of choice:

    |Language  |Package version  |
    |---------|---------|
    |.NET     | [1.0.0](https://www.nuget.org/packages/Azure.AI.Language.Conversations/1.0.0)        |
    |Python     | [1.0.0](https://pypi.org/project/azure-ai-language-conversations/1.0.0)         |

1. After you've installed the client library, use the following samples on GitHub to start calling the API.

    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Language.Conversations_1.0.0/sdk/cognitivelanguage/Azure.AI.Language.Conversations)
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-language-conversations_1.0.0/sdk/cognitivelanguage/azure-ai-language-conversations)

1. See the following reference documentation for more information:

    * [C#](/dotnet/api/azure.ai.language.conversations)
    * [Python](/python/api/azure-ai-language-conversations/azure.ai.language.conversations.aio)

---

## Next steps

* [Orchestration workflow overview](../overview.md)
