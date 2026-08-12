---
title: Pricing for Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Understand the pricing model for Azure Content Understanding in Foundry Tools, including what you're charged for and how to estimate costs.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-content-understanding-foundry-tools
ms.topic: concept-article
ms.date: 07/22/2026
ai-usage: ai-assisted
ms.custom:
  - build-2025
---

# Pricing for Azure Content Understanding in Foundry Tools 
This article explains the Azure Content Understanding in Foundry Tools pricing model. Learn what you're charged for and how to estimate costs for your workload.
 
For specific pricing rates, see [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/).

Unless otherwise noted, this article references GA behavior with API version `2025-11-01`. Sections that describe workflow-family resolution and agentic mode switch to preview behavior with API version `2026-06-01-preview`.
 
## Understand the two types of charges
 
Azure Content Understanding pricing is based on two main usage categories:
 
### 1. Content extraction charges
 
Content extraction transforms unstructured input (documents, audio, video) into structured, searchable text and content. This output includes optical character recognition (OCR) for documents, speech-to-text for audio/video, and layout detection. You pay per input unit processed:
- **Documents**: Per 1,000 pages  
- **Audio and video**: Per minute

### 2. Generative feature charges

When you use AI-powered features that call large language models (LLMs), you incur two types of charges:

- **Contextualization charges**: Prepares context, generates confidence scores, provides source grounding, and formats output. For details, see [Contextualization tokens](#contextualization-tokens).
- **Generative model charges**: Token-based costs from Microsoft Foundry model deployments (LLMs for generation, embeddings for training examples). Content Understanding uses the Foundry model deployment you provide for all generative AI-related calls. You don't see any LLM or embedding token usage billing in Content Understanding. That usage appears on your Foundry model deployment. For details, see [Generative model charges](#generative-model-charges-llm).

**Generative features include**: Field extraction, figure analysis, segmentation, categorization, training.

> [!NOTE]
> The `"agentic"` [workflow](concepts/agentic-mode.md#select-agentic-workflow) (preview) resolves to the `agentic.*` workflow family and uses the advanced contextualization rate. It can also consume more model tokens than a nonagentic workflow. Test with representative documents when you estimate costs. For how labeled data and agentic mode affect the resolved workflow, see [Custom analyzers](#custom-analyzers).

### Cost components

Your total cost includes each usage category that applies to your analyzer: content extraction, contextualization tokens, completion model input and output tokens, and embedding model tokens. If you use only content extraction without generative capabilities, you pay only for content extraction.

## How to estimate your costs

### 1. Test with representative files  
Run a small test analysis with your actual files and schema. To see usage for GA and preview operations, check the `usage` object in the Analyzers API response:

```jsonc
{
  "usage": {
      "documentPagesMinimal": 0, // Asynchronous: Digital file extraction.
      "documentPagesBasic": 0, // Asynchronous: Read extraction.
      "documentPagesStandard": 2, // Asynchronous: Layout extraction.
      "documentPagesMinimalInline": 0, // Preview: Synchronous digital file extraction.
      "documentPagesBasicInline": 0, // Preview: Synchronous Read extraction.
      "documentPagesStandardInline": 0, // Preview: Synchronous Layout extraction.
      "contextualizationTokens": 2000,
      "advancedContextualizationTokens": 0, // Preview: Advanced contextualization.
      "tokens": {
         "gpt-5.2-input": 10400,
         "gpt-5.2-output": 360
    }
  }
}
```

In the `2026-06-01-preview` API, synchronous operations report content
extraction usage in the `documentPages*Inline` properties. Advanced
contextualization usage is reported in `advancedContextualizationTokens`. These
property names identify usage in the API response; they aren't the names of
published pricing meters.

### 2. Get current rates

Use the pricing pages for [Azure Content Understanding](https://azure.microsoft.com/pricing/details/content-understanding/) and [Foundry Models](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) to get the current rates for your region, deployment type, and selected models.

### 3. Calculate the estimate

For each applicable usage category, multiply the measured usage by its current rate. Include content extraction and contextualization charges from Content Understanding, completion model input and output token charges, and embedding token charges when your analyzer uses embeddings. Add the resulting charges to estimate the total cost for your expected volume.

Rates vary by region, deployment type, and model, so this article doesn't provide numerical calculations. For current model options, see [Supported generative models](service-limits.md#supported-generative-models).


## Detailed cost components
 
### Content extraction
 
Content extraction is the essential first step for transforming unstructured input—whether it's a document, audio, or video—into a standardized, reusable format. This foundational processing is required for all generative features and can be used standalone.

**Content extraction pricing by modality**:
- **Documents**: Three tiered meters (minimal, basic, or standard) based on processing complexity
- **Audio**: Speech-to-text transcription (single standard meter, priced per minute)
- **Video**: Frame extraction, shot detection, and speech-to-text transcription (single standard meter, priced per minute)
- **Images**: No content extraction available

#### Document content extraction meters

For documents, you're charged for the type of processing Content Understanding performs. Content Understanding charges based on the actual work performed on each page, not the analyzer you select.

**Minimal meter**: Applies to digital documents (DOCX, XLSX, PPTX, HTML, TXT, MSG, EML) where no OCR or layout processing is needed. This meter is the lowest-cost option for digital-native documents. You're charged the minimal rate regardless of which analyzer you use—even if you call a layout analyzer on a digital document, you're only charged for the minimal processing performed.

**Basic meter**: Applies when Content Understanding performs OCR processing to extract text from image-based documents (scanned PDFs, images, TIFFs) without layout analysis.

**Standard meter**: Applies when Content Understanding performs layout analysis, including table recognition and structural element detection from image-based documents (scanned PDFs, images, TIFFs).

The following table shows which meter applies based on your file type and analysis level:

| File Type | Read (Basic) | Layout (Standard) |
|-----------|--------------|-------------------|
| **Image-based** (PDF, PNG, TIFF, JPG, and other image-based formats) | Basic meter | Standard meter |
| **Digital formats** (DOCX, XLSX, HTML, TXT, and other digital formats) | Minimal meter | Minimal meter |

> [!TIP]
> The meter charged depends on the processing Content Understanding actually performs, not which analyzer you choose. Digital documents always use the minimal meter because they don't require OCR or layout processing.
  
### Generative capabilities

The generative capabilities of Content Understanding use generative AI models to enhance the quality of the output. In the latest API version **`2025-11-01`**, you can choose a generative model based on your use case. 

When you use any generative capabilities, Content Understanding uses the Foundry models deployment you provide. The token usage for the completion or embeddings models is on that deployment. 

#### Contextualization tokens

Contextualization is the processing layer in Content Understanding that preprocesses user content, prepares data and context for generative models, and post-processes model output into the final structured results. The type of data processing, data preparation, and context processing applied determines the type and amount of contextualization tokens charged.

**Standard contextualization** applies general-purpose extraction capabilities to your content and schema.

**Advanced contextualization** applies specialized technology to improve quality, simplify implementation, and solve more complex content understanding problems.

With the `2026-06-01-preview` API, the resolved `config.workflow` value makes the applicable rate explicit:

* Workflow values that start with `standard` use the standard contextualization rate.
* All other workflow families, including `advanced` and `agentic`, use the advanced contextualization rate.

Customers set `"default"` or `"agentic"` when creating an analyzer. The service returns a versioned workflow family value, such as `standard.2026-06-01-preview`, `advanced.2026-06-01-preview`, or `agentic.2026-06-01-preview`. For the complete resolution rules, see [`workflow`](concepts/analyzer-reference.md#workflow).

**When you're charged**: Whenever you use generative capabilities (field extraction, figure analysis, segmentation, categorization, training).

**Pricing**: Fixed rate per content unit.

Contextualization tokens are calculated per unit of content:

| Units | Contextualization tokens | Effective standard contextualization price per unit | Effective advanced contextualization price per unit |
|---|---:|---|---|
| Per page | 1,000 contextualization tokens | $1 per 1,000 pages | $3 per 1,000 pages |
| Per image | 1,000 contextualization tokens | $1 per 1,000 images | $3 per 1,000 images |
| Per hour of audio | 100,000 contextualization tokens | $0.10 per hour | Not applicable |
| Per hour of video | 1,000,000 contextualization tokens | $1 per hour | Not applicable |

Assuming a standard contextualization rate of $1.00 per 1 million contextualization tokens and an advanced contextualization rate of $3.00 per 1 million contextualization tokens.

##### Prebuilt analyzers

The following table summarizes the prebuilt analyzers and their applicable content extraction and context processing billing meters. The field extraction meter is charged based on actual usage of the generative model.

| Analyzer name | Content extraction meter | Contextualization meter |
|---|---|---|
| **Content extraction analyzers** |  |  |
| prebuilt-layout | Document Standard | None |
| prebuilt-read | Document Basic | None |
| prebuilt-digitalParse | Document Minimal | None |
| **Base analyzers** |  |  |
| prebuilt-audio | Audio | None |
| prebuilt-document | Document Minimal/ Basic/ Standard (depending on file type and analyzer configuration) | None |
| prebuilt-image | None | None |
| prebuilt-video | Video | None |
| **RAG analyzers** |  |  |
| prebuilt-documentSearch | Document Minimal/ Basic/ Standard (depending on file type and analyzer configuration) | Standard Contextualization |
| prebuilt-imageSearch | None | Standard Contextualization |
| prebuilt-audioSearch | Audio | Standard Contextualization |
| prebuilt-videoSearch | Video | Standard Contextualization |
| **Domain-specific analyzers** |  |  |
| prebuilt-invoice | Document Standard | Standard Contextualization |
| prebuilt-receipt | Document Standard | Standard Contextualization |
| prebuilt-receipt.generic | Document Basic | Standard Contextualization |
| prebuilt-receipt.hotel | Document Standard | Standard Contextualization |
| prebuilt-creditCard | Document Basic | Standard Contextualization |
| prebuilt-creditMemo | Document Standard | Standard Contextualization |
| prebuilt-check.us | Document Standard | Standard Contextualization |
| prebuilt-bankStatement.us | Document Standard | Standard Contextualization |
| prebuilt-idDocument | Document Basic | Standard Contextualization |
| prebuilt-idDocument.generic | Document Basic | Standard Contextualization |
| prebuilt-idDocument.passport | Document Basic | Standard Contextualization |
| prebuilt-healthInsuranceCard.us | Document Standard | Standard Contextualization |
| prebuilt-tax.us | Document Standard | Standard/Advanced Contextualization |
| prebuilt-tax.us.1040 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040Senior | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040Schedule1 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040Schedule2 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040Schedule3 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040Schedule8812 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleA | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleB | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleC | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleD | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleE | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleEIC | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleF | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleH | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleJ | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleR | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1040ScheduleSE | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099Combo | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099A | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099B | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099C | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099CAP | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099DA | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099DIV | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099G | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099H | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099INT | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099K | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099LS | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099LTC | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099MISC | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099NEC | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099OID | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099PATR | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099Q | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099QA | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099R | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099S | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099SA | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099SB | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1099SSA | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1098 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1098E | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1098T | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1095A | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.1095C | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.w2 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.w4 | Document Standard | Standard Contextualization |
| prebuilt-tax.us.1041ScheduleK1 | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.1120SScheduleK1 | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.1065ScheduleK1 | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.8865ScheduleK1 | Document Standard | Advanced Contextualization |
| prebuilt-tax.us.mn.m1 | Document Standard | Advanced Contextualization |
| prebuilt-mortgage.us | Document Standard | Standard Contextualization |
| prebuilt-mortgage.us.1003 | Document Standard | Standard Contextualization |
| prebuilt-mortgage.us.1004 | Document Standard | Standard Contextualization |
| prebuilt-mortgage.us.1005 | Document Standard | Standard Contextualization |
| prebuilt-mortgage.us.1008 | Document Standard | Standard Contextualization |
| prebuilt-mortgage.us.closingDisclosure | Document Standard | Standard Contextualization |
| prebuilt-contract | Document Standard | Standard Contextualization |
| prebuilt-marriageCertificate.us | Document Standard | Standard Contextualization |
| prebuilt-procurement | Document Standard | Standard Contextualization |
| prebuilt-purchaseOrder | Document Standard | Standard Contextualization |
| prebuilt-payStub.us | Document Standard | Standard Contextualization |
| prebuilt-utilityBill | Document Standard | Standard Contextualization |
| **Utility analyzers** |  |  |
| prebuilt-documentFieldSchema | Document Standard | Standard Contextualization |
| prebuilt-documentFields | Document Standard | Standard Contextualization |

<sup>1</sup>Extracting content from text-based files by using supported analyzers is billed with the Document Minimal meter.

##### Custom analyzers

When you build custom analyzers and provide labeled training data, the system applies the advanced contextualization meter. Otherwise, it applies the standard contextualization meter.

Custom analyzers created with API version `2025-11-01` or earlier continue to use the standard contextualization rate. If you retrieve one of these analyzers with the `2026-06-01-preview` API, the response shows `standard.2025-11-01` in `config.workflow`. The `2025-11-01` API response is unchanged.

When you create a custom analyzer with the `2026-06-01-preview` API:

* A custom analyzer without labeled data resolves to `standard.2026-06-01-preview` and uses the standard rate.
* A custom analyzer with labeled data resolves to `advanced.2026-06-01-preview` and uses the advanced rate.
* A custom analyzer created with `workflow` set to `"agentic"` resolves to `agentic.2026-06-01-preview` and uses the advanced rate.

#### Generative model charges (LLM)

Token-based charges from Foundry models that power the actual field extraction, analysis, and other generative capabilities.

**Input tokens include**:
- Extracted text and transcripts
- Image tokens (for visual analysis)
- Your schema definitions
- System prompts
- Labeled training examples with the `2025-11-01` API

**Output tokens include**:
- Field values and structured data
- Confidence scores and source grounding
- Analysis results and descriptions

**Cost optimization**: Compare the current rates for supported models and deployment types, and choose an option that meets your quality, latency, data residency, and cost requirements.

#### Embeddings charges

Token-based charges for embedding models used when training custom analyzers with labeled examples to improve accuracy.

- **When charged**: Only when using the training feature with labeled data
- **Models**: For current options, see [Supported generative models](service-limits.md#supported-generative-models).
- **Typical usage**: The entire document is embedded. Usage can vary depending on the density of text, but about 1,500 tokens per page is a useful initial estimate.

## Generative feature details
Each generative feature has different cost implications.

### Field extraction
Generates structured key-value pairs based on your schema definition. Examples include invoice sender/receiver, line items, or video ad elements like tagline and product appearance.

**Cost impact**: Charges scale with schema complexity and content size.

### Figure analysis  
Creates descriptive text for images, charts, and diagrams to make visual content searchable in RAG workflows.

**Cost impact**: LLM tokens per image analyzed - both input tokens for image interpretation and output tokens for descriptions. Usage scales with the size and number of images contained in the document.

### Segmentation
Divides documents or videos into logical sections for targeted processing and improved efficiency.

**Cost impact**: Output token costs for each segment created. Optionally, you can chain analyzers for further analysis on each segment. Chaining uses more content extraction and generative usage, equivalent to running the chained analyzers independently.

### Categorization
Assigns labels to documents or segments for classification and intelligent routing to specialized analyzers.

**Cost impact**: LLM and contextualization costs for classification. Routing to another analyzer adds its respective charges.

### Training
Builds custom analyzers using labeled examples for domain-specific accuracy improvements.

**Cost impact**: Both API versions use embedding tokens when you add labeled data. With the `2025-11-01` API, retrieved training examples also add LLM input tokens during analysis. With the `2026-06-01-preview` API, the built analyzer doesn't retrieve the labeled documents at analysis time.


## Frequently asked questions

### When am I charged for LLM usage?
You're charged for LLM tokens only when you provide the analyzer with a Foundry deployment and use a generative capability in Content Understanding. Analyzers that only perform content extraction, such as `prebuilt-read`, `prebuilt-layout`, or custom analyzers without generative capabilities, don't incur LLM charges.

### How do I know which content extraction meter applies to my documents?
The actual processing performed determines the meter, not the analyzer you choose:
- **Minimal**: Digital documents (DOCX, XLSX, HTML, TXT, etc.) always use minimal, regardless of analyzer
- **Basic**: Image-based documents with OCR-only processing (Read analyzer)
- **Standard**: Image-based documents with layout analysis (Layout analyzer)

For more information about meters, see [Document content extraction meters](#document-content-extraction-meters).

### Am I charged twice for Foundry model usage?
No. Content Understanding uses the LLM deployments linked for all LLM and embedding calls. You're billed on those deployments. You pay Content Understanding for content extraction and contextualization, and Foundry for the generative model tokens (input/output tokens and embeddings).



### How does model choice affect cost?
Model token rates vary by model and deployment type. Compare current rates and test representative files before choosing a model. Content extraction and contextualization charges don't depend on the completion model you select.

### What increases token usage?
Several features can increase token consumption:
- **Source grounding and confidence scores** add processing context.
- **Extractive mode** adds instructions and output details.
- **Training examples** add retrieved examples to the model context by using the `2025-11-01` API.
- **Segmentation and categorization** can require additional model calls.

### Am I charged if my request fails?
Content Understanding doesn't charge for content extraction or contextualization when a request fails with an error (such as a 400 error). If a Foundry completion model call succeeded before the failure, you're charged for that Foundry model usage based on Foundry's billing policies. 

## Cost optimization tips

- **Compare supported models and deployment types** to balance cost, quality, latency, and data residency requirements.
- **Start with mini models** - Mini models offer substantial savings for most extraction tasks
- **Use global deployments** when data residency and compliance allows   
- **Enable advanced features selectively** - Only use source grounding and confidence scores when needed
- **Test representative files** before scaling to understand actual token consumption
- **Monitor usage regularly** through the Azure portal to identify optimization opportunities

## More pricing examples

Here are detailed examples showing how pricing works across different scenarios:

### Example 1: Document processing for RAG workflows

**Scenario**: You need to extract content from documents for a Retrieval-Augmented Generation (RAG) solution. You use `prebuilt-documentSearch` to extract text, layout, and figure descriptions.
 
**Input**:
- 10 pages
- Model: GPT-5.2 global deployment
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: 10 pages
   - Cost: (10 / 1,000) × $5.00 = **$0.05**
 
2. **Figure analysis**:
 
   Assuming two figures per page. It costs about 1000 input and 200 output tokens per figure.
 
   - Input tokens: 20 figures × 1,000 tokens/image = 20,000 tokens
   - Cost: (20,000 / 1,000,000) × $2.00 = **$0.04**
   - Output tokens: 20 figures × 200 tokens/figure = 4,000 tokens
   - Cost: (4,000 / 1,000,000) × $8.00 = **$0.032**
 
3. **Contextualization**: 10 pages × 1,000 tokens/page = 10,000 tokens
   - Cost: (10,000 / 1,000,000) × $1.00 = **$0.01**
 
**Total estimated cost**: $0.05 + $0.04 + $0.032 + $0.01 = **$0.132**

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
 
#### Example 2: Processing invoices with field extraction
 
**Scenario**: You're automating invoice processing using `prebuilt-invoice` to extract structured data (invoice number, date, vendor, total, line items).
 
**Input**:
- 10 pages
- Model: GPT-5.2 global deployment
- Features: Extractive mode + source estimation + confidence scores
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: 10 pages
   - Cost: (10 / 1,000) × $5.00 = **$0.05**
 
2. **Field extraction**: with source estimation + confidence enabled, the token usage is ~2x more per page:
   - Base input tokens: 10 pages × 5,200 tokens/page = 52,000 tokens
   - Cost: (52,000 / 1,000,000) × $0.40 = **$0.0208**
   - Base output tokens: 10 pages × 180 tokens/page = 1,800 tokens
   - Cost: (1,800 / 1,000,000) × $1.60 = **$0.0029**
 
3. **Contextualization**: 10 pages × 1,000 tokens/page = 10,000 tokens
   - Cost: (10,000 / 1,000,000) × $1.00 = **$0.01**
 
**Total estimated cost**: $0.05 + $0.0208 + $0.0029 + $0.01 = **$0.0837**
 
 
> [!NOTE]
> Model token rates vary. Use the current rate for your selected model when you estimate field extraction costs.

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
 
#### Example 3: Analyzing video content with segment-level field extraction
 
**Scenario**: You're extracting a structured representation of video content for a RAG application. To extract structured data per segment of video, you can use the `prebuilt-videoSearch`. Segments are short clips of 15-30 seconds on average, resulting in numerous output segments with a single summary field per segment.
 
**Input**:
- 60 minutes (1 hour) of video
- Model: GPT-5.2 global deployment
- Region: East US
 
**Assumptions**:
- Input tokens: 7,500 tokens per minute (based on sampled frames, transcription, schema prompts, and metaprompts)
- Output tokens: 900 tokens per minute (assuming 10-20 short structured fields per segment with auto segmentation)
- Contextualization: 1,000,000 tokens per hour of video
 
**Pricing breakdown**:
 
1. **Content extraction**: 60 minutes
   - Cost: 60 minutes × $1/hour = **$1.00**
 
2. **Field extraction**:
   - Input tokens: 60 minutes × 7,500 tokens/minute = 450,000 tokens
   - Cost: (450,000 / 1,000,000) × $2.00 = **$0.90**
   - Output tokens: 60 minutes × 900 tokens/minute = 54,000 tokens
   - Cost: (54,000 / 1,000,000) × $8.00 = **$0.43**
 
3. **Contextualization**: 1,000,000 tokens per hour
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**
 
**Total estimated cost**: $1.00 + $0.90 + $0.43 + $1.00 = **$3.33**
 
> [!NOTE]
>Actual cost varies based on the specifics of your input and output. This transparent, usage-based billing model ensures you only pay for what you use.

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
 
#### Example 4: Processing audio call center recordings
 
**Scenario**: You're analyzing call center recordings using `prebuilt-callCenter` to generate transcripts, speaker diarization, sentiment analysis, and summaries.
 
**Input**:
- 60 minutes of audio
- Model: GPT-5.2 global deployment
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: 60 minutes
   - Cost: 60 minutes × $0.36/minute = **$0.36**
 
2. **Field extraction**:
   - Input tokens: 60 minutes × 604 tokens/minute = 36,240 tokens
   - Cost: (36,240 / 1,000,000) × $0.40 = **$0.01** 
   - Output tokens: 60 minutes × 19 tokens/minute = 1,140 tokens
   - Cost: (1,140 / 1,000,000) × $1.60 = **$0.00** 
 
3. **Contextualization**: 60 minutes × 1,667 tokens/minute = 100,020 tokens
   - Cost: (100,020 / 1,000,000) × $1.00 = **$0.10**
 
**Total estimated cost**: $0.36 + $0.01 + $0.00 + $0.10 = **$0.47**
 
 >[!Note] 
 >These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates

#### Example 5: Processing images with captions
 
**Scenario**: You're generating descriptive captions for product images using `prebuilt-imageSearch`.
 
**Input**:
- 1,000 images
- Model: GPT-5.2 global deployment
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: No charge for images
   - Cost: **$0.00**
 
2. **Field extraction**:
   - Input tokens: 1,000 images × 1,043 tokens/image = 1,043,000 tokens
   - Cost: (1,043,000 / 1,000,000) × $2.00 = **$2.09**
   - Output tokens: 1,000 images × 170 tokens/image = 170,000 tokens
   - Cost: (170,000 / 1,000,000) × $8.00 = **$1.36**
 
3. **Contextualization**: 1,000 images × 1,000 tokens/image = 1,000,000 tokens
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**
 
**Total estimated cost**: $0.00 + $2.09 + $1.36 + $1.00 = **$4.45**

## Usage categories by workload

Use the following table to identify the usage categories to include in your estimate. The exact token usage depends on your content, schema, analyzer configuration, and selected model.

| Workload | Usage categories to review |
|---|---|
| Document extraction and RAG | Document content extraction, contextualization, completion input and output tokens, and embedding tokens when applicable |
| Structured field extraction | Content extraction, contextualization, and completion input and output tokens |
| Video analysis | Video content extraction, contextualization, and completion input and output tokens |
| Audio analysis | Audio content extraction, contextualization, and completion input and output tokens |
| Image analysis | Contextualization and completion input and output tokens |

## Next steps

- [Azure Content Understanding Pricing page](https://azure.microsoft.com/pricing/details/content-understanding/)
- [Content Understanding quickstart](quickstart/use-rest-api.md)
- [Best practices for Content Understanding](concepts/best-practices.md)
- [Prebuilt analyzers](concepts/prebuilt-analyzers.md)
