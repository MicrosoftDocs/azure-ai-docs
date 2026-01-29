---
title: "AudioVisual analysis: extracting structured content with Azure Content Understanding in Foundry Tools"
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools audiovisual analysis and content extraction capabilities for audio and video inputs.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# AudioVisual analysis: extracting structured content

Azure Content Understanding's multimodal analysis capabilities help you transform unstructured audio and video data into structured, machine-readable information. By precisely identifying and extracting audiovisual elements while preserving their temporal relationships, you can build powerful media processing workflows for a wide range of applications.

The `contents` object with `kind: "audioVisual"` supports both audio-only and video inputs, with different capabilities available depending on the input type.

**Supported content types** include:
- **Audio files**: Common audio formats
- **Video files**: Common video formats

For complete details about supported file types, file size limits, and other constraints, see [service quotas and limits](../service-limits.md).

## JSON response structure

The Content Understanding API returns analysis results in a structured JSON format. This document focuses on the element in the `contents` array with `kind` set to `audioVisual`. Here's the overall container structure of the response:

```json
{
  "id": "73719670-2326-40c3-88ca-197c52deab2c",
  "status": "Succeeded",
  "result": {
    "analyzerId": "my-analyzer",
    "contents": [
      {
        "markdown": "# Video: 00:00.000 => 23:16.997\nWidth: 854\nHeight: 480\n...",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "..."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 1000000,
        "transcriptPhrases": [/* ... */],
        "width": 854,
        "height": 480,
        "keyFrameTimesMs": [/* ... */],
        "cameraShotTimesMs": [/* ... */]
      }
    ]
  }
}
```

## AudioVisual elements

The following audiovisual elements can be extracted:

