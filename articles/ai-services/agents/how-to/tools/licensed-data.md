---
title: 'How to use Agents with your licensed data'
titleSuffix: Azure AI services
description: Learn how to connect your licensed data for grounding with Azure AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 12/03/2024
author: aahill
ms.author: aahi
zone_pivot_groups: selection-agents-licenced-data
recommendations: false
---

# Bring your licensed data

::: zone pivot="overview"

Azure AI Agent Service integrates your own licensed data from specialized data providers, 
such as Tripadvisor. Enhance the quality of your agent's responses with high-quality, fresh data, 
such as travel guidance and reviews. These insights empower your agents to deliver nuanced, informed 
solutions tailored to specific use cases.

Tripadvisor is the first licensed data provider and you can ground with your licensed Tripadvisor data through the API, SDK, and Azure AI Foundry portal. 

> [!IMPORTANT]
> 1. You are responsible for obtaining license from licensed data provider and bring your license to authorize the connection with the licensed data.
> 2. Grounding with licensed data will incur usage with licensed data providers, please review the pricing plan with your selected licensed data providers.

::: zone pivot="tripadvisor"

## Prerequisites

* Obtain an API key for your [Tripadvisor developer account](https://www.tripadvisor.com/developers?screen=credentials)

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
   1. Set the connection name to your connection name. You'll use this connection name when you in your sample code later.
   1. For the **Access** setting you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the connection string of the project you entered has access to this connection.

   :::image type="content" source="../../media/tools/licensed-data/connect-custom-resource.png" alt-text="A screenshot showing the screen for adding Tripadvisor connection information." lightbox="../../media/tools/licensed-data/connect-custom-resource.png":::

## Use OpenAPI spec to connect with your licensed data

You can apply the OpenAPI Spec tool to connect with your licensed data.

::: zone-end

