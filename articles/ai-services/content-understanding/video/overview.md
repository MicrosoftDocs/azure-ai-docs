---
title: Azure AI Content Understanding video overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding video solutions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
---

# Azure AI Content Understanding video solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities before General Availability (GA).
> * For more information, *see* **[Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms)**.

Azure AI Content Understanding allows you to generate a standard set of video metadata and create custom fields for your specific use case using the power of generative models. Content Understanding helps efficiently manage, categorize, retrieve, and build workflows for video assets. It enhances your media asset library, supports workflows such as highlight generation, categorizes content, and facilitates applications like retrieval-augmented generation (RAG).

:::image type="content" source="../media/video/video-processing-flow.png" alt-text="Illustration of the Content Understanding video processing flow.":::

The **pre-built video analyzer** outputs RAG-ready Markdown that includes:

- **Transcript:** Inline transcripts in standard WEBVTT format
- **Description:** Natural-language segment descriptions with visual and speech context
- **Segmentation:** Automatic scene segmentation breaking the video into logical chunks
- **Key Frames:** Ordered key-frame thumbnails enabling deeper analysis

This format can drop straight into a vector store to enable an agent or RAG workflows—no post-processing required.

From there you can **customize the analyzer** for more fine-grained control of the output. You can define custom fields, segments, or enable face identification. Customization allows you to use the full power of generative models to extract deep insights from the visual and audio details of the video.

For example, customization allows you to:

- **Define custom fields:** to identify what products and brands are seen or mentioned in the video.
- **Generate custom segments:** to segment a news broadcast into chapters based on the topics or news stories discussed.
- **Identify people using a person directory** enabling a customer to label conference speakers in footage using face identification, for example, `CEO John Doe`, `CFO Jane Smith`.

## Why use Content Understanding for video?

Content understanding for video has broad potential uses. For example, you can customize metadata to tag specific scenes in a training video, making it easier for employees to locate and revisit important sections. You can also use metadata customization to identify product placement in promotional videos, which helps marketing teams analyze brand exposure. Other use cases include:

- **Broadcast media and entertainment:** Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.
- **Education and e-Learning:** Index and retrieve specific moments in educational videos or lectures.
- **Corporate training:** Organize training videos by key topics, scenes, or important moments.
- **Marketing and advertising:** Analyze promotional videos to extract product placements, brand appearances, and key messages.

## Prebuilt video analyzer example

With the prebuilt video analyzer (prebuilt-videoAnalyzer), you can upload a video and get an immediately usable knowledge asset. The service packages every clip into both richly formatted Markdown and JSON. This process allows your search index or chat agent to ingest without custom glue code.

* For example, creating the base `prebuilt-videoAnalyzer` as follows:

  ```jsonc
  {
    "config": {},
    "BaseAnalyzerId": "prebuilt-videoAnalyzer",
  }
  ```

* Next, analyzing a 30-second advertising video, would result in the following output:

```markdown
  # Video: 00:00.000 => 00:30.000
  Width: 1280
  Height: 720

  ## Segment 1: 00:00.000 => 00:06.000
  A lively room filled with people is shown, where a group of friends is gathered around a television. They are watching a sports event, possibly a football match, as indicated by the decorations and the atmosphere.

  Transcript

  WEBVTT

  00:03.600 --> 00:06.000
  <Speaker 1 Speaker>Get new years ready.

  Key Frames
  - 00:00.600 ![](keyFrame.600.jpg)
  - 00:01.200 ![](keyFrame.1200.jpg)

  ## Segment 2: 00:06.000 => 00:10.080
  The scene transitions to a more vibrant and energetic setting, where the group of friends is now celebrating. The room is decorated with football-themed items, and everyone is cheering and enjoying the moment.

  Transcript

  WEBVTT

  00:03.600 --> 00:06.000
  <Speaker 1 Speaker>Go team!

  Key Frames
  - 00:06.200 ![](keyFrame.6200.jpg)
  - 00:07.080 ![](keyFrame.7080.jpg)
  
     *…additional data omitted for brevity…*
```

## Walk-through

