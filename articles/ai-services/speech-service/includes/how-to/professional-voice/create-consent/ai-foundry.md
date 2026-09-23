---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 09/07/2026
ms.custom: include
ai-usage: ai-assisted
---

A voice talent is an individual or target speaker whose voices are recorded and used to create neural voice models. 

Before you can fine-tune a professional voice, you must submit a recording of the voice talent's consent statement. The voice talent statement is a recording of the voice talent reading a statement that they consent to the usage of their speech data for professional voice fine-tuning. The consent statement is also used to verify that the voice talent is the same person as the speaker in the fine-tuning data. 

> [!TIP]
> Before you get started in the Microsoft Foundry portal, define your voice [persona and choose the right voice talent](../../../../record-custom-voice-samples.md#choose-your-voice-talent).

You can find the verbal consent statement in multiple languages on [GitHub](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt). The language of the verbal statement must be the same as your recording. See also the [disclosure for voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

## Add voice talent

> [!TIP]
> For a sample consent statement and training data, see the [GitHub repository](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/Sample%20Data). 

To add a voice talent profile and upload their consent statement, follow these steps:

# [Foundry (new)](#tab/foundry-new)

These steps continue from the **Customize a model** page you opened in [Set up a professional voice](../../../../professional-voice-create-project.md).

If you closed the page, [resume your draft customization](../../../../professional-voice-create-project.md?tabs=foundry-new&pivots=ai-foundry-portal#resume-an-unfinished-customization) before continuing.

> [!TIP]
> If you need sample consent and training files, select **Download sample data** on the **Register voice talent** step.

1. On the **Register voice talent** step, select **Add voice talent**.
1. In the **Add voice talent** pane, provide the voice talent details and upload the recorded verbal consent statement:

   - For **Target scenario**, select one or more scenarios that match the intended use of the voice.
   - Optionally, for **Voice characteristics**, describe the characteristics of the voice.
   - Enter the **Voice talent name**. The name must match the person who recorded the consent statement, in the same language used in the recording.
   - Enter the **Company name**. The company name must match what was spoken in the recording, in the same language.
   - Drag the `.mp3` or `.wav` file into the upload area, or select **Browse for a file** to select it.
   - Make sure the verbal statement was [recorded](../../../../record-custom-voice-samples.md) with the same settings, environment, and speaking style as your fine-tuning data.

1. Select **Upload**.
1. Wait for the voice talent status to become **Succeeded**. If processing fails, review the reported error and check the recording, consent statement, and matching voice talent and company names.
1. On the **Register voice talent** step, select the voice talent you just added, and then select **Next**.

Continue with [Add training datasets](../../../../professional-voice-create-training-set.md).

### View or delete an existing voice talent

If you uploaded the wrong consent recording, find the voice talent entry on the **Data** tab under **Services**. This tab is separate from **Data** in the left navigation.

1. Open the Foundry project that contains the voice talent.
1. Select **Build** > **Services**, and then select the **Data** tab.
1. Find the entry with the **Voice Talent** type and **Text to Speech** tag. Select its name to review the details and play the consent recording.

To delete an unwanted voice talent entry:

1. Return to **Services** > **Data**.
1. In the voice talent's row, open the **Actions** menu (three dots), and then select **Delete**.
1. In the **Delete AI service resource** dialog, confirm that the displayed name matches the voice talent you want to remove.
1. Select **Delete** to confirm, or **Cancel** to keep the entry.

> [!IMPORTANT]
> Deletion can't be undone. Confirm that you selected the unwanted voice talent entry before deleting it.

To upload the correct recording, return to **Register voice talent** in your customization and follow [Add voice talent](#add-voice-talent).

# [Foundry (classic)](#tab/foundry-classic)

1. Sign in to the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Set up voice talent** > **+ Add voice talent**. 
1. In the **Add new voice talent** wizard, select the target scenarios for the voice talent. The target scenarios must be consistent with what you provided in the application form. The scenarios are used to help identify the voice talent and to ensure that the voice model is trained for the intended use cases.
1. Optionally in the **Voice characteristics** text box, enter a description of the characteristics of the voice you're going to create. 
1. Select **Next**.
1. On the **Upload verbal statement** page, follow the instructions to upload the voice talent statement you recorded beforehand. 

    - Enter the voice talent name and company name. The voice talent name must be the name of the person who recorded the consent statement. Enter the name in the same language used in the recorded statement. The company name must match the company name that was spoken in the recorded statement. Ensure the company name is entered in the same language as the recorded statement.
    - Make sure the verbal statement was [recorded](../../../../record-custom-voice-samples.md) with the same settings, environment, and speaking style as your fine-tuning data.

    :::image type="content" source="../../../../media/custom-voice/professional-voice/upload-verbal-statement.png" alt-text="Screenshot of the voice talent statement upload dialog." lightbox="../../../../media/custom-voice/professional-voice/upload-verbal-statement.png":::

1. Select **Next**.
1. Review the voice talent and persona details, and select **Add voice talent**.

After the voice talent status is *Succeeded*, you can [add fine-tuning data](../../../../professional-voice-create-training-set.md).

---

## Next steps

> [!div class="nextstepaction"]
> [Add training data for professional voice fine-tuning](../../../../professional-voice-create-training-set.md)
