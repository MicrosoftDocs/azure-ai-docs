---
title: How to create a custom photo avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to create a custom photo avatar.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.custom: references_regions
ms.date: 11/24/2025
ms.author: pafarley
author: PatrickFarley
zone_pivot_groups: foundry-speech-studio
---

# How to create a custom photo avatar

Custom photo avatar enables users to create a talking head avatar with only a photo. With custom photo avatar, users can efficiently create a personalized and more engaging Voice Live agent. 

Custom photo avatar creation is a manual process. You can follow the below process, and after custom photo avatars are set up, you can access them in the Microsoft Foundry or through API.

>[!Important]
> Photo avatar (preview) and custom photo avatar (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms) and the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA)("DPA"), as well as the Microsoft Generative AI Services Previews terms in the [supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
> Access to custom photo avatar (preview), which is part of custom text to speech avatar, is limited based on eligibility and usage criteria. Learn more [here](https://aka.ms/limitedaccesscogservices).


## Step 1: Request access

Custom photo avatar is available only to Microsoft managed customers and partners. You can request access on the [intake form](https://aka.ms/customneural).
After the request is approved, please contact your Microsoft account manager to proceed.

## Step 2: Prepare training data
The custom photo avatar creation supports real human photos and virtual human images. Here are some tips for preparing the images.
- The photo avatar only includes the head, so it’s best to provide an image showing the character from the shoulders up.
- The face must look like a real or virtual human. Cartoon-like characteristics, such as eyes that are larger than normal human proportions, are not supported.
- Avoid showing elaborate accessories or jewelry.
- The head should be fully visible and facing forward.
- Make sure the face is fully visible, without shadows or any hidden parts.

## Step 3: Prepare consent for real human photo
If you are creating a custom photo avatar from a real person’s photo, you must obtain consent from that person. Provide a video of the person reading a consent statement acknowledging the use of their image. Microsoft verifies that the recorded statement matches the predefined script and compares the face in the video with the photo to confirm they belong to the same person.
For an example of the consent statement see the verbal-statement-all-locales.txt file in the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-all-locales.txt) GitHub repository.

## Step 4: Create and deploy custom photo avatar
This step is handled in a manual process. Microsoft will set up the custom photo avatar in the Azure resources you provide offline.

Prepare resources:
- Foundry resource: [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the supported regions.
- For more information about region availability, see [Text to speech avatar regions](../regions.md).

## Step 5: Use custom photo avatar

You can use the custom photo avatar in a voice agent or create video content in Microsoft Foundry or via API.

### Use in Microsoft Foundry

To use custom photo avatar in **Voice Live** to create personalized voice agent:
1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Make sure the New Foundry toggle is on. 
2. Select an existing project or create a new project in the resource where your custom photo avatars are deployed.
3. Find the Voice Live model playground
   1. Select **Discover** in the upper-right navigation.
   1. Select **Models**.
   1. Search "speech"
   1. Click **Azure-Speech-Voice-Live** in the search result
   1. Select **Open in Playground**

To use custom photo avatar in **Text to speech avatar** to create talking head video:
1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Make sure the New Foundry toggle is on. 
2. Select an existing project or create a new project in the resource where your custom photo avatars are deployed.
3. Find the Text to speech avatar model playground
   1. Select **Discover** in the upper-right navigation.
   1. Select **Models**.
   1. Search "speech"
   1. Click **Azure-Speech-Text-to-speech-Avatar** in the search result
   1. Select **Open in Playground**
   
### Use through API
  Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). Search "photo" to quickly go to photo avatar part in sample code.

* [Batch synthesis (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-avatar)
* [Real-time synthesis (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
* [Use avatar in Voice Live API](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node/web/voice-live-avatar)


