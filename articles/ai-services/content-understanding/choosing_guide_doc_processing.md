---

title: Choosing the right Azure AI tool for document processing
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding, Azure AI Document Intelligence and Azure LLM solutions, processes, workflows, use-cases, and field extractions for document processing.
author: PatrickFarley
ms.author: admaheshwari
manager: nitinme
ms.date: 06/26/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
---
 

# Choosing the right Azure AI tool for Document Processing: Azure Document Intelligence, Azure AI Content Understanding, and Azure OpenAI 

As organizations increasingly rely on Generative AI to manage documents and unstructured data, selecting the right tools is essential for building robust, secure, and scalable document processing workflows. Let's review a comparative overview of the leading Azure AI solutions for intelligent document processing (IDP), helping you evaluate and choose the most effective approach for your business requirements. 

## Azure AI Document Intelligence 
Azure AI Document Intelligence is the trusted choice for many document-centric scenarios. Customers rely on its industry leading OCR capability and structure extraction, including table recognition, figures, paragraphs, selection marks, sections, and more output in markdown format for easy integrations with LLMs for ingestion in RAG, field extraction, and document chat scenarios. Document Intelligence has the tools to build scalable and flexible IDP solutions with classification and conditional routing for high-accuracy extraction from prebuilt models like invoices, receipts, tax forms, and identification cards. For any custom template, you can label a few samples to train a custom extraction model on any document type. Document Intelligence models have some limitations like supporting only extracting results, limited generalization of custom models across many template variations, and limited semantic understanding capabilities. With confidence scores and grounded results, you can build an effective, low latency, consistent extractive document processing solution for most scenarios. Document Intelligence provides the following models:

* Document digitization or [Optical Character Recognition (OCR)](/azure/ai-services/document-intelligence/prebuilt/read?view=doc-intel-4.0.0&branch=main&tabs=sample-code) to extract printed or handwritten text from documents.

* Document structure extraction with [Layout](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0&branch=main&tabs=rest%2Csample-code) to extract table, selection marks, sections and document structure along with OCR.

* Document [classification](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-classifier?view=doc-intel-4.0.0) to accurately identify, split and classify multiple documents.

* Document field extraction with [prebuilt models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview?view=doc-intel-4.0.0) for predefined schema extraction from standard document type like tax, mortgage, bank checks and forms with higher variations like invoices, receipts, ID and [custom models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/train/custom-model?view=doc-intel-4.0.0) to label and train your own model. 


## Azure AI Content Understanding 

Built on the same foundational capabilities of Document Intelligence, it extends document scenarios to images and embedded content, expanding to truly multimodal scenarios with audio and video. Content Understanding is built for a content processing with Generative AI, maximizing your ability to generate the specific output you need with inferred fields, enrichments, validations and reasoning. Content Understanding simplifies the process of building an effective document processing solution, packaging these capabilities into a simple and easy to use analyzer building process with zero shot output and no labeling, all while providing a rich schema that includes confidence scores and grounding, whereever applicable. Content Understanding provides a rich set of tools among others that can be configured to solve most document processing challenges.

* Inferred fields & enrichments: Output required that are not always directly present in the document, like the total tax on an invoice or the jurisdiction on a contract that can be inferred from the parties’ addresses or clause wording. 
* Multi-file input: Process multiple input files in the same request and extract a unified schema across all the input files.
* Classification & Splitting: For parsing large files into individual documents for routing and schema extraction. 
* Reasoning: Intelligent Document Processing typically is a multi-step process with extraction, validation, aggregation and reviews. Content Understanding is built for IDP, simplifying everything into a single step process. 
* Post processing & validations: Use the description to define any post processing rules like converting date formats, currency codes and consistency checks. 

## Azure hosted LLM Models (Azure Open AI)

