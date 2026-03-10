---
title: "Quickstart: Use the Content Understanding Python SDK"
author: PatrickFarley
manager: nitinme
description: Get started with the Content Understanding Python SDK to extract structured data from documents, images, audio, and video files.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://pypi.org/project/azure-ai-contentunderstanding/) | [Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples) | [SDK source](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This quickstart shows you how to use the Content Understanding Python SDK to extract structured data using prebuilt analyzers from document, image, audio, and video files. To learn more about prebuilt analyzers and other features, see the documentation of [Prebuilt Analyzers](../../concepts/prebuilt-analyzers.md).

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under Keys and Endpoint in the Azure portal).
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

## Create a client

The `ContentUnderstandingClient` is the main entry point for interacting with the service. Create an instance by providing your endpoint and credential.



```python
import os
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
key = os.environ["CONTENTUNDERSTANDING_KEY"]

client = ContentUnderstandingClient(endpoint=endpoint, credential=AzureKeyCredential(key))
```

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.


# [Document](#tab/document)

This example uses the `prebuilt-invoice` analyzer to extract structured data from an invoice document.

```python
import sys
from azure.ai.contentunderstanding.models import (
    AnalysisInput,
    AnalysisResult,
    DocumentContent,
    ArrayField,
    ObjectField,
)

# Sample invoice
invoice_url = (
    "https://raw.githubusercontent.com/"
    "Azure-Samples/"
    "azure-ai-content-understanding-assets/"
    "main/document/invoice.pdf"
)

poller = client.begin_analyze(
    analyzer_id="prebuilt-invoice",
    inputs=[AnalysisInput(url=invoice_url)],
)
result: AnalysisResult = poller.result()

if not result.contents or len(result.contents) == 0:
    print("No content found in the analysis result.")
    sys.exit(0)

# Get the document content
document_content: DocumentContent = (
    result.contents[0]  # type: ignore
)

print(
    f"Document unit: {document_content.unit or 'unknown'}"
)
print(
    f"Pages: {document_content.start_page_number}"
    f" to {document_content.end_page_number}"
)

if not document_content.fields:
    print("No fields found in the analysis result.")
    sys.exit(0)

# Extract simple string fields
customer_name = document_content.fields.get("CustomerName")
if customer_name:
    print(f"Customer Name: {customer_name.value}")
    if customer_name.confidence:
        print(
            f"  Confidence: {customer_name.confidence:.2f}"
        )
    print(f"  Source: {customer_name.source or 'N/A'}")

# Extract date fields
invoice_date = document_content.fields.get("InvoiceDate")
if invoice_date:
    print(f"Invoice Date: {invoice_date.value}")
    if invoice_date.confidence:
        print(
            f"  Confidence: {invoice_date.confidence:.2f}"
        )

# Extract object fields (nested structures)
total_amount = document_content.fields.get("TotalAmount")
if (
    isinstance(total_amount, ObjectField)
    and total_amount.value
):
    amount_field = total_amount.value.get("Amount")
    currency_field = total_amount.value.get(
        "CurrencyCode"
    )
    amount = (
        amount_field.value if amount_field else None
    )
    currency = (
        currency_field.value
        if currency_field and currency_field.value
        else ""
    )
    if isinstance(amount, (int, float)):
        print(f"\nTotal: {currency}{amount:.2f}")
    else:
        print(f"\nTotal: {currency}{amount or '(None)'}")

# Extract array fields (line items)
line_items = document_content.fields.get("LineItems")
if (
    isinstance(line_items, ArrayField)
    and line_items.value
):
    print(f"\nLine Items ({len(line_items.value)}):")
    for i, item in enumerate(line_items.value, 1):
        if (
            isinstance(item, ObjectField)
            and item.value
        ):
            desc = item.value.get("Description")
            qty = item.value.get("Quantity")
            description = (
                desc.value
                if desc and desc.value
                else "N/A"
            )
            quantity = (
                qty.value
                if qty and qty.value
                else "N/A"
            )
            print(f"  Item {i}: {description}")
            print(f"    Quantity: {quantity}")
```

This will produce the following output:
```text
Document unit: LengthUnit.INCH
Pages: 1 to 1
Customer Name: MICROSOFT CORPORATION
  Confidence: 0.39
  Source: D(1,6.2250,2.0092,8.0020,2.0077,8.0021,2.1638,6.2251,2.1653)
Invoice Date: 2019-11-15
  Confidence: 0.91

Total: USD110.00

Line Items (3):
  Item 1: Consulting Services
    Quantity: 2.0
  Item 2: Document Fee
    Quantity: 3.0
  Item 3: Printing Fee
    Quantity: 10.0
```

> [!NOTE]
> This code is based on the [sample_analyze_invoice.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_analyze_invoice.py) sample in the SDK repository.

# [Image](#tab/image)

This example uses the `prebuilt-imageSearch` analyzer to generate a description of the image.

```python
from azure.ai.contentunderstanding.models import AnalysisInput

image_url = "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/image/pieChart.jpg"

poller = client.begin_analyze(
    analyzer_id="prebuilt-imageSearch",
    inputs=[AnalysisInput(url=image_url)],
)
result = poller.result()

content = result.contents[0]
print(content.markdown)

summary = content.fields.get("Summary")
if summary and hasattr(summary, "value"):
    print(f"Summary: {summary.value}")
```