| Element | Audio Support | Video Support | Requires returnDetails |
|---------|---------------|---------------|------------------------|
| [**Markdown content**](#markdown-content-elements) | ✓ | ✓ | No |
| [**Contents collection**](#contents-collection)| ✓ | ✓ | No |
| [**Transcript phrases**](#transcript-phrases) | ✓ | ✓ | Yes |
| [**Timing information**](#timing-information) | ✓ | ✓ | No |
| [**Key frames**](#key-frames) | ✗ | ✓ | No |
| [**Camera shots**](#camera-shots) | ✗ | ✓ | Yes |
| [**Field extraction**](#field-extraction) | ✓ | ✓ | No |

Face also requires `enableFace: true` in analyzer configuration and limited access registration.

### Markdown content elements
For details on the markdown format for audiovisual content see [AudioVisual Markdown](markdown.md).

### Contents collection
The contents collection contains one or more content objects that contain the data extracted from the file. When segmentation is enabled (`enableSegment = true`) then a content object is returned for each segment found in the content. 

#### Transcript phrases

A `transcriptPhrases` element contains the complete audio transcription, broken down into individual phrases with speaker identification and precise timing information. This element is available for both audio and video inputs. Content Understanding supports multilingual transcription and speaker diarization. This output is included when the user sets `"returnDetails": true` in the analyzer definition. For details, see [Audio language handling](../audio/overview.md#language-handling).

**JSON example:**
```json
{
  "transcriptPhrases": [
    {
      "speaker": "Speaker 1",
      "startTimeMs": 280,
      "endTimeMs": 3560,
      "text": "Welcome to this first session",
      "words": []
    },
    {
      "speaker": "Speaker 2",
      "startTimeMs": 4640,
      "endTimeMs": 5440,
      "text": "Thanks for having me. Excited to be here.",
      "words": []
    }
  ]
}
```
#### Timing information

Timing information provides the overall temporal bounds of the audiovisual content:

- `startTimeMs`: The start time of the content in milliseconds (typically 0)
- `endTimeMs`: The end time of the content in milliseconds
- `width`: The video width in pixels (video only)
- `height`: The video height in pixels (video only)

**JSON example:**
```json
{
  "kind": "audioVisual",
  "startTimeMs": 0,
  "endTimeMs": 1396997,
  "width": 854,
  "height": 480
}
```

#### Key frames

A `keyFrameTimesMs` element represents the timestamps for the visual frames extracted from the video at key moments. Timestamps are represented in milliseconds from the beginning of the video. These frames are intelligently selected based on signals like shot detection. These frames are used as input to generate custom fields.

**Keyframe sampling behavior:**

- Keyframes are uniformly selected from each camera shot
- Each shot includes at least one sampled keyframe, even for short shots (less than one second)
- The number of keyframes is consistent across multiple runs
- Timestamp values can have minor numerical differences between runs, but these differences are minimal and shouldn't significantly affect the content of the selected frames

**JSON example:**
```json
{
  "keyFrameTimesMs": [
    660,
    1320,
    2970,
    3927,
    4884,
    5841,
    6798,
    7755,
    8712,
    9669
  ]
}
```

#### Camera shots

A `cameraShotTimesMs` element identifies points in the video where camera shots change, indicating cuts, transitions, or significant changes in camera angle or perspective. This helps you understand the video's editing structure. The values are timestamps in milliseconds from the beginning of the video. This output is included when the user sets `"returnDetails": true` in the analyzer definition.

**Camera shot detection behavior:**

- `cameraShotTimesMs` stores the timestamps of cuts between camera shots
- The array values indicate the starting time of all camera shots, excluding the first shot (which always starts at 0 ms)
- The output is deterministic and consistent across multiple runs
- This model may miss transitions that are visually gradual

**JSON example:**
```json
{
  "cameraShotTimesMs": [
    2002,
    22356,
    26960,
    53353,
    71071,
    76210,
    78111,
    113487,
    148882,
    152953
  ]
}
```

### Custom elements

#### Field extraction

Custom field extraction allows you to define and extract specific information from audiovisual content based on your business requirements. Fields are defined in the analyzer configuration. Fields can be populated for the entire content by default or for each segment, for video when segmentation is enabled.

**Field extraction JSON example:**
```json
{
  "fields": {
    "Summary": {
      "type": "string",
      "valueString": "The conversation revolves around an introduction to Microsoft Foundry's latest features."
    },
    "Sentiment": {
      "type": "string",
      "valueString": "Positive"
    }
  }
}
```

## Complete JSON example

The following example shows the complete JSON response structure from analyzing an Xbox instructional video. The JSON included here represents the full output from Content Understanding when processing a video with multiple element types:

```json
{
  "id": "cca7cf12-7b2c-46db-9d9a-d7c2dc78c120",
  "status": "Succeeded",
  "result": {
    "analyzerId": "auto-labeling-model-1750376726735-970",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-06-19T23:45:31Z",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Video: 00:00.000 => 00:42.520\nWidth: 640\nHeight: 360\n\nTranscript\n```\nWEBVTT\n\n00:02.480 --> 00:04.720\n<Speaker 1>Need help redeeming a code on your Xbox?\n\n00:05.440 --> 00:06.840\n<Speaker 1>Follow these quick steps.\n\n00:08.960 --> 00:15.680\n<Speaker 1>Press the Xbox button on your controller to open the guide while signed into the console with the account you want to apply the code to.\n```\n\nKey Frames\n- 00:00.400 ![](keyFrame.400.jpg)\n- 00:01.800 ![](keyFrame.1800.jpg)\n- 00:02.840 ![](keyFrame.2840.jpg)\n- 00:08.040 ![](keyFrame.8040.jpg)\n- 00:16.360 ![](keyFrame.16360.jpg)",
        "fields": {
          "ProductOrFeature": {
            "type": "string",
            "valueString": "Xbox code redemption"
          },
          "Problem": {
            "type": "string",
            "valueString": "How to redeem a code on Xbox"
          },
          "Steps": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "StepTitle": {
                    "type": "string",
                    "valueString": "Open the Guide"
                  },
                  "Instructions": {
                    "type": "string",
                    "valueString": "Press the Xbox button on your controller to open the guide while signed into the console with the account you want to apply the code to."
                  },
                  "Timestamp": {
                    "type": "string",
                    "valueString": "00:00:08.960"
                  }
                }
              },
              {
                "type": "object",
                "valueObject": {
                  "StepTitle": {
                    "type": "string",
                    "valueString": "Enter Code"
                  },
                  "Instructions": {
                    "type": "string",
                    "valueString": "Enter the 25-character code without the hyphens, then follow steps to finish redeeming."
                  },
                  "Timestamp": {
                    "type": "string",
                    "valueString": "00:00:26.960"
                  }
                }
              }
            ]
          },
          "FinalOutcome": {
            "type": "string",
            "valueString": "Successfully redeem a code on Xbox and access the associated content or service."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 42520,
        "width": 640,
        "height": 360,
        "keyFrameTimesMs": [
          400,
          1800,
          2840,
          3880,
          4920,
          5960,
          7000,
          8040,
          9080,
          10120,
          16360,
          17400,
          26760,
          27800,
          30920,
          31960,
          40280,
          41040,
          41800
        ],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 2480,
            "endTimeMs": 4720,
            "text": "Need help redeeming a code on your Xbox?",
            "words": []
          },
          {
            "speaker": "Speaker 1",
            "startTimeMs": 5440,
            "endTimeMs": 6840,
            "text": "Follow these quick steps.",
            "words": []
          },
          {
            "speaker": "Speaker 1",
            "startTimeMs": 8960,
            "endTimeMs": 15680,
            "text": "Press the Xbox button on your controller to open the guide while signed into the console with the account you want to apply the code to.",
            "words": []
          },
          {
            "speaker": "Speaker 1",
            "startTimeMs": 26960,
            "endTimeMs": 29840,
            "text": "Enter the 25-character code without the hyphens.",
            "words": []
          },
          {
            "speaker": "Speaker 1",
            "startTimeMs": 33600,
            "endTimeMs": 34640,
            "text": "Game on.",
            "words": []
          }
        ],
        "cameraShotTimesMs": [
          760,
          33240,
          39520
        ]
      }
    ]
  }
}
```

This complete example demonstrates how Content Understanding extracts and structures all the different element types from an audio or video, providing both the raw content and the detailed temporal and structural information that enables advanced video processing workflows.

## Next steps

* Try out analyzing videos in the [Content Understanding Studio](https://aka.ms/cu-studio).
* Check out the [Content Understanding Studio quickstart](../quickstart/content-understanding-studio.md).
* Learn more about analyzing video content using [analyzer templates](../concepts/analyzer-templates.md).
* Review code sample: [video analysis with segments](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Review code sample: [video analyzer templates](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
