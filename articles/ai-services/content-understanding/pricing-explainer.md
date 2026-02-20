---
title: Pricing for Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Understand the pricing model for Azure Content Understanding in Foundry Tools, including what you're charged for, how to estimate costs, and pricing examples.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: concept-article
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.custom:
  - build-2025
---

# Pricing for Azure Content Understanding in Foundry Tools
 
This article explains the Azure Content Understanding in Foundry Tools pricing model with clear examples and cost breakdowns. Learn what you're charged for and how to estimate costs for your workload.
 
For specific pricing rates, see [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/).
 
## Understanding the two types of charges
 
Azure Content Understanding pricing is based on two main usage categories:
 
### 1. Content extraction charges
 
Content extraction transforms unstructured input (documents, audio, video) into structured, searchable text and content. This output includes optical character recognition (OCR) for documents, speech-to-text for audio/video, and layout detection. You pay per input unit processed:
- **Documents**: Per 1,000 pages  
- **Audio and Video**: Per minute

### 2. Generative feature charges

When you use AI-powered features that call large language models (LLMs), you incur two types of charges:

- **Contextualization charges**: Prepares context, generates confidence scores, provides source grounding, and formats output. For details, see [Contextualization tokens](#contextualization-tokens).
- **Generative model charges**: Token-based costs from Microsoft Foundry model deployments (LLMs for generation, embeddings for training examples). Content Understanding uses the Foundry model deployment you provide for all generative AI-related calls. You don't see any LLM or embedding token usage billing in Content Understanding. That usage appears on your Foundry model deployment. For details see [Generative model charges](#generative-model-charges-llm). 

**Generative features include**: Field extraction, figure analysis, segmentation, categorization, training.

### Cost equation

Your total cost for running a Content Understanding analyzer follows this formula:

```
Total Cost = Content Extraction + Contextualization Tokens + LLM Input Tokens + LLM Output Tokens + Embeddings Tokens
```

If you only use content extraction without generative capabilities, you're charged only for content extraction. When you use generative features, all applicable charges apply.

## How to estimate your costs

### 1. Test with representative files  
Run a small test analysis with your actual files and schema. To see actual token consumption, check the `usage` object in the Analyzers API response:

```jsonc
  "usage": {
    "documentPagesMinimal": 0, // Pages processed at the minimal level (i.e. txt, xlsx, html, and other digital file types)
    "documentPagesBasic": 0, // Pages processed at the basic level (i.e. read)
    "documentPagesStandard": 2, // Pages processed at the standard level (i.e. layout)
   
    "contextualizationToken": 2000,
    "tokens": {
      "gpt-4.1-input": 10400,
         "gpt-4.1-output": 360
    }
  }
```

### 2. Use the Azure Pricing Calculator
Find Content Understanding in the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) and configure your settings:

