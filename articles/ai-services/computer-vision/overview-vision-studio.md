---
title: What is Vision Studio?
titleSuffix: Foundry Tools
description: Learn how to set up and use Vision Studio to test features of Azure Vision in Foundry Tools on the web.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: overview
ms.date: 01/30/2026
ms.author: pafarley
---

# What is Vision Studio?

[Vision Studio](https://portal.vision.cognitive.azure.com) is a set of UI-based tools that lets you explore, build, and integrate features from Azure Vision in Foundry Tools.

Vision Studio lets you try several service features and sample their returned data in a quick, straightforward manner. Using Vision Studio, you can start experimenting with the services and learning what they offer without needing to write any code. Then, use the available client libraries and REST APIs to embed these services into your own applications.

## Get started using Vision Studio

To use Vision Studio, you need an Azure subscription and a resource for Foundry Tools for authentication. You can also use this resource to call the services in the try-it-out experiences. Follow these steps to get started.

1. Create an Azure subscription if you don't have one already. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

1. Go to the [Vision Studio website](https://portal.vision.cognitive.azure.com). If it's your first visit, a popup window prompts you to sign in to Azure and then choose or create a Vision resource. You can skip this step and do it later.

    :::image type="content" source="./Images/vision-studio-wizard-1.png" alt-text="Screenshot of Vision Studio startup wizard.":::

1. Select **Choose resource**, then select an existing resource within your subscription. If you want to create a new one, select **Create a new resource**. Then enter information for your new resource, such as a name, location, and resource group.

    :::image type="content" source="./Images/vision-studio-wizard-2.png" alt-text="Screenshot of Vision Studio resource selection panel.":::

    > [!TIP]
    > * For lower latency, select a location for your Azure resource that's closest to you.
    > * If you use the free pricing tier, you can keep using the Vision service even after your Azure free trial or service credit expires.

1. Select **Create resource**. After your resource is created, you can try the different features offered by Vision Studio.

    :::image type="content" source="./Images/vision-studio-home-page.png" alt-text="Screenshot of Vision Studio home page.":::

1. From here, you can select any of the different features offered by Vision Studio. Some of them are outlined in the service quickstarts:
   * [Optical character recognition (OCR) quickstart](quickstarts-sdk/client-library.md?pivots=vision-studio)
   * Image Analysis [4.0 quickstart](quickstarts-sdk/image-analysis-client-library-40.md?pivots=vision-studio) and [3.2 quickstart](quickstarts-sdk/image-analysis-client-library.md?pivots=vision-studio)
   * [Face quickstart](quickstarts-sdk/identity-client-library.md?pivots=vision-studio)

## Preconfigured features

Azure Vision offers multiple features that use prebuilt, preconfigured models for performing various tasks, such as: understanding how people move through a space, detecting faces in images, and extracting text from images. See the [Azure Vision overview](overview.md) for a list of features offered by the Vision service.

Each of these features has one or more try-it-out experiences in Vision Studio that allow you to upload images and receive JSON and text responses. These experiences help you quickly test the features using a no-code approach.

## Clean up resources

If you want to remove a Foundry resource after using Vision Studio, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it. You can't delete your resource directly from Vision Studio, so use one of the following methods:
* [Use the Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Use the Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)

> [!TIP]
> In Vision Studio, you can find your resource's details (such as its name and pricing tier) as well as switch resources by selecting the Settings icon in the top-right corner of the Vision Studio screen.

## Related content

* Go to [Vision Studio](https://portal.vision.cognitive.azure.com) to begin using features offered by the service.
* For more information on the features offered, see the [Azure Vision overview](overview.md).
