---
title: 'How to use Agents with your licensed data'
titleSuffix: Azure AI Foundry
description: Learn how to connect your licensed data for grounding with Azure AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 03/04/2025
author: aahill
ms.author: aahi
recommendations: false
---

# Use Tripadvisor data to ground your AI agents

Azure AI Agent Service lets you integrate licensed data from specialized data providers to enhance the quality of your agent's responses with high-quality, fresh data. [Tripadvisor](https://tripadvisor-content-api.readme.io/reference/overview) is a useful travel platform that can, for example, provide travel guidance and reviews. The insights from this data source can empower your agents to deliver nuanced, informed solutions tailored to specific use cases.

> [!IMPORTANT]
> - Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data.
> - Grounding with licensed data incurs usage with licensed data providers, review the pricing plan with your selected licensed data providers.

## Prerequisites

* Obtain an API key for your [Tripadvisor developer account](https://www.tripadvisor.com/developers?screen=credentials).
* Make sure when you put 0.0.0.0/0 for the IP address restriction to allow traffic from Azure AI Agent Service.

[!INCLUDE [licensed-data-setup](../../includes/licensed-data-setup.md)]

## Use your tool in code

You can follow the instructions in [OpenAPI spec tool](./openapi-spec.md) to connect your tool through the OpenAPI spec.

1. Remember to store and import your Tripadvisor OpenAPI spec. You can find it in the Azure AI Foundry portal.

1. Make sure you have updated the authentication method to be `connection` and fill in the connection ID of your custom key connection.

   ``` python
   auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
   ```
    
   > [!TIP]
   > Your connection ID will have the following format:`/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.CognitiveService/account/{project name}/connections/{connection name}`  