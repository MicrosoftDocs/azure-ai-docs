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
recommendations: false
---
# Bring your licensed data

::: zone pivot="overview"

Azure AI Agent Service integrates your own licensed data from specialized data providers, 
such as Tripadvisor. Enhance the quality of your agent’s responses with high-quality, fresh data, 
such as travel guidance and reviews. These insights empower your agents to deliver nuanced, informed 
solutions tailored to specific use cases.

We have enabled **Tripadvisor** as the first licensed data provider and you can ground with your licensed 
Tripadvisor data through API, SDK and Azure AI Foundry Portal. 

> [!IMPORTANT]
> 1. You are responsible for obtaining license from licensed data provider and bring your license to authorize the connection with the licensed data.
> 2. Grounding with licensed data will incur usage with licensed data providers, please review the pricing plan with your selected licensed data providers.

::: zone pivot="Tripadvisor"
## Prerequisie
1. Obtain an API key for your [Tripadvisor developer account](https://www.tripadvisor.com/developers?screen=credentials)

## Setup
1. Go to [Azure AI Foundry Portal](https://ai.azure.com/) and select the AI Project. Click **Management Center**
   
   ![image](https://github.com/user-attachments/assets/ada3e517-b258-462d-92ca-73cd9768a8c4)

1. Select **+new connection** in the settings page.

  ![image](https://github.com/user-attachments/assets/152669bf-fd56-4824-b2ed-9084f5e5e923)
   
1. Select **custom keys** in **other resource types**.

   ![image](https://github.com/user-attachments/assets/75f740f8-d884-4430-99d0-8c904aeacb46)

1. Enter the following information to create a connection to store your Tripadvisor key

   - Click to add a new key-value pair
   - key: "key"
   - value: Your Tripadvisor API key
   - check `is secret`
   - Connection name: `YOUR_CONNECTION_NAME` (You will use this connection name in the sample code below.
   - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.
  ![image](https://github.com/user-attachments/assets/8e64d7cb-7ced-4f47-9e3b-d4a531a1651e)

## Use OpenAPI Spec to connect with your licensed data
You can leverage OpenAPI Spec tool to connect with your licensed data.
::: zone-end

