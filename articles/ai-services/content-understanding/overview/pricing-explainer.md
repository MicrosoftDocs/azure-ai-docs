---
title: Pricing explainer for Azure AI Content Understanding
titleSuffix: Azure AI services
description: Understand the pricing model for Azure AI Content Understanding, including what you're charged for, how to estimate costs, and pricing examples.
author: PatrickFarley
ms.author: jfilcik
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.date: 10/03/2025
ms.custom:
  - build-2025
---

# Pricing for Azure AI Content Understanding

This article provides a comprehensive explanation of the Azure AI Content Understanding pricing model. It helps you understand what you are charged for, how to estimate costs, and how different features affect your bill.

For specific pricing rates, see [Azure AI Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/).

## Content Understanding pricing components

Azure AI Content Understanding charges are based on two main components:

1. **Content extraction**: The base cost for extracting text, layout, and structure from your files (documents, audio, video)
2. **Field extraction**: Token-based charges when you define fields to extract structured data from your content


### Content extraction

Content Extraction is the essential first step for transforming unstructured input—whether it’s a document, audio, video, or image—into a standardized, reusable format. This process alone delivers significant value, as it allows you to consistently access and utilize information from any source, no matter how varied or complex the original data might be. Content Extraction also serves as the foundation for the more advanced data processing of Field Extraction.

The exact output from content extraction depends on the file type:

- **Documents**: Optical Character Recognition (OCR) to extract text, layout detection, table recognition, and structural elements
- **Audio**: Speech-to-text transcription
- **Video**: Frame extraction, scene detection, and speech-to-text transcription
- **Images**: No content extraction preformed (free)
- **Text**: No content extraction performed (free)

Content extraction is priced based on:
- **Documents**: Per 1,000 pages
- **Audio/Video**: Per minute

#### Figure Analysis add-on

Figure analysis is an optional enhancement to content extraction that automatically generates rich descriptions for images, charts, and diagrams within your documents. This feature is particularly valuable for retrieval-augmented generation (RAG) workflows, as it ensures that visual content is properly represented and searchable in your knowledge base.

**Cost impact**: Figure analysis adds generative model (LLM) token charges for each image analyzed. Each image processed requires additional input tokens to analyze the visual content and output tokens for the generated descriptions. The base content extraction charge remains the same—you only pay for the additional LLM calls needed to analyze the images.

### Field extraction:
Field Extraction is where your custom schema comes to life. Using generative models like GPT-4.1 and GPT-4.1-mini, we extract the specific fields you define—whether it’s invoice totals, contract terms, or customer sentiment. With this update. You can now choose the mode depending on your use case. These tokens will be charged based on the actual content processed by the generative models for field extraction using the standard Azure OpenAI tokenizer.

### Understanding the underlying service charges for field extraction

When you use field extraction, you incur charges from both Content Understanding and other Azure AI services that Content Understanding uses:

**From Content Understanding:**
- **Contextualization**: This is a token based charge for all the processing Content Understanding does to facilitate the generation of the fields. This processing enables confidence scores and source estimation. It also improves accuracy by expanding context around extracted content and optimizing the usage of the generative model context window. These tokens scale based on the length of the input in pages, minutes, or image count.

**From Azure AI Foundry Models:**
- **Azure AI Foundry Models - Generative model (LLMs)**: Token-based charges for the AI models (like GPT-4.1) that power field extraction
- **Azure AI Foundry Models -Embeddings model** (optional): Token-based charges for generating vector embeddings to leverage labeled data in a knowledge base to improve the accuracy of field extraction. Currently only support for documents. 

Your total cost is the sum of these components. If you only use content extraction without defining any fields, you're only charged for content extraction.

### Generative model tokens: What contributes to the input and output tokens for my analyzer?

When you use field extraction, you're charged for all the input and output tokens that are processed by the generative model. Content Understanding works to process your files most efficiently, carefully utilizing the context window of the LLM to balance cost with achieving the best quality results for your extraction tasks.

#### Understanding token counts

**Input tokens** include all the tokens that are passed to the generative model:
- Extracted text from documents and transcripts from audio
- Images tokens when images are passed directly to the model (currently standard for video, image and figure analysis)
- Your schema definition
- Content Understanding system prompts 
- Knowledge base in-context examples (if used)

