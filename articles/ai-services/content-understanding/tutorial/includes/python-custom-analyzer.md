---
title: "Tutorial: Create a custom analyzer using the Content Understanding Python SDK"
author: PatrickFarley
manager: nitinme
description: Learn to create a custom analyzer with Content Understanding using the Python SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/16/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://pypi.org/project/azure-ai-contentunderstanding/) | [Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples) | [SDK source](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This guide shows you how to use the Content Understanding Python SDK to create a custom analyzer that extracts structured data from your content. Custom analyzers support document, image, audio, and video content types.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under **Keys and Endpoint** in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_update_defaults.py) for setup instructions.
* [Python 3.9 or later](https://www.python.org/).

## Set up

1. Install the Content Understanding client library for Python with pip:

    ```console
    pip install azure-ai-contentunderstanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    pip install azure-identity
    ```

## Set up environment variables

To authenticate with the Content Understanding service, set the environment variables with your own values before running the sample:
1) `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
2) `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

### Windows

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

### Linux / macOS

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create the client
Import required libraries and models. Create the client with your resource endpoint and credentials. 

```python
import os
import time
from azure.ai.contentunderstanding import (
    ContentUnderstandingClient,
)
from azure.ai.contentunderstanding.models import (
    AnalysisInput,
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentFieldSchema,
    ContentFieldDefinition,
    ContentFieldType,
    GenerationMethod,
)
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
key = os.environ["CONTENTUNDERSTANDING_KEY"]

client = ContentUnderstandingClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)
```

## Create a custom analyzer

# [Document](#tab/document)

The following example creates a custom document analyzer based on the [prebuilt document analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated fields or interpretations, and `classify` for categorization.

```python
# Generate a unique analyzer ID
analyzer_id = f"my_document_analyzer_{int(time.time())}"

# Define field schema with custom fields
field_schema = ContentFieldSchema(
    name="company_schema",
    description="Schema for extracting company information",
    fields={
        "company_name": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.EXTRACT,
            description="Name of the company",
            estimate_source_and_confidence=True,
        ),
        "total_amount": ContentFieldDefinition(
            type=ContentFieldType.NUMBER,
            method=GenerationMethod.EXTRACT,
            description="Total amount on the document",
            estimate_source_and_confidence=True,
        ),
        "document_summary": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.GENERATE,
            description=(
                "A brief summary of the document content"
            ),
        ),
        "document_type": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.CLASSIFY,
            description="Type of document",
            enum=[
                "invoice", "receipt", "contract",
                "report", "other",
            ],
        ),
    },
)

# Create analyzer configuration
config = ContentAnalyzerConfig(
    enable_formula=True,
    enable_layout=True,
    enable_ocr=True,
    estimate_field_source_and_confidence=True,
    return_details=True,
)

# Create the analyzer with field schema
analyzer = ContentAnalyzer(
    base_analyzer_id="prebuilt-document",
    description=(
        "Custom analyzer for extracting company information"
    ),
    config=config,
    field_schema=field_schema,
    models={
        "completion": "gpt-4.1",
        "embedding": "text-embedding-3-large",
    }, # Required when using field_schema
)

# Create the analyzer
poller = client.begin_create_analyzer(
    analyzer_id=analyzer_id,
    resource=analyzer,
)
result = poller.result() # Wait for creation to complete

# Get the full analyzer details after creation
result = client.get_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' created successfully!")

if result.description:
    print(f"  Description: {result.description}")

if result.field_schema and result.field_schema.fields:
    print(f"  Fields ({len(result.field_schema.fields)}):")
    for field_name, field_def in result.field_schema.fields.items():
        method = field_def.method if field_def.method else "auto"
        field_type = field_def.type if field_def.type else "unknown"
        print(f"    - {field_name}: {field_type} ({method})")

# Clean up - delete the analyzer
print(f"\nCleaning up: deleting analyzer '{analyzer_id}'...")
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")

```

> [!TIP]
> This code is based on the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) sample in the SDK repository.

# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```python
analyzer_id = f"my_image_analyzer_{int(time.time())}"

field_schema = ContentFieldSchema(
    name="chart_schema",
    description=(
        "Schema for extracting chart information"
    ),
    fields={
        "Title": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            description="Title of the chart",
        ),
        "ChartType": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.CLASSIFY,
            description="Type of chart",
            enum=["bar", "line", "pie"],
        ),
    },
)

analyzer = ContentAnalyzer(
    base_analyzer_id="prebuilt-image",
    description=(
        "Custom analyzer for charts and graphs"
    ),
    field_schema=field_schema,
    models={
        "completion": "gpt-4.1",
    },
)

poller = client.begin_create_analyzer(
    analyzer_id=analyzer_id,
    resource=analyzer,
)
result = poller.result()
print(f"Analyzer '{analyzer_id}' created successfully!")
```

> [!TIP]
> This code adapts the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```python
analyzer_id = f"my_audio_analyzer_{int(time.time())}"

field_schema = ContentFieldSchema(
    name="call_center_schema",
    description=(
        "Schema for analyzing customer support calls"
    ),
    fields={
        "Summary": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.GENERATE,
            description="Summary of the call",
        ),
        "Sentiment": ContentFieldDefinition(
            type=ContentFieldType.STRING,
            method=GenerationMethod.CLASSIFY,
            description="Overall sentiment of the call",
            enum=["Positive", "Neutral", "Negative"],
        ),
        "People": ContentFieldDefinition(
            type=ContentFieldType.ARRAY,
            description="List of people mentioned",
            items=ContentFieldDefinition(
                type=ContentFieldType.OBJECT,
                properties={
                    "Name": ContentFieldDefinition(
                        type=ContentFieldType.STRING,
                    ),
                    "Role": ContentFieldDefinition(
                        type=ContentFieldType.STRING,
                    ),
                },
            ),
        ),
    },
)

