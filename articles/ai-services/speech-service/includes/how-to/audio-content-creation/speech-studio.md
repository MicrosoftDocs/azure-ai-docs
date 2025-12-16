---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/31/2025
---

## Prerequisites

- An active Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Permission to create resources in your subscription.
- A Speech resource. Create one in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) or [Speech Studio](https://aka.ms/speechstudio).

> [!NOTE]
> The [Foundry resource type](../../../../multi-service-resource.md) isn't supported in Speech Studio. 

## Use the audio content creation tool

The following diagram displays the process for fine-tuning the text to speech outputs. 

:::image type="content" source="../../../media/audio-content-creation/audio-content-creation-diagram.jpg" alt-text="Diagram of the sequence of steps for fine-tuning text to speech outputs." lightbox="../../../media/audio-content-creation/audio-content-creation-diagram.jpg":::

To use the audio content creation tool, do the following:

1. Sign in to [Speech Studio](https://aka.ms/speechstudio/), and then select **Audio Content Creation**.

1. Select the Azure subscription and the Speech resource you want to work with, and then select **Use resource**. 

   > [!NOTE]
   > If you're returning to audio content creation, you can select a different Speech resource that you want to work with. Go to your account settings at the top right corner of the page.

1. [Create an audio tuning file](#create-an-audio-tuning-file) by using plain text or SSML scripts. Enter or upload your content into audio content creation.
1. Choose the voice and the language for your script content. Audio content creation includes all of the [standard text to speech voices](../../../language-support.md?tabs=tts). You can use standard voices or a custom voice.

   > [!NOTE]
   > Custom voice access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

1. Select the content you want to preview, and then select **Play** (via the triangle icon) to preview the default synthesis output. 

   If you make any changes to the text, select the **Stop** icon, and then select **Play** again to regenerate the audio with changed scripts. 

   Improve the output by adjusting pronunciation, break, pitch, rate, intonation, voice style, and more. For a complete list of options, see [Speech Synthesis Markup Language](../../../speech-synthesis-markup.md). 

   For more information about adjusting the speech output, see the [how to convert text to speech video on YouTube](https://youtu.be/ygApYuOOG6w). However, the video might not be available in all regions and might not be up to date by the time you watch it.

1. Save and [export your tuned audio](#export-tuned-audio). 

   When you save the tuning track in the system, you can continue to work and iterate on the output. When you're satisfied with the output, you can create an audio creation task with the export feature. You can observe the status of the export task and download the output for use with your apps and products.

## Create an audio tuning file

You can get your content into the audio content creation tool in either of two ways:

### Option 1: Create a new audio tuning file

1. Select **New** > **Text file** to create a new audio tuning file.

1. Enter or paste your content into the editing window. The allowable number of characters for each file is 20,000 or fewer. If your script contains more than 20,000 characters, you can use Option 2 to automatically split your content into multiple files.

1. Select **Save**.

### Option 2: Upload an audio tuning file

1. Select **Upload** > **Text file** to import one or more text files. Both plain text and SSML are supported. 

   If your script file is more than 20,000 characters, split the content by paragraphs, by characters, or by regular expressions.

1. When you upload your text files, make sure that they meet these requirements:

   | Property | Description |
   |----------|---------------|
   | File format | Plain text (.txt) or SSML text (.txt)<br/><br/>Zip files aren't supported. |
   | Encoding format | UTF-8 |
   | File name | Each file must have a unique name. Duplicate files aren't supported. |
   | Text length | Character limit is 20,000. If your files exceed the limit, split them according to the instructions in the tool. |
   | SSML restrictions | Each SSML file can contain only a single piece of SSML. |
      

   Here's a plain text example:

   ```txt
   Welcome to use audio content creation to customize audio output for your products.
   ```

   Here's an SSML example:

   ```xml
   <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" version="1.0" xml:lang="en-US">
      <voice name="en-US-AvaMultilingualNeural">
      Welcome to use audio content creation <break time="10ms" />to customize audio output for your products.
      </voice>
   </speak>
   ```

## Export tuned audio

After you review your audio output and are satisfied with your tuning and adjustment, you can export the audio.

1. Select **Export** to create an audio creation task. 

   We recommend **Export to Audio library** to easily store, find, and search audio output in the cloud. You can better integrate with your applications through Azure blob storage. You can also download the audio to your local disk directly.
   
1. Choose the output format for your tuned audio. The **supported audio formats and sample rates** are listed in the following table:

    | Format | 8 kHz sample rate | 16 kHz sample rate | 24 kHz sample rate | 48 kHz sample rate |
    |--- |--- |--- |--- |--- |
    | wav | riff-8khz-16bit-mono-pcm | riff-16khz-16bit-mono-pcm | riff-24khz-16bit-mono-pcm |riff-48khz-16bit-mono-pcm |
    | mp3 | N/A | audio-16khz-128kbitrate-mono-mp3 | audio-24khz-160kbitrate-mono-mp3 |audio-48khz-192kbitrate-mono-mp3 |
    
1. To view the status of the task, select the **Task list** tab. 

   If the task fails, see the detailed information page for a full report.

1. When the task is complete, your audio is available for download on the **Audio library** pane.

1. Select the file you want to download and **Download**. 

Now you're ready to use your custom tuned audio in your apps or products.
   
## Configure BYOS and anonymous public read access for blobs
   
If you lose access permission to your bring your own storage (BYOS), you can't view, create, edit, or delete files. To resume your access, you need to remove the current storage and reconfigure the BYOS in the [Azure portal](https://portal.azure.com/#allservices). To learn more about how to configure BYOS, see [Mount Azure Storage as a local share in App Service](/azure/app-service/configure-connect-to-azure-storage?pivots=container-linux&tabs=portal). 

After configuring the BYOS permission, you need to configure anonymous public read access for related containers and blobs. Otherwise, blob data isn't available for public access and your lexicon file in the blob is inaccessible. By default, a container’s public access setting is disabled. To grant anonymous users read access to a container and its blobs, first set **Allow Blob anonymous access** to **Enabled** to allow public access for the storage account, then set the container's (named **acc-public-files**) public access level (**anonymous read access for blobs only**). To learn more about how to configure anonymous public read access, see [Configure anonymous public read access for containers and blobs](/azure/storage/blobs/anonymous-read-access-configure?tabs=portal). 
   
## Add or remove audio content creation users

If more than one user wants to use audio content creation, you can grant them access to the Azure subscription and the Speech resource. If you add users to an Azure subscription, they can access all the resources under the Azure subscription. But if you add users to a Speech resource only, they only have access to the Speech resource and not to other resources under this Azure subscription. Users with access to the Speech resource can use the audio content creation tool.

The users you grant access to need to set up a [Microsoft account](https://account.microsoft.com/account). If they don' have a Microsoft account, they can create one in just a few minutes. They can use their existing email and link it to a Microsoft account, or they can create and use an Outlook email address as a Microsoft account.

### Add users to a Speech resource

To add users to a Speech resource so that they can use audio content creation, do the following:

1. In the [Azure portal](https://portal.azure.com/), select **All services** from the left pane, and then search for **Foundry Tools** or **Speech**.
1. Select your Speech resource.

   > [!NOTE]
   > You can also set up Azure RBAC for whole resource groups, subscriptions, or management groups. Do this by selecting the desired scope level and then navigating to the desired item (for example, selecting **Resource groups** and then selecting your resource group).

1. Select **Access control (IAM)** on the left pane.
1. Select **Add** > **Add role assignment**.
1. On the **Role** tab on the next screen, select a role (such as **Owner**) that you want to add.
1. On the **Members** tab, enter a user's email address and select the user's name in the directory. The email address must be linked to a Microsoft account that's trusted by Microsoft Entra ID. Users can easily sign up for a [Microsoft account](https://account.microsoft.com/account) by using their personal email address. 
1. On the **Review + assign** tab, select **Review + assign** to assign the role.

Here's what happens next:

1. An email invitation is automatically sent to users. 

   > [!NOTE]
   > If users don't receive the invitation email, you can search for their account under **Role assignments** and go into their profile. Look for **Identity** > **Invitation accepted**, and select **(manage)** to resend the email invitation. You can also copy and send the invitation link to them. 

1. They can accept it by selecting **Accept invitation** > **Accept to join Azure** in their email. 
1. They're then redirected to the Azure portal. They don't need to take further action in the Azure portal. 
1. After a few moments, users are assigned the role at the Speech resource scope, which gives them access to this Speech resource. 

Users now visit or refresh the [audio content creation](https://aka.ms/audiocontentcreation) product page, and sign in with their Microsoft account. They select **Audio Content Creation** block among all speech products. They choose the Speech resource in the pop-up window or in the settings at the upper right. 

If they can't find the available Speech resource, they can check to ensure that they're in the right directory. To do so, they select the account profile at the upper right and then select **Switch** next to **Current directory**. If there's more than one directory available, it means they have access to multiple directories. They can switch to different directories and go to **Settings** to see whether the right Speech resource is available. 

Users who are in the same Speech resource see each other's work in the audio content creation tool. If you want each individual user to have a unique and private workplace in audio content creation, create a new Speech resource.

### Remove users from a Speech resource

To remove a user's permission from a Speech resource, do the following:
1. Search for **Foundry Tools** in the Azure portal, select the Speech resource that you want to remove users from.
1. Select **Access control (IAM)**, and then select the **Role assignments** tab to view all the role assignments for this Speech resource.
1. Select the users you want to remove, select **Remove**, and then select **OK**.

   :::image type="content" source="../../../media/audio-content-creation/remove-user.png" alt-text="Screenshot of the 'Remove' button on the 'Remove role assignments' pane." lightbox="../../../media/audio-content-creation/remove-user.png":::

### Enable users to grant access to others

If you want to allow a user to grant access to other users, you need to assign them the owner role for the Speech resource and set the user as the Azure directory reader.
1. Add the user as the owner of the Speech resource. For more information, see [Add users to a Speech resource](#add-users-to-a-speech-resource).

   :::image type="content" source="../../../media/audio-content-creation/add-role.png" alt-text="Screenshot showing the 'Owner' role on the 'Add role assignment' pane." lightbox="../../../media/audio-content-creation/add-role.png":::

1. In the [Azure portal](https://portal.azure.com/), select the collapsed menu at the upper left, select **Microsoft Entra ID**, and then select **Users**.
1. Search for the user's Microsoft account, go to their detail page, and then select **Assigned roles**.
1. Select **Add assignments** > **Directory Readers**. If the **Add assignments** button is unavailable, it means that you don't have access. You must have the role of **Owner** or **User Access Administrator** to assign roles to users. 

