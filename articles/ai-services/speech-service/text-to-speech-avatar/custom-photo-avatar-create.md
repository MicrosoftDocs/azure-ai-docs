---
title: How to create a custom photo avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to create a custom photo avatar.
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.custom: references_regions
ms.date: 09/18/2026
ms.author: pafarley
author: PatrickFarley
ai-usage: ai-assisted
---

# How to create a custom photo avatar

Custom photo avatar enables users to create a talking head avatar with only a photo. With custom photo avatar, users can efficiently create a personalized and more engaging voice agent through Voice Live API or a talking heads video.

Users can now create custom photo avatars directly in Microsoft Foundry. Self-creation supports two types of custom photo avatars:
 - **Avatars created from a real person’s photo**  -  Users can upload a photo of a real person along with a consent video from the same individual authorizing avatar creation.

 - **Avatars created from an AI-generated character** - Users can describe the character they want, and the embedded GenAI image model will generate it before creating the avatar.


> [!Note]
> Custom photo avatar access is limited based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).


## Prerequisites

- A Foundry project. To create a project, see [Create a Foundry project](../../../foundry/how-to/create-projects.md?tabs=foundry#create-a-foundry-project).
- Image to create the custom photo avatar, if you want to create an avatar from an existing image.
- If you use a real person's photo, a video recording of the same person reading a consent statement acknowledging the use of their image. Microsoft uses the video to verify consent and confirm identity. For more information, see [Prepare consent for real human photo](#step-3-prepare-consent-for-real-human-photo). This recording isn't required for the **Create with AI** path.

## Step 1: Start an avatar customization
1. [!INCLUDE [foundry-sign-in](../../../foundry/includes/foundry-sign-in.md)]
2. Open the Foundry project associated with the resource you want to use for your avatar, and select **Build** from the top-right menu.
3. Select **Services** from the left pane.
4. Select **Customizations**.
5. Select **Create**.
6. In **Basic details** on the **Customize a model** page, select **Azure Speech - Text to Speech Avatar** as the model.
7. Select **Photo avatar** in **Type**.
8. Enter an **Avatar name** and an optional **Description**, and select **Next**.


## Step 2: Add image data
On the **Data** step, choose **Select data source**:

- **Create with image**: Use **Select data** to choose a previously uploaded photo, or select **Upload data** to upload a `.jpg`, `.jpeg`, or `.png` file. Select **Next** to continue to **Register avatar talent**.
- **Create with AI**: Set **Age**, **Gender**, **Ethnicity**, and **Style** as needed, and describe the character you want. Select **Next** to continue to **Review**, skipping the consent step. A preview isn't available before submission; view the generated avatar image on the details page after creation succeeds.

To get the best results when creating an avatar, please follow these image preparation guidelines.
- The photo avatar only includes the head, so it’s best to provide an image showing the character from the shoulders up.
- The face must look like a real or virtual human. Cartoon-like characteristics, such as eyes that are larger than normal human proportions, are not supported.
- Avoid showing elaborate accessories or jewelry.
- The head should be fully visible and facing forward.
- Make sure the face is fully visible, without shadows or any hidden parts.

## Step 3: Prepare consent for real human photo
If you create a custom photo avatar from a real person's photo, you must get consent from that person. Provide a video of the person reading the consent statement that acknowledges the use of their image. Microsoft verifies that the recorded statement matches the predefined script and compares the face in the video with the photo to confirm they belong to the same person. The video must be an `.mp4` or `.mov` file smaller than 500 MB, longer than 3 seconds, and shorter than 1 minute.
For an example of the consent statement see the verbal-statement-all-locales.txt file in the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-all-locales.txt) GitHub repository.

On **Register avatar talent**, use **Select avatar talent** to reuse an existing talent. To add a new one:

1. Select **Add avatar talent**.
1. Select the **Speaking language** of the consent recording.
1. Enter the **Avatar talent name** and **Company name** exactly as spoken in the recording, in the same language.
1. Select **Local files** to choose the consent video, or **Azure Blob** to provide its storage URL.
1. Select **Upload**.

After consent validation succeeds, confirm that the intended talent is selected, and select **Next** to continue to **Review**.

## Step 4: Create custom photo avatar
1. Review the avatar details, confirm the acknowledgment, and then select **Submit**
2. After you submit, return to **Build** > **Services** > **Customizations** to check the job status.
3. When the job status shows **Succeeded**, open the customization to view the avatar preview. A separate deployment isn't required; **Deployment** shows **Not required, ready to use**.

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
2. Open a project in the resource containing your custom photo avatar.
3. Open the Voice Live playground:
   1. Select **Build** > **Services** > **Playgrounds**.
   1. Select **Azure Speech - Voice Live**.
   1. Turn on **Avatar**, select **More avatars**, and select your avatar under **Custom**.

To use custom photo avatar in **Text to speech avatar** to create talking head video:
1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Make sure the new Foundry toggle is on. 
2. Open a project in the resource containing your custom photo avatar.
3. Open the Text to Speech Avatar playground:
   1. Select **Build** > **Services** > **Playgrounds**.
   1. Select **Azure Speech - Text to Speech Avatar**.
   1. In **Avatar**, select **More avatars**, and select your avatar under **Custom**.
   
### Use through API
  Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). Search "photo" to quickly go to photo avatar part in sample code.

  Related samples:
* [Batch synthesis (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-avatar)
* [Real-time synthesis (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
* [Use avatar in Voice Live API](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node/web/voice-live-avatar)


