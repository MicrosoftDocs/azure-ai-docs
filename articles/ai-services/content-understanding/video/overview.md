---
title: Azure AI Content Understanding video overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding video solutions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 04/14/2025
ms.custom: ignite-2024-understanding-release
---

# Azure AI Content Understanding video solutions (preview)

> \[!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities before General Availability (GA).
> * For more information, *see* **[Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms)**.

Azure AI Content Understanding allows you to extract and customize video metadata. Content Understanding helps efficiently manage, categorize, retrieve, and build workflows for video assets. It enhances your media asset library, supports workflows such as highlight generation, categorizes content, and facilitates applications like retrieval‑augmented generation (RAG).

Content understanding for video has broad potential uses. For example, you can customize metadata to tag specific scenes in a training video, making it easier for employees to locate and revisit important sections. You can also use metadata customization to identify product placement in promotional videos, which helps marketing teams analyze brand exposure.

---

## Business use cases

Azure AI Content Understanding provides a range of business use cases, including:

* **Broadcast media and entertainment**: Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.
* **Education and e‑Learning**: Index and retrieve specific moments in educational videos or lectures.
* **Corporate training**: Organize training videos by key topics, scenes, or important moments.
* **Marketing and advertising**: Analyze promotional videos to extract product placements, brand appearances, and key messages.

---

## Video understanding capabilities

\:::image type="content" source="../media/video/video-overview\.png" alt-text="Screenshot of video analyzer flow.":::

Content Understanding processes video files through a customizable pipeline that can perform both **content extraction** and **field extraction** tasks.

* **Content Extraction** focuses on analyzing the raw video to generate foundational metadata (for example, transcription, shot detection, and face grouping).
* **Field Extraction** uses that metadata to create domain‑specific insights and, starting with this release, also drives **segmentation** when requested.

Below is an overview of each capability.

### Content extraction

Content Extraction operations are performed over sampled frames from the entire video (see *Technical constraints*). They provide grounding data for Field Extraction and can also be consumed directly.

| Capability                            | Description                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Transcription**                     | Converts speech to structured, searchable text via Azure AI Speech.                                                                                                                                                                                                                                                                                                                            |
| **Shot detection**                    | Identifies shot boundaries for precise editing and repackaging.                                                                                                                                                                                                                                                                                                                                |
| **Key frame extraction**              | Captures key frames per shot. This is used to give generative models visual context for field extraction.                                                                                                                                                                                                                                                                                      |
| **Face identification & description** | Detects and groups faces across the video, can identify each group against a Face API *faceTemplateId*. Additionally when face description is enabled the model to describe visible facial features (for example, "person with beard and glasses") and use unblurred frames to track people through the videos. **Note:** Turning on face grouping/identification incurs an additional charge. |

#### How face grouping, identification, and description work

> Face‑related options give you progressively richer information about **who appears** in a video and **how they look**. You can enable them individually or in combination.

| Capability                           | What it does                                                                                                                                                                                            | Typical questions it answers                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Face grouping** *(base)*           | Clusters visually similar faces across the entire video. Returns a **cast list** (one row per person) and timestamps of every appearance.                                                               | *Who are the distinct characters in this video? When does each one show up?* |
| **Face identification** *(optional)* | Compares each face group against your **Face API template list** (`faceTemplateId`). If a match is found, the cluster is labeled with the person’s name.                                                | *Which executive appears in this scene? How many minutes does Satya speak?*  |
| **Face description** *(independent)* | When `unblurFaces: true` is set (passive, limited‑access resources only), the model sees unblurred thumbnails and can describe facial attributes (beard, glasses, emotion) and track them through time. | *Show me every segment with a smiling customer wearing glasses.*             |

**Conceptual flow**

1. **Group** – `faceGrouping` clusters faces → *Person 1, Person 2, …* with presence intervals.
2. **Identify** (*optional*) – `faceTemplateId` maps each cluster to a known identity → *Person 2 = "Ada Lovelace"*.
3. **Describe** (*independent*) – `unblurFaces` lets the generative model attach rich natural‑language descriptions to each appearance → *“Ada Lovelace, a woman with round glasses and a blue blazer.”*

##### Minimal JSON switches

```jsonc
{
  "faceGrouping": true,              // Step 1 – required for grouping/identification
  "faceTemplateId": "execs-list-01", // Step 2 – optional identification
  "unblurFaces": true                // Step 3 – optional description (passive resources only)
}
```

> **Cost note:** Enabling *faceGrouping* (and thus identification) incurs an additional charge.

### Field extraction (includes segmentation)

Field Extraction invokes a multimodal generative model that analyzes key frames, shot boundaries, and any segmentation you request. You can define a custom schema of fields to extract (for example, *shot type*, *brand logo*, *speaker name*).

#### Segmentation modes

Segmentation is now configured **inside Field Extraction** using the **`segmentation`** property.

| Mode                            | Value      | Use case                                                       | Notes                                                                                                                          |
| ------------------------------- | ---------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **No segmentation** *(default)* | `"none"`   | Whole‑video summarization, ad compliance checklists.           | All fields are extracted over the entire video.                                                                                |
| **Shot‑based**                  | `"shot"`   | Technical edits, granular highlight creation.                  | Boundaries align to detected shots.                                                                                            |
| **Auto scene‑based**            | `"auto"`   | Human‑cohesive scene summaries.                                | Attempts to merge consecutive shots, **capped at 1‑minute segments**. Longer scenes are split, boundaries still respect shots. |
| **Custom**                      | `"custom"` | Semantic or domain‑specific cuts (sports plays, news stories). | Requires **`segmentationDescription`** prompt describing the segmentation logic.                                               |

##### Quick JSON examples

```jsonc
// 1) Process whole video (default)
{
  "segmentation": "none"
}

// 2) Auto scene segmentation
{
  "segmentation": "auto"
}

// 3) Custom segmentation by soccer plays
{
  "segmentation": "custom",
  "segmentationDescription": "Segment the match into kick‑offs, goals, fouls, and halftime."
}
```

> \[!NOTE]
> Specifying **`segmentation`** automatically triggers Field Extraction, even if your field list is empty.

#### Example extracted fields by industry

* **Media asset management**

  * `shotType` – Technical framing (close‑up, wide, drone).
  * `colorScheme` – Dominant palette per scene.
* **Advertising**

  * `brand` – Detected product or logo appearance.
  * `adCategory` – Classified industry vertical.

### Key benefits

* **Segment‑aware multi‑frame analysis**.
* **Prompt‑based customization** of both segmentation and field schema.
* **Generative models** convert natural‑language requests into structured metadata.
* **Optimized preprocessing** provides rich context for downstream AI.

---

## Technical constraints and limitations

| Area                    | Current preview limit        | Impact                                                                      |
| ----------------------- | ---------------------------- | --------------------------------------------------------------------------- |
| **Frame sampling rate** | \~1 frame per second (1 FPS) | Fast motion may be missed; not suitable for frame‑accurate action analysis. |
| **Image resolution**    | 512 × 512 px per frame       | Fine‑detail recognition (small text, distant objects) may be limited.       |
| **Audio understanding** | Speech only                  | Music, sound effects, and other non‑speech audio are ignored.               |

---

## Input requirements

For supported formats, see [Service quotas and limits](../service-limits.md).

---

## Supported languages and regions

See [Language and region support](../language-region-support.md).

---

## Data privacy and security

As with all Azure AI services, review Microsoft’s [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) documentation.

> \[!IMPORTANT]
> If you process **Biometric Data** (for example, enable **Face Grouping** or **Face Identification**), you must meet all notice, consent, and deletion requirements under GDPR or other applicable laws. See [Data and Privacy for Face](/legal/cognitive-services/face/data-privacy-security).

---

## Next steps

* Process videos in the [Azure AI Foundry portal](https://aka.ms/cu-landing).
* Quickstart: [Analyze video content with analyzer templates](../quickstart/use-ai-foundry.md).
* Samples:

  * [Video content extraction notebook](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/content_extraction.ipynb)
  * [Video search with natural language queries](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/tree/main#samples)
  * [Analyzer templates](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates)
