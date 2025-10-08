---
title: Pricing explainer for Azure AI Content Understanding
titleSuffix: Azure AI services
description: Understand the pricing model for Azure AI Content Understanding, including what you're charged for, how to estimate costs, and pricing examples.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.date: 10/03/2025
ms.custom:
  - build-2025
---

# Pricing explainer for Azure AI Content Understanding

This article provides a comprehensive explanation of the Azure AI Content Understanding pricing model in Q&A format. It helps you understand what you're charged for, how to estimate costs, and how different features affect your bill.

For specific pricing rates, see [Azure AI Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/).

## What exactly am I charged for?

Azure AI Content Understanding charges are based on four main components:

1. **Content extraction**: The base cost for extracting text, layout, and structure from your files
2. **Field extraction (LLM usage)**: Token-based charges for using generative AI models to extract, classify, or generate field values
3. **Embeddings** (optional): Token-based charges for generating vector embeddings for search and similarity scenarios
4. **Contextualization**: Additional token charges for context expansion to improve accuracy

Your total cost is the sum of these components. If you only use content extraction without defining any fields, you're only charged for content extraction.

## Am I charged twice for field extraction through both Content Understanding and Azure OpenAI?

No, you're not charged twice. When you use Content Understanding for field extraction, the Azure OpenAI charges are included in the Content Understanding pricing. You don't need to separately pay for Azure OpenAI service when using Content Understanding's field extraction capabilities.

Content Understanding provides a unified billing model that includes the underlying AI model usage.

## If I select a cheaper model, like GPT-4o-mini, does it reduce the charge?

Yes, selecting a more cost-effective model deployment significantly reduces your charges. Content Understanding supports different model deployments with varying price points:

- **Standard models** (like GPT-4o): Higher capability at standard pricing
- **Mini models** (like GPT-4o-mini): Optimized for cost, up to 60% lower pricing while maintaining quality for many scenarios

When you choose a mini deployment, both the input and output token costs are reduced. For example, if standard deployment charges $2.50 per 1M input tokens, a mini deployment might charge $1.00 per 1M input tokens.

> [!TIP]
> Mini models offer excellent value for many common extraction tasks. Test with mini models first and only move to standard models if needed for complex scenarios.

## How exactly can I estimate the charge for a specific workload?

To estimate costs for your workload, follow these steps:

### Step 1: Use the Azure Pricing Calculator

Find Content Understanding in the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) and configure:
- Your region
- File type (document, image, audio, or video)
- Expected quantity (pages, minutes, or images)
- Model deployment type

### Step 2: Run a test analysis

For accurate token estimation when using field extraction:

1. Select a representative file from your dataset
2. Define your analyzer schema with the fields you plan to extract
3. Analyze the file using the Content Understanding API
4. Check the `usage` section in the API response:

```json
{
  "usage": {
    "documentPages": 25,
    "tokens": {
      "contextualization": 25000,
      "input": 84216,
      "output": 2899
    }
  }
}
```

### Step 3: Calculate averages

- Compute per-page or per-minute averages from your test results
- Multiply by your expected volume
- Input these numbers into the pricing calculator

### Understanding token counts

**Input tokens** include:
- Extracted text from documents and transcripts from audio
- Images from video and image modalities
- Your schema definition
- Content Understanding system tokens
- Knowledge base in-context examples (if used)

**Output tokens** include:
- The field values returned from the model
- Structural overhead for organizing the output

## What is content extraction?

Content extraction is the base processing step that extracts raw content from your files:

- **Documents**: Optical Character Recognition (OCR) to extract text, layout detection, table recognition, and structural elements
- **Audio**: Speech-to-text transcription
- **Video**: Frame extraction, scene detection, and speech-to-text transcription
- **Images**: Visual content analysis
- **Text**: No content extraction performed (free)

Content extraction is priced based on:
- **Documents**: Per 1,000 pages
- **Audio/Video**: Per minute
- **Text**: Free (3,000 UTF-8 characters = 1 page for measurement)
- **Images**: No content extraction charge

