---
title: 'How to connect the Azure Speech tool to an agent'
titleSuffix: Microsoft Foundry
description: Learn how to use Agents Azure Speech in Foundry Tools tool.
services: azure-ai-speech
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 09/12/2025
author: PatrickFarley
ms.author: pafarley
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
---

# Azure Speech in Foundry Tools MCP server

The Azure Speech in Foundry Tools tool allows agents to interact with users through speech. By integrating this model context protocol (MCP), AI agents can convert text responses into spoken words and process spoken user inputs into text.

> [!IMPORTANT]
> The speech MCP tool doesn't support [Network-secured Microsoft Foundry](/azure/ai-foundry/agents/how-to/virtual-networks). For more information, see [Connect to an MCP server](/azure/ai-foundry/agents/how-to/tools/model-context-protocol).

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) created in a [supported region](../../../../ai-services/speech-service/regions.md). Your Foundry resource includes speech capabilities and will be used by the Speech MCP server

## Set up storage

You need an Azure Storage account to store input audio files for speech-to-text processing and receive output audio files from text-to-speech processing. [Create an Azure blob storage account](/azure/storage/common/storage-account-create?tabs=azure-portal). 

Ensure your user account has the **Storage Blob Data Contributor** role assigned for the storage account, so you can create SAS URLs later on.

Create one or more blob containers to store the input and output audio files.

## Create an agent

1. Go to the [!INCLUDE [foundry-link](../../../default/includes/foundry-link.md)].
1. In the top right menu, go to **Build**
1. On the left pane, select **Agents**, and select the **Create agent** button.  
1. Create a new agent by providing a name and description, then select **Create**. You don't need to configure your agent any further for this scenario.


## Connect the Azure Speech tool to your agent

1. Go on to the Agent playground. Under the **Tools** section in the playground, select **Add** -> **Add a new tool**.
1. In the **Select a tool** dialog, go to the **Catalog** tab. Search for and select Azure Speech MCP Server, then select **Create**.
1. On the setup page, fill in the following fields:  

    - Parameters -> `foundry-resource-name`: Enter the name of the Foundry resource you created in the Prerequisites section. 
    - Authorization -> `Bearer` (API Key): Enter the API key from your Foundry resource. You can use either KEY1 or KEY2 from the **Keys and Endpoint** section of your resource's page in the Azure portal. 
    - Authorization -> `X-Blob-Container-Url`: Generate a SAS URL for your storage container, with read and write permissions, and enter it here. This location is where the service will store audio output files.
    
1. Select **Connect** to add the remote Speech MCP server as a tool for your agent.

## Test the Azure Speech tool

Stay in the agent playground, and in the agent chat window, type `What can you do?`

> [!TIP]
> Select gpt-4.1 as the agent's base model for best results. 

The agent lists its available capabilities, including the newly added Speech Capabilities such as speech-to-text and text-to-speech. This confirms that the remote Speech MCP server is successfully connected.

### Test the speech to text capability

The Speech tool supports converting an audio file into text. The audio input file can be stored in Azure blob storage and accessible with a SAS URL, or it can be any publicly accessible URL to an audio file. Follow these steps to test speech to text:

1. Upload your audio file to your Azure blob storage container.  
1. Generate a SAS URL for the specific file: Select your uploaded audio file and go to the **Properties** section. Select **Generate SAS**. Adjust the URL's expiration time if necessary. Select **Generate SAS token and URL**. 
1. Copy the SAS URL. Then use it in one of the following example prompts in the agent chat window: 
    - `Recognize this English audio file located in <blob SAS URL>` 
    - `Recognize the audio file located in <blob SAS URL> with these phrase hints: "Azure, OpenAI, Cognitive Services, Lucy" to improve accuracy.` 
    - `Convert this audio file located in <blob SAS URL> into text and summarize it for me.` 
    - `Recognize this French audio file located in <blob SAS URL> with detailed output format.` 
    - `Recognize this Hindi audio file located in <blob SAS URL> and remove profanity.` 
1. View the output text in the chat window.

### Test text to speech capability 

Start a new chat in the agent playground, and use one of the following example prompts in the agent chat window, adding your own sample text where indicated: 
- `Convert text to speech: <your text to speak>` 
- `Synthesize speech from "<your text to speak>"`
- `Generate speech audio from text "<your text to speak>"` 
- `Convert text to speech with Chinese language: <your text to speak>` 
- `Synthesize speech with voice en-US-JennyNeural from text <your text to speak>` 

An audio link is displayed in the chat window (its source is in your blob storage container). Select it to listen to the output.