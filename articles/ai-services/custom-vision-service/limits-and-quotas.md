---
title: Limits and quotas - Custom Vision Service
titleSuffix: Foundry Tools
description: This article explains the different types of licensing keys and about the limits and quotas for the Custom Vision Service.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-custom-vision
ms.topic: limits-and-quotas
ms.date: 01/22/2025
ms.author: pafarley
---

# Limits and quotas

[!INCLUDE [custom-vision-retirement](includes/custom-vision-retirement.md)]

There are two tiers of subscription to the Custom Vision service. You can sign up for an F0 (free) or S0 (standard) subscription through the Azure portal. This page outlines the limitations of each tier. See the [Custom Vision pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/custom-vision-service/) for more details on pricing and transactions.

|Factor|**F0 (free)**|**S0 (standard)**|
|-----|-----|-----|
|Projects|2|100|
|Training images per project |5,000|100,000|
|Predictions / month|10,000 |Unlimited|
|Tags / project|50|500|
|Iterations |20|20|
|Min labeled images per Tag, Classification (50+ recommended) |5|5|
|Min labeled images per Tag, Object Detection (50+ recommended)|15|15|
|How long prediction images stored|30 days|30 days|
|[Prediction](/rest/api/customvision/predictions) operations with storage (Transactions Per Second)|2|10|
|[Prediction](/rest/api/customvision/predictions) operations without storage (Transactions Per Second)|2|20|
|[TrainProject](/rest/api/customvision/train-project/train-project) (API calls Per Second)|2|10|
|[Other API calls](/rest/api/custom-vision) (Transactions Per Second)|10|10|
|Accepted image types|jpg, png, bmp, gif|jpg, png, bmp, gif|
|Min image height/width in pixels|256 (see note)|256 (see note)|
|Max image height/width in pixels|10,240|10,240|
|Max image size (training image upload) |6 MB|6 MB|
|Max image size (prediction)|4 MB|4 MB|
|Max number of regions per image (training) (object detection)|300|300|
|Max number of regions per image (prediction) (object detection)|200|200|
|Max number of tags per image (classification)|100|100|

> [!NOTE]
> Images smaller than 256 pixels will be accepted but upscaled.

> [!NOTE]
> The image aspect ratio shouldn't be larger than 25:1.
