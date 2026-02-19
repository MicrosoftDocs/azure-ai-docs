---

title: Choose the right Azure AI tool for document processing
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools, Azure Document Intelligence in Foundry Tools and Azure large language model (LLM) solutions, processes, workflows, use-cases, and field extractions for document processing.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
---
 

# Choose the right Foundry tool for document processing: Document Intelligence, Content Understanding, or Foundry models

As organizations increasingly use Generative AI to manage documents and unstructured data, it's essential to select the right tool for building robust, secure, and scalable document processing workflows. This is a comparative overview of the leading Azure AI solutions for intelligent document processing (IDP) to help you evaluate and choose the most effective approach for your business requirements. This article compares the following options:

* **Azure Document Intelligence in Foundry Tools**: Trusted service for extracting text, tables, and structured fields from documents with industry-leading OCR and proven accuracy.
* **Azure Content Understanding in Foundry Tools**: Multimodal service with industry-leading content extraction (ex. OCR, speech-to-text), multimodal processing of documents, images, audio, and video, and  generative AI capabilities for complex field extraction.
* **Azure-hosted LLMs (Azure Foundry models)**: Flexible platform for building custom AI solutions with maximum control over models, prompts, and workflows.


## Overview of services

Here’s a summary of the three available services:

|Service | What it Does | Ideal For | Strengths | Core Features |
|--------|---------------|-----------|-----------|----------------|
| Document Intelligence | Extracts text, key-value pairs, tables, and layout  (structure) from documents, field extraction with grounding, confidence, support for classification and splitting | Standard forms, invoices, receipts, purchase orders, IDs, contracts, legal documents | Proven, high-accuracy extraction, consistency, confidence score and grounding, predefined schemas for many templated document types | OCR/Read/Layout models, Prebuilt Models (invoice, tax, receipt, etc.), Custom model (field extraction and classification) |
| Content Understanding | Processes documents, images, audio, and video; richer field extraction  and inference, built-in support for validation, enrichment, and post processing, integrated reasoning for complex tasks (preview) | Complex document processing requiring extractive and inferred fields, document formats with large number of complex variations or truly unstructured documents, inferring, summarization and generate metadata | Built-in unified process for multimodal inputs; start with no labeling. Handles varying templates and unstructured documents, supports continuous improvement with labeled samples| Enhanced support for content extraction(OCR, layout), field extraction, inferred fields and classification, tackle large documents with high variations, configure your Gen AI model for control over quality and price. |
| Build your own solution with Azure OpenAI Service | Build a solution with any Azure-hosted LLM models, Fully control on model, prompt, and tools | Developers aiming to build, own, and manage a solution that requires fine grained control on models, costs, and prompts | Maximum flexibility and control | Multiple options to plug and play with model choice, prompt tuning, workflow definition with complete flexibility in building each component. Requires engineering investment in model upgrades, quality, and reliability. |

## Azure Document Intelligence

Document Intelligence is the trusted choice for many document-centric scenarios. Customers rely on its industry leading OCR capability and structure extraction, including table recognition, figures, paragraphs, selection marks, sections, and more output in markdown format for easy integrations with LLMs for ingestion in RAG, field extraction, and document chat scenarios. 

Document Intelligence has the tools to build scalable and flexible IDP solutions with classification and conditional routing for high-accuracy extraction from prebuilt models like invoices, receipts, tax forms, and identification cards. For any custom template, you can label a few samples to train a custom extraction model on any document type. Document Intelligence models have some limitations like supporting only extracting results, limited generalization of custom models across many template variations, and limited semantic understanding capabilities. With confidence scores and grounded results, you can build an effective, low latency, consistent extractive document processing solution for most scenarios. Document Intelligence provides the following models:

* Document digitization or [Optical Character Recognition (OCR)](/azure/ai-services/document-intelligence/prebuilt/read) to extract printed or handwritten text from documents.

* Document structure extraction with [Layout](/azure/ai-services/document-intelligence/prebuilt/layout) to extract table, selection marks, sections, and document structure along with OCR.

* Document [classification](/azure/ai-services/document-intelligence/train/custom-classifier) to accurately identify, split, and classify multiple documents.

* Document field extraction with [prebuilt models](/azure/ai-services/document-intelligence/model-overview) for predefined schema extraction from standard document types like tax, mortgage, bank checks, forms with higher variations like invoices, receipts, and ID, and [custom models](/azure/ai-services/document-intelligence/train/custom-model) to label and train your own model. 


