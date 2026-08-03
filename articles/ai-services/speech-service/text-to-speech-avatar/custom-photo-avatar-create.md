---
title: How to create a custom photo avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to create a custom photo avatar.
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.custom: references_regions
ms.date: 11/24/2025
ms.author: pafarley
author: PatrickFarley
---

# How to create a custom photo avatar

Custom photo avatar enables users to create a talking head avatar with only a photo. With custom photo avatar, users can efficiently create a personalized and more engaging voice agent through Voice Live API or a talking heads video.

Users can now create custom photo avatars directly in Microsoft Foundry. Self-creation supports two types of custom photo avatars:
 - **Avatars created from a real person’s photo**  -  Users can upload a photo of a real person along with a consent video from the same individual authorizing avatar creation.

 - **Avatars created from an AI-generated character** - Users can describe the character they want, and the embedded GenAI image model will generate it before creating the avatar.


> [!Note]
> Custom photo avatar access is limited based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).


## Prerequisites

- A Foundry project. If you need to create a project, see [Create a Microsoft Foundry project](../../../ai-foundry/how-to/create-projects.md).
- Image to create the custom photo avatar, if you want to create an avatar from an existing image.
- You need a video recording of the talent reading a consent statement acknowledging the use of their image. You upload this video when you set up the avatar talent. For more information, see [Prepare consent for real human photo](#step-3-prepare-consent-for-real-human-photo).

## Step 1: Start fine-tuning
1. [!INCLUDE [foundry-sign-in](../../../foundry/includes/foundry-sign-in.md)]
2. Select **Build** from the top right menu.
3. Select **Fine-tune** from the left pane.
4. Select **AI Services**
5. Click **Fine-tune** button on the top right corner.
6. In the **Fine-tune a model** page, select model as **Azure Speech - Text to Speech Avatar**
7. Select **Photo avatar** in Type
8. Name your avatar and add optional description and click **Next**


## Step 2: Add image data
In this step, you can upload a photo of a real person or reuse a photo previously stored in Foundry by selecting **Existing data**,  or create a GenAI character by selecting **Create with AI** in the Select data source.

To get the best results when creating an avatar, please follow these image preparation guidelines.
- The photo avatar only includes the head, so it’s best to provide an image showing the character from the shoulders up.
- The face must look like a real or virtual human. Cartoon-like characteristics, such as eyes that are larger than normal human proportions, are not supported.
- Avoid showing elaborate accessories or jewelry.
- The head should be fully visible and facing forward.
- Make sure the face is fully visible, without shadows or any hidden parts.

## Step 3: Prepare consent for real human photo
If you are creating a custom photo avatar from a real person’s photo, you must obtain consent from that person. Provide a video of the person reading a consent statement acknowledging the use of their image. Microsoft verifies that the recorded statement matches the predefined script and compares the face in the video with the photo to confirm they belong to the same person.
For an example of the consent statement see the verbal-statement-all-locales.txt file in the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-all-locales.txt) GitHub repository.

## Step 4: Create custom photo avatar
1. Review the avatar details, confirm the acknowledgment, and then select **Submit**
2. After you submit, the custom photo avatar is created and you’re returned to the fine-tuning job list. The new fine-tuning job appears in the list immediately.
3. When the job status shows Succeeded, open the fine-tuning job to view the avatar preview.

## Step 5: Use custom photo avatar
You can use your custom photo avatar in the following ways:
 - Start a live chat (Voice Live) in Foundry
    - From the **Use your avatar** box, select **Try Voice Live**, or
    - Select **Open in Playground** (top-right), then choose **Voice Live**.
 - Create video content (Text to Speech Avatar) in Foundry
    - From the **Use your avatar box**, select **Try Text to Speech Avatar**, or
    - Select **Open in Playground** (top-right), then choose **Text to Speech Avatar**.
 - Use the avatar through the API
    - Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). Search "photo" to quickly go to photo avatar part in sample code.


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
1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Make sure the new Foundry toggle is on. 
2. Select an existing project or create a new project in the resource where your custom photo avatars are deployed.
3. Find the Text to speech avatar model playground
   1. Select **Discover** in the upper-right navigation.
   1. Select **Models**.
   1. Search "speech"
   1. Click **Azure-Speech-Text-to-speech-Avatar** in the search result
   1. Select **Open in Playground**
   
### Use through API
  Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). Search "photo" to quickly go to photo avatar part in sample code.

  Related samples:
* [Batch synthesis (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-avatar)
* [Real-time synthesis (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
* [Use avatar in Voice Live API](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node/web/voice-live-avatar)


