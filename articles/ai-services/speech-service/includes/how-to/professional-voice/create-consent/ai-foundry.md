---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/29/2025
ms.custom: include
---

A voice talent is an individual or target speaker whose voices are recorded and used to create neural voice models. 

Before you can fine-tune a professional voice, you must submit a recording of the voice talent's consent statement. The voice talent statement is a recording of the voice talent reading a statement that they consent to the usage of their speech data for professional voice fine-tuning. The consent statement is also used to verify that the voice talent is the same person as the speaker in the fine-tuning data. 

> [!TIP]
> Before you get started in Microsoft Foundry (classic) portal, define your voice [persona and choose the right voice talent](../../../../record-custom-voice-samples.md#choose-your-voice-talent).

You can find the verbal consent statement in multiple languages on [GitHub](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt). The language of the verbal statement must be the same as your recording. See also the [disclosure for voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

## Add voice talent

> [!TIP]
> For a sample consent statement and training data, see the [GitHub repository](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/Sample%20Data). 

To add a voice talent profile and upload their consent statement, follow these steps:

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

    :::image type="content" source="../../../../media/custom-voice/professional-voice/upload-verbal-statement.png" alt-text="Screenshot of the voice talent statement upload dialog." lightbox="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png"::: 

1. Select **Next**.
1. Review the voice talent and persona details, and select **Add voice talent**.

After the voice talent status is *Succeeded*, you can [add fine-tuning data](../../../../professional-voice-create-training-set.md).

## Next steps

> [!div class="nextstepaction"]
> [Add training data for professional voice fine-tuning](../../../../professional-voice-create-training-set.md)