You're always charged for content extraction (except for text and images), regardless of whether you use field extraction.

## What is contextualization and when am I charged for it?

Contextualization is an additional processing step that expands the context around extracted content to improve field extraction accuracy. It adds relevant surrounding information to help the AI model better understand and extract fields.

### When you're charged for contextualization

You're charged for contextualization tokens when you:
- Enable field extraction (define fields in your analyzer)
- Use prebuilt analyzers that include field extraction (like `prebuilt-invoice` or `prebuilt-callCenter`)

You're **not** charged for contextualization when you:
- Only use content extraction without defining fields
- Use `prebuilt-read` or `prebuilt-layout` (these don't use generative models)

### How contextualization tokens are calculated

Contextualization tokens are calculated per unit of content:

| File type | Contextualization tokens |
|-----------|-------------------------|
| Document | 1,000 tokens per page |
| Text | 1,000 tokens per 1,000 characters |
| Image | 1,000 tokens per image |
| Audio | 1,667 tokens per minute |
| Video | 16,667 tokens per minute |

**Pricing**: $1.00 per 1 million contextualization tokens for both regular and mini models.

## Am I always charged for LLM usage no matter the prebuilt analyzer or custom analyzer?

No, LLM usage charges depend on whether the analyzer uses field extraction:

### Analyzers that use LLM (you're charged for tokens):
- Custom analyzers with defined fields
- `prebuilt-invoice`
- `prebuilt-callCenter`
- `prebuilt-documentAnalyzer`
- `prebuilt-imageAnalyzer`
- `prebuilt-audioAnalyzer`
- `prebuilt-videoAnalyzer`

### Analyzers that don't use LLM (no token charges):
- `prebuilt-read`: Only performs OCR, no field extraction
- `prebuilt-layout`: Only extracts layout and structure, no generative processing
- Custom analyzers with no fields defined (content extraction only)

If you explicitly don't request any fields, you only receive content extraction results and only pay for content extraction.

## What features increase token usage?

Several features increase the number of tokens consumed during field extraction:

### Baseline configuration (lowest token usage)
- All fields have `mode = "generative"`
- Source estimation is turned **off**
- No confidence score generation

### Features that increase tokens

| Feature | Token multiplier | Description |
|---------|-----------------|-------------|
| **Extractive mode** | ~1.5x | When all fields are set to `mode = "extractive"`, Content Understanding must perform additional analysis to locate and extract exact text spans |
| **Source estimation + confidence scores** | ~2x | When fields use source estimation and confidence score generation, Content Understanding performs additional processing with the generative model plus proprietary algorithms |
| **In-context learning (Knowledge Base)** | Variable | When you provide labeled examples in the knowledge base, Content Understanding retrieves and adds relevant examples into the context window, increasing token usage based on the number and size of examples |
| **Custom video segmentation** | Additional tokens | For videos, custom segmentation processes the video sequentially to break down the timeline, resulting in additional token consumption |

### Example comparison

For a 10-page document:
- **Baseline** (generative, no estimation): ~26,000 input tokens + ~900 output tokens
- **With extractive mode**: ~39,000 input tokens + ~900 output tokens  
- **With source estimation + confidence**: ~52,000 input tokens + ~1,800 output tokens

> [!TIP]
> Start with the baseline configuration and add features only when needed. Many scenarios work well without source estimation or extractive mode, significantly reducing costs.

## Cost estimation examples

Here are detailed examples showing how pricing works for different scenarios:

### Example 1: Processing documents for content ingestion (RAG)

**Scenario**: You need to extract content from documents for a Retrieval-Augmented Generation (RAG) solution. You use `prebuilt-documentAnalyzer` which extracts text, layout, and generates a summary.

**Input**:
- 1,000 documents
- Average 5 pages per document (5,000 total pages)
- Model: GPT-4o standard deployment
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 5,000 pages
   - Cost: (5,000 / 1,000) × $10.00 = **$50.00**

2. **Field extraction** (for summary generation):
   - Input tokens: 5,000 pages × 2,600 tokens/page = 13,000,000 tokens
   - Cost: (13,000,000 / 1,000,000) × $2.50 = **$32.50**
   - Output tokens: 5,000 pages × 90 tokens/page = 450,000 tokens
   - Cost: (450,000 / 1,000,000) × $10.00 = **$4.50**

3. **Contextualization**: 5,000 pages × 1,000 tokens/page = 5,000,000 tokens
   - Cost: (5,000,000 / 1,000,000) × $1.00 = **$5.00**

**Total estimated cost**: $50.00 + $32.50 + $4.50 + $5.00 = **$92.00**

**Cost per document**: $92.00 / 1,000 = **$0.092**

### Example 2: Processing invoices with field extraction

**Scenario**: You're automating invoice processing using `prebuilt-invoice` to extract structured data (invoice number, date, vendor, total, line items).

**Input**:
- 10,000 invoices
- Average 3 pages per invoice (30,000 total pages)
- Model: GPT-4o-mini deployment (cost-optimized)
- Features: Extractive mode + source estimation + confidence scores
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 30,000 pages
   - Cost: (30,000 / 1,000) × $10.00 = **$300.00**

2. **Field extraction** with 2x multiplier for source estimation + confidence:
   - Base input tokens: 30,000 pages × 2,600 tokens/page = 78,000,000 tokens
   - With 2x multiplier: 156,000,000 tokens
   - Cost: (156,000,000 / 1,000,000) × $1.00 = **$156.00** (mini pricing)
   - Base output tokens: 30,000 pages × 90 tokens/page = 2,700,000 tokens
   - With 2x multiplier: 5,400,000 tokens
   - Cost: (5,400,000 / 1,000,000) × $4.00 = **$21.60** (mini pricing)

3. **Contextualization**: 30,000 pages × 1,000 tokens/page = 30,000,000 tokens
   - Cost: (30,000,000 / 1,000,000) × $1.00 = **$30.00**

**Total estimated cost**: $300.00 + $156.00 + $21.60 + $30.00 = **$507.60**

**Cost per invoice**: $507.60 / 10,000 = **$0.051**

> [!NOTE]
> Using a standard deployment instead of mini would increase the field extraction cost by approximately 2.5x, bringing the total to approximately $800.

### Example 3: Analyzing video content

**Scenario**: You're analyzing video content to extract transcripts, identify keyframes, segment the video, and generate summaries using `prebuilt-videoAnalyzer`.

**Input**:
- 100 videos
- Average 10 minutes per video (1,000 total minutes)
- Model: GPT-4o standard deployment
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 1,000 minutes
   - Cost: 1,000 minutes × $0.10/minute = **$100.00**

2. **Field extraction**:
   - Input tokens: 1,000 minutes × 604 tokens/minute = 604,000 tokens
   - Cost: (604,000 / 1,000,000) × $2.50 = **$1.51**
   - Output tokens: 1,000 minutes × 19 tokens/minute = 19,000 tokens
   - Cost: (19,000 / 1,000,000) × $10.00 = **$0.19**

3. **Contextualization**: 1,000 minutes × 16,667 tokens/minute = 16,667,000 tokens
   - Cost: (16,667,000 / 1,000,000) × $1.00 = **$16.67**

**Total estimated cost**: $100.00 + $1.51 + $0.19 + $16.67 = **$118.37**

**Cost per video**: $118.37 / 100 = **$1.18**

### Example 4: Processing audio call center recordings

**Scenario**: You're analyzing call center recordings using `prebuilt-callCenter` to generate transcripts, speaker diarization, sentiment analysis, and summaries.

**Input**:
- 5,000 calls
- Average 6 minutes per call (30,000 total minutes)
- Model: GPT-4o-mini deployment
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 30,000 minutes
   - Cost: 30,000 minutes × $0.05/minute = **$1,500.00**

2. **Field extraction**:
   - Input tokens: 30,000 minutes × 604 tokens/minute = 18,120,000 tokens
   - Cost: (18,120,000 / 1,000,000) × $1.00 = **$18.12** (mini pricing)
   - Output tokens: 30,000 minutes × 19 tokens/minute = 570,000 tokens
   - Cost: (570,000 / 1,000,000) × $4.00 = **$2.28** (mini pricing)

3. **Contextualization**: 30,000 minutes × 1,667 tokens/minute = 50,010,000 tokens
   - Cost: (50,010,000 / 1,000,000) × $1.00 = **$50.01**

**Total estimated cost**: $1,500.00 + $18.12 + $2.28 + $50.01 = **$1,570.41**

**Cost per call**: $1,570.41 / 5,000 = **$0.31**

### Example 5: Processing images with captions

**Scenario**: You're generating descriptive captions for product images using `prebuilt-imageAnalyzer`.

**Input**:
- 10,000 images
- Model: GPT-4o standard deployment
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: No charge for images
   - Cost: **$0.00**

2. **Field extraction**:
   - Input tokens: 10,000 images × 1,043 tokens/image = 10,430,000 tokens
   - Cost: (10,430,000 / 1,000,000) × $2.50 = **$26.08**
   - Output tokens: 10,000 images × 170 tokens/image = 1,700,000 tokens
   - Cost: (1,700,000 / 1,000,000) × $10.00 = **$17.00**

3. **Contextualization**: 10,000 images × 1,000 tokens/image = 10,000,000 tokens
   - Cost: (10,000,000 / 1,000,000) × $1.00 = **$10.00**

**Total estimated cost**: $0.00 + $26.08 + $17.00 + $10.00 = **$53.08**

**Cost per image**: $53.08 / 10,000 = **$0.0053**

## Additional pricing considerations

### Embeddings for search scenarios

If you enable embeddings (for documents only), there are additional costs:

- **Model**: text-embedding-3-small (most common)
- **Tokens**: Typically ~1,500 tokens per page
- **Rate**: $0.02 per 1,000 tokens

**Example**: For 1,000 pages:
- Tokens: 1,000 × 1,500 = 1,500,000 tokens
- Cost: (1,500,000 / 1,000) × $0.02 = **$30.00**

### Regional pricing variations

Pricing may vary by region. Always check the [Azure AI Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) page for the most current rates in your region.

### Free tier considerations

Azure AI services typically offer a free tier for testing and development. Check the pricing page for current free tier limits.

## Cost optimization tips

### 1. Choose the right model deployment
Start with mini model deployments (like GPT-4o-mini) for most scenarios. They offer up to 60% cost savings with minimal quality impact for typical extraction tasks.

### 2. Use baseline field configuration
Unless you need source grounding or extractive mode, use the baseline configuration:
- Set fields to `mode = "generative"`
- Disable source estimation
- This can reduce token usage by up to 50%

### 3. Use prebuilt-read or prebuilt-layout when possible
If you only need OCR and layout extraction without field extraction, use `prebuilt-read` or `prebuilt-layout` to avoid LLM token charges.

### 4. Test before scaling
Always test with representative files to understand actual token usage before processing large volumes.

### 5. Optimize field definitions
- Only define fields you actually need
- Use clear, concise field descriptions
- Avoid redundant fields that can be computed from other extracted data

### 6. Monitor usage regularly
Use the Azure portal to monitor your usage and identify opportunities for optimization. See metrics under your Content Understanding resource.

### 7. Consider in-context learning carefully
While in-context learning (knowledge base) improves accuracy, it increases token usage. Use it only when baseline accuracy isn't sufficient.

## Next steps

- [Azure AI Content Understanding Pricing page](https://azure.microsoft.com/pricing/details/content-understanding/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Content Understanding quickstart](../quickstart/use-rest-api.md)
- [Best practices for Content Understanding](../concepts/best-practices.md)
- [Prebuilt analyzers](../concepts/prebuilt-analyzers.md)