---
title: Azure Content Understanding in Foundry Tools video overview
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools video solutions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Azure Content Understanding in Foundry Tools video solutions

Azure Content Understanding allows you to generate a standard set of video metadata and create custom fields for your specific use case using generative models. Content Understanding helps you manage, categorize, retrieve, and build workflows for video assets. It enhances your media asset library, supports features such as highlight generation, categorizes content, and facilitates applications like retrieval-augmented generation (RAG).

:::image type="content" source="../media/video/video-processing-flow.png" alt-text="Illustration of the Content Understanding video processing flow.":::

The **pre-built video analyzer** (`prebuilt-videoAnalysis`) outputs RAG-ready output. In Markdown it outputs the following:
- **Transcript:** Inline transcripts in standard WEBVTT format
- **Key Frames:** Ordered key-frame thumbnails enabling deeper analysis

And the JSON schema contains more details from the visual analysis. 
- **Description:** Natural-language segment descriptions with visual and speech context
- **Segmentation:** Automatic scene segmentation breaking the video into logical chunks based on categories you define

This format can drop straight into a vector store to enable an agent or RAG workflow—no post-processing is required.

From there you can customize the analyzer for more fine-grained control of the output. You can define custom fields and segments. Customization allows you to use the full power of generative models to extract deep insights from the visual and audio details of the video.

For example, customization allows you to:
- **Define custom fields:** to identify what products and brands are seen or mentioned in the video.
- **Generate custom segments:** to segment a news broadcast into chapters based on the topics or news stories discussed.
- **Identify prominent people using face description:** enabling a customer to label celebrities in footage with name and title based on the generative model's world knowledge, for example, `Satya Nadella`.

## Why use Content Understanding for video?

Content understanding for video has broad potential uses. For example, you can customize metadata to tag specific scenes in a training video, making it easier for employees to locate and revisit important sections. You can also use metadata customization to identify product placement in promotional videos, which helps marketing teams analyze brand exposure. Other use cases include:
- **Broadcast media and entertainment:** Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.
- **Education and e-Learning:** Index and retrieve specific moments in educational videos or lectures.
- **Corporate training:** Organize training videos by key topics, scenes, or important moments.
- **Marketing and advertising:** Analyze promotional videos to extract product placements, brand appearances, and key messages.

## Prebuilt video analyzer example

With the prebuilt video analyzer (prebuilt-videoSearch), you can upload a video and get an immediately usable knowledge asset. The service packages the content into richly formatted Markdown and JSON. This process allows your search index or chat agent to ingest the content without custom glue code.

1. For example, call the analyzer designed for Retrieval-augmented generation for video `prebuilt-videoSearch`. See the [REST API quickstart](../quickstart/use-rest-api.md) for details.

1. Next, analyzing a 30-second advertising video, would result in the following output:

   ```markdown
     # Video: 00:00.000 => 00:06.000
     A lively room filled with people is shown, where a group of friends is gathered around a television. They are watching a sports event, possibly a football match, as indicated by the decorations and the atmosphere.

     Transcript

     WEBVTT

     00:03.600 --> 00:06.000
     <Speaker 1>Get new years ready.

     Key Frames
     - 00:00.600 ![](keyFrame.600.jpg)
     - 00:01.200 ![](keyFrame.1200.jpg)

     ## Video: 00:06.000 => 00:10.080
     The scene transitions to a more vibrant and energetic setting, where the group of friends is now celebrating. The room is decorated with football-themed items, and everyone is cheering and enjoying the moment.

     Transcript

     WEBVTT

     00:03.600 --> 00:06.000
     <Speaker 1>Go team!

     Key Frames
     - 00:06.200 ![](keyFrame.6200.jpg)
     - 00:07.080 ![](keyFrame.7080.jpg)

        *…additional data omitted for brevity…*
   ```

## Walkthrough

See the following walkthrough for RAG on Video using Content Understanding:

