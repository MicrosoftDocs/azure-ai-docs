---
title: "Quickstart: Face recognition using Azure AI Foundry portal"
titleSuffix: "Azure AI services"
description: In this quickstart, get started with the Face service using the Azure AI Foundry portal.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: include
ms.date: 07/28/2025
ms.author: pafarley
---

Use Azure AI Foundry portal to detect faces in an image.

## Prerequisites

* An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=ai-services).
* An [Azure AI Foundry resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/%7E/AIServices)

## Setup 

Go to the [Azure AI Foundry portal](https://ai.azure.com/), and sign in with your Azure account that has the AI Foundry resource.

Select **Azure AI Foundry** in the top-left corner, scroll down and select **Explore Azure AI Services**, and then select **Vision + Document**. On the **Face** tab, select **Detect faces in an image**.

## Detect faces

Select an image from the available set, or upload your own. The service will detect faces in the image and return their bounding box coordinates, face landmark coordinates, and attributes. Select the **JSON** tab to see the full JSON response from the API.



## Next steps

In this quickstart, you did face detection by using the Azure AI Foundry portal. Next, learn about the different face detection models and how to specify the right model for your use case.

> [!div class="nextstepaction"]
> [Specify a face detection model version](../how-to/specify-detection-model.md)

* [What is the Face service?](../overview-identity.md)