config = ContentAnalyzerConfig(
    locales=["en-US", "fr-FR"],
    return_details=True,
)

analyzer = ContentAnalyzer(
    base_analyzer_id="prebuilt-audio",
    description=(
        "Custom analyzer for customer support calls"
    ),
    config=config,
    field_schema=field_schema,
)

poller = client.begin_create_analyzer(
    analyzer_id=analyzer_id,
    resource=analyzer,
)
result = poller.result()
print(f"Analyzer '{analyzer_id}' created successfully!")
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```python
analyzer_id = f"my_video_analyzer_{int(time.time())}"

field_schema = ContentFieldSchema(
    name="video_schema",
    description=(
        "Schema for analyzing product demo videos"
    ),
    fields={
        "Segments": ContentFieldDefinition(
            type=ContentFieldType.ARRAY,
            items=ContentFieldDefinition(
                type=ContentFieldType.OBJECT,
                properties={
                    "SegmentId": ContentFieldDefinition(
                        type=ContentFieldType.STRING,
                    ),
                    "Description": ContentFieldDefinition(
                        type=ContentFieldType.STRING,
                        method=GenerationMethod.GENERATE,
                        description=(
                            "Detailed summary of the "
                            "video segment"
                        ),
                    ),
                    "Sentiment": ContentFieldDefinition(
                        type=ContentFieldType.STRING,
                        method=GenerationMethod.CLASSIFY,
                        enum=[
                            "Positive", "Neutral",
                            "Negative",
                        ],
                    ),
                },
            ),
        ),
    },
)

config = ContentAnalyzerConfig(
    locales=["en-US", "fr-FR"],
    return_details=True,
    segmentation_mode="auto",
)

analyzer = ContentAnalyzer(
    base_analyzer_id="prebuilt-video",
    description=(
        "Custom analyzer for product demo videos"
    ),
    config=config,
    field_schema=field_schema,
    models={
        "completion": "gpt-4.1",
    },
)

poller = client.begin_create_analyzer(
    analyzer_id=analyzer_id,
    resource=analyzer,
)
result = poller.result()
print(f"Analyzer '{analyzer_id}' created successfully!")
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields.

```python
document_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-python/"
    "main/data/receipt.png"
)

poller = client.begin_analyze(
    analyzer_id=analyzer_id,
    inputs=[AnalysisInput(url=document_url)],
)
result = poller.result()

if result.contents and len(result.contents) > 0:
    content = result.contents[0]
    if content.fields:
        company = content.fields.get("company_name")
        if company:
            print(f"Company Name: {company.value}")
            if company.confidence:
                print(
                    f"  Confidence:"
                    f" {company.confidence:.2f}"
                )

        total = content.fields.get("total_amount")
        if total:
            print(f"Total Amount: {total.value}")

        summary = content.fields.get(
            "document_summary"
        )
        if summary:
            print(f"Summary: {summary.value}")

        doc_type = content.fields.get("document_type")
        if doc_type:
            print(f"Document Type: {doc_type.value}")
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for document content.

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields.

```python
image_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-python/"
    "main/data/pieChart.jpg"
)

poller = client.begin_analyze(
    analyzer_id=analyzer_id,
    inputs=[AnalysisInput(url=image_url)],
)
result = poller.result()

if result.contents and len(result.contents) > 0:
    content = result.contents[0]
    if content.fields:
        title = content.fields.get("Title")
        if title:
            print(f"Title: {title.value}")

        chart_type = content.fields.get("ChartType")
        if chart_type:
            print(f"Chart Type: {chart_type.value}")
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for image content.

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields.

```python
audio_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-python/"
    "main/data/audio.wav"
)

poller = client.begin_analyze(
    analyzer_id=analyzer_id,
    inputs=[AnalysisInput(url=audio_url)],
)
result = poller.result()

if result.contents and len(result.contents) > 0:
    content = result.contents[0]
    if content.fields:
        summary = content.fields.get("Summary")
        if summary:
            print(f"Summary: {summary.value}")

        sentiment = content.fields.get("Sentiment")
        if sentiment:
            print(f"Sentiment: {sentiment.value}")
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for audio content.

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields.

```python
video_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-python/"
    "main/data/FlightSimulator.mp4"
)

poller = client.begin_analyze(
    analyzer_id=analyzer_id,
    inputs=[AnalysisInput(url=video_url)],
)
result = poller.result()

if result.contents and len(result.contents) > 0:
    content = result.contents[0]
    if content.fields:
        segments = content.fields.get("Segments")
        if segments and segments.value:
            print(f"Found {len(segments.value)} segments")
            for i, segment in enumerate(
                segments.value
            ):
                if segment.value:
                    seg_id = segment.value.get(
                        "SegmentId"
                    )
                    desc = segment.value.get(
                        "Description"
                    )
                    print(f"Segment {i + 1}:")
                    if seg_id:
                        print(
                            f"  ID: {seg_id.value}"
                        )
                    if desc:
                        print(
                            f"  Desc: {desc.value}"
                        )
```

> [!TIP]
> This code adapts the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for video content.

---

## Clean up resources

Delete the analyzer when you no longer need it.

```python
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")
```

> [!NOTE]
> The document example is based on the [sample_create_analyzer.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) sample. Custom analyzers support the same field schema concepts across all content types. For the complete set of samples, see [Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples).