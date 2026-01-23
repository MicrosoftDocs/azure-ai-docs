---
title: What is Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Learn how to integrate AI into your applications that can extract information and understand written language.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
---
# What is Azure Language in Foundry Tools?

Azure Language is a cloud-based service that provides Natural Language Processing (NLP) features for understanding and analyzing text. Use this service to help build intelligent applications using the web-based Microsoft Foundry, REST APIs, and client libraries. For AI agent development, the service capabilities are also available as tools in Azure Language [MCP server](#azure-language-mcp-server-), which is available both as a remote server in the **Microsoft Foundry Tool Catalog** and as a local server for self-hosted environments.

## Available tools

Azure Language provides specialized tools that enable seamless integration between AI agents and language processing services through standardized protocols.

### Azure Language MCP server 🆕

The MCP (Model Context Protocol) server creates a standardized bridge that connects AI agents directly to Azure Language services through industry-standard protocols. This integration enables developers to build sophisticated conversational applications with reliable natural language processing capabilities while ensuring enterprise-grade compliance, data protection, and processing accuracy throughout their AI workflows. 

Azure Language provides both remote and local MCP server options:
* **Remote server**: Available through Foundry Tool Catalog for cloud-hosted deployments.
* **Local server**: Available for developers who prefer to host the server in their own environment.

For more information, *see* [Azure Language MCP server](concepts/foundry-tools-agents.md#azure-language-mcp-server-preview).

## Available agents

Azure Language offers prebuilt agents that handle specific conversational AI scenarios with built-in governance, routing logic, and quality control mechanisms.

### Azure Language Intent Routing agent 🆕

The Intent Routing agent intelligently manages conversation flows by understanding user intentions and delivering accurate responses in conversational AI applications. This agent uses predictable decision-making processes combined with controlled response generation to ensure consistent, reliable interactions that organizations can trust and monitor. 

For more information, *see* [Azure Language Intent Routing agent](concepts/foundry-tools-agents.md#azure-language-intent-routing-agent-preview).

### Azure Language Exact Question Answering agent 🆕

The Exact Question Answering agent provides reliable, word-for-word responses to your most important business questions. This agent automates frequently asked questions while maintaining human oversight and quality control to ensure accuracy and compliance.

For more information, *see* [Azure Language Exact Question Answering agent](concepts/foundry-tools-agents.md#azure-language-exact-question-answering-agent-preview).

## Available features

> [!TIP]
> Unsure which feature to use? See [Which Language feature should I use](#which-language-feature-should-i-use) to help you decide.

[**Microsoft Foundry**](https://ai.azure.com/) enables you to use most of the following service features without the need to write code.

### Named Entity Recognition (NER)

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/named-entity-recognition.png" alt-text="A screenshot of named entity recognition in Foundry." lightbox="media/overview/named-entity-recognition.png":::
   :::column-end:::
   :::column span="":::
      [Named entity recognition](./named-entity-recognition/overview.md) identifies different entries in text and categorizes them into predefined types.

   :::column-end:::
:::row-end:::

### Personal and health data information detection

> [!IMPORTANT]
> The Azure Language in Foundry Tools Text Personally Identifiable Information (PII) detection anonymization feature (synthetic replacement) is currently available in `preview` and licensed to you as part of your Azure subscription. Your use of this feature is subject to the terms applicable to **Previews** as described in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms) and the [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/microsoft-products-and-services-data-protection-addendum-dpa).

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/conversation-pii.png" alt-text="A screenshot of conversation personally identifying information in Foundry." lightbox="media/overview/conversation-pii.png":::
      :::image type="content" source="media/overview/text-pii.png" alt-text="A screenshot of text personally identifying information in Foundry." lightbox="media/overview/text-pii.png":::
   :::column-end:::
   :::column span="":::

      [Personally Identifiable Information (PII) detection](./personally-identifiable-information/overview.md) identifies entities in text and conversations (chat or transcripts) that are associated with individuals.

   :::column-end:::
:::row-end:::

### Language detection

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/language-detection.png" alt-text="A screenshot of language detection in Foundry." lightbox="media/overview/language-detection.png":::
   :::column-end:::
   :::column span="":::
      [Language detection](./language-detection/overview.md) evaluates text and detects a wide range of languages and variant dialects.

   :::column-end:::
:::row-end:::

### Sentiment Analysis and opinion mining

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/sentiment-analysis.png" alt-text="A screenshot of sentiment analysis in Foundry." lightbox="media/overview/sentiment-analysis.png":::
   :::column-end:::
   :::column span="":::
      [Sentiment analysis and opinion mining](./sentiment-opinion-mining/overview.md) preconfigured features that help you understand public perception of your brand or topic. These features analyze text to identify positive or negative sentiments and can link them to specific elements within the text.

   :::column-end:::
:::row-end:::

### Summarization

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/conversation-summarization.png" alt-text="A screenshot of conversation summarization  in Foundry." lightbox="media/overview/conversation-summarization.png":::
      :::image type="content" source="media/overview/call-center-summarization.png" alt-text="A screenshot of call center summarization in Foundry." lightbox="media/overview/call-center-summarization.png":::
      :::image type="content" source="media/overview/text-summarization.png" alt-text="A screenshot of text summarization in Foundry." lightbox="media/overview/text-summarization.png":::
   :::column-end:::
   :::column span="":::
      [Summarization](./summarization/overview.md) condenses information for text and conversations (chat and transcripts).
      Text summarization generates a summary, supporting two approaches: Extractive summarization creates a summary by selecting key sentences from the document and preserving their original positions. In contrast, abstractive summarization generates a summary by producing new, concise, and coherent sentences or phrases that aren't directly copied from the original document.
Conversation summarization recaps and segments long meetings into timestamped chapters. Call center summarization summarizes customer issues and resolution.
   :::column-end:::
:::row-end:::

### Key phrase extraction

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/key-phrase-extraction.png" alt-text="A screenshot of key phrase extraction in Foundry." lightbox="media/overview/key-phrase-extraction.png":::
   :::column-end:::
   :::column span="":::
      [Key phrase extraction](./key-phrase-extraction/overview.md) is a preconfigured feature that evaluates and returns the main concepts in unstructured text, and returns them as a list.
   :::column-end:::
:::row-end:::

### Entity linking

> [!IMPORTANT]
> Entity Linking is retiring from Azure Language in Foundry Tools effective **September 1, 2028**. After this date, the Entity Linking feature is no longer supported.   During the support window, we recommend that users migrate existing workloads and direct all new projects to Azure Language [**Named Entity Recognition**](named-entity-recognition/overview.md) or consider other alternative solutions.


:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/entity-linking.png" alt-text="A screenshot of an entity linking example." lightbox="media/studio-examples/entity-linking.png":::
   :::column-end:::
   :::column span="":::
      [Entity linking](./entity-linking/overview.md) is a preconfigured feature that disambiguates the identity of entities (words or phrases) found in unstructured text and returns links to Wikipedia.
   :::column-end:::
:::row-end:::

### Text analytics for health

:::row:::
   :::column span="":::
      :::image type="content" source="media/overview/text-analytics-for-health.png" alt-text="A screenshot of text analytics for health in Foundry." lightbox="media/overview/text-analytics-for-health.png":::
   :::column-end:::
   :::column span="":::
      [Text analytics for health](./text-analytics-for-health/overview.md) Extracts and labels relevant health information from unstructured text.
   :::column-end:::
:::row-end:::

### Custom text classification

:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/single-classification.png" alt-text="A screenshot of a custom text classification example." lightbox="media/studio-examples/single-classification.png":::
   :::column-end:::
   :::column span="":::
      [Custom text classification](./custom-text-classification/overview.md) enables you to build custom AI models to classify unstructured text documents into custom classes you define.
   :::column-end:::
:::row-end:::

### Custom Named Entity Recognition (Custom NER)


:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/custom-named-entity-recognition.png" alt-text="A screenshot of a custom NER example." lightbox="media/studio-examples/custom-named-entity-recognition.png":::
   :::column-end:::
   :::column span="":::
      [Custom NER](custom-named-entity-recognition/overview.md) enables you to build custom AI models to extract custom entity categories (labels for words or phrases), using unstructured text that you provide.
   :::column-end:::
:::row-end:::


### Conversational language understanding

:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/conversational-language-understanding.png" alt-text="A screenshot of a conversational language understanding example." lightbox="media/studio-examples/conversational-language-understanding.png":::
   :::column-end:::
   :::column span="":::
      [Conversational language understanding (CLU)](./conversational-language-understanding/overview.md) enables users to build custom natural language understanding models to predict the overall intention of an incoming utterance and extract important information from it.
   :::column-end:::
:::row-end:::

### Orchestration workflow

:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/orchestration-workflow.png" alt-text="A screenshot of an orchestration workflow example." lightbox="media/studio-examples/orchestration-workflow.png":::
   :::column-end:::
   :::column span="":::
      [Orchestration workflow](./language-detection/overview.md) is a custom feature that enables you to connect [Conversational Language Understanding (CLU)](./conversational-language-understanding/overview.md), [question answering](./question-answering/overview.md), and [LUIS](../LUIS/what-is-luis.md) applications.

   :::column-end:::
:::row-end:::

### Question answering

:::row:::
   :::column span="":::
      :::image type="content" source="media/studio-examples/question-answering.png" alt-text="A screenshot of a question answering example." lightbox="media/studio-examples/question-answering.png":::
   :::column-end:::
   :::column span="":::
      [Question answering](./question-answering/overview.md) is a custom feature that identifies the most suitable answer for user inputs. This feature is typically utilized to develop conversational client applications, including social media platforms, chat bots, and speech-enabled desktop applications.

   :::column-end:::
:::row-end:::

## Which Language feature should I use?

This section helps you decide which Language feature you should use for your application:

|What do you want to do?  |Document format  |Your best solution  | Is this solution customizable?* |
|---------|---------|---------|---------|
| Detect and/or redact sensitive information such as `PII` and `PHI`. | Unstructured text, <br> transcribed conversations | [PII detection](./personally-identifiable-information/overview.md) | |
| Extract categories of information without creating a custom model.     | Unstructured text         | The [preconfigured NER feature](./named-entity-recognition/overview.md) |       |
| Extract categories of information using a model specific to your data. | Unstructured text | [Custom NER](./custom-named-entity-recognition/overview.md) | ✓ |
|Extract main topics and important phrases.     | Unstructured text        | [Key phrase extraction](./key-phrase-extraction/overview.md) |   |
| Determine the sentiment and opinions expressed in text. | Unstructured text | [Sentiment analysis and opinion mining](./sentiment-opinion-mining/overview.md) |  |
| Summarize long chunks of text or conversations. | Unstructured text, <br> transcribed conversations. | [Summarization](./summarization/overview.md) | |
| Disambiguate entities and get links to Wikipedia. | Unstructured text | [Entity linking](./entity-linking/overview.md) | |
| Classify documents into one or more categories. | Unstructured text | [Custom text classification](./custom-text-classification/overview.md) | ✓|
| Extract medical information from clinical/medical documents, without building a model. | Unstructured text | [Text analytics for health](./text-analytics-for-health/overview.md) | |
| Build a conversational application that responds to user inputs. | Unstructured user inputs | [Question answering](./question-answering/overview.md) | ✓ |
| Detect the language that a text was written in. | Unstructured text | [Language detection](./language-detection/overview.md) | |
| Predict the intention of user inputs and extract information from them. | Unstructured user inputs | [Conversational language understanding](./conversational-language-understanding/overview.md) | ✓ |
| Connect apps from conversational language understanding, LUIS, and question answering. | Unstructured user inputs | [Orchestration workflow](./orchestration-workflow/overview.md) | ✓ |

\* If a feature is customizable, you can train an AI model using our tools to fit your data specifically. Otherwise a feature is preconfigured, meaning the AI models it uses can't be changed. You just send your data, and use the feature's output in your applications.

## Tutorials

After you get started with Azure Language quickstarts, try our tutorials that show you how to solve various scenarios.

* [Extract key phrases from text stored in Power BI](key-phrase-extraction/tutorials/integrate-power-bi.md)
* [Use Power Automate to sort information in Microsoft Excel](named-entity-recognition/tutorials/extract-excel-information.md)
* [Use Flask to translate text, analyze sentiment, and synthesize speech](/training/modules/python-flask-build-ai-web-app/)
* [Use Foundry Tools in canvas apps](/powerapps/maker/canvas-apps/cognitive-services-api?context=/azure/ai-services/language-service/context/context)
* [Create an FAQ Bot](question-answering/tutorials/bot-service.md)

## Code samples

You can find more code samples on GitHub for the following languages:

* [C#](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/textanalytics/Azure.AI.TextAnalytics/samples)
* [Java](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/textanalytics/azure-ai-textanalytics/src/samples)
* [JavaScript](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/textanalytics/ai-text-analytics/samples)
* [Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics/samples)

## Deploy on premises using Docker containers
Use Language containers to deploy API features on-premises. These Docker containers enable you to bring the service closer to your data for compliance, security, or other operational reasons. The Language offers the following containers:

* [Sentiment analysis](sentiment-opinion-mining/how-to/use-containers.md)
* [Language detection](language-detection/how-to/use-containers.md)
* [Key phrase extraction](key-phrase-extraction/how-to/use-containers.md)
* [Custom Named Entity Recognition](custom-named-entity-recognition/how-to/use-containers.md)
* [Text Analytics for health](text-analytics-for-health/how-to/use-containers.md)
* [Summarization](summarization/how-to/use-containers.md)

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people affected by it, and the deployment environment. Read the following articles to learn about responsible AI use and deployment in your systems:

* [Transparency note for Azure Language](../../ai-foundry/responsible-ai/language-service/transparency-note.md)
* [Integration and responsible use](../../ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use.md)
* [Data, privacy, and security](../../ai-foundry/responsible-ai/language-service/data-privacy.md)