This will produce an output like the following:
```text
![image](pages/1)

Summary: The pie chart displays the distribution of hours spent in four categories: 1-39 hours (6.7%), 40-50 hours (18.9%), 50-60 hours (36.6%), and 60+ hours (37.8%). The largest segment is 60+ hours, followed closely by 50-60 hours, then 40-50 hours, and the smallest segment is 1-39 hours.
```
 > [!NOTE]
 > This code is based on the [sample_analyze_url.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_analyze_url.py) sample in the SDK repository.



# [Audio](#tab/audio)

This example uses the `prebuilt-audioSearch` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```python
from azure.ai.contentunderstanding.models import (
    AnalysisInput, 
    AudioVisualContent
)

audio_url = "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/audio/callCenterRecording.mp3"

poller = client.begin_analyze(
    analyzer_id="prebuilt-audioSearch",
    inputs=[AnalysisInput(url=audio_url)],
)
result = poller.result()

# Cast to AudioVisualContent for audio-specific properties (timing, transcript phrases, etc.)
audio_content: AudioVisualContent = result.contents[0]  # type: ignore
print(audio_content.markdown)

summary = audio_content.fields.get("Summary")
if summary and hasattr(summary, "value"):
    print(f"Summary: {summary.value}")

if audio_content.transcript_phrases and len(audio_content.transcript_phrases) > 0:
    print("Transcript (first two phrases):")
    for phrase in audio_content.transcript_phrases[:2]:
        print(f"  [{phrase.speaker}] {phrase.start_time_ms} ms: {phrase.text}")
```

This will produce an output like the following:
```text
# Audio: 00:00.000 => 00:32.183

Transcript

WEBVTT

00:00.080 --> 00:00.640
<v Speaker 1>Good day.

00:00.880 --> 00:02.240
<v Speaker 1>Welcome to Contoso.

00:02.560 --> 00:03.760
<v Speaker 1>My name is John Doe.

00:03.920 --> 00:05.120
<v Speaker 1>How can I help you today?

00:05.440 --> 00:06.320
<v Speaker 2>Yes, good day.

00:06.640 --> 00:08.160
<v Speaker 2>My name is Maria Smith.

00:08.560 --> 00:11.360
<v Speaker 2>I would like to inquire about my current point balance.

00:11.680 --> 00:12.560
<v Speaker 1>No problem.

00:12.880 --> 00:13.920
<v Speaker 1>I am happy to help.

00:14.240 --> 00:16.720
<v Speaker 1>I need your date of birth to confirm your identity.

00:17.120 --> 00:19.600
<v Speaker 2>It is April 19th, 1988.

00:20.000 --> 00:20.480
<v Speaker 1>Great.

00:20.800 --> 00:24.160
<v Speaker 1>Your current point balance is 599 points.

00:24.560 --> 00:26.160
<v Speaker 1>Do you need any more information?

00:26.480 --> 00:27.200
<v Speaker 2>No, thank you.

00:27.600 --> 00:28.320
<v Speaker 2>That was all.

00:28.720 --> 00:29.360
<v Speaker 2>Goodbye.

00:29.680 --> 00:31.920
<v Speaker 1>You're welcome, goodbye a Cantoso.

Summary: The conversation is a customer service interaction where Maria Smith contacts Contoso to inquire about her current point balance. The agent, John Doe, verifies her identity by asking for her date of birth and then provides her with the information that she has 599 points. The customer confirms that she does not need any further information and ends the call politely.
Transcript (first two phrases):
  [Speaker 1] 80 ms: Good day.
  [Speaker 1] 880 ms: Welcome to Contoso.
```
 > [!NOTE]
 > This code is based on the [sample_analyze_url.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_analyze_url.py) sample in the SDK repository.


# [Video](#tab/video)

This example uses the `prebuilt-videoSearch` analyzer to extract keyframes, transcript, and chapter segments from video.

```python
from azure.ai.contentunderstanding.models import (
    AnalysisInput,
    AudioVisualContent
)

video_url = "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/videos/sdk_samples/FlightSimulator.mp4"

poller = client.begin_analyze(
    analyzer_id="prebuilt-videoSearch",
    inputs=[AnalysisInput(url=video_url)],
)
result = poller.result()

# prebuilt-videoSearch can detect video segments, so iterate through all contents
for media in result.contents:
    video_content: AudioVisualContent = media  # type: ignore
    print(video_content.markdown)

    summary = video_content.fields.get("Summary")
    if summary and hasattr(summary, "value"):
        print(f"Summary: {summary.value}")

    print(f"Start: {video_content.start_time_ms} ms, End: {video_content.end_time_ms} ms")
    print(f"Frame size: {video_content.width} x {video_content.height}")
```

