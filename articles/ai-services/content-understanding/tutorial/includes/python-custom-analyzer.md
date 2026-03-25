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
Import required libraries and models, and then create the client with your resource endpoint and credentials. 

```python
import os
import time
from azure.ai.contentunderstanding import ContentUnderstandingClient
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

The following example creates a custom document analyzer based on the [prebuilt document base analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated fields or interpretations, and `classify` for categorization.

```python
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentFieldSchema,
    ContentFieldDefinition,
    ContentFieldType,
    GenerationMethod,
)

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
    }, # Required when using field_schema and prebuilt-document base analyzer
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

```
An example output looks like:

```text
Analyzer 'my_document_analyzer_ID' created successfully!
  Description: Custom analyzer for extracting company information
  Fields (4):
    - company_name: ContentFieldType.STRING (GenerationMethod.EXTRACT)
    - total_amount: ContentFieldType.NUMBER (GenerationMethod.EXTRACT)
    - document_summary: ContentFieldType.STRING (GenerationMethod.GENERATE)
    - document_type: ContentFieldType.STRING (GenerationMethod.CLASSIFY)
```

> [!TIP]
> This code is based on the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) sample in the SDK repository.


Optionally, you can create a classifier analyzer to categorize documents and use its results to route documents to prebuilt or custom analyzers you created. Here is an example of creating a custom analyzer for classification workflows.

```python
import time
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentCategoryDefinition,
)

# Generate a unique analyzer ID
analyzer_id = f"my_classifier_{int(time.time())}"

print(f"Creating classifier '{analyzer_id}'...")

# Define content categories for classification
categories = {
    "Loan_Application": ContentCategoryDefinition(
        description="Documents submitted by individuals or businesses to request funding, "
        "typically including personal or business details, financial history, "
        "loan amount, purpose, and supporting documentation."
    ),
    "Invoice": ContentCategoryDefinition(
        description="Billing documents issued by sellers or service providers to request "
        "payment for goods or services, detailing items, prices, taxes, totals, "
        "and payment terms."
    ),
    "Bank_Statement": ContentCategoryDefinition(
        description="Official statements issued by banks that summarize account activity "
        "over a period, including deposits, withdrawals, fees, and balances."
    ),
}

# Create analyzer configuration
config = ContentAnalyzerConfig(
    return_details=True,
    enable_segment=True,  # Enable automatic segmentation by category
    content_categories=categories,
)

# Create the classifier analyzer
classifier = ContentAnalyzer(
    base_analyzer_id="prebuilt-document",
    description="Custom classifier for financial document categorization",
    config=config,
    models={"completion": "gpt-4.1"},
)

# Create the classifier
poller = client.begin_create_analyzer(
    analyzer_id=analyzer_id,
    resource=classifier,
)
result = poller.result()  # Wait for creation to complete

# Get the full analyzer details after creation
result = client.get_analyzer(analyzer_id=analyzer_id)

print(f"Classifier '{analyzer_id}' created successfully!")
if result.description:
    print(f"  Description: {result.description}")
```
> [!TIP]
> This code is based on the [create_classifier](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_classifier.py) sample in the SDK repository.



# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image base analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```python
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentFieldSchema,
    ContentFieldDefinition,
    ContentFieldType,
    GenerationMethod,
)

# Generate a unique analyzer ID
analyzer_id = f"my_image_analyzer_{int(time.time())}"

# Define field schema with custom fields
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

# Create the analyzer with field schema
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

```
An example output looks like:
```text
Analyzer 'my_image_analyzer_ID' created successfully!
  Description: Custom analyzer for charts and graphs
  Fields (2):
    - Title: ContentFieldType.STRING (auto)
    - ChartType: ContentFieldType.STRING (GenerationMethod.CLASSIFY)
```
> [!TIP]
> This code adapts the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```python
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentFieldSchema,
    ContentFieldDefinition,
    ContentFieldType,
    GenerationMethod,
)
# Generate a unique analyzer ID
analyzer_id = f"my_audio_analyzer_{int(time.time())}"

