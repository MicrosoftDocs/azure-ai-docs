---
title: What is summarization?
titleSuffix: Foundry Tools
description: Learn about summarizing text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-summarization, build-2024, ignite-2024
---
# What is summarization?

[!INCLUDE [availability](includes/regional-availability.md)]

Summarization is a feature offered by [Azure Language in Foundry Tools](../overview.md), a combination of generative Large Language models and task-optimized encoder models that offer summarization solutions with higher quality, cost efficiency, and lower latency.
Use this article to learn more about this feature, and how to use it in your applications.

Out of the box, the service provides summarization solutions for three types of genre, plain texts, conversations, and native documents. Text summarization only accepts plain text blocks. Conversation summarization accepts conversational input, including various speech audio signals. Native document summarization accepts documents in their native formats, such as Word, PDF, or plain text. For more information, *see* [Supported document formats](../native-document-support/overview.md#supported-document-formats).

> [!TIP]
> Try out Summarization [in Microsoft Foundry portal](https://ai.azure.com/explore/language). There you can [utilize a currently existing Language Studio resource or create a new Foundry resource](../../../ai-services/connect-services-foundry-portal.md) in order to use this service.

## Capabilities

# [Text summarization](#tab/text-summarization)

This documentation contains the following article types:

* **[Quickstarts](quickstart.md?pivots=rest-api&tabs=text-summarization)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](how-to/text-summarization.md)** contain instructions for using the service in more specific or customized ways.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## Key features for text summarization

Text summarization uses natural language processing techniques to generate a summary for plain texts, which can be from a document, conversation, or any texts. There are two approaches of summarization this API provides:

* [**Extractive summarization**](how-to/text-summarization.md#try-text-extractive-summarization): Produces a summary by extracting salient sentences within the source text, together the positioning information of these sentences.

  * Multiple extracted sentences: These sentences collectively convey the main idea of the input text. They're original sentences extracted from the input text content.
  * Rank score: The rank score indicates how relevant a sentence is to the main topic. Text summarization ranks extracted sentences, and you can determine whether they're returned in the order they appear, or according to their rank.
 For example, if you request a three-sentence summary extractive summarization returns the three highest scored sentences.
  * Positional information: The start position and length of extracted sentences.

* [**Abstractive summarization**](how-to/text-summarization.md#try-text-abstractive-summarization): Generates a summary with concise, coherent sentences or words that aren't verbatim extract sentences from the original source.
  * Summary texts: Abstractive summarization returns a summary for each contextual input range. A long input can be segmented so multiple groups of summary texts can be returned with their contextual input range.
  * Contextual input range: The range within the input that was used to generate the summary text.

As an example, consider the following paragraph of text:

*"At Microsoft, we are on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we achieve human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that's closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."*

The text summarization API request is processed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API is returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response can contain text offsets. For more information, see [how to process offsets](../concepts/multilingual-emoji-support.md).

If we use the preceding example, the API might return these summaries:

**Extractive summarization**:
- "At Microsoft, we are on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding."
- "We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages."
- "The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today."

**Abstractive summarization**:
- "Microsoft is taking a more holistic, human-centric approach to learning and understanding. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. Over the past five years, we achieved human performance on benchmarks in conversational speech recognition."

# [Conversation summarization](#tab/conversation-summarization)

This documentation contains the following article types:

* **[Quickstarts](quickstart.md?pivots=rest-api&tabs=conversation-summarization)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](how-to/conversation-summarization.md)** contain instructions for using the service in more specific or customized ways.

## Key features for conversation summarization

Conversation summarization supports the following features:

* [**Recap**](how-to/conversation-summarization.md#get-recap-and-follow-up-task-summarization): Summarizes a conversation into a brief paragraph.
* [**Issue/resolution summarization**](quickstart.md?tabs=conversation-summarization%2Cwindows&pivots=rest-api#conversation-issue-and-resolution-summarization): Call center specific features that give a summary of issues and resolutions in conversations between customer-service agents and your customers.
* [**Chapter title summarization**](how-to/conversation-summarization.md#get-chapter-titles): Segments a conversation into chapters based on the topics discussed in the conversation, and gives suggested chapter titles of the input conversation.
* [**Narrative summarization**](how-to/conversation-summarization.md#get-narrative-summarization): Generates detail call notes, meeting notes or chat summaries of the input conversation.

As an example, consider the following example conversation:

**Agent**: "*Hello, you're chatting with Rene. How may I help you?*"

**Customer**: "*Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn't work.*"

**Agent**: "*I'm sorry to hear that. Let's see what we can do to fix this issue. Could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking?*"

**Customer**: "*Yes, I pushed the wifi connection button, and now the power light is slowly blinking.*"

**Agent**: "*Great. Thank you! Now, check in your Contoso Coffee app. Does it prompt to ask you to connect with the machine?*"

**Customer**: "*No. Nothing happened.*"

**Agent**: "*I see. Thank you. Let's try if a factory reset can solve the issue. Could you please press and hold the center button for 5 seconds to start the factory reset.*"

**Customer**: *"I tried the factory reset and followed the above steps again, but it still didn't work."*

**Agent**: "*I'm sorry to hear that. Let me see if there's another way to fix the issue. Please hold on for a minute.*"

Conversation summarization feature would simplify the text as follows:

|Example summary  | Remark | Conversation aspect |
|---------|----|----|
| Customer is unable to set up wifi connection for Smart Brew 300 espresso machine |  a customer issue in a customer-and-agent conversation     | issue  |
| The agent suggested several troubleshooting steps, including checking the wifi connection, checking the Contoso Coffee app, and performing a factory reset. However, none of these steps resolved the issue. The agent then put the customer on hold to look for another solution.   | solutions tried in a customer-and-agent conversation | resolution |
| The customer contacted the agent for assistance with setting up a wifi connection for their Smart Brew 300 espresso machine. The agent guided the customer through several troubleshooting steps, including a wifi connection check, checking the power light, and a factory reset. Despite following these steps, the issue persisted. The agent then decided to explore other potential solutions | Summarizes a conversation into one paragraph | recap |
| Troubleshooting SmartBrew 300 Espresso Machine | Segments a conversation and generates a title for each segment; usually cowork with `narrative` aspect  | chapterTitle
| The customer is having trouble setting up a wifi connection for their Smart Brew 300 espresso machine. The agent suggests several solutions, including a factory reset, but the issue persists. | Segments a conversation and generates a summary for each segment, usually cowork with `chapterTitle` aspect  | narrative

# [Document summarization (Preview)](#tab/document-summarization)

This documentation contains the following article types:

* **[Quickstarts](quickstart.md?pivots=rest-api&tabs=document-summarization)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](../native-document-support/overview.md)** contain instructions for using the service in more specific or customized ways.

Native document summarization uses natural language processing techniques to generate a summary for native documents. A native document refers to the file format used to create the original document such as Microsoft Word (docx) or a portable document file (pdf). Native document support eliminates the need for text preprocessing before using Azure Language in Foundry Tools resource capabilities. Currently, native document support is available for two types of summarization:

* [**Extractive summarization**](how-to/document-summarization.md): Produces a summary by extracting salient sentences within the document, together the positioning information of those sentences.

  * Multiple extracted sentences: These sentences collectively convey the main idea of the document. They're original sentences extracted from the input document's content.
  * Rank score: The rank score indicates how relevant a sentence is to the main topic. Text summarization ranks extracted sentences, and you can determine whether they're returned in the order they appear, or according to their rank.
 For example, if you request a three-sentence summary extractive summarization returns the three highest scored sentences.
  * Positional information: The start position and length of extracted sentences.

* **Abstractive summarization**: Generates a summary with concise, coherent sentences or words that aren't verbatim extract sentences from the original document.
  * Summary texts: Abstractive summarization returns a summary for each contextual input range. A long input can be segmented so multiple groups of summary texts can be returned with their contextual input range.
  * Contextual input range: The range within the input that was used to generate the summary text.


Currently, **Document Summarization** supports the following native document formats:

|File type|File extension|Description|
|---------|--------------|-----------|
|Text| `.txt`|An unformatted text document.|
|Adobe PDF| `.pdf`       |A portable document file formatted document.|
|Microsoft Word|`.docx`|A Microsoft Word document file.|

For more information, *see* [**Summarize native documents**](how-to/document-summarization.md)

---

## Get started with summarization

[!INCLUDE [development options](./includes/development-options.md)]

## Input requirements and service limits

# [Text summarization](#tab/text-summarization)

* Summarization takes text for analysis. For more information, see [Data and service limits](../concepts/data-limits.md) in the how-to guide.
* Summarization works with various written languages. For more information, see [language support](language-support.md?tabs=text-summarization).

# [Conversation summarization](#tab/conversation-summarization)

* Conversation summarization takes structured text for analysis. For more information, see [data and service limits](../concepts/data-limits.md).
* Conversation summarization works with various spoken languages. For more information, see [language support](language-support.md?tabs=conversation-summarization).

# [Document summarization](#tab/document-summarization)

* Summarization takes text for analysis. For more information, see [Data and service limits](../concepts/data-limits.md) in the how-to guide.
* Summarization works with various written languages. For more information, see [language support](language-support.md?tabs=document-summarization).

---

## Reference documentation and code samples

As you use text summarization in your applications, see the following reference documentation and samples for Language:

|Development option / language  |Reference documentation |Samples  |
|---------|---------|---------|
|C#     | [C# documentation](/dotnet/api/azure.ai.textanalytics?view=azure-dotnet-preview&preserve-view=true)        | [C# samples](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics/samples)        |
| Java     | [Java documentation](/java/api/overview/azure/ai-textanalytics-readme?view=azure-java-preview&preserve-view=true)        | [Java Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/textanalytics/azure-ai-textanalytics/src/samples) |
|JavaScript     | [JavaScript documentation](/javascript/api/overview/azure/ai-text-analytics-readme?view=azure-node-preview&preserve-view=true)        | [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/textanalytics/ai-text-analytics/samples/v5) |
|Python | [Python documentation](/python/api/overview/azure/ai-textanalytics-readme?view=azure-python-preview&preserve-view=true)        | [Python samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics/samples) |

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people affected by it, and the deployment environment. Read the [transparency note for summarization](/azure/ai-foundry/responsible-ai/language-service/transparency-note-extractive-summarization) to learn about responsible AI use and deployment in your systems. For more information, see the following articles:

* [Transparency note for Language](/azure/ai-foundry/responsible-ai/language-service/transparency-note)
* [Integration and responsible use](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use-summarization)
* [Characteristics and limitations of summarization](/azure/ai-foundry/responsible-ai/language-service/characteristics-and-limitations-summarization)
* [Data, privacy, and security](/azure/ai-foundry/responsible-ai/language-service/data-privacy)