For organizations requiring niche AI workflows, custom solutions built with Azure OpenAI Service/ or any other Azure based LLM services offer maximum flexibility. Developers can combine models like GPT-4o, Vision, Whisper, and Embeddings to build highly customized AI solutions, typically integrating Azure Document Intelligence/ Azure AI Content Understanding for pre-processing documents into custom workflows. This approach provides the maximum flexibility, but requires users to evaluate models, update models as needed, manage the prompts and optimize for costs. A common challenge with these solutions is the trade-off between cost management and accuracy as this approach lacks adequate tools to trigger reviews only for challenging cases. 

## Service Overview

Here’s a summary of the three available services:
| Service | What it Does | Ideal For | Strengths | Core Features |
|--------|---------------|-----------|-----------|----------------|
| Azure AI Document Intelligence | Extracts text, key-value pairs, tables, and layout from structured, semi and unstructured documents, field extraction with grounding,confidence, support for classification and splitting | Standard forms, invoices, receipts, purchase orders, IDs, contracts, legal documents | Proven, high-accuracy extraction, consistency, low latency, confidence score and grounding, predefined schemas for many document types | OCR/Read/Layout models, Prebuilt Models (invoice, tax, receipt, etc), Custom model (extraction and classification) |
| Azure AI Content Understanding | Processes documents, images, audio, and video; integrated reasoning for complex tasks, richer field extraction with built in support for validation, enrichment, and post processing | Complex document processing requiring extractive and inferred fields, document formats with large number of complex variations or truly unstructured documents, inferring, summarization and generate metadata | Built-in unified process for multimodal inputs with zero shot model Unified process for multimodal inputs, handles varying templates and unstructured documents, supports continuous improvement with labeled samples| Support for content extraction(OCR, layout), field extraction, inferred fields and classification for handling complex, large documents with high variations, reasoning with multi-file inputs and knowledge base |
| Build your own solution with Azure OpenAI Service | Build a solution with any Azure-hosted LLM models, Fully control on model, prompt and tools | Developers aiming to build, own and manage a solution that require fine grained control on models, costs and prompts | Maximum flexibility and control | Multiple options to plug and play with model choice, prompt tuning, workflow defination with complete flexibility in building each component |


## Capabilites Overview
Here's an capabilites overview for all three services. 

| Capabilities             | Document Intelligence                              | Content Understanding                              | Build Your Own with AOAI                          |
|--------------------------|----------------------------------------------------|----------------------------------------------------|---------------------------------------------------|
| OCR                      | Industry leading OCR                               | Industry leading OCR                               | Requires preprocessing                            |
| Complex document structure | Layout with tables, sections, selection marks, figures and more   | Layout with tables, sections, selection marks, figures and more   | Requires preprocessing  |
| Extract fields           | Yes                                                | Yes                                                | Yes                                               |
| Confidence and Grounding | Yes                                                | Yes                                                | No, requires additional implementation            |
| Inferred fields          | No                                                 | Yes, has support for generative and classify fields  | Yes                                               |
| Generate metadata        | No                                                 | Yes                                                | Yes                                               |
| Post-processing          | Limited                                            | Custom with limitations                            | User defined process                                    |
| Process large files      | Yes                                                | Yes                                                | Requires chunking and other strategies to get optimal performance      |
| Ease of use              | Requires labeling and training to build a custom model, can directly use layout and prebuilt models  | Simple schema definition without  any labelling required to get zero shot results          | Optimize results with prompt engineering                     |
| Scale for use            | Managed                                            | Managed                                            | Manually scale components as needed               |
| Latency                  | Low                                                | Medium                                             | Depends on PTUs deployed                          |
| Multi-file inputs        | No                                                 | Yes, support in multi file analysis or Pro Mode    | No                                                |
| Knowledge base           | No                                                 | Yes                                                | Complex and requires engineering                  |
| Reasoning                | No                                                 | Yes, support in multi file analysis or Pro Mode  | Complex and requires engineering                  |

---

## When to choose Content Understanding over Build your own model ?

