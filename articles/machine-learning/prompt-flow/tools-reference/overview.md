---
title: Overview of tools in prompt flow
titleSuffix: Azure Machine Learning
description: This overview of the tools in prompt flow includes an index table for tools and the instructions for custom tool package creation and tool package usage.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: reference
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenjieting
ms.date: 10/24/2023
---

# Overview of tools in prompt flow

This page provides an overview of the tools that are available in prompt flow. It also offers instructions on how to create your own custom tool and how to install custom tools.

## An index of tools

The following table shows an index of tools in prompt flow.

| Tool (set) name | Description | Environment | Package name |
|------|-----------|-------------|--------------|
| [Python](./python-tool.md) | Runs Python code. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [LLM](./llm-tool.md) | Uses OpenAI's large language model (LLM) for text completion or chat. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Prompt](./prompt-tool.md) | Crafts a prompt by using Jinja as the templating language. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Embedding](./embedding-tool.md) | Uses OpenAI's embedding model to create an embedding vector that represents the input text. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Open Model LLM](./open-model-llm-tool.md) | Enable the utilization of a variety of Open Model and Foundational Models, such as Falcon and Llama 2 from the Azure Model catalog. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Serp API](./serp-api-tool.md) | Uses Serp API to obtain search results from a specific search engine. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Content Safety (Text)](./content-safety-text-tool.md) | Uses Azure Content Safety to detect harmful content. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Azure OpenAI GPT-4 Turbo with Vision](./azure-open-ai-gpt-4v-tool.md) | Use AzureOpenAI GPT-4 Turbo with Vision model deployment to analyze images and provide textual responses to questions about them. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [OpenAI GPT-4V](./openai-gpt-4v-tool.md) | Use OpenAI GPT-4V to leverage vision ability. | Default | [promptflow-tools](https://pypi.org/project/promptflow-tools/) |
| [Index Lookup](./index-lookup-tool.md)*<sup>1</sup> | Search an Azure Machine Learning Vector Index for relevant results using one or more text queries. | Default | [promptflow-vectordb](https://pypi.org/project/promptflow-vectordb/) |
| [Azure AI Language tools](https://microsoft.github.io/promptflow/integrations/tools/azure-ai-language-tool.html)* | This collection of tools is a wrapper for various Azure AI Language APIs, which can help effectively understand and analyze documents and conversations. The capabilities currently supported include: Abstractive Summarization, Extractive Summarization, Conversation Summarization, Entity Recognition, Key Phrase Extraction, Language Detection, PII Entity Recognition, Conversational PII, Sentiment Analysis, Conversational Language Understanding, Translator. You can learn how to use them by the [Sample flows](https://github.com/microsoft/promptflow/tree/e4542f6ff5d223d9800a3687a7cfd62531a9607c/examples/flows/integrations/azure-ai-language). | Custom | [promptflow-azure-ai-language](https://pypi.org/project/promptflow-azure-ai-language/) |
| [Rerank](./rerank-tool.md) | Rerank documents based on the relevancy to a given query | Default | [promptflow-vectordb](https://pypi.org/project/promptflow-vectordb/) |

<sup>1</sup> The Index Lookup tool replaces the three deprecated legacy index tools: Vector Index Lookup, Vector DB Lookup, and Faiss Index Lookup. If you have a flow that contains one of those tools, follow the [migration steps](./index-lookup-tool.md#how-to-migrate-from-legacy-tools-to-the-index-lookup-tool) to upgrade your flow.

_*The asterisk marks indicate custom tools, which are created by the community that extend prompt flow's capabilities for specific use cases. They aren't officially maintained or endorsed by prompt flow team. When you encounter questions or issues for these tools, prioritize using the support contact if it's provided in the description._

To discover more custom tools developed by the open-source community, see [More custom tools](https://microsoft.github.io/promptflow/integrations/tools/index.html). 
  
## Remarks

- If existing tools don't meet your requirements, you can [develop your own custom tool and make a tool package](https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/create-and-use-tool-package.html). 
- To install custom tools or add more tools to the custom environment, see [Custom tool package creation and usage](../how-to-custom-tool-package-creation-and-usage.md) to start compute session. Then the tools can be displayed in the tool list.
