---
title: "Azure AI Foundry API & SDK reference"
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to start using the Preview experience of the Azure AI Foundry portal and the Azure AI Foundry SDK.
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 08/20/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - preview
---

# Azure AI Foundry API & SDK reference

This page provides links to SDKs and REST APIs available in Azure AI Foundry.

## Azure AI Projects

- [C#](/dotnet/api/overview/azure/ai.projects-readme)
- [JavaScript](/javascript/api/overview/azure/ai-projects-readme?view=azure-node-preview&preserve-view=true)
- [Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true)
- [REST API](/rest/api/aifoundry/aiprojects/)

## Azure AI Agents

- [C#](/dotnet/api/overview/azure/ai.agents.persistent-readme?view=azure-dotnet-preview&preserve-view=true)
- [Java](/java/api/overview/azure/ai-agents-persistent-readme)
- [JavaScript](/javascript/api/overview/azure/ai-projects-readme?view=azure-node-preview&preserve-view=true)
- [Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true)
- [REST API](/rest/api/aifoundry/aiagents)
- [Data monitoring reference](../../agents/reference/monitor-service.md)

## SDKs & REST APIs (general)

- [Azure AI Evaluation SDK](/python/api/overview/azure/ai-evaluation-readme)
- [Azure AI services SDKs (client library development kit)](../../../ai-services/reference/sdk-package-resources.md?context=/azure/ai-foundry/context/context)
- [Azure AI services REST APIs (swagger)](../../../ai-services/reference/rest-api-resources.md?context=/azure/ai-foundry/context/context)

## Azure AI Model Inference API

- [What is the Model Inference API?](/rest/api/aifoundry/modelinference)
<!-- - [Get Chat Completions](/rest/api/aifoundry/get-chat-completions/get-chat-completions) -->
<!-- - [Get Embeddings](/rest/api/aifoundry/get-embeddings/get-embeddings)
- [Get Image Embeddings](/rest/api/aifoundry/get-image-embeddings/get-image-embeddings) -->

## Azure OpenAI

### v1 APIs

- [v1 Preview API](../../openai/reference-preview-latest.md)
- [v1 API](../../openai/latest.md)

### Pre v1 API

- [GA API reference](../../openai/reference.md)
- [2025-04-01-preview - Authoring](../../openai/authoring-reference-preview.md)
- [2025-04-01-preview - Inference](../../openai/reference-preview.md)

### Assistants API Reference — REST

- [Assistants](../../openai/reference-preview.md#list---assistants)
- [Threads](../../openai/reference-preview.md#create---thread)
- [Messages](../../openai/reference-preview.md#list---messages)
- [Runs](../../openai/reference-preview.md#create---thread-and-run)

### Assistants API Reference — SDK

- [C#](/dotnet/api/overview/azure/ai.openai.assistants-readme?context=/azure/ai-foundry/openai/context/context)
- [Go](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)
- [Java](/java/api/overview/azure/ai-openai-assistants-readme?context=/azure/ai-foundry/openai/context/context)
- [JavaScript](/javascript/api/overview/azure/openai-assistants-readme?context=/azure/ai-foundry/openai/context/context)
- [Python](https://platform.openai.com/docs/api-reference/assistants)

### Azure OpenAI On Your Data API Reference

- [Azure OpenAI On Your Data](../../openai/references/on-your-data.md)
- [Data source - Azure AI Search](../../openai/references/azure-search.md)
- [Data source - Azure Cosmos DB for MongoDB vCore](../../openai/references/cosmos-db.md)
- [Data source - Elasticsearch (preview)](../../openai/references/elasticsearch.md)
- [Data source - Pinecone (preview)](../../openai/references/pinecone.md)
- [Data source - Mongo DB (preview)](../../openai/references/mongo-db.md)
- [Ingestion API (preview)](/rest/api/azureopenai/ingestion-jobs)

### Other Azure OpenAI links

- [ARM/Bicep/Terraform](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep)
- [Azure CLI](/cli/azure/cognitiveservices?view=azure-cli-latest&preserve-view=true)
- [Go](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)
- [Java](/java/api/com.azure.ai.openai?view=azure-java-preview&preserve-view=true)
- [JavaScript](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-secure%2Ccommand&pivots=programming-language-javascript)
- [.NET](/dotnet/api/azure.ai.openai?view=azure-dotnet-preview&preserve-view=true)
- [REST (fine-tuning)](/rest/api/azureopenai/fine-tuning?view=rest-azureopenai-2024-03-01-preview&preserve-view=true)
- [REST (resource creation & deployment)](/rest/api/aiservices/accountmanagement/deployments/create-or-update?tabs=HTTP)
- [Azure OpenAI monitoring data reference](../../openai/monitor-openai-reference.md)
- [Audio events reference](../../openai/realtime-audio-reference.md)
