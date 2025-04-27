---
title: Build an agentic retrieval solution
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/30/2025
---

# Build an agent-to-agent retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article describes an approach or pattern for building a solution that uses Azure AI Search for data retrieval and how to integrate the retrieval into a custom solution.

## Development tasks

Development tasks on the Azure AI Search side include:

+ Create an agent on Azure AI Search that maps to your deployed model in Azure AI Foundry Model.
+ Call the retriever and provide a query, conversation, and override parameters.
+ Parse the response for the parts you want to include in your chat application. For many scenarios, just the content portion of the response is sufficient.

## Components of the solution

Your custom application makes API calls to Azure AI Search and Azure SDK.

+ External data from anywhere
+ Azure AI Search, hosting indexed data and the agentic data retrieval engine
+ Azure AI Foundry Model, providing a chat model (an LLM) for user interaction
+ Azure SDK with a Foundry project, providing programmatic access to chat and chat history

Agentic retrieval on Azure AI Search calls:

+ LLM on Azure AI Foundry Model for query planning

<!-- ## Setting up Azure AI Agent service

This step includes the basics for setting up. Link to their docs.

## Setting up an Azure AI agent

How to create a tool that connects to agent to agentic retrieval.

## Running your Azure AI agent
 -->
<!-- 
### How to customize grounding data

include reference data brings back retrievable index data. Similar to classic search. customizable.

response.content output is semantic fields and semantic config determines output.

## Create the project

The canonical use case for agentic retrieval is through the Agent service. We recommend it because it's the easiest way to create a chatbot.

An agent-to-agent solution combines Azure AI Search with Foundry projects that you use to build custom agents. An agent service handles a lot of common problems,such as tracking conversation history and calling other tools.

### Order of operations

1. Call this.
1. Call that.
1. Pass the content string from the agent to the chat model. You shouldn't need to parse or serialize the string.

## Tips for improving performance

summarizing message threads
use gpt mini

## How to design a prompt

The prompt sent to the LLM includes instructions for working with the grounding data, which is passed as a large single string with no serialization or structure.

What does the prompt look like

## Control the number of subqueries

The LLM will determine some quantity of subqueries based on the user query and chat history.

You as the developer can control by setting default max docs.

this is verbatim but it's only partially true because it's clear the LLM is creating subqueries based on other things
The best way to control the number of subqueries that are generated is by setting the `defaultMaxDocsForReranker` in either the agent definition or as an override on the retrieve action. The semantic ranker processes up to 50 documents as an input. If you only wanted two subqueries, you could set `defaultMaxDocsForReranker` to 100.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the `defaultMaxDocsForReranker` threshold.

## Control the number of threads in chat history

An agent object in Azure AI Search acquires chat history through API calls to the Azure Evaluations SDK, which maintains the thread history. You can filter this list to get a subset of the messages, for example the last 5 conversation turns.

## Control costs and limit operations

Look at output tokens in the [activity array](search-agentic-retrieval-how-to-retrieve.md#review-the-activity-array). -->

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)\
