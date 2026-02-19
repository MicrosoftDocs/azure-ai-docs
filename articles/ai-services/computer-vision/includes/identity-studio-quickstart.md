---
title: "Quickstart: Face recognition using Microsoft Foundry portal"
titleSuffix: "Foundry Tools"
description: In this quickstart, get started with the Face service using the Microsoft Foundry portal.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: include
ms.date: 07/28/2025
ms.author: pafarley
---

Use Microsoft Foundry portal to detect faces in an image.

## Prerequisites

* An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/%7E/AIServices)

## Setup 

Go to the [Microsoft Foundry portal](https://ai.azure.com/), and sign in with your Azure account that has the Foundry resource.

Select **Microsoft Foundry** in the top-left corner, scroll down and select **Explore Foundry Tools**, and then select **Vision + Document**. On the **Face** tab, select **Detect faces in an image**.

## Detect faces

Select an image from the available set, or upload your own. The service will detect faces in the image and return their bounding box coordinates, face landmark coordinates, and attributes. Select the **JSON** tab to see the full JSON response from the API.



## Next steps

In this quickstart, you did face detection by using the Microsoft Foundry portal. Next, learn about the different face detection models and how to specify the right model for your use case.

> [!div class="nextstepaction"]
> [Specify a face detection model version](../how-to/specify-detection-model.md)

* [What is the Face service?](../overview-identity.md)
