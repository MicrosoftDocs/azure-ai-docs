---
title: "AudioVisual analysis: extracting structured content with Azure AI Content Understanding"
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding's audiovisual analysis and content extraction capabilities for both audio and video inputs
author: laujan
ms.author: paulhsu
manager: nitinme
ms.date: 06/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# AudioVisual analysis: extracting structured content

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## Overview

Azure AI Content Understanding's multimodal analysis capabilities help you transform unstructured audio and video data into structured, machine-readable information. By precisely identifying and extracting audiovisual elements while preserving their temporal relationships, you can build powerful media processing workflows for a wide range of applications.

The `contents` object with `kind: "audioVisual"` supports both audio-only and video inputs, with different capabilities available depending on the input type.

**Supported content types** include:
- **Audio files**: Common audio formats
- **Video files**: Common video formats

For complete details about supported file types, file size limits, and other constraints, see [service quotas and limits](../service-limits.md#analyzers).

## JSON response structure

The Content Understanding API returns analysis results in a structured JSON format. This document focused on the element in the contents array with kind set to audioVisual. Here's the overall container structure of the response:

```json
{
  "id": "73719670-2326-40c3-88ca-197c52deab2c",
  "status": "Succeeded",
  "result": {
    "analyzerId": "my-analyzer",
    "contents": [
      {
        "markdown": "# Video: 00:00.000 => 23:16.997\nWidth: 854\nHeight: 480\n..." 
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
        "cameraShotTimesMs": [/* ... */], 
        "segments": [/* ... */] 
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
| **Content extraction elements** | | | |
| [**Transcript phrases**](#transcript-phrases) | ✓ | ✓ | Yes |
| [**Timing information**](#timing-information) | ✓ | ✓ | No |
| [**Key frames**](#key-frames) | ✗ | ✓ | No |
| [**Camera shots**](#camera-shots) | ✗ | ✓ | Yes |
| [**Faces and persons**](#faces-and-persons) | ✗ | ✓ | Yes* |
| **Custom elements** | | | |
| [**Field extraction**](#field-extraction) | ✓ | ✓ | No |
| [**Segments**](#segments) | ✗ | ✓ | Yes |

Face also requires `enableFace: true` in analyzer configuration and limited access registration.

### Markdown content elements
For details on the markdown format for audiovisual content see [AudioVisual Markdown](markdown.md).

### Content extraction elements

#### Transcript phrases

A `transcriptPhrases` element contains the complete audio transcription, broken down into individual phrases with speaker identification, and precise timing information. This element is available for both audio and video inputs. Content Understanding supports multilingual transcription and speaker diarization. This output is included when the user sets  `"returnDetails": true` in the analyzer definition. Details of language support can be found here [Audio Language Handling](../audio/overview.md#language-handling).

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

A `cameraShotTimesMs` element identifies points in the video where camera shots change, indicating cuts, transitions, or significant changes in camera angle or perspective. This helps in understanding the video's editing structure. The values are timestamps in milliseconds from the beginning of the video. This output is included when the user sets  `"returnDetails": true` in the analyzer definition.

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

#### Faces and persons

When face detection is enabled through analyzer configuration, Content Understanding can identify and track faces throughout the video. It also can optionally identify specific individuals when a person directory is provided. The face add-on is limited access and involves face identification and grouping; customers need to register for access at [Face Recognition](https://aka.ms/facerecognition). Face features incur added costs.

##### Configuration

To enable face capabilities, you need to configure your analyzer with the appropriate settings:

**Enable face detection and tracking:**
```json
{
  "config": {
    "enableFace": true,
    "returnDetails": true
  }
}
```

**Enable face identification with person directory:**
```json
{
  "config": {
    "enableFace": true,
    "personDirectoryId": "your-person-directory-name",
    "returnDetails": true
  }
}
```

For face identification, you must first create a person directory and reference it in the analyzer. For details on how to create a person directory, see [How to build a person directory](../tutorial/build-person-directory.md).

##### Person properties

The `persons` array contains identified individuals detected throughout the video:

- **`personId`**: A unique identifier for the person. The identifier can be:
  - A default identifier like "Person-1," "Person-2," etc. when no person directory is used
  - A GUID that corresponds to a person ID in the person directory when identification is enabled
- **`confidence`**: A decimal value between 0 and 1 indicating the confidence level of person identification
- **`source`**: A string containing temporal and spatial information about where the person appears in the video. The output is formatted as `AV(startTimeMs,x,y,width,height)-AV(endTimeMs,x,y,width,height)` where:
  - `startTimeMs`, `endTimeMs`: Timestamp in milliseconds for the start and end of the appearance of the person 
  - `x,y`: Top-left corner coordinates of the bounding box
  - `width,height`: Dimensions of the bounding box
- **Multiple appearances**: Separated by semicolons (`;`) for different time periods
- **Continuous tracking**: Connected by hyphens (`-`) for start and end of the same appearance


**JSON example (default person identification):**
```json
{
  "persons": [
    {
      "personId": "Person-1",
      "confidence": 1,
      "source": "AV(0,176,12,392,589)-AV(2433,192,56,374,561);AV(2933,185,29,380,576)-AV(6400,199,29,384,588)"
    },
    {
      "personId": "Person-2", 
      "confidence": 1,
      "source": "AV(2467,201,143,348,562)-AV(2900,192,125,369,594);AV(6433,40,0,630,858)-AV(31467,426,152,294,531)"
    }
  ]
}
```

**JSON example (with person directory identification):**
```json
{
  "persons": [
    {
      "personId": "a7784fd0-a24e-47d7-b125-351fe1d61f21",
      "confidence": 1,
      "source": "AV(160,150,120,200,300)-AV(5000,155,125,195,295);AV(8000,160,130,190,290)-AV(12000,165,135,185,285)"
    },
    {
      "personId": "0a9bc856-487a-4ce8-82dd-34db13d5e1a4",
      "confidence": 1, 
      "source": "AV(3000,300,200,180,250)-AV(7500,305,205,175,245);AV(15000,310,210,170,240)-AV(20000,315,215,165,235)"
    }
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
      "valueString": "The conversation revolves around an introduction to Azure AI Foundry's latest features."
    },
    "Sentiment": {
      "type": "string",
      "valueString": "Positive"
    }
  }
}
```

#### Segments

A `segments` collection is a grouping of video content that represents a logical temporal unit within the video. Segments can be created automatically based on scene detection or defined using custom segmentation definition provided by the user. Each segment contains timing information, descriptions, and optionally custom field extractions.

When `"returnDetails": true` is set in the analyzer definition, the segments object is returned. When segmentation is enabled, fields are always returned in the `valueArray` format for segment-based field extraction.

##### Configuration

Content Understanding offers three ways to slice a video, letting you get the output you need for whole videos or short clips. You can use these options by setting the `segmentationMode` property on a custom analyzer:

**Whole-video segmentation:**
```json
{
  "config": {
    "segmentationMode": "noSegmentation"
  }
}
```
The service treats the entire video file as a single segment and extracts metadata across its full duration.

**Use cases:**
- Compliance checks that look for specific brand-safety issues anywhere in an ad
- Full-length descriptive summaries

**Automatic segmentation:**
```json
{
  "config": {
    "segmentationMode": "auto"
  }
}
```
The service analyzes the timeline and breaks it up for you. Groups successive shots into coherent scenes, capped at one minute each.

**Use cases:**
- Create storyboards from a show
- Inserting mid-roll ads at logical pauses

**Custom segmentation:**
```json
{
  "config": {
    "segmentationMode": "custom",
    "segmentationDefinition": "news broadcasts divided by individual stories"
  }
}
```
You describe the logic in natural language and the model creates segments to match. Set `segmentationDefinition` with a string describing how you'd like the video to be segmented. Custom allows segments of varying length from seconds to minutes depending on the prompt.

**Use cases:**
- Break a news broadcast up into stories
- Segment educational content by topics
- Divide sports broadcasts by plays or events

##### Segment properties

- `startTimeMs`: The start time of the segment in milliseconds
- `endTimeMs`: The end time of the segment in milliseconds  
- `segmentId`: A unique identifier for the segment
- `description`: A natural language description of what happens in the segment

##### JSON examples

**Basic segments output:**
```json
{
  "segments": [
    {
      "startTimeMs": 2001,
      "endTimeMs": 22356,
      "description": "The segment transitions to a sports montage with the 'CTN SPORTS' logo appearing prominently. Various sports clips are shown, including volleyball, softball, football, basketball, golf, hockey, swimming, and track events.",
      "segmentId": "2"
    },
    {
      "startTimeMs": 26960,
      "endTimeMs": 53353,
      "description": "The video opens with a wide view of the soccer field at the Cardinals Sports Complex. Players from both teams are positioned on the field, preparing for the start of the game.",
      "segmentId": "4"
    }
  ]
}
```

**Field extraction with segments:**
When segmentation is enabled, custom field extraction returns results in a structured array format for each segment:

```json
{
  "fields": {
    "Segments": {
      "type": "array",
      "valueArray": [
        {
          "type": "object",
          "valueObject": {
            "SegmentType": {
              "type": "string",
              "valueString": "SportsBroadcast"
            },
            "PlayEvent": {
               "type": "string", 
              "valueString": "FreeKick"
            },
            "GameClock": {
              "type": "string",
              "valueString": "25:46"
            },
            "SegmentId": {
              "type": "string",
              "valueString": "4"
            },
            "StartTimeMs": {
              "type": "integer",
              "valueInteger": 26960
            },
            "EndTimeMs": {
              "type": "integer",
              "valueInteger": 53353
            }
          }
        }
      ]
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

* Try processing your video content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze video content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: [**video analysis with segments**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Review code sample: [**video analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