This will produce an output like the following:
```text
# Video: 00:00.733 => 00:15.467
Width: 1080
Height: 608

Transcript

WEBVTT

00:01.360 --> 00:06.640
<Speaker 1>When it comes to the neural TTS, in order to get a good voice, it's better to have good data.

00:07.120 --> 00:13.320
<Speaker 2>To achieve that, we build a universal TTS model based on 3,000 hours of data.

00:13.440 --> 00:23.680
<Speaker 1>We actually accumulated tons of the data so that this universal model is able to capture the nuance of the audio and generate a more natural voice for the algorithm.


Key Frames
- 00:00.733 ![](keyFrame.733.jpg)
- 00:02.067 ![](keyFrame.2067.jpg)
- 00:02.667 ![](keyFrame.2667.jpg)
- 00:04.067 ![](keyFrame.4067.jpg)
- 00:04.900 ![](keyFrame.4900.jpg)
- 00:05.733 ![](keyFrame.5733.jpg)
- 00:06.567 ![](keyFrame.6567.jpg)
- 00:07.800 ![](keyFrame.7800.jpg)
- 00:09.000 ![](keyFrame.9000.jpg)
- 00:09.800 ![](keyFrame.9800.jpg)
- 00:10.600 ![](keyFrame.10600.jpg)
- 00:12.100 ![](keyFrame.12100.jpg)
- 00:12.833 ![](keyFrame.12833.jpg)
- 00:14.200 ![](keyFrame.14200.jpg)
- 00:14.833 ![](keyFrame.14833.jpg)
- 00:15.467 ![](keyFrame.15467.jpg)
Summary: The video opens with a Flight Simulator plane flying over an island, followed by a discussion about neural text-to-speech (TTS) technology. A speaker explains the importance of having good data to create a natural voice, mentioning a universal TTS model built on 3,000 hours of data. Visuals include audio waveforms and shots of data centers and server farms, emphasizing the scale and technology behind the TTS model.
Start: 733 ms, End: 15467 ms
Frame size: 1080 x 608
# Video: 00:15.467 => 00:23.100
Width: 1080
Height: 608



Key Frames
- 00:15.467 ![](keyFrame.15467.jpg)
- 00:16.933 ![](keyFrame.16933.jpg)
- 00:17.767 ![](keyFrame.17767.jpg)
- 00:18.600 ![](keyFrame.18600.jpg)
- 00:20.167 ![](keyFrame.20167.jpg)
- 00:20.900 ![](keyFrame.20900.jpg)
- 00:21.633 ![](keyFrame.21633.jpg)
- 00:22.367 ![](keyFrame.22367.jpg)
- 00:23.100 ![](keyFrame.23100.jpg)
Summary: The video transitions to scenic aerial views from the Flight Simulator, showing a biplane flying over coastal and mountainous landscapes, including a castle. This segment visually showcases the realism and detail of the Flight Simulator environment.
Start: 15467 ms, End: 23100 ms
Frame size: 1080 x 608
# Video: 00:23.100 => 00:43.233
Width: 1080
Height: 608

Transcript

WEBVTT

00:24.040 --> 00:29.120
<Speaker 3>What we liked about cognitive services offerings were that they had a much higher fidelity.

00:29.600 --> 00:32.880
<Speaker 3>And they sounded a lot more like an actual human voice.

00:33.680 --> 00:37.200
<Speaker 4>Orlando ground 9555 requesting the end of pushback.

00:38.680 --> 00:41.280
<Speaker 4>9555 request to end pushback received.


Key Frames
- 00:23.100 ![](keyFrame.23100.jpg)
- 00:24.833 ![](keyFrame.24833.jpg)
- 00:25.700 ![](keyFrame.25700.jpg)
- 00:26.567 ![](keyFrame.26567.jpg)
- 00:27.433 ![](keyFrame.27433.jpg)
- 00:28.300 ![](keyFrame.28300.jpg)
- 00:29.167 ![](keyFrame.29167.jpg)
- 00:30.833 ![](keyFrame.30833.jpg)
- 00:31.633 ![](keyFrame.31633.jpg)
- 00:32.433 ![](keyFrame.32433.jpg)
- 00:33.900 ![](keyFrame.33900.jpg)
- 00:34.600 ![](keyFrame.34600.jpg)
- 00:36.067 ![](keyFrame.36067.jpg)
- 00:36.867 ![](keyFrame.36867.jpg)
- 00:38.200 ![](keyFrame.38200.jpg)
- 00:38.700 ![](keyFrame.38700.jpg)
- 00:39.900 ![](keyFrame.39900.jpg)
- 00:40.600 ![](keyFrame.40600.jpg)
- 00:41.300 ![](keyFrame.41300.jpg)
- 00:42.633 ![](keyFrame.42633.jpg)
- 00:43.233 ![](keyFrame.43233.jpg)
Summary: A new speaker discusses the high fidelity of cognitive services' TTS offerings, emphasizing how the voices sound more like actual human voices. The visuals shift to an airport scene with an Airbus plane being marshaled by ground crew, illustrating real-world aviation communication and tying back to the naturalness of the TTS voices.
Start: 23100 ms, End: 43233 ms
Frame size: 1080 x 608
```
 > [!NOTE]
 > This code is based on the [sample_analyze_url.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_analyze_url.py) sample in the SDK repository.