- Add "Content Understanding" to the calculator 
- Use your test results from step 1 to calculate per-page or per-minute token averages
- Enter token counts along with your region, [file type](/azure/ai-services/content-understanding/service-limits#input-file-limits), expected volume, and model deployment

The calculator provides accurate cost projections for your workload. 

## Pricing example: Invoice field extraction

Following the estimation approach, let's walk through a concrete example manually to demonstrate how the costs are calculated. You're processing invoices to extract structured data like vendor name, invoice number, total amount, and line items.

**Scenario**: You want to process 1,000 invoice pages using GPT-4o-mini with source grounding and confidence scores disabled. 

**Step 1: Test with representative files**
After testing representative files, you found the following average token usage per page:
- **Input tokens**: 1,100 per page 
- **Output tokens**: 60 per page 
- **Contextualization**: 1,000 tokens per page (fixed rate)

For 1,000 pages, totals equal:
- **Total input tokens**: 1,000 pages × 1,100 = 1,100,000 tokens
- **Total output tokens**: 1,000 pages × 60 = 60,000 tokens
- **Total contextualization tokens**: 1,000 pages × 1,000 = 1,000,000 tokens

**Step 2: Calculate costs manually (instead of using the pricing calculator)**
Using GPT-4o-mini global deployment with the following pricing assumptions:

**Pricing assumptions** :
- Content extraction: $5.00 per 1,000 pages
- Contextualization: $1.00 per 1M tokens
- GPT-4o-mini input tokens: $0.40 per 1M tokens
- GPT-4o-mini output tokens: $1.60 per 1M tokens
- Embeddings: $0.02 per 1,000 tokens. You're not using a knowledge base with training examples, so no embeddings charges apply. If you add labeled examples to improve accuracy, the system adds embedding token usage to embed the text from the input documents and completion input tokens to process example data added to the context window. 

**Cost calculation**:
- Content extraction: 1,000 pages × $5.00 per 1,000 pages = $5.00
- Contextualization: 1,000,000 tokens × $1.00 per 1M tokens = $1.00  
- Input tokens: 1,100,000 tokens × $0.40 per 1M tokens = $0.44
- Output tokens: 60,000 tokens × $1.60 per 1M tokens = $0.10
- Embeddings: Not used = $0.00

```
Total Cost = $5.00 + $1.00 + $0.44 + $0.10 + $0.00 = $6.54 per 1000 pages
```

> [!NOTE]
> These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates.


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
| **Image-based** (PDF, PNG, TIFF, JPG, etc.) | Basic meter | Standard meter |
| **Digital formats** (DOCX, XLSX, HTML, TXT, etc.) | Minimal meter | Minimal meter |

> [!TIP]
> The meter charged depends on the processing Content Understanding actually performs, not which analyzer you choose. Digital documents always use the minimal meter because they don't require OCR or layout processing.
  
### Generative capabilities

The generative capabilities of Content Understanding use generative AI models to enhance the quality of the output. In the latest API version [**`2025-11-01`**], you can choose a generative model based on your use case (ex. GPT-4o or GPT-4o-mini). 

When you use any generative capabilities, Content Understanding uses the Foundry models deployment you provide. The token usage for the completion or embeddings models is on that deployment. 

#### Contextualization tokens

Contextualization is Content Understanding's processing layer that prepares context for generative models and post-processes their output into the final structured results.

**What contextualization provides**:
- Output normalization and formatting into structured schemas
- Source grounding to show where information came from
- Confidence score calculation for extraction reliability  
- Context engineering to optimize LLM usage and accuracy

**When you're charged**: Whenever you use generative capabilities (field extraction, figure analysis, segmentation, categorization, training).

**Pricing**: Fixed rate per content unit 

Contextualization tokens are calculated per unit of content:

| Units | Contextualization Tokens | Effective Standard Price per unit |
|-------|-------------------------|-----------------------------------|
| Per page | 1,000 contextualization tokens | $1 per 1,000 pages |
| Per image | 1,000 contextualization tokens | $1 per 1,000 images |
| Per hour of audio | 100,000 contextualization tokens | $0.10 per hour |
| Per hour of video | 1,000,000 contextualization tokens | $1 per hour |

Assuming $1.00 per 1 million contextualization tokens.

#### Generative model charges (LLM)

Token-based charges from Foundry models that power the actual field extraction, analysis, and other generative capabilities.

**Input tokens include**:
- Extracted text and transcripts
- Image tokens (for visual analysis)
- Your schema definitions
- System prompts
- Training examples (when using knowledge base)

**Output tokens include**:
- Field values and structured data
- Confidence scores and source grounding
- Analysis results and descriptions

**Cost optimization**: Choose smaller models (GPT-4o-mini) or global deployments for significant savings.

#### Embeddings charges

Token-based charges for embedding models used when training custom analyzers with labeled examples to improve accuracy.

- **When charged**: Only when using the training feature with labeled data
- **Models**: text-embedding-3-large, text-embedding-3-small, or text-embedding-ada-002
- **Typical usage**: The entire document is embedded. Usage can vary depending on the density of text, but ~1,500 tokens per page are a good initial estimate.

## Generative feature details
There are several generative features each of which has slightly different cost implications. 

### Field extraction
Generates structured key-value pairs based on your schema definition. Examples include invoice sender/receiver, line items, or video ad elements like tagline and product appearance.

**Cost impact**: Charges scale with schema complexity and content size.

### Figure analysis  
Creates descriptive text for images, charts, and diagrams to make visual content searchable in RAG workflows.

**Cost impact**: LLM tokens per image analyzed - both input tokens for image interpretation and output tokens for descriptions. Usage scales with the size and number of images contained in the document.

### Segmentation
Divides documents or videos into logical sections for targeted processing and improved efficiency.

**Cost impact**: Output token costs for each segment created. Optionally you can chain analyzers for further analysis on each segment. When chaining you incurs more content extraction and generative usage equivalent to running the chained analyzers independently. 

### Categorization
Assigns labels to documents or segments for classification and intelligent routing to specialized analyzers.

**Cost impact**: LLM and contextualization costs for classification. Routing to another analyzers adds their respective charges.

### Training
Builds custom analyzers using labeled examples for domain-specific accuracy improvements.

**Cost impact**: Embedding token usage when adding labeled data, plus more LLM tokens during analysis when training examples are retrieved and provided to the model.

### Knowledge base
Enhances custom analyzers with labeled training examples for domain-specific accuracy improvements. 

**Cost impact**: Embeddings model is used to index and retrieve the samples. In addition, LLM tokens are used during analysis when training examples are retrieved and provided to the model.


## Frequently asked questions

### When am I charged for LLM usage?
You're charged for LLM tokens only when you provide the analyzer with a Foundry deployment and use a generative capability in Content Understanding. Analyzers that only perform content extraction (ex. `prebuilt-read`, `prebuilt-layout`, or custom analyzers without any generative capabilities) don't incur LLM charges.

### How do I know which content extraction meter applies to my documents?
The actual processing performed determines the meter, not the analyzer you choose:
- **Minimal**: Digital documents (DOCX, XLSX, HTML, TXT, etc.) always use minimal, regardless of analyzer
- **Basic**: Image-based documents with OCR-only processing (Read analyzer)
- **Standard**: Image-based documents with layout analysis (Layout analyzer)

For more information about meters, see [Document content extraction meters](#document-content-extraction-meters).

### Am I charged twice for Foundry model usage?
No. Content Understanding uses the LLM deployments linked for all LLM and embedding calls. You're billed on those deployments. You pay Content Understanding for content extraction and contextualization, and Foundry for the generative model tokens (input/output tokens and embeddings).



### How much can I save with smaller models?
Choosing GPT-4o-mini instead of GPT-4o can reduce LLM costs by up to 80%. Global deployments provide additional savings. Content extraction and contextualization charges remain the same regardless of model choice.

### What increases token usage?
Several features multiply token consumption:
- **Source grounding + confidence scores**: ~2x token usage
- **Extractive mode**: ~1.5x token usage  
- **Training examples**: ~2x token usage
- **Segmentation/categorization**: ~2x token usage

### Am I charged if my request fails?
Content Understanding doesn't charge for content extraction or contextualization when a request fails with an error (such as a 400 error). If a Foundry completion model call succeeded before the failure, you're charged for that Foundry model usage based on Foundry's billing policies. 

## Cost optimization tips

- **Start with mini models** - GPT-4o-mini offers substantial savings for most extraction tasks
- **Use global deployments** when data residency and compliance allows   
- **Enable advanced features selectively** - Only use source grounding and confidence scores when needed
- **Test representative files** before scaling to understand actual token consumption
- **Monitor usage regularly** through the Azure portal to identify optimization opportunities

## More pricing examples

Here are detailed examples showing how pricing works across different scenarios:

### Example 1: Document processing for RAG workflows

**Scenario**: You need to extract content from documents for a Retrieval-Augmented Generation (RAG) solution. You use `prebuilt-documentSearch` to extract text, layout, and figure descriptions.
 
**Input**:
- 1,000 pages
- Model: GPT-4.1 global deployment
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: 1,000 pages
   - Cost: (1,000 / 1,000) × $5.00 = **$5.00**
 
2. **Figure analysis**:
 
   Assuming two figures per page. It costs about 1000 input and 200 output tokens per figure.
 
   - Input tokens: 2,000 figures × 1000 tokens/image = 2,000,000 tokens
   - Cost: (2,000,000 / 1,000,000) × $2.00 = **$4.00**
   - Output tokens: 2,000 pages × 200 tokens/page = 400,000 tokens
   - Cost: (400,000 / 1,000,000) × $8.00 = **$3.2**
 
3. **Contextualization**: 1,000 pages × 1,000 tokens/page = 1,000,000 tokens
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**
 
**Total estimated cost**: $5.00 + $4 + $3.2 + $1.00 = **$13.20**

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
 
#### Example 2: Processing invoices with field extraction
 
**Scenario**: You're automating invoice processing using `prebuilt-invoice` to extract structured data (invoice number, date, vendor, total, line items).
 
**Input**:
- 1,000 pages
- Model: GPT-4.1-mini global deployment (cost-optimized)
- Features: Extractive mode + source estimation + confidence scores
- Region: East US
 
**Pricing breakdown**:
 
1. **Content extraction**: 1,000 pages
   - Cost: (1,000 / 1,000) × $5.00 = **$5.00**
 
2. **Field extraction**: with source estimation + confidence enabled, the token usage is ~2x more per page:
   - Base input tokens: 1,000 pages × 5,200 tokens/page = 5,200,000 tokens
   - Cost: (5,200,000 / 1,000,000) × $0.40 = **$2.08** 
   - Base output tokens: 1,000 pages × 180 tokens/page = 180,000 tokens
   - Cost: (180,000 / 1,000,000) × $1.60 = **$0.29** 
 
3. **Contextualization**: 1,000 pages × 1,000 tokens/page = 1,000,000 tokens
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**
 
**Total estimated cost**: $5.00 + $2.08 + $0.29 + $1.00 = **$8.37**
 
 
> [!NOTE]
> Using a standard GPT-4.1 global deployment instead of mini would increase the field extraction cost by approximately 5x, bringing the total to approximately $33.

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
 
#### Example 3: Analyzing video content with segment-level field extraction
 
**Scenario**: You're extracting a structured representation of video content for a RAG application. To extract structured data per segment of video, you can use the `prebuilt-videoSearch`. Segments are short clips of 15-30 seconds on average, resulting in numerous output segments with a single summary field per segment.
 
**Input**:
- 60 minutes (1 hour) of video
- Model: GPT-4.1 global deployment
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
- Model: GPT-4.1-mini global deployment
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
- Model: GPT-4.1 global deployment
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

>[!Note] 
>These prices are for illustration purposes only and aren't intended to represent the actual cost. Check [Azure Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) and [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates

## Next steps

- [Azure Content Understanding Pricing page](https://azure.microsoft.com/pricing/details/content-understanding/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Content Understanding quickstart](quickstart/use-rest-api.md)
- [Best practices for Content Understanding](concepts/best-practices.md)
- [Prebuilt analyzers](concepts/prebuilt-analyzers.md)