---
title: Data, privacy, and security for Spatial Analysis
titleSuffix: Azure AI services
description: This document details issues for compliance, privacy, and security for an Azure AI Vision spatial analysis container deployment.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: article
ms.date: 09/14/2020
---

# Data, privacy, and security for Spatial Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Azure AI Vision spatial analysis was designed with compliance, privacy, and security in mind, however, the customer is responsible for its use and the implementation of this technology. For example, it is your responsibility to:

- Install and position cameras in your locations, and in doing so take care to avoid sensitive areas and limit collection of data not needed by Spatial Analysis.

- Inform people in your locations with conspicuous disclosure about use of video data and use of AI.

- Comply with all applicable laws and regulations in your jurisdiction.

Each of Microsoft's customers has a different environment and space occupants, and some jurisdictions may have special laws enacted, such as CCTV-related rules and/or licensing requirements or prohibiting use of cameras in sensitive areas. Before using spatial analysis, you must have all the proper rights to use your cameras and video images, including, where required, the necessary consent from individuals for the use of processing images to generate insights in compliance with the laws and regulations of your jurisdiction.

## Data and privacy for spatial analysis

Spatial analysis runs in a container customers deploy on an edge compute device. The container runs a pipeline that ingests video frames, detects people in the video, tracks the people as they move around over time, and generates AI insights as people interact with regions of interest. The customer directs where the AI insights are stored. For example, AI insights can flow to the cloud via Azure IoT Hub or Event Grid.

:::image type="content" source="media/spatial-analysis/spatial-analysis-container-architecture.png" alt-text="A deployment architecture for the spatial analysis container.":::

## What data does the spatial analysis container process?

Spatial analysis containers process the following types of data:

- **Video frames** - Video streams from cameras deployed in the environment. The video data is processed in memory, in real time, on the edge device to generate the AI insights. Spatial analysis does not store this data on the edge device or send it to the cloud unless the customer specifically enables the VideoRecorder operator. When the VideoRecorder operator is enabled it can save video frames locally to the edge device or upload them to Azure Storage.

- **AI insights** - This is the event data output by the operators that describes an inferred event. Event data includes data such as time stamp, location of detected people, and event type. For example, the *PersonCrossingLine* operator can be configured to output an AI insight every time someone is detected crossing a designated line. Details on all supported AI insights can be found in [AI Operations Output](/azure/ai-services/computer-vision/spatial-analysis-operations).

- **Configuration data** - Configuration data is pushed from Azure IoT Hub to the spatial analysis container when the customer sets up the container.

## How does the spatial analysis container process data?

Spatial analysis processes data as instructed by the customer to provide the service.

When the developer configures the spatial analysis container, they provide information necessary to stream video from their cameras and configured zones for each camera. After the spatial analysis container is configured, it will continuously stream and process video frames.

Spatial analysis detects and tracks people's movements in the video feed based on algorithms that identify the presence of one or more humans. The algorithms generate events based on the specific operator that's enabled. For example, *PersonCrossingZone* generates an event when a person moves in or out of designated zones in the camera's field of view and outputs the coordinates of the person's body into a bounding box. For each bounding box movement detected in a camera zone, the AI skill output inference data includes the following:

- Bounding box coordinates of person's body

- Event type (for example, zone entry or exit, directional line crossing)

- Bounding box coordinate of the location of person’s face and face mask detection result  

- Pseudonymous identifier to track the bounding box

- Confidence score for the detection

The AI inferencing requires only images to be streamed from customer's cameras. No video data leaves the premises and no video data is stored on the edge unless specifically configured using the VideoRecorder operator. The AI data inferencing is performed locally in memory on the edge device without storing video footage. The data inferencing occurs near real-time.

The AI insight data is then sent to a message hub, like Azure IoT Hub for further processing. The developer can connect it with their custom application using Azure Web Apps, Power Platform, or whatever services they want.

## Security for customers' data

Security of customer data is a shared responsibility.

Details on the security model of Azure AI containers, like the spatial analysis container can be found here - [Azure AI container security](/azure/ai-services/cognitive-services-container-support?tabs=luis#azure-cognitive-services-container-security). Additionally, the spatial analysis container deploys using Azure IoT
Edge. Details on securing Azure IoT Edge can be found here - [Security standards for Azure IoT Edge](/azure/iot-edge/security).

Azure services like Azure IoT Hub and Azure Event Grid have implemented and will maintain appropriate technical and organizational measures to protect customer data in the cloud.

You are responsible for securing and maintaining the equipment and infrastructure required to operate spatial analysis containers located on your premises, such as your edge device, network and video feeds from your cameras.

To learn more about Microsoft's privacy and security commitments visit the Microsoft [Trust Center](https://www.microsoft.com/TrustCenter/CloudServices/Azure/default.aspx).

## Next steps

> [!div class="nextstepaction"]
> [Responsible use deployment guidance for spatial analysis](/azure/ai-foundry/responsible-ai/computer-vision/responsible-use-deployment?context=%2fazure%2fcognitive-services%2fComputer-vision%2fcontext%2fcontext)