We recently published a walk-through for RAG on Video using Content Understanding.
[https://www.youtube.com/watch?v=fafneWnT2kw\&lc=Ugy2XXFsSlm7PgIsWQt4AaABAg](https://www.youtube.com/watch?v=fafneWnT2kw&lc=Ugy2XXFsSlm7PgIsWQt4AaABAg)

## Capabilities

1. [Content extraction](#content-extraction-capabilities)
1. [Field extraction](#field-extraction-and-segmentation)
1. [Face identification](#face-identification-description-add-on)

Under the hood, two stages transform raw pixels into business-ready insights. The diagram below shows how extraction feeds generation, ensuring each downstream step has the context it needs.

:::image type="content" source="../media/video/video-overview.png" alt-text="Screenshot of video analyzer flow.":::

The service operates in two stages. The first stage, content extraction, involves capturing foundational metadata such as transcripts, shots, and faces. The second stage, field extraction, uses a generative model to produce custom fields and perform segmentation. Additionally, you can optionally enable a Face add-on to identify individuals and describe them in the video.

## Content extraction capabilities

The first pass is all about extracting a first set of details—who's speaking, where are the cuts, and which faces recur. It creates a solid metadata backbone that later steps can reason over.

* **Transcription:** Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Sentence-level timestamps are available if `"returnDetails": true` is set. Content Understanding supports the full set of Azure AI Speech speech-to-text languages. For more information on supported languages, *see* [Language and region support](../language-region-support.md#language-support). The following transcription details are important to consider:

  * **Diarization:** Distinguishes between speakers in a conversation in the output, attributing parts of the transcript to specific speakers.
  * **Multilingual transcription:** Generates multilingual transcripts. Language/locale is applied per phrase in the transcript. Phrases output when `"returnDetails": true` is set. Deviating from language detection this feature is enabled when no language/locale is specified or language is set to `auto`.

    > [!NOTE]
    > When Multilingual transcription is used, any files with unsupported locales produce a result based on the closest supported locale, which is likely incorrect. This result is a known
    > behavior. Avoid transcription quality issues by ensuring that you configure locales when not using a multilingual transcription supported locale!

  * **Key frame extraction:** Extracts key frames from videos to represent each shot completely, ensuring each shot has enough key frames to enable field extraction to work effectively.
  * **Shot detection:** Identifies segments of the video aligned with shot boundaries where possible, allowing for precise editing and repackaging of content with breaks exactly existing edits. The output is a list of timestamps in milliseconds in `cameraShotTimesMs`. The output is only returned when `"returnDetails": true` is set.

## Field extraction and segmentation

Next, the generative model layers meaning—tagging scenes, summarizing actions, and slicing footage into segments per your request. This action is where prompts turn into structured data.

### Custom fields

Shape the output to match your business vocabulary. Use a `fieldSchema` object where each entry defines a field's name, type, and description. At run-time, the generative model fills those fields for every segment.

**Examples:**

* **Media asset management:**

  * **Video Category:** Helps editors and producers organize content, by classifying it as News, Sports, Interview, Documentary, Advertisement, etc. Useful for metadata tagging and quicker content filtering and retrieval.
  * **Color scheme:** Conveys mood and atmosphere, essential for narrative consistency and viewer engagement. Identifying color themes helps in finding matching clips for accelerated video editing.

* **Advertising:**

  * **Brand:** Identifies brand presence, critical for analyzing ad impact, brand visibility, and association with products. This capability allows advertisers to assess brand prominence and ensure compliance with branding guidelines.
  * **Ad categories:** Categorizes ad types by industry, product type, or audience segment, which supports targeted advertising strategies, categorization, and performance analysis.

**Example:**

```jsonc

"fieldSchema": {
  "description": "Extract brand presence and sentiment per scene",
  "fields": {
    "brandLogo": {
      "type": "string",
      "method": "generate",
      "description": "Brand being promoted in the video. Include the product name if available."
    },
    "Sentiment": {
      "type": "string",
      "method": "classify",
      "description": "Ad categories",
      "enum": [
        "Consumer Packaged Goods",
        "Groceries",
        "Technology"
      ]
    }
  }
}
```



### Segmentation mode

> [!NOTE]
>
> Setting segmentation triggers field extraction even if no fields are defined.


Content Understanding offers three ways to slice a video, letting you get the output you need for whole videos or short clips. You can use these options by setting the `SegmentationMode` property on a custom analyzer.

* **Whole-video** – `SegmentationMode = NoSegmentation`
  The service treats the entire video file as a single segment and extracts metadata across its full duration.

  **Example:**
    * Compliance checks that look for specific brand-safety issues anywhere in an ad
    * full-length descriptive summaries

* **Automatic segmentation** – `SegmentationMode = Auto`
  The service analyzes the timeline and breaks it up for you. Groups successive shots into coherent scenes, capped at one minute each.

  **Example:**
    * Create storyboards from a show
    * Inserting mid-roll ads at logical pauses.

* **Custom segmentation** – `SegmentationMode = Custom`
  You describe the logic in natural language and the model creates segments to match. Set `segmentationDefinition` with a string describing how you'd like the video to be segmented. Custom allows segments of varying length from seconds to minutes depending on the prompt.

  **Example:**
    * Break a news broadcast up into stories.

    ```jsonc
    {
      "segmentationMode": "custom",
      "segmentationDefinition": "news broadcasts divided by individual stories"
    }
    ```

## Face identification description add-on

> [!NOTE]
>
>  This feature is limited access and involves face identification and grouping; customers need to register for access at [Face Recognition](https://aka.ms/facerecognition). Face features incur added costs.

Face identification description is an add-on that provides context to content extraction and field extraction using face information.

### Content extraction - Grouping and identification

The face add-on enables grouping and identification as output from the content extraction section. To enable face capabilities set `"enableFace":true` in the analyzer configuration.

* **Grouping:** Grouped faces appearing in a video to extract one representative face image for each person and provides segments where each one is present. The grouped face data is available as metadata and can be used to generate customized metadata fields when `returnDetails: true` for the analyzer.
* **Identification:** Labels individuals in the video with names based on a Face API person directory. Customers can enable this feature by supplying a name for a Face API directory in the current resource in the `personDirectoryId` property of the analyzer. To use this capability, first you must create a personDirectory then reference it in the analyzer. For details on how to do that, check out [How to build a person directory](../../content-understanding/tutorial/build-person-directory.md)

### Field Extraction – Face description

 The field extraction capability is enhanced by providing detailed descriptions of identified faces in the video. This capability includes attributes such as facial hair, emotions, and the presence of celebrities, which can be crucial for various analytical and indexing purposes. To enable face capabilities set `disableFaceBlurring=true` in the analyzer configuration.

**Examples:**

* **Example field: emotionDescription:** Provides a description of the emotional state of the primary person in this clip (for example, `happy`, `sad`, `angry`)
* **Example field: facialHairDescription:** Describes the type of facial hair (for example, `beard`, `mustache`, `clean-shaven`)


## Key benefits

Content Understanding provides several key benefits when compared to other video analysis solutions:

* **Segment-based multi-frame analysis:** Identify actions, events, topics, and themes by analyzing multiple frames from each video segment, rather than individual frames.
* **Customization:** Customize the fields and segmentation you generate by modifying the schema in accordance with your specific use case.
* **Generative models:** Describe in natural language what content you want to extract, and Content Understanding uses generative models to extract that metadata.
* **Optimized preprocessing:** Perform several content extraction preprocessing steps, such as transcription and scene detection, optimized to provide rich context to AI generative models.


## Technical constraints and limitations

Specific limitations of video processing to keep in mind:

* **Frame sampling (\~ 1 FPS)**: The analyzer inspects about one frame per second. Rapid motions or single-frame events may be missed.
* **Frame resolution (512 × 512 px)**: Sampled frames are resized to 512 pixels square. Small text or distant objects can be lost.
* **Speech**: Only spoken words are transcribed. Music, sound effects, and ambient noise are ignored.

## Input requirements

For supported formats, see [Service quotas and limits](../service-limits.md).

## Supported languages and regions

See [Language and region support](../language-region-support.md).

## Data privacy and security

As with all Azure AI services, review Microsoft's [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) documentation.

> [!IMPORTANT]
>
> If you process **Biometric Data** (for example, enable **Face Grouping** or **Face Identification**), you must meet all notice, consent, and deletion requirements under GDPR or other applicable laws. See [Data and Privacy for Face](/legal/cognitive-services/face/data-privacy-security).

## Next steps

* Process videos in the [Azure AI Foundry portal](https://aka.ms/cu-landing).
* Quickstart: [Analyze video content with analyzer templates](../quickstart/use-ai-foundry.md).
* Samples:

  * [Video content extraction notebook](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/content_extraction.ipynb)
  * [Video search with natural language queries](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/tree/main#samples)
  * [Analyzer templates](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates)