[RAG on Video using Azure Content Understanding](https://www.youtube.com/watch?v=fafneWnT2kw&lc=Ugy2XXFsSlm7PgIsWQt4AaABAg)

## Capabilities

- [Content extraction](#content-extraction-capabilities)
- [Field extraction](#field-extraction-and-segmentation)

> [!NOTE]
> Face identification and grouping capabilities are only available in the preview API version and are not included in the GA release.

Under the hood, two stages transform raw pixels into business-ready insights. The diagram below shows how extraction feeds generation, ensuring each downstream step has the context it needs.

:::image type="content" source="../media/video/video-overview.png" alt-text="Screenshot of video analyzer flow.":::

The service operates in two stages. The first stage, content extraction, involves capturing foundational metadata such as transcripts and shots. The second stage, field extraction, uses a generative model to produce custom fields and perform segmentation.

## Content extraction capabilities

The first pass is all about extracting a first set of details—who's speaking and where are the cuts. It creates a solid metadata backbone that later steps can reason over.

* **Transcription:** Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Sentence-level timestamps are available if `"returnDetails": true` is set. Content Understanding supports the full set of Azure Speech in Foundry Tools speech-to-text languages. Details of language support for video are the same as audio, *see* [Audio Language Handling](../audio/overview.md#language-handling) for details. The following transcription details are important to consider:

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

* **Media asset management:**

  * **Video Category:** Helps editors and producers organize content, by classifying it as News, Sports, Interview, Documentary, Advertisement, etc. Useful for metadata tagging and quicker content filtering and retrieval.
  * **Color scheme:** Conveys mood and atmosphere, essential for narrative consistency and viewer engagement. Identifying color themes helps in finding matching clips for accelerated video editing.

* **Advertising:**

  * **Brand:** Identifies brand presence, critical for analyzing ad impact, brand visibility, and association with products. This capability allows advertisers to assess brand prominence and ensure compliance with branding guidelines.
  * **Ad categories:** Categorizes ad types by industry, product type, or audience segment, which supports targeted advertising strategies, categorization, and performance analysis.

**Example:**

```json
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
### Face description fields

> [!NOTE]
>
>  This feature is limited access; customers need to request to disable face blur for Azure OpenAI models with an Azure support request. Learn more [Manage an Azure support request](/azure/azure-portal/supportability/how-to-manage-azure-support-request).

The field extraction capability can optionally be enhanced to provide detailed descriptions of faces in the video. This capability includes attributes such as facial hair, facial expression, and the presence of celebrities, which can be crucial for various analytical and indexing purposes. To enable face description capabilities set `disableFaceBlurring : true` in the analyzer configuration.

**Examples:**

* **Example field: facialHairDescription:** Describes the type of facial hair (for example, `beard`, `mustache`, `clean-shaven`)
* **Example field: nameOfProminentPerson:** Provides a name if possible of a celebrity in the video (for example, `Satya Nadella`)
* **Example field: faceSmilingFrowning:** Provides a description of whether a person is smiling or frowning

### Segmentation mode

> [!NOTE]
>
> Setting segmentation will use the generative model, consuming tokens even if no fields are defined.


Content Understanding offers two ways to slice a video, letting you get the output you need for whole videos or short clips. You can use these options by setting the `enableSegment` property on a custom analyzer.

* **Whole-video** – `enableSegment : false`
  The service treats the entire video file as a single segment and extracts metadata across its full duration.

  **Use cases:**
    * Compliance checks that look for specific brand-safety issues anywhere in an ad
    * full-length descriptive summaries

* **Custom segmentation** – `enableSegment : true` 
  You describe the logic in natural language and the model creates segments to match. Set `contentCategories` with a string describing how you'd like the video to be segmented. Custom allows segments of varying length from seconds to minutes depending on the prompt. In this version, video only supports one `contentCategories` object. 

  **Example:**
    Break a news broadcast up into stories.

  ```json
  {
    "config": {
      "enableSegment": true,
      "contentCategories": {
        "news-story": { 
        "description": "Segment the video based on each distinct news segment. Use the timestamp of each image to identify the start and end time of each segment, no overlap segments. Ignore non-news segments like ads or promotion.",
        "analyzerId": "NewsAnalyzer"
        }         
      }
    }
  }
  ```

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

As with all Foundry Tools, review Microsoft's [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) documentation.

> [!IMPORTANT]
>
> If you process **Biometric Data** (for example, enable **Face Description**), you must meet all notice, consent, and deletion requirements under applicable laws. See [Data and Privacy for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security).

## Related content

* Try out analyzing videos in the [Content Understanding Studio](https://aka.ms/cu-studio).
* Check out the [Content Understanding Studio quickstart](../quickstart/content-understanding-studio.md).
* Learn more about analyzing video content using [analyzer templates](../concepts/analyzer-templates.md).
* Samples:

  * [Video content extraction notebook](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/content_extraction.ipynb)
  * [Video search with natural language queries](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/tree/main#samples)
  * [Analyzer templates](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates)
