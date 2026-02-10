---
title: Azure Content Understanding in Foundry Tools standard and pro modes (preview)
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools standard and pro modes.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Azure Content Understanding in Foundry Tools standard and pro modes (preview)

Azure Content Understanding in Foundry Tools is a generative AI service designed to derive structured insights from multimodal content such as documents, images, videos, and audio. With the introduction of the `2025-05-01-preview` version, the service offers two modes: `standard` and `pro`.

* **Standard**: This mode is the default for processing diverse content types. It's optimized to provide efficient schema extraction tailored to specific tasks across data formats. This mode emphasizes cost-effectiveness and reduced latency.

* **Pro**: This mode is designed for advanced use cases that require multi-step reasoning and complex decision-making (for example, identifying inconsistencies, drawing inferences, and making decisions). The pro mode supports multiple input documents and lets you provide reference data at analyzer creation time. Currently, pro mode is available only for document data.


## Standard mode overview

The Content Understanding standard mode delivers structured insights across various data types, including documents, videos, images, audio, and text. While it doesn't support data inferencing, it minimizes cost and latency, making it ideal for broad, data-centric scenarios. This mode enables the creation or customization of schemas to extract precise insights tailored to your needs. Additionally, it incorporates data labeling for document data, allowing human input to enhance the quality of your outputs.

### Standard mode: use case

Standard mode is ideal for extracting the exact insights you need on any type of data. If you need to unlock the content of your data, your scenario might not require complex reasoning or decision-making. Scenarios that standard mode works well for include:

* Structuring data to power your RAG search workflows and integrating with [AI Search](../../../search/search-what-is-azure-search.md).
* Extracting data to integrate with [Microsoft Fabric](https://blog.fabric.microsoft.com/en-US/blog/).
* Analyzing advertising videos to screen for content guidelines.
* Segmenting video footage to create chapters and identify ideal advertising breaks.
* Extracting critical data points from sports games and providing post-game recaps.

## Pro mode overview

Content Understanding pro mode is tailored for customers with complex use cases, offering multi-step reasoning capabilities, and multi-input document support. It enables reasoning over both input content and reference data, making it ideal for scenarios requiring complex analysis. By incorporating reference data, pro mode adds context to each request, aiding tasks such as validation and enrichment. Currently, pro mode is exclusively available for document data.

### Pro mode reference data

During analyzer creation, you can provide reference documents that add context at analysis time. For example, to analyze invoices for consistency with a contractual agreement, you can provide the invoice and related documents (for example, a purchase order) as inputs, and provide the contract files as reference data. The service applies reasoning to validate input documents according to your schema, such as identifying discrepancies to flag for review. If your documents are within the pro mode input document limits, try supplying all related documents as inputs if you encounter quality issues.

### Multi-step reasoning

Multi-step reasoning decomposes complex problems into simpler tasks. It takes data analysis beyond extracting and aggregating structured data and lets you draw conclusions on that data, minimizing the need for human review. Examples of questions that pro mode can answer include:

* Does x match y?
* Does x pass the outlined criteria?
* Does x document follow the required guidelines?
* Does the total equal the sum of the items?
* Find all inconsistencies between the invoice and the contract.

## Standard and pro mode features

Not sure which mode is right for your scenario? The following charts compare standard and pro mode features.

| Feature | Standard mode | Pro mode |
|---|---|---|
| **Large documents** | &check;  | &check; |
| **Field mode** | &check; | &check; |
| **Extract, classify, and generate fields** | &check; | &check; |
| **Grounding and confidence scores** | &check; | &cross; |
| **Input document type** | Documents, images, video, audio | Documents |
| **Max fields** | 100 | 100 |
| **Multiple input document processing** | &cross; | &check; |
| **Reference dataset integration** | &cross;  | &check; |
| **Multi-step reasoning** | &cross;  | &check; |


## Apply standard or pro mode to your scenarios

You can apply both Content Understanding standard and pro modes to many scenarios. How you build your solution depends on the questions you're aiming to answer. The following scenarios provide examples.

| Scenario | Standard mode | Pro mode|
|---|---|---|
| **Invoice analysis** | Extract insights on invoice data at scale and enable RAG search and further data analysis and visualization. Answer questions like: <br> &bullet; Extract purchase order number, total, due date, and line items for entry into database. | Analyze invoices and contractual agreements with clients and apply multi-step reasoning to draw conclusions on that data. Answer questions like: <br> &bullet; Does this invoice fulfill the contractual agreement we have in place with this client? <br> &bullet; Does this invoice need further review? |
| **Call center transcript analytics** | Extract insights on large volumes of call center data to gain valuable insights on sentiment, understand customer issues, and create targeted training to address major pain points. Answer questions like: <br> &bullet; What are the main issues customers are calling about? <br> &bullet; What is the average length of calls made about x issue? | Analyze call center transcript data and apply multi-step reasoning to understand how call center employees are addressing customer needs, and if they're following guidelines. Answer questions like: <br> &bullet; Did the call center employee introduce themselves? <br> &bullet; Did this answer *pass* certain criteria? |
| **Mortgage application processing** | Extract the key values from mortgage application data and make it searchable and more easily accessible. Answer questions like: <br> &bullet;  What year was the mortgage application submitted? <br> &bullet; What are the names on the application? | Analyze supplementary supporting documentation and mortgage applications to determine whether a prospective home buyer provides all the necessary documentation to secure a mortgage. Answer questions like: <br> &bullet;  Do the names and social security numbers on the mortgage application match the supporting documentation? |

## Try pro mode

You can try out the features of both Content Understanding standard and pro modes using the [Microsoft Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding). The service enables you to bring your own data and experiment with all the functionalities of both modes in a lightweight, no-code approach to help you find the best fit for your unique scenario.

### Pro mode known limitations and best practices

* Content Understanding pro mode currently doesn't offer confidence scores or grounding. It supports `classify` and `generate` fields, but it doesn't support `extract` fields.

* Content Understanding pro mode is currently only available for documents.

* The system operates in lookup mode when referencing documents. If you need exhaustive recovery of data, incorporate the content into the input set.

* Schemas should be designed with the highest level of specificity possible. For instance, instead of presenting a generalized list of inconsistencies, it's advisable to create distinct fields for each type of inconsistency, accompanied by detailed descriptions. Additionally, wherever feasible, references to specific sections of relevant documents that should be reviewed should be included.

* Reference documents should be concise and focused. Prioritize essential documents and ensure they're as brief as possible to enhance retention and recall.




## Next steps

For more information on document processing, see [Document processing overview](../document/overview.md).



