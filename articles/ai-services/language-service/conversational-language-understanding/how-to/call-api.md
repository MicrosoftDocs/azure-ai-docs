---
title: Send prediction requests to a conversational language understanding deployment
titleSuffix: Foundry Tools
description: Learn about sending prediction requests for conversational language understanding.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/17/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# Send prediction requests to a deployment

After the deployment is added successfully, you can query the deployment for intent and entities predictions from your utterance based on the model you assigned to the deployment.
You can query the deployment programmatically through the [prediction API](https://aka.ms/ct-runtime-swagger) or through the client libraries (Azure SDK).

## Test deployed model

Once your model is deployed, you can test it by sending prediction requests to evaluate its performance with real utterances. Testing helps you verify that the model accurately identifies intents and extracts entities as expected before integrating it into your production applications. You can test your deployment using either the REST API or the Azure SDK client libraries.

###  Send a conversational language understanding request

First you need to get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

### Query your model

[!INCLUDE [Query model](../includes/rest-api/query-model.md)]


You can also use the client libraries provided by the Azure SDK to send requests to your model.

> [!NOTE]
> The client library for conversational language understanding is only available for:
> * .NET
> * Python

1. Go to your resource overview page in the [Azure portal](https://portal.azure.com/#home)

1. From the menu on the left side, select **Keys and Endpoint**. Use endpoint for the API requests and you need the key for `Ocp-Apim-Subscription-Key` header.

    :::image type="content" source="../../custom-text-classification/media/get-endpoint-azure.png" alt-text="A screenshot showing a key and endpoint in the Azure portal." lightbox="../../custom-text-classification/media/get-endpoint-azure.png":::


1. Download and install the client library package for your language of choice:

    | Language | Package version |
    |--|--|
    | .NET | [1.0.0](https://www.nuget.org/packages/Azure.AI.Language.Conversations/1.0.0) |
    | Python | [1.0.0](https://pypi.org/project/azure-ai-language-conversations/1.0.0) |

1. After you install the client library, use the following samples on GitHub to start calling the API.

    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Language.Conversations_1.0.0/sdk/cognitivelanguage/Azure.AI.Language.Conversations)
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-language-conversations_1.0.0/sdk/cognitivelanguage/azure-ai-language-conversations)

1. For more information, *see* the following reference documentation:

    * [C#](/dotnet/api/azure.ai.language.conversations)
    * [Python](/python/api/azure-ai-language-conversations/azure.ai.language.conversations.aio)

## Next steps

* [Conversational language understanding overview](../overview.md)