**Output tokens** include:
- The field values returned from the model
- Structural overhead for organizing the output

### Embeddings for in context learning 

If you are using the in-context learning knowlege based then Content Understanding will use embeddings to lookup related label data in the knowlege base to improve the accuracy of field extraction (for documents only), there are additional costs:

- **Model**: text-embedding-3-small (most common)
- **Tokens**: Then entire document will be embedded onces. Typically ~1,500 tokens per page
- **Rate**: $0.02 per 1,000 tokens

**Example**: For 1,000 pages:
- Tokens: 1,000 × 1,500 = 1,500,000 tokens
- Cost: (1,500,000 / 1,000) × $0.02 = **$30.00**

### Contextualization tokens: What is contextualization & how is it charged?

Contextualization is an additional processing step that expands the context around extracted content to improve field extraction accuracy. Accurate field extraction depends on context, which is why Content Understanding includes a separate charge for contextualization.

#### What contextualization provides

Contextualization covers several critical processes that enhance accuracy and consistency:

- **Output normalization**: Standardizes extracted data into consistent formats
- **Source references**: Adds grounding to show where information came from in the source content
- **Confidence scores**: Calculates reliability metrics to help you determine which extractions need review
- **In-context learning support**: Enables continuous refinement of analyzers with feedback from your knowledge base examples

#### The value of contextualization

Contextualization is an investment in quality with measurable returns. For example, confidence scores enable more straight-through processing by automatically routing high-confidence extractions while flagging low-confidence items for review—reducing manual review costs and improving overall quality. These features are now priced transparently so you can see exactly where your value comes from.

**Important**: Contextualization tokens are always used as part of analyzers that run field extraction.

#### When you're charged for contextualization

You're charged for contextualization tokens when you:
- Enable field extraction (define fields in your analyzer)
- Use prebuilt analyzers that include field extraction (like `prebuilt-invoice` or `prebuilt-callCenter`)

You're **not** charged for contextualization when you:
- Only use content extraction without defining fields
- Use `prebuilt-read` or `prebuilt-layout` (these don't use generative models)

#### How contextualization tokens are calculated

Contextualization tokens are calculated per unit of content:

| Units | Contextualization Tokens | Effective Standard Price per unit |
|-------|-------------------------|-----------------------------------|
| 1 Page | 1,000 contextualization tokens | $1 per 1,000 pages |
| 1 Image | 1,000 contextualization tokens | $1 per 1,000 images |
| 1 hour audio | 100,000 contextualization tokens | $0.10 per hour |
| 1 hour video | 1,000,000 contextualization tokens | $1 per hour |

Assuming $1.00 per 1 million contextualization tokens.

## Estimating cost of a Content Understanding analyzer

To estimate costs for your workload, follow these steps:

### Step 1: Use the Azure Pricing Calculator

Find Content Understanding in the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) by searching for "Content Understanding" in the search box then configure:
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

### Step 3: Calculate averages and enter into the Pricing calculator

- Compute per-page,per-minute, or per-image averages number of tokens used from your test results
- Add those input and output token values into the pricing calculator

### Step 4: Read the total price in the calculator 
The Azure pricing calculator will give you a total cost estimate based on your total quantity of files and tokens

# Pricing frequently asked questions

## Am I always charged for LLM usage no matter the prebuilt analyzer or custom analyzer?

No, LLM usage charges depend on whether the analyzer uses field extraction:

### Example analyzers that use LLM:
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


## Am I charged twice for field extraction through both Content Understanding and Azure OpenAI?

No, you're not charged twice. When you use Content Understanding for field extraction with the GA version, you pay for Content Understanding for Content Extraction and Contextualization and Azure OpenAI for field extraction generation and embedding. 

## If I select a cheaper model, like GPT-4o-mini, or deployment type, like global, does it reduce the charge?

Yes, selecting a more cost-effective model deployment significantly reduces your charges for the generative model (LLM) component. Content Understanding supports different model deployment options from Azure OpenAI each with a different pricing:

