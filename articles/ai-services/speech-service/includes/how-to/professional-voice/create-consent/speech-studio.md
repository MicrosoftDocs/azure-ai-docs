---
title: include file
description: include file
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/1/2023
ms.custom: include
---

A voice talent is an individual or target speaker whose voices are recorded and used to create neural voice models. 

Before you can train a neural voice, you must submit a recording of the voice talent's consent statement. The voice talent statement is a recording of the voice talent reading a statement that they consent to the usage of their speech data to train a custom voice model. The consent statement is also used to verify that the voice talent is the same person as the speaker in the training data. 

> [!TIP]
> Before you get started in Speech Studio, define your voice [persona and choose the right voice talent](../../../../record-custom-voice-samples.md#choose-your-voice-talent).

You can find the verbal consent statement in multiple languages on [GitHub](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt). The language of the verbal statement must be the same as your recording. See also the [disclosure for voice talent](/legal/cognitive-services/speech-service/disclosure-voice-talent?context=/azure/ai-services/speech-service/context/context).

## Add voice talent

To add a voice talent profile and upload their consent statement, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customvoice).
1. Select **Custom voice** > Your project name > **Set up voice talent** > **Add voice talent**. 
1. In the **Add new voice talent** wizard, describe the characteristics of the voice you're going to create. The scenarios that you specify here must be consistent with what you provided in the application form.
1. Select **Next**.
1. On the **Upload voice talent statement** page, follow the instructions to upload the voice talent statement you've recorded beforehand. Make sure the verbal statement was [recorded](../../../../record-custom-voice-samples.md) with the same settings, environment, and speaking style as your training data.
    :::image type="content" source="../../../../media/custom-voice/upload-verbal-statement.png" alt-text="Screenshot of the voice talent statement upload dialog.":::   
1. Enter the voice talent name and company name. The voice talent name must be the name of the person who recorded the consent statement. Enter the name in the same language used in the recorded statement. The company name must match the company name that was spoken in the recorded statement. Ensure the company name is entered in the same language as the recorded statement.
1. Select **Next**.
1. Review the voice talent and persona details, and select **Submit**.

After the voice talent status is *Succeeded*, you can proceed to [train your custom voice model](../../../../professional-voice-train-voice.md).

## Next steps

> [!div class="nextstepaction"]
> [Add training data to the professional voice project](../../../../professional-voice-create-training-set.md)