## Azure Content Understanding

Azure Content Understanding, built on the same foundational capabilities as Document Intelligence, extends document scenarios to images and embedded content, expanding to multimodal scenarios with audio and video. Content Understanding is built for content processing with Generative AI, improving your ability to generate the specific output you need with inferred fields, enrichments, validations, and reasoning.

Content Understanding simplifies the process of building an effective document processing solution, packaging these capabilities into a simple and easy to use analyzer building process with zero-shot output and no labeling, all while providing a rich schema that includes confidence scores and grounding, wherever applicable. Content Understanding provides a rich set of tools among others that can be configured to solve most document processing challenges.

* **Updated Read and Layout**: Content Understanding Layout has a few updated features, including multi-page tables, hyperlink extraction and more. Learn more about [the new features in Layout](whats-new.md#content-extraction). The models for Read and Layout are updated with AI quality improvements.
* **Improved Layout pricing**: Content Understanding has a new and lower pricing for Layout, see [pricing for more details](https://azure.microsoft.com/pricing/details/content-understanding/).
* **Inferred fields and enrichments**: Generate output fields that aren't explicitly present in the document. For example, calculate total tax on an invoice, determine jurisdiction on a contract from parties' addresses, or derive insights from clause wording.
* **Classification and splitting**: Parse large files to identify and split individual segments for intelligent routing and targeted schema extraction. Targets include all analyzers including prebuilt and custom.
* **Post-processing and validations**: Define post-processing rules directly in field descriptions, such as converting date formats, normalizing currency codes, and performing consistency checks.
* **Model choice**: Content Understanding supports multiple Gen AI models for use, providing you with the flexibility to select the model that provides the best result quality/cost trade-off. Learn more about the [models supported](./concepts/models-deployments.md).
* **Multi-file input (preview)**: Process multiple input files in a single request and extract a unified schema across all inputs, enabling cross-document validation and aggregation.
* **Reasoning (preview)**: Simplify complex intelligent document processing workflows. Instead of building multi-step processes for extraction, validation, aggregation, and reviews, Content Understanding handles everything in a single unified operation.

> [!NOTE]
>
> Starting with the GA version, Content Understanding uses your Foundry model deployments for all operations that require a Gen AI model. To learn more about which models to deploy and use, refer to the [Models and deployments](./concepts/models-deployments.md) page.

## Azure-hosted LLMs (Foundry models) 

For organizations requiring niche AI workflows, custom solutions built with Foundry models directly offer maximum flexibility. Developers can combine models like GPT-4.1, Whisper, and Embeddings to build highly customized AI solutions, typically integrating Azure Document Intelligence or Azure Content Understanding for pre-processing documents into custom workflows. This approach provides the maximum flexibility but requires users to evaluate models, update models as needed, manage the prompts, and optimize for costs. A common challenge with these solutions is the trade-off between cost management and accuracy as this approach lacks adequate tools to trigger reviews only for challenging cases. Confidence scores and source or citation is a critical gap that requires significant engineering investment or human review.


## Service capabilities

Here's a capabilities overview for all three services. 

| Capabilities             | Document Intelligence                              | Content Understanding                              | Build Your Own with Azure OpenAI                          |
|--------------------------|----------------------------------------------------|----------------------------------------------------|---------------------------------------------------|
| OCR                      | Industry leading OCR                               | Industry leading OCR                               | Requires preprocessing                            |
| Complex document structure | Layout with tables, sections, selection marks, figures, and more   | Enhanced layout with multi-page tables, sections, selection marks, figures, and more   | Requires preprocessing  |
| Extract fields           | Yes                                                | Yes                                                | Yes                                               |
| Confidence scores | Yes                                                | Yes                                                | No, requires extra implementation            |
| Source grounding | Yes                                                | Yes                                                | No, requires extra implementation            |
| Inferred fields          | No                                                 | Yes, with generative and classify fields  | Yes                                               |
| Generate metadata        | No                                                 | Yes                                                | Yes                                               |
| Post-processing          | Limited                                            | Custom with limitations                            | User defined process                                    |
| Process large files      | Yes                                                | Yes                                                | Requires chunking and other strategies to get optimal performance      |
| Ease of use              | Requires labeling and training to build a custom model, can directly use layout and prebuilt models  | Simple schema definition without  any labeling required to get started. Label to improve.          | Optimize results with prompt engineering                     |
| Scale for use            | Managed                                            | Managed with connected Gen AI deployment                                            | Manually scale components as needed               |
| Latency                  | Low                                                | Medium                                             | Depends on PTUs deployed                          |
| Multi-file inputs        | No                                                 | Yes, support in Pro Mode (preview)    | No                                                |
| Knowledge base           | No                                                 | Yes  (preview)                                              | Complex and requires engineering                  |
| Reasoning                | No                                                 | Yes, support in Pro Mode (preview) | Complex and requires engineering                  |

---

## When to choose Content Understanding over build-your-own-model

| Advantage | Azure Content Understanding | Build your own model |
|-----------|-------------------------------|------------------|
| Unified, multimodal pipeline | ✅ Supports docs, images, audio, video | ❌ Requires orchestration |
| Prebuilt enrichments and schema normalization | ✅ Prebuilt templates available | ❌ Requires implementation |
| Simplified pricing | ✅ Token based pricing |  ✅ Token based pricing |
| Enterprise governance & security | ✅ Azure security compliance | ❌ Custom implementation |
| Confidence Scores | ✅ In-built scores | ❌ Custom implementation |
| Source Grounding | ✅ In-built scores | ❌ Custom implementation |
| Chunking & normalization | ✅ Built-in algorithms | ❌ Custom implementation |
| Prompt tuning | ✅ Optimized automatically | ❌ Needs engineering |
| Context window | ✅ Optimized for long files | ❌ Manual handling |
| Enterprise reasoning workflows | ✅ In-built reasoning capabilities(preview) | ❌ Custom chaining |

---

## Guided scenario walkthroughs

Let's take a look at various categories of document processing scenarios that you might encounter and how to navigate each one with the best fitted service. Here are a few examples of different document processing scenarios, the associated challenges, and the considerations for building an effective solution. If the document type you're processing is supported by a prebuilt, you should start there and only choose to build a custom solution if the prebuilt schema doesn't cover your scenario.

Considerations: 

* Straight Through Processing (STP): The measure of the number of documents you can process without requiring human review based on the confidence scores. Higher confidence and accuracy levels can help in automating most documents without manual intervention. 
* Latency: Time to process a document, critical for scenarios where the inference time matters for the end user experience.
* Accuracy: The overall error rate of the solution. Higher accuracy means better reliability on system's output. 
* Continuous Improvement: To ensure that the system can improve over time and to measure quality change with time. 
* Complexity: Depending on the use case, what do you want to extract or infer from the documents. 
* Build Effort: Effort to build the model including handling complex logic, business requirements, labeling data and putting complex workflows together. 
* Total cost of ownership: Comparative view of infrastructure, management, and maintenance costs for your use case with handling scale. 

### Scenario 1: Processing a standardized, single-format form

**Business Process**:  
Extract fixed fields like Name, Date of Birth, Address, Account Number, and other details from forms with identical templates every time. **Examples**:
- Employment onboarding form (same layout for all employees)
- Refund request form for a specific e-commerce provider
- Patient intake form for a specific health provider
- Account opening application for a specific bank provider
  
:::image type="content" source="media/overview/simple-form.png" alt-text="Scan of a sample W2 form." :::

**Recommendation**:
* This class of documents would be served by either Content Understanding ```(recommended)``` or Document Intelligence. Content Understanding would offer an easier getting started experience. Both services would provide confidence scores and grounding to ensure you minimize your human review costs and scale. 



### Scenario 2: Managing document with few known variants

**Business Process**:  
Extract consistent fields (name, amount, policy number, claim date) across a small, known set of templates.  **Examples**:
- Insurance claim forms with few formats for specific geography (for example: US, UK, APAC)
- Annual tax forms with minor layout updates each year
- University admission applications for different degree programs
- Employee expense reports with department-specific templates

:::image type="content" source="media/overview/mid-form.png" alt-text="Scan of a sample driver's license." :::
:::image type="content" source="media/overview/mid-form-2.png" alt-text="Scan of a sample passport." :::

**Recommendation**:

* Content Understanding ```(Recommended)```: Start with the prebuilt invoice analyzer. A generalized solution with confidence scores and grounding. With improved layout and OCR capabilities, and semantic understanding of documents, Content Understanding should provide the best results.
* Document Intelligence: Train custom models with at least five samples of each variant and combine variants into a single model if differences are minor. The outputs are consistent with confidence scores and grounding. 
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution needs to be tested and verified with different variations and you'll need to scale and manage the deployed solution. With no confidence scores, you either accept all results or review all results based on the expected error rate, or you can build your own confidence model to score the output. 



### Scenario 3: High-variation semi-structured documents

**Business Process**:  
Extract key fields like Invoice Number, Vendor Name, Total Amount, Line Items, and Dates from highly varied documents with inconsistent templates.  **Examples**:
- Invoices from multiple vendors all with different formats
- Receipts from international store chains
- Delivery notes with different templates from vendors
- Purchase orders with inconsistent layouts across suppliers
- Student transcripts from different universities

:::image type="content" source="media/overview/invoice-1.png" alt-text="Scan of a sample invoice form." :::
:::image type="content" source="media/overview/invoice-2.png" alt-text="Scan of a sample invoice form with a vertical layout." :::

**Recommendation**:
* Content Understanding ```(Recommended)```: With a simple getting started experience and analyzers that can generalize across templates and variations in language, Content Understanding is best equipped to provide a high quality output with minimal management overhead.  
* Document Intelligence: Prebuilt Model if they're applicable, or you can build your own custom models with multiple labeling to get grounded, low latency, consistent output. 
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution needs to be tested and verified with different variations and you'll need to scale and manage the deployed solution. With no confidence scores, you either accept all results or review all results based on the expected error rate. 


### Scenario 4: Extracting insights from unstructured documents

**Business Process**:  
Extract, generate abstract details like obligations, summaries, inferencing details like contract parties, risk indicators, sentiment, or decisions from free-text, multi-page, narrative documents.  **Examples**:
- Legal contracts and service agreements
- Investment reports
- Research papers
- Patient referral letters
- Employee feedback reports

:::image type="content" source="media/overview/contracts.png" alt-text="Scan of a sample web hosting agreement contract." :::

**Recommendation**:
* Content Understanding ```(Recommended)```: The ideal service for this use case. Content Understanding can extract inferred fields, like an end date of a contract with start date and duration, total tax or geography
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution needs to be tested and verified with different variations, and you'll need to scale and manage the deployed solution. With no confidence scores, you either accept all results or review all results based on the expected error rate. 



### Scenario 5: Multi-document, mixed media processing

**Business Process**:  
Aggregate content from diverse formats, cross-reference details, validate consistency (for example, name matches across documents), and surface inconsistencies. **Examples**:
- Onboarding content: PDF forms + ID images + recorded video interviews
- Compliance cases: Email text + contract + call transcript
- Medical claims: Doctor notes + lab reports + phone consultations
- Multimedia RFP submissions: Proposal PDF + product images + explainer videos

:::image type="content" source="media/overview/invoice-mixed.png" alt-text="Scan of a sample tax invoice form." lightbox="media/overview/invoice-mixed.png":::
:::image type="content" source="media/overview/receipt-mixed.png" alt-text="Scan of a sample receipt form." lightbox="media/overview/receipt-mixed.png":::

**Recommendation**:
* Content Understanding: With pro mode (preview), Content Understanding can accept multiple input documents in the same request, reason over the content and reference data and generate the required output schema.  
* Build a custom solution: This scenario requires an agentic solution where the different input files need to be parsed and collectively reasoned over. The solution requires complex processing to determine document types and expected values and generate a unified output.



## Summary

Choosing the right document processing service depends on the complexity of the task, format or template diversity, reasoning needs, latency sensitivity, human review needs, and enterprise integration requirements. Building on Document Intelligence, Content Understanding delivers improved OCR, layout, and field extraction capabilities with built-in postprocessing. It fully matches Document Intelligence functionality while extending support for more complex and varied document types. Start with Content Understanding for most IDP scenarios.  

Use Foundry models for custom, experimental, or conversational AI workflows where managed services aren’t a fit. Layout from Content Understanding can be used as preprocessing service for all input documents. 

In the past, many enterprises combine these services into hybrid solutions—using Document Intelligence for layout or content extraction integrated as preprocessing step, now Content Understanding provides a solution for most of these scenarios. 


