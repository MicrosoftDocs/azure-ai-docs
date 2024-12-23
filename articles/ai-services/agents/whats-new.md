---
title: What's new in Azure AI Agent Service?
titleSuffix: Azure AI services
description: Learn about new feature updates and additions for your AI Agents.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: overview
ms.date: 12/11/2024
ms.custom: azure-ai-agents
---

# What's new in Azure AI Agent Service

This article provides a summary of the latest releases and major documentation updates for Azure AI Agent Service.

## December 2024

### Azure AI Service public preview

Azure AI Service is now available in preview. The service builds off of the [Assistants API](../openai/how-to/assistant.md) in Azure OpenAI, and offers several additional features, such as:

* Several [additional tools](./how-to/tools/overview.md) to enhance your AI agents' functionality, such as the ability to use Bing and as a knowledge source and call functions. 
* The ability to use non Azure OpenAI [models](./concepts/model-region-support.md#more-models): 
    * Llama 3.1-70B-instruct
    * Mistral-large-2407    
    * Cohere command R+
* Enterprise ready security with secure data handling, keyless authentication, and no public egress.
* The ability to either use Microsoft-managed storage, or bring your own.
* SDK support for:
    * [.NET](./quickstart.md?pivots=programming-language-csharp) 
    * [The Azure Python SDK](./quickstart.md?pivots=programming-language-python-azure)  
    * [The OpenAI Python SDK](./quickstart.md?pivots=programming-language-python-openai)   
* Debugging support using [tracing with Application Insights](./concepts/tracing.md)

## Next steps

Use the [quickstart article](./quickstart.md) to get started creating a new AI Agent.