| Advantage | Azure AI Content Understanding | Build your own model |
|-----------|-------------------------------|------------------|
| Unified, multimodal pipeline | ✅ Supports docs, images, audio, video | ❌ Requires orchestration |
| Enterprise reasoning workflows | ✅ In-built reasoning capabilities | ❌ Custom chaining |
| Prebuilt enrichments and schema normalization | ✅ Prebuilt templates available | ❌ Requires implementation |
| Simplified pricing | ✅ Token based pricing |  ✅ Token based pricing |
| Enterprise governance & security | ✅ Azure security compliance | ❌ Custom implementation |
| Confidence and Grounding | ✅ In-built scores | ❌ Custom implementation |
| Chunking & normalization | ✅ Built-in algorithms | ❌ Custom implementation |
| Prompt tuning | ✅ Optimized automatically | ❌ Needs engineering |
| Context window | ✅ Optimized for long files | ❌ Manual handling |

---

## Guided Scenario Walkthrough

Let's take a look at various categories of document processing scenarios that you may encounter and how to navigate each of such scenarios with the best fitted service. Here are a few examples of different document processing scenarios, the associated challenges and the considerations for building an effective solution. If the document type you are processing is supported by a prebuilt, you should start there and only choose to build a custom solution if the prebuilt schema does not cover your scenario.

Considerations: 

* Straight Through Processing (STP): The measure of the number of documents you can process without requiring human review based on the confidence scores. Higher confidence and accruacy levels can help in automating a majority of documents without manual intervention. 
* Latency: Time to process a document, critical for scenarios where the inference time matters for the end user experience.
* Accuracy: The overall error rate of the solution. Higher accuracy means better reliability on system's output. 
* Continuous Improvement: To ensure that the system can improve over time and to measure quality change with time. 
* Complexity: Depending on the use case, what do you want to extract or infer from the documents. 
* Build Effort: Effort to build the model including handling complex logic, business requriements, labeling data and putting complex workflows together. 
* Total cost of ownership: Comparative view of infrastructure, management and maintenance costs for your use case with handling scale. 

### Scenario 1: Processing a Standardized, Single-Format Form

**Business Process**:  
Extract fixed fields like Name, Date of Birth, Address, Account Number, and other details from forms with identical templates every time.  **Examples**:
- Employment onboarding form (same layout for all employees)
- Refund request form for a specific e-commerce provider
- Patient intake form for a specific health provider
- Account opening application for a specific bank provider
  
:::image type="content" source="media/overview/simple_form.png" alt-text="Simple form with fixed template." :::

**Recommendation**:
* This class of documents would be well served by either Document Intelligence or Content Understanding. Document Intelligence would provide a lower latency, consistent solution while Content Understanding would offer an easier getting started experience. Both services would provide confidence scores and grounding to ensure you minimize your human review costs and scale. 

---

### Scenario 2: Managing Document with Few Known Variants

**Business Process**:  
Extract consistent fields (name, amount, policy number, claim date) across a small, known set of templates.  **Examples**:
- Insurance claim forms with few formats for specific geography (Eg: US, UK, APAC)
- Annual tax forms with minor layout updates each year
- University admission applications for different degree programs
- Employee expense reports with department-specific templates

:::image type="content" source="media/overview/mid_form.png" alt-text="Forms with few variations" :::
:::image type="content" source="media/overview/mid_form1.png" alt-text="Forms with few variations" :::

**Recommendation**:

* Azure AI Document Intelligence: Train custom models with at least 5 samples of each variant and combine variants into a single model if differences are minor. The outputs are consistent with confidence scores and grounding. 
* Azure AI Content Understanding: Start with the recommended schema or define your schema and the analyzer extracts the fields across all variations with no labeling required. A generalized solution with confidence scores and grounding. 
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution will need to be tested and verified with different variations and you will need to scale and manage the deployed solution. With no confidence scores, you are either accepting all results or reviewing all results based on the expected error rate or you can build your own confidence model to score the output. 

---

### Scenario 3: High-Variation Semi-Structured Documents

