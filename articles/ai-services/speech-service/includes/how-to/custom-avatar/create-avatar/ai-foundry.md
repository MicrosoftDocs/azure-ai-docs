---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 09/18/2026
ai-usage: ai-assisted
---

Getting started with a custom text to speech avatar is a straightforward process. All it takes are a few video clips of your actor. If you'd like to train a [custom voice](../../../../custom-neural-voice.md) for the same actor, you can do so separately.

> [!Note]
> Custom avatar access is limited based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).


## Prerequisites

You need a Microsoft Foundry resource in one of the [regions that supports custom avatar training](../../../../text-to-speech-avatar/what-is-custom-text-to-speech-avatar.md#available-locations). Custom avatar only supports standard (S0) Foundry or Speech resources.

You need a video recording of the talent reading the consent statement for the avatar type you want to create, with or without voice sync for avatar. You upload this video when you set up the avatar talent. For more information, see [Add avatar talent consent](#step-2-add-avatar-talent-consent).

You need video recordings of your avatar talent as training data. You upload these videos when you prepare training data. For more information, see [Add training data](#step-3-add-training-data).

> [!NOTE]
> If you upload data from Azure Blob storage, the storage account must allow public network access. The URL must be retrievable using a simple anonymous GET request. For example, use a [SAS URL](/azure/storage/common/storage-sas-overview) or a publicly accessible URL. URLs that require extra authorization or expect user interaction aren't supported.

## Step 1: Start an avatar customization

> [!TIP]
> Create a separate customization for each avatar. Select consent and training data from the same avatar talent for each customization.

To fine-tune a custom avatar, follow these steps:

1. [!INCLUDE [foundry-sign-in](../../../../../../foundry/includes/foundry-sign-in.md)]
1. Open your Foundry project. If you need to create one, see [Create a Foundry project](../../../../../../foundry/how-to/create-projects.md?tabs=foundry#create-a-foundry-project).
1. Select **Build** from the top-right menu.
1. Select **Services** from the left pane.
1. Select **Customizations**, and then select **Create**.
1. In **Basic details** on the **Customize a model** page, select **Azure Speech - Text to Speech Avatar** as the model.
1. Select **Video avatar** as the type.
1. Enter an **Avatar name** and an optional **Description**. The avatar name is used in synthesis requests through the SDK or speech synthesis markup language (SSML). Only letters, numbers, hyphens, and underscores are allowed. The name must be unique within the same Speech or Foundry resource.
1. Select **Next** to continue to **Register avatar talent**.

Steps 2-4 continue in the same wizard. To resume a draft or check a submitted job, return to the **Customizations** tab and select the avatar by name.

## Step 2: Add avatar talent consent

An avatar talent is an individual or target actor whose video of speaking is recorded and used to create neural avatar models. You must obtain sufficient consent under all relevant laws and regulations from the avatar talent to use their video to create the custom text to speech avatar.

You must provide a video file with a recorded statement from your avatar talent that matches the selected consent type. Microsoft verifies that the content in the recording matches the predefined script provided by Microsoft. Microsoft compares the face of the avatar talent in the recorded video statement file with randomized videos from the training datasets to ensure that the avatar talent in video recordings and the avatar talent in the statement video file are from the same person.

> [!IMPORTANT]
> The consent type selected in **Register avatar talent** determines whether the trained model includes voice sync for avatar. When you reuse an existing consent recording, its registered type also determines this behavior.

- **Avatar with a voice sync for avatar**: A custom voice resembling your avatar talent's voice is created alongside the custom avatar. The voice is used exclusively with the specified avatar. Your consent statement must include both the custom avatar and the voice sync for avatar. For an example of the consent statement for custom avatar with voice sync, see the *verbal-statement-voice-sync-for-avatar-all-locales.txt* file in the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-voice-sync-for-avatar-all-locales.txt) GitHub repository.
- **Avatar only**: The model is trained without voice sync for avatar, and your consent statement must reflect this scope. For an example of the consent statement for custom avatar only, see the *verbal-statement-all-locales.txt* file in the [Azure-Samples/cognitive-services-speech-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-all-locales.txt) GitHub repository.

For more information about recording the consent video, see [How to record video samples](../../../../text-to-speech-avatar/custom-avatar-record-video-samples.md) and [Disclosure for avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

On **Register avatar talent**, use **Select data** to reuse an existing consent recording. To upload a new consent recording, follow these steps:

1. Select **Upload video**.
1. In the **Upload data** dialog, follow the instructions to upload the avatar talent consent video you recorded beforehand.
    - In **Select avatar type to build**, choose **Avatar with a voice sync for avatar** or **Avatar only**. Choose the type that matches both the recorded consent statement and the model you want to train.
    - Select the speaking language of the verbal consent statement recorded by the avatar talent. 
    - Enter the avatar talent name and your company name in the same language as the recorded statement. 
        - The avatar talent name must be the name of the person who recorded the consent statement. 
        - The company name must match the company name that was spoken in the recorded statement. 

1. Select local files from your computer or enter the Azure Blob storage URL where your data is stored.
1. Select **Upload**.

After the consent recording is validated, confirm that it's selected under **Select data**, and select **Next** to continue to **Training data**.

## Step 3: Add training data

The Speech service uses your training data to create a unique avatar tuned to match the look of the person in the recordings. After you train the avatar model, you can start synthesizing avatar videos or use it for live chats in your applications.

All data you upload must meet the requirements for the data type that you choose. To ensure that the Speech service accurately processes your data, it's important to correctly format your data before upload. To confirm that your data is correctly formatted, see [Data requirements](../../../../text-to-speech-avatar/custom-avatar-record-video-samples.md#data-requirements). 

### Upload your data

On the **Training data** step, use **Select data** to reuse existing training data, or upload new videos.

To upload training data, follow these steps:
1. Select **Upload data**.
1. In the **Upload data** dialog, choose **Select data type**. **Naturally speaking** is required for training, and **Silent status** is required for interactive conversation. Add **Gesture** and **Status 0 speaking** for gesture insertion in video content generation. For recording requirements, see [what video clips to record](../../../../text-to-speech-avatar/custom-avatar-record-video-samples.md#what-video-clips-to-record).
1. Select local files from your computer or enter the Azure Blob storage URL where your data is stored.
1. Select **Upload**. Repeat for the data types you need.

Data files are automatically validated when you select **Upload**. Data validation includes series of checks on the video files to verify their file format, size, and total volume. If there are any errors, fix them and submit again.

After uploading, confirm that the intended training data is selected. Check **Data preview**, which groups the selected videos by type and indicates whether you provided enough data for training and your scenario. Resolve validation errors or missing data, and then select **Next**.

## Step 4: Train your avatar model

> [!IMPORTANT]
> Training uses the data you select for this avatar customization. The model quality depends on the data you provide, and you're responsible for the video quality. Ensure you record the training videos according to the [how to record video samples guide](../../../../text-to-speech-avatar/custom-avatar-record-video-samples.md).

To create a custom avatar in the Microsoft Foundry portal, follow these steps:
1. On **Training settings**, select **Dimension** and **Resolution**:
   - **Dimension**: Choose **16:9 (Landscape)** or **9:16 (Portrait)**. To select **9:16 (Portrait)**, use portrait resolution for all training data, such as 1080 × 1920.
   - **Resolution**: Choose **1080p (Full HD)** or **2160p (4K)**. To select **2160p (4K)**, use 4K resolution for all training data. Options that don't meet the data requirements are unavailable.

1. Select **Next** to continue to **Review**.
1. Review the avatar details, selected data, training settings, and estimated training hours. Review and accept the usage acknowledgment and terms of use to proceed.
1. Select **Submit** to start training. Open the submitted job from the **Customizations** tab and wait for **Training** to show **Succeeded** before deploying.
  
Training duration varies depending on how much data you use. It normally takes 20-40 compute hours on average to train a custom avatar. Check the [pricing note](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services) on how training is charged. 

### Copy your custom avatar model to another project (optional)

Custom avatar training is currently only available in some regions. After your avatar model is trained in a supported region, you can copy it to an AI Services resource for Speech in another region as needed. For more information, see footnotes in the [regions table](../../../../regions.md).

> [!NOTE]
> You can only copy the voice sync for avatar model to the regions that support the voice sync for avatar feature, which are the same regions that support personal voice. See the [Region support](/azure/ai-services/speech-service/regions?tabs=ttsavatar) page.

To copy your custom avatar model to another project:
1. On the completed customization's details page, select **More actions** > **Copy to**.
1. In **Copy speech model**, select **Subscription**, **Resource group**, **Target foundry resource**, and **Target foundry project**. Create the target resource and project first if needed.
1. Select **Copy**.

Once the model is copied, you see a notification in the Microsoft Foundry portal.

Navigate to the project where you copied the model to deploy the model copy.

## Step 5: Deploy and use your avatar model

After you successfully created and trained your avatar model, you deploy it to your endpoint.

To deploy your avatar:
1. Open the completed avatar customization.
1. Select **Deploy** at the top of the details page and complete the deployment prompts.
1. Select **Deployments** to check the deployment status. Wait for **Succeeded**, and then select the deployment row to open its details panel.

    > [!IMPORTANT]
    > When a model is deployed, you pay for continuous up time of the endpoint regardless of your interaction with that endpoint. Check the pricing note on how model deployment is charged. You can delete a deployment when the model isn't in use to reduce spending and conserve resources.

After you deploy your custom avatar, you can use it in the following ways:

- Create video content (Text to Speech Avatar) in Microsoft Foundry
   - From **Use your avatar** in the deployment details panel, select **Try Text to Speech Avatar**, or
   - Select **Open in Playground** in that panel, then choose **Text to Speech Avatar**.
- Start a live chat (Voice Live) in Microsoft Foundry
   - From **Use your avatar** in the deployment details panel, select **Try Voice Live**, or
   - Select **Open in Playground** in that panel, then choose **Voice Live**.
- Use the avatar through the API by specifying the avatar model name in the SDK or speech synthesis markup language (SSML) input. For more information, see the [avatar properties](../../../../text-to-speech-avatar/batch-synthesis-avatar-properties.md#avatar-properties).

### Use in Microsoft Foundry

- To open a playground independently, select **Build** > **Services** > **Playgrounds** in the project associated with your deployed avatar.
- Select **Azure Speech - Text to Speech Avatar**, go to the **Avatar** section, select **More avatars**, and then select your custom avatar under the **Custom** tab.
- For **Azure Speech - Voice Live**, turn on the **Avatar** toggle, select **More avatars**, and then select your custom avatar under the **Custom** tab.

Check that your custom avatar is selected, choose a voice, and then start using it.
 
### Remove a deployment 

To remove your deployment, follow these steps:
1. Open the avatar customization and select **Deployments**. The model is actively hosted if the deployment status is **Succeeded**.
1. Select the deployment row to open its details panel.
1. Select **Delete** and confirm the deletion to remove the hosting.

> [!TIP]
> Once a deployment is removed, you no longer pay for its hosting. Deleting a deployment doesn't cause any deletion of your model. If you want to use the model again, create a new deployment. 

