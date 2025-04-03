---
title: 'How to use Agents with your licensed data'
titleSuffix: Azure AI services
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

# Bring your licensed data

Azure AI Agent Service integrates your own licensed data from specialized data providers, 
such as Tripadvisor. This integration enhances the quality of your agent's responses with high-quality, fresh data, 
such as travel guidance and reviews. These insights empower your agents to deliver nuanced, informed 
solutions tailored to specific use cases.

Tripadvisor is the first licensed data provider and you can ground with your licensed Tripadvisor data through the API, SDK, and Azure AI Foundry portal. 

> [!IMPORTANT]
> - Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data.
> - Grounding with licensed data incurs usage with licensed data providers, review the pricing plan with your selected licensed data providers.

## Prerequisites

* Obtain an API key for your [Tripadvisor developer account](https://www.tripadvisor.com/developers?screen=credentials).

## Setup
1. Go to [Azure AI Foundry portal](https://ai.azure.com/) and select your AI Project. Select **Management Center**.
   
   :::image type="content" source="../../media/tools/licensed-data/project-assets.png" alt-text="A screenshot showing the selectors for the management center for an AI project." lightbox="../../media/tools/licensed-data/project-assets.png":::

1. Select **+new connection** in the settings page.

   :::image type="content" source="../../media/tools/licensed-data/connected-resources.png" alt-text="A screenshot showing the connections for the selected AI project." lightbox="../../media/tools/licensed-data/connected-resources.png":::
   
1. Select **custom keys** in **other resource types**.

   :::image type="content" source="../../media/tools/licensed-data/custom-keys.png" alt-text="A screenshot showing the custom key option in the settings page." lightbox="../../media/tools/licensed-data/custom-keys.png":::

1. Enter the following information to create a connection to store your Tripadvisor key:
   1. Set **Custom keys** to "key", with the value being your Tripadvisor API key.
   1. Make sure **is secret** is checked.
   1. Set the connection name to your connection name. You use this connection name in your sample code or Foundry Portal later.
   1. For the **Access** setting, you can choose either *this project only* or *shared to all projects*. Just make sure in your code, the connection string of the project you entered has access to this connection.

   :::image type="content" source="../../media/tools/licensed-data/connect-custom-resource.png" alt-text="A screenshot showing the screen for adding Tripadvisor connection information." lightbox="../../media/tools/licensed-data/connect-custom-resource.png":::

## Use Tripadvisor tool through Foundry portal

1. To use the Tripadvisor tool in the Azure AI Foundry, in the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **action**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Tripadvisor** and follow the prompts to add the tool. 

   :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing available knowledge tools." lightbox="../../media/tools/knowledge-tools-list.png":::

1. Give a name for your Tripadvisor tool and provide an optional description.
 
    :::image type="content" source="../../media/tools/licensed-data/add-data-source.png" alt-text="A screenshot showing the Tripadvisor data source." lightbox="../../media/tools/licensed-data/add-data-source.png":::

1. Select the custom key connection you just created. 

    :::image type="content" source="../../media/tools/licensed-data/add-connection.png" alt-text="A screenshot showing the connection for your Tripadvisor tool, and a JSON example." lightbox="../../media/tools/licensed-data/add-connection.png":::

1. Finish and start chatting.

## Connect Tripadvisor through code-first experience

You can follow the instructions in [OpenAPI Spec tool](./openapi-spec.md) to connect Tripadvisor through OpenAPI spec.

1. Remember to store and import Tripadvisor OpenAPI spec. You can find it through Foundry Portal.

1. Make sure you have updated the authentication method to be `connection` and fill in the connection ID of your custom key connection.
   ``` python
   auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
   ```