**Business Process**:  
Extract key fields like Invoice Number, Vendor Name, Total Amount, Line Items, and Dates from highly varied documents with inconsistent templates.  **Examples**:
- Invoices from multiple vendors all with different formats
- Receipts from international store chains
- Delivery notes with different templates from vendors
- Purchase orders with inconsistent layouts across suppliers
- Student transcripts from different universities

:::image type="content" source="media/overview/invoice1.png" alt-text="Forms with high variations" :::
:::image type="content" source="media/overview/invoice2.png" alt-text="Forms with high variations" :::

**Recommendation**:
* Azure AI Document Intelligence Prebuilt Model if they are applicable or you can build your own custom models with multiple labelling to get grounded, low latency, consistent output. 
* Azure AI Content Understanding: With a simple getting started experience and analyzers that can generalize across templates and variations in language, Content Understanding is best equipped to provide a high quality output with minimal management overhead.  
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution will need to be tested and verified with different variations and you will need to scale and manage the deployed solution. With no confidence scores, you are either accepting all results or reviewing all results based on the expected error rate.Shape 
---

### Scenario 4: Extracting Insights from Unstructured Documents

**Business Process**:  
Extract, generate abstract details like obligations, summaries, inferencing details like contract parties, risk indicators, sentiment, or decisions from free-text, multi-page, narrative documents.  **Examples**:
- Legal contracts and service agreements
- Investment reports
- Research papers
- Patient referral letters
- Employee feedback reports

:::image type="content" source="media/overview/contracts.png" alt-text="Unstructured forms" :::

**Recommendation**:
* Azure AI Content Understanding: The ideal service for this use case. Content Understanding can extract inferred fields, enriched with reasoning, multi-file input support with knowledge base for insight extraction with quick getting started experience without labeling.
* Build a custom solution: Build and configure the components needed for parsing the documents (Layout), extracting the fields and any build any post-processing needed. The solution will need to be tested and verified with different variations, and you will need to scale and manage the deployed solution. With no confidence scores, you are either accepting all results or reviewing all results based on the expected error rate. 

---

### Scenario 5: Multi-Document, Mixed Media Processing

**Business Process**:  
Aggregate content from diverse formats, cross-reference details, validate consistency (e.g., name matches across documents), and surface inconsistencies. **Examples**:
- Onboarding content: PDF forms + ID images + recorded video interviews
- Compliance cases: Email text + contract + call transcript
- Medical claims: Doctor notes + lab reports + phone consultations
- Multimedia RFP submissions: Proposal PDF + product images + explainer videos

:::image type="content" source="media/overview/invoice_mixed.png" alt-text="Invoice with details" :::
:::image type="content" source="media/overview/receipt_mixed.png" alt-text="Receipts with cross reference details" :::

**Recommendation**:
* Azure AI Content Understanding: With pro mode, Content Understanding can accept multiple input documents in the same request, reason over the content and reference data and generate the required output schema.  
* Build a custom solution: This solution will require an agentic solution where the different input files will need to be parsed and collectively reasoned over. The solution will require some complex processing to determine document types, expected values and generating a unified output.  

---

## Conclusion

Choosing the right document processing service is dependent on the complexity of the task, format or template diversity, reasoning needs, latency sensitivity, human review needs and enterprise integration requirements. 
For new applications and workloads, Content Understanding matches Document Intelligence capabilities and have more feature set to handle complex diverse documents.  

Start with Azure AI Document Intelligence for well-defined forms and simple workflows if you have a latency sensitive workload and need to rely on the consistency of the outputs. Move to Azure AI Content Understanding for reasoning, multi-format content, or complex business logic. Both services have grounding and confidence scores for quality. 

Leverage Azure OpenAI Service for custom, experimental, or conversational AI workflows where managed services aren’t a fit. Layout from Document Intelligence or Content Understanding can be leveraged as preprocessing service for all input documents. 

Many enterprises combine these services into hybrid solutions — using Document Intelligence/Content Understanding for extraction integrated as tools with AI agent based solutions. 



