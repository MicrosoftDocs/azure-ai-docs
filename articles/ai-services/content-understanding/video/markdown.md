---
title: Content Understanding audiovisual modality markdown representation
titleSuffix: Foundry Tools
description: Learn how Content Understanding represents audiovisual output as Markdown for audio and video inputs.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: concept-article
ms.custom:
  - build-2025
---

# AudioVisual analysis: Markdown representation

Azure Content Understanding in Foundry Tools converts unstructured audio and video content into richly formatted [GitHub Flavored Markdown](https://github.github.com/gfm), while preserving temporal relationships and content structure for accurate downstream use. This document describes how each audiovisual content element is represented in markdown for both audio and video inputs.

## Overview

The Markdown representation from Content Understanding includes timing information and transcripts.

The markdown format differs based on input type:
- **Audio inputs**: Focus on transcript content, timing, and speaker information
- **Video inputs**: Include all audio elements plus key frames

For complete details about supported file types, file size limits, and other constraints, see [service quotas and limits](../service-limits.md).


## Document structure and metadata

### Header information

All audiovisual content begins with a header that identifies the content type, duration, and dimensions (for video).

**Audio header example:**
```markdown
# Audio: 00:00.000 => 04:23.773
```

**Video header example:**
```markdown
# Video: 00:00.000 => 00:42.520
Width: 640
Height: 360
```

The header provides essential metadata:
- Content type (`Audio` or `Video`)
- Total duration in `HH:MM:SS.mmm` format
- Video dimensions in pixels (video only)

## Transcript representation

### WebVTT format

Transcripts are represented using the standard WebVTT (Web Video Text Tracks) format, preserving speaker identification and precise timing information. This format is consistent across both audio and video inputs.

**Transcript example:**
```markdown
Transcript

WEBVTT

00:02.480 --> 00:04.720
<Speaker 1>Need help redeeming a code on your Xbox?

00:05.440 --> 00:06.840
<Speaker 1>Follow these quick steps.

00:08.960 --> 00:15.680
<Speaker 1>Press the Xbox button on your controller to open the guide while signed into the console with the account you want to apply the code to.
```

### Speaker identification

Speakers are identified using the `<v Speaker N>` or `<Speaker N>` format within the WebVTT transcript. Content Understanding automatically performs speaker diarization to distinguish between different speakers in the audio track.

## Visual elements (video only)

### Key frames

Key frames represent significant visual moments extracted from the video timeline. They are embedded as markdown image references with precise timestamps.

**Key frames example:**
```markdown
Key Frames
- 00:00.400 ![](keyFrame.400.jpg)
- 00:01.800 ![](keyFrame.1800.jpg)
- 00:02.840 ![](keyFrame.2840.jpg)
- 00:03.880 ![](keyFrame.3880.jpg)
- 00:04.920 ![](keyFrame.4920.jpg)
```

Key frame properties:
- Timestamp in `HH:MM:SS.mmm` format
- Image reference in standard markdown format
- Automatically extracted at significant visual transitions

## Complete markdown example
The following is a complete example of the Markdown generated for a video.

````markdown
# Video: 00:00.960 => 00:25.040

Key Frames
- 00:08.040 ![](keyFrame.8040.jpg)
- 00:16.360 ![](keyFrame.16360.jpg)
- 00:19.480 ![](keyFrame.19480.jpg)

Transcript
```
WEBVTT

00:08.960 --> 00:15.680
<Speaker 1>Press the Xbox button on your controller to open the guide while signed into the console with the account you want to apply the code to.

00:16.720 --> 00:18.560
<Speaker 1>From the guide, select Store.

00:19.520 --> 00:25.040
<Speaker 1>Once opened, press the View button on the controller to open the side menu and select Redeem.
```
````

## Next steps

* Try out analyzing videos in the [Content Understanding Studio](https://aka.ms/cu-studio).
* Check out the [Content Understanding Studio quickstart](../quickstart/content-understanding-studio.md).
* Learn more about analyzing video content using [analyzer templates](../concepts/analyzer-templates.md).
* Review code samples: [video analysis with segments](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Review the complete [audiovisual elements documentation](elements.md) for detailed information about all supported elements.