### Ways to reduce model costs

1. **Smaller models** (like GPT-4o-mini): Optimized for cost, offering substantially lower pricing compared to standard models while maintaining quality for many scenarios

2. **Global or Data zone Deployments type**: Azure OpenAI global or data zone deployments provide additional cost savings

3. **Provisioned Throughput Units (PTUs)**: If your organization has dedicated throughput with Provisioned Throughput Units (PTU), you can leverage that capacity to get additional savings. 

When you choose a mini or global deployment, the input and output token costs for the generative model are reduced. For example at the time fo this writing:
- Regional Deployment of GPT 4.1:      $2.20 per 1M input tokens
- Global Deployment of GPT 4.1:        $2.0  per 1M input tokens (9% savings)
- Regional Deployment of GPT 4.1 mini: $0.40 per 1M input tokens (82% savings)

*Note: These numbers are only for illustration purposes. Model prices changes frequently. Check the official (Azure pricing page)[https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/] for up to date pricing*

### What charges remain the same

Important to note: **Content extraction** and **contextualization** charges from Content Understanding remain the same regardless of which model deployment you use. Only the generative model (LLM) token charges vary based on your deployment choice.

> [!TIP]
> Mini models offer excellent value for many common extraction tasks. Test with mini models to see if they'll provide accurate results for your tasks. Consider global deployments for additional cost optimization. 

## What features increase token usage?

Many things can influence token usage, like the contents of the files you process, instructions in your schema, etc. However, there are several features are worth noting that directly increase the number of tokens consumed during field extraction:

### Features that increase tokens

| Feature | Token multiplier | Description |
|---------|-----------------|-------------|
| **Extractive mode** | ~1.5x | When all fields are set to `mode = "extractive"`, Content Understanding must perform additional analysis to locate and extract exact text spans |
| **Generative mode fields with Source estimation and confidence scores** | ~2x | When fields use source estimation and confidence scores are enabled for generative mode fields, Content Understanding performs additional processing with the generative model plus proprietary algorithms to generate the additional output |
| **In-context learning (Knowledge Base)** | Variable | When you provide labeled examples in the knowledge base, Content Understanding retrieves and adds relevant examples into the context window, increasing token usage based on the number and size of examples. |
| **Custom video segmentation** | Additional output tokens | For videos, custom segmentation outputs fields for each segment identified in the video. The quantity of additional tokens depends on the number of segments in the video.  |

Token multiplier refers to the approx increase in cost when enabling this feature compared to a baseline. The baseline would be to process the same files with the following settings:

- All fields have `mode = "generative"`
- Source estimation is turned **off**
- No confidence score generation
- Segmentation = NoSegmentation

### Example comparison

For a 10-page document:
- **Baseline** (generative, no estimation): ~26,000 input tokens + ~900 output tokens
- **With extractive mode**: ~39,000 input tokens + ~1350 output tokens  
- **Generative model With source estimation + confidence**: ~52,000 input tokens + ~1,800 output tokens


## Cost estimation examples

Here are detailed examples showing how pricing works for different scenarios. All examples use global deployment pricing for GPT-4.1 and GPT-4.1-mini models.

### Example 1: Processing documents for content ingestion (RAG)

**Scenario**: You need to extract content from documents for a Retrieval-Augmented Generation (RAG) solution. You use `prebuilt-documentAnalyzer` which extracts text, layout, andfigure descriptions.

**Input**:
- 1,000 pages
- Model: GPT-4.1 global deployment
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 1,000 pages
   - Cost: (1,000 / 1,000) × $5.00 = **$5.00**

2. **Field extraction** (for figure description):

   Assuming 2 figures per page. It costs about 1000 input and 200 output tokens per figure.

   - Input tokens: 2,000 figures × 1000 tokens/image = 2,000,000 tokens
   - Cost: (2,000,000 / 1,000,000) × $2.00 = **$4.00**
   - Output tokens: 2,000 pages × 200 tokens/page = 400,000 tokens
   - Cost: (400,000 / 1,000,000) × $8.00 = **$3.2**

3. **Contextualization**: 1,000 pages × 1,000 tokens/page = 1,000,000 tokens
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**

