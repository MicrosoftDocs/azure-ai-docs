---
title: What is Video Analysis?
titleSuffix: Azure AI services
description: Learn about the basic concepts and features of Azure AI Vision Spatial Analysis and Video Retrieval.
author: PatrickFarley
manager: nitinme
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: overview
ms.date: 04/04/2025
ms.custom: contperf-fy22q2, ignite-2022
---

# What is Video Analysis?

Video Analysis includes video-related features like Spatial Analysis and Video Retrieval.

## Spatial Analysis

[!INCLUDE [spatial-analysis-deprecation](includes/spatial-analysis-deprecation.md)]

<!--
You can use Azure AI Vision Spatial Analysis to detect the presence and movements of people in video. Ingest video streams from cameras, extract insights, and generate events to be used by other systems. The service can do things like count the number of people entering a space or measure compliance with face mask and social distancing guidelines. By processing video streams from physical spaces, you can learn how people use them and maximize the space's value to your organization.

Try out the capabilities of Spatial Analysis quickly and easily in your browser by using Azure AI Vision Studio.

> [!div class="nextstepaction"]
> [Try Vision Studio](https://portal.vision.cognitive.azure.com/)


### People counting

This operation counts the number of people in a specific zone over time using the *PersonCount* operation. It generates an independent count for each frame processed without attempting to track people across frames. This operation can be used to estimate the number of people in a space or generate an alert when a person appears.

:::image type="content" source="https://user-images.githubusercontent.com/11428131/139924111-58637f2e-f2f6-42d8-8812-ab42fece92b4.gif" alt-text="Animation showing how Spatial Analysis counts the number of people in the cameras field of view.":::

### Entrance Counting

This feature monitors how long people stay in an area or when they enter through a doorway. This monitoring can be done using the PersonCrossingPolygon or PersonCrossingLine operations. In retail scenarios, these operations can be used to measure wait times for a checkout line or engagement at a display. Also, these operations could measure foot traffic in a lobby or a specific floor in other commercial building scenarios.

:::image type="content" source="https://user-images.githubusercontent.com/11428131/137016574-0d180d9b-fb9a-42a9-94b7-fbc0dbc18560.gif" alt-text="Animation showing frames of people moving in and out of a bordered space, with rectangles drawn around them.":::

### Social distancing and face mask detection

This feature analyzes how well people follow social distancing requirements in a space. The system uses the *PersonDistance* operation to automatically calibrate itself as people walk around in the space. Then it identifies when people violate a specific distance threshold (6 ft. or 10 ft.).

:::image type="content" source="https://user-images.githubusercontent.com/11428131/139924062-b5e10c0f-3cf8-4ff1-bb58-478571c022d7.gif" alt-text="Animation showing how Spatial Analysis visualizes social distance violation events showing lines between people showing the distance.":::

Spatial Analysis can also be configured to detect if a person is wearing a protective face covering such as a mask. A mask classifier can be enabled for the PersonCount, PersonCrossingLine, and PersonCrossingPolygon operations by configuring the `ENABLE_FACE_MASK_CLASSIFIER` parameter.

:::image type="content" source="https://user-images.githubusercontent.com/11428131/137015842-ce524f52-3ac4-4e42-9067-25d19b395803.png" alt-text="Photograph showing how Spatial Analysis classifies whether people have facemasks in an elevator.":::
-->

## Video Retrieval

[!INCLUDE [video-retrieval-deprecation](includes/video-retrieval-deprecation.md)]

Video Retrieval is a service that lets you create a search index, add documents (videos and images) to it, and search with natural language. Developers can define metadata schemas for each index and ingest metadata to the service to help with retrieval. Developers can also specify what features to extract from the index (vision, speech) and filter their search based on features.

> [!div class="nextstepaction"]
> [Call the Video Retrieval APIs](./how-to/video-retrieval.md)

## Input requirements

<!--
Spatial Analysis works on videos that meet the following requirements:
* The video must be in RTSP, rawvideo, MP4, FLV, or MKV format.
* The video codec must be H.264, HEVC(H.265), rawvideo, VP9, or MPEG-4.

#### [Video Retrieval](#tab/vr)
-->
[!INCLUDE [video-retrieval-input](./includes/video-retrieval-input.md)]



<!--
## Responsible use of Spatial Analysis technology

To learn how to use Spatial Analysis technology responsibly, see the [Transparency note](/azure/ai-foundry/responsible-ai/computer-vision/transparency-note-spatial-analysis). Microsoft's transparency notes help you understand how our AI technology works and the choices system owners can make that influence system performance and behavior. They focus on the importance of thinking about the whole system including the technology, people, and environment.
-->

<!--
## Next step

> [!div class="nextstepaction"]
> [Install and run the Spatial Analysis container](spatial-analysis-container.md)
-->