# Define field schema with custom fields
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
            item_definition=ContentFieldDefinition(
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

# Create analyzer configuration
config = ContentAnalyzerConfig(
    locales=["en-US", "fr-FR"],
    return_details=True,
)

# Create the analyzer with field schema
analyzer = ContentAnalyzer(
    base_analyzer_id="prebuilt-audio",
    description=(
        "Custom analyzer for customer support calls"
    ),
    config=config,
    field_schema=field_schema,
    models={
        "completion": "gpt-4.1",
    },
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
```
An example output looks like:
```text
Analyzer 'my_audio_analyzer_ID' created successfully!
  Description: Custom analyzer for customer support calls
  Fields (3):
    - Summary: ContentFieldType.STRING (GenerationMethod.GENERATE)
    - Sentiment: ContentFieldType.STRING (GenerationMethod.CLASSIFY)
    - People: ContentFieldType.ARRAY (auto)
```

> [!TIP]
> This code adapts the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video base analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```python
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentFieldSchema,
    ContentFieldDefinition,
    ContentFieldType,
    GenerationMethod,
)
# Generate a unique analyzer ID
analyzer_id = f"my_video_analyzer_{int(time.time())}"

# Define field schema with custom fields
field_schema = ContentFieldSchema(
    name="video_schema",
    description=(
        "Schema for analyzing product demo videos"
    ),
    fields={
        "Segments": ContentFieldDefinition(
            type=ContentFieldType.ARRAY,
            item_definition=ContentFieldDefinition(
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

# Create analyzer configuration
config = ContentAnalyzerConfig(
    locales=["en-US", "fr-FR"],
    return_details=True,
)

# Create the analyzer with field schema
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
```
An example output looks like:
```text
Analyzer 'my_video_analyzer_ID' created successfully!
  Description: Custom analyzer for product demo videos
  Fields (1):
    - Segments: ContentFieldType.ARRAY (auto)
```

> [!TIP]
> This code adapts the [create_analyzer](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_create_analyzer.py) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields. Delete the analyzer when you no longer need it.

```python
# --- Use the custom document analyzer ---
from azure.ai.contentunderstanding.models import AnalysisInput

print("\nAnalyzing document...")
document_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-assets/"
    "main/document/invoice.pdf"
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
else:
    print("No content returned from analysis.")

# --- Clean up ---
print(f"\nCleaning up: deleting analyzer '{analyzer_id}'...")
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")
```
An example output looks like:
```text
Analyzing document...
Company Name: CONTOSO LTD.
  Confidence: 0.81
Total Amount: 610.0
Summary: This document is an invoice from CONTOSO LTD. to Microsoft Corporation for consulting, document, and printing services provided during the service period. It details line items, subtotal, sales tax, total, previous unpaid balance, and the final amount due.
Document Type: invoice

Cleaning up: deleting analyzer 'my_document_analyzer_ID'...
Analyzer 'my_document_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples).

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields. Delete the analyzer when you no longer need it.

```python
from azure.ai.contentunderstanding.models import AnalysisInput

# --- Use the custom image analyzer ---
print("\nAnalyzing image...")
image_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-assets/"
    "main/image/pieChart.jpg"
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
else:
    print("No content returned from analysis.")

# --- Clean up ---
print(f"\nCleaning up: deleting analyzer '{analyzer_id}'...")
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")
```
An example output looks like:
```text
Analyzing image...
Title: Distribution of Weekly Working Hours
Chart Type: pie

Cleaning up: deleting analyzer 'my_image_analyzer_ID'...   
Analyzer 'my_image_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples).

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields. Delete the analyzer when you no longer need it.

```python
from azure.ai.contentunderstanding.models import AnalysisInput

print("\nAnalyzing audio...")
audio_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-assets/"
    "main/audio/callCenterRecording.mp3"
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
else:
    print("No content returned from analysis.")

# --- Clean up ---
print(f"\nCleaning up: deleting analyzer '{analyzer_id}'...")
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")
```

An example output looks like:
```text
Analyzing audio...
Summary: Maria Smith contacted Contoso to inquire about her current point balance. John Doe, the representative, verified her identity by requesting her date of birth and informed her that her balance is 599 points. Maria confirmed she needed no further information and ended the call.
Sentiment: Positive

Cleaning up: deleting analyzer 'my_audio_analyzer_ID'...
Analyzer 'my_audio_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples).

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields. Delete the analyzer when you no longer need it.

```python
from azure.ai.contentunderstanding.models import AnalysisInput

print("\nAnalyzing video...")
video_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-assets/"
    "main/videos/sdk_samples/FlightSimulator.mp4"
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
else:
    print("No content returned from analysis.")

# --- Clean up ---
print(f"\nCleaning up: deleting analyzer '{analyzer_id}'...")
client.delete_analyzer(analyzer_id=analyzer_id)
print(f"Analyzer '{analyzer_id}' deleted successfully.")
```
An example output looks like:
```text
Analyzing video...
Found 16 segments
Segment 1:
  ID: 00:00:00.000-00:00:01.467
  Desc: The video opens with a scenic aerial view of an island, featuring a small airplane flying over the landscape. The screen displays the logos for 'Flight Simulator' and 'Microsoft Azure AI,' indicating a collaboration or integration between the two products.
Segment 2:
  ID: 00:00:01.467-00:00:03.233
  Desc: A man is shown sitting in a modern office setting, likely preparing to speak or introduce the topic. The background features geometric wall decorations and a plant, giving a professional and contemporary atmosphere.
Segment 3:
  ID: 00:00:03.233-00:00:07.367
  Desc: The segment displays a close-up of audio waveforms on a screen, visually representing sound data. This is accompanied by narration about the importance of good data for neural TTS (Text-to-Speech) and the process of building a universal TTS model using 3,000 hours of data.
Segment 4:
  ID: 00:00:07.367-00:00:08.200
  Desc: Another man appears in a similar office environment, possibly continuing the explanation or providing additional insights about the TTS model.
Segment 5:
  ID: 00:00:08.200-00:00:11.367
  Desc: The video transitions to an outdoor scene showing a large facility surrounded by fields, likely representing a data center or server farm. This visual supports the narration about accumulating large amounts of data for the universal TTS model.
Segment 6:
  ID: 00:00:11.367-00:00:13.567
  Desc: Inside a data center, rows of servers are shown, emphasizing the technological infrastructure required for processing and storing vast amounts of audio data.
Segment 7:
  ID: 00:00:13.567-00:00:16.100
  Desc: The first man returns, continuing his explanation in the office setting. The narration discusses how the universal model captures audio nuances to generate more natural voices.
Segment 8:
  ID: 00:00:16.100-00:00:19.433
  Desc: A biplane is seen flying over a picturesque landscape, reinforcing the connection to Flight Simulator and showcasing the realism enabled by advanced AI voice technology.
Segment 9:
  ID: 00:00:19.433-00:00:23.967
  Desc: A plane flies past a castle surrounded by lush greenery and mountains, further highlighting the immersive environments possible in Flight Simulator. The narration continues to emphasize the natural quality of AI-generated voices.
Segment 10:
  ID: 00:00:23.967-00:00:30.033
  Desc: A bald man is interviewed in a modern office space, discussing the high fidelity and human-like quality of voices produced by cognitive services offerings. The background features glass walls and plants, maintaining a professional tone.
Segment 11:
  ID: 00:00:30.033-00:00:33.200
  Desc: The interview continues with the bald man, focusing on the benefits of the AI voice technology. The setting remains consistent, reinforcing the credibility and expertise of the speaker.        
Segment 12:
  ID: 00:00:33.200-00:00:35.267
  Desc: The video shifts to a top-down view of an airplane on a runway, preparing for movement. This visual ties back to the Flight Simulator theme and the realism of the simulation.
Segment 13:
  ID: 00:00:35.267-00:00:37.700
  Desc: A ground crew member directs an Airbus aircraft, with pilots visible in the cockpit. The scene demonstrates realistic airport operations, likely enhanced by AI-driven voice interactions.       
Segment 14:
  ID: 00:00:37.700-00:00:39.200
  Desc: Two ground crew members walk near an airplane on the tarmac, with airport buildings in the background. The visuals continue to showcase the detailed simulation environment.
Segment 15:
  ID: 00:00:39.200-00:00:42.033
  Desc: A close-up of an Airbus aircraft at the gate, with sunlight illuminating the scene. The realism of the simulation is highlighted, possibly referencing the natural-sounding AI voices used in communications.
Segment 16:
  ID: 00:00:42.033-00:00:43.866
  Desc: The video concludes with the Microsoft logo and branding, signaling the end of the product demo and reinforcing the association with Microsoft Azure AI.

Cleaning up: deleting analyzer 'my_video_analyzer_ID'...   
Analyzer 'my_video_analyzer_ID' deleted successfully. 
```

> [!TIP]
> Check out more examples of running analyzers at [SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples).

---