**Total estimated cost**: $5.00 + $4 + $3.2 + $1.00 = **$13.20**

### Example 2: Processing invoices with field extraction

**Scenario**: You're automating invoice processing using `prebuilt-invoice` to extract structured data (invoice number, date, vendor, total, line items).

**Input**:
- 1,000 pages
- Model: GPT-4.1-mini global deployment (cost-optimized)
- Features: Extractive mode + source estimation + confidence scores
- Region: East US

**Pricing breakdown**:

1. **Content extraction**: 1,000 pages
   - Cost: (1,000 / 1,000) × $5.00 = **$5.00**

2. **Field extraction** with 2x multiplier for source estimation + confidence:
   - Base input tokens: 1,000 pages × 2,600 tokens/page = 2,600,000 tokens
   - With 2x multiplier: 5,200,000 tokens
   - Cost: (5,200,000 / 1,000,000) × $0.40 = **$2.08** (mini pricing)
   - Base output tokens: 1,000 pages × 90 tokens/page = 90,000 tokens
   - With 2x multiplier: 180,000 tokens
   - Cost: (180,000 / 1,000,000) × $1.60 = **$0.29** (mini pricing)

3. **Contextualization**: 1,000 pages × 1,000 tokens/page = 1,000,000 tokens
   - Cost: (1,000,000 / 1,000,000) × $1.00 = **$1.00**

**Total estimated cost**: $5.00 + $2.08 + $0.29 + $1.00 = **$8.37**


> [!NOTE]
> Using a standard GPT-4.1 global deployment instead of mini would increase the field extraction cost by approximately 5x, bringing the total to approximately $33.

### Example 3: Analyzing video content with segment-level field extraction

**Scenario**: You're analyzing video content to extract structured data at a segment level using `prebuilt-videoAnalyzer`. Segments are short clips of 15-30 seconds on average, resulting in numerous output segments with structured fields per segment.

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
> Actual cost savings will vary based on the specifics of your input and output. This transparent, usage-based billing model ensures you only pay for what you use.

### Example 4: Processing audio call center recordings

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
   - Cost: (36,240 / 1,000,000) × $0.40 = **$0.01** (mini pricing)
   - Output tokens: 60 minutes × 19 tokens/minute = 1,140 tokens
   - Cost: (1,140 / 1,000,000) × $1.60 = **$0.00** (mini pricing)

3. **Contextualization**: 60 minutes × 1,667 tokens/minute = 100,020 tokens
   - Cost: (100,020 / 1,000,000) × $1.00 = **$0.10**

**Total estimated cost**: $0.36 + $0.01 + $0.00 + $0.10 = **$0.47**

### Example 5: Processing images with captions

**Scenario**: You're generating descriptive captions for product images using `prebuilt-imageAnalyzer`.

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

## Additional pricing considerations

### Regional pricing variations

Pricing may vary by region. Always check the [Azure AI Content Understanding Pricing](https://azure.microsoft.com/pricing/details/content-understanding/) page for the most current rates in your region.


## Cost optimization tips

### 1. Choose the right model deployment
Starting with mini model deployments (like GPT-4o-mini) can offer up to 80% cost savings with minimal quality impact for typical light extraction tasks.

### 2. Use source Estimation only when needed
Unless you need source estimation or extractive mode, use the baseline configuration:
- Set fields to `mode = "generative"`
- Disable source estimation
- This can reduce token usage by up to 50%

### 3. Test before scaling
Always test with representative files to understand actual token usage before processing large volumes.

### 4. Optimize field definitions
- Only define fields you actually need
- Use clear, concise field descriptions
- Avoid redundant fields that can be computed from other extracted data

### 5. Monitor usage regularly
Use the Azure portal to monitor your usage and identify opportunities for optimization. See metrics under your Content Understanding resource.


## Next steps

- [Azure AI Content Understanding Pricing page](https://azure.microsoft.com/pricing/details/content-understanding/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Content Understanding quickstart](../quickstart/use-rest-api.md)
- [Best practices for Content Understanding](../concepts/best-practices.md)
- [Prebuilt analyzers](../concepts/prebuilt-analyzers.md)