---
title: Custom voice lite - Speech service
titleSuffix: Foundry Tools
description: Use custom voice lite to demo and evaluate custom voice before investing in professional recordings to create a higher-quality voice.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/29/2025
ms.author: pafarley
---

# Custom voice lite

Custom voice lite is a project type you can use to demo and evaluate a custom voice before you invest in professional recordings to create a higher-quality voice. 

> [!IMPORTANT]
> No application is required for demo and evaluation purposes. However, Microsoft restricts and selects the recording and testing samples for use with custom voice lite. You must apply for full access to professional voice fine-tuning in order to deploy and use the custom voice lite model for business purpose. Request access using the [intake form](https://aka.ms/customneural).

> [!NOTE]
> Custom voice lite is only available in the [Speech Studio](https://aka.ms/speechstudio/customvoice). It isn't available through the Microsoft Foundry portal, REST API, or SDKs.

With a custom voice lite project, you record your voice online by reading 20-50 pre-defined scripts provided by Microsoft. After you've recorded at least 20 samples, you can start to train a model. Once the model is trained successfully, you can review the model and check out 20 output samples produced with another set of pre-defined scripts.

See the [supported languages](language-support.md?tabs=tts) for custom voice.

## Compare project types

The following table summarizes key differences between custom voice lite and professional voice fine-tuning.  

|**Item**|**Lite**| **Professional**|
|---------------|---------------|---------------|
|Target scenarios |Demonstration or evaluation |Professional scenarios like brand and character voices for chat bots, or audio content reading.|   
|Training data |Record online using Speech Studio |Bring your own data. Recording in a professional studio is recommended. |   
|Scripts for recording  |Provided in Speech Studio |Use your own scripts that match the use case scenario. Microsoft provides [example scripts](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/script) for reference. |   
|Required data size  |20-50 utterances |300-2000 utterances|
|Training time  |Less than one compute hour| Approximately 20-40 compute hours |
|Voice quality  |Moderate quality|High quality |
|Availability  |Anyone can record samples online and train a model for demo and evaluation purpose. Full access to custom voice is required if you want to deploy the custom voice lite model for business use. |Data upload isn't restricted, but you can only fine-tune a professional voice after access is approved. Professional voice fine-tuning is limited based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).|
|Pricing  |Per unit prices apply equally for both custom voice lite and professional voice fine-tuning. Check the [pricing details here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). |Per unit prices apply equally for both custom voice lite and professional voice fine-tuning. Check the [pricing details here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).  |

## Create a custom voice lite project

To create a custom voice lite project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customvoice).
1. Select the subscription and Speech resource to work with.
1. Select **Custom voice** > **Create a project**. 
1. Select **Custom neural voice lite** > **Next**. To create a custom voice professional project instead, see the [professional voice fine-tuning documentation](professional-voice-create-project.md).

1. Follow the instructions provided by the wizard to create your project. 
    
    > [!IMPORTANT]
    > The custom voice lite project expires after 90 days unless the [verbal statement](#submit-verbal-statement) recorded by the voice talent is submitted.

1. Select the new project by name or select **Go to project**. You see these menu items in the left panel: **Record and build**, **Review model**, and **Deploy model**.  

    :::image type="content" source="media/custom-voice/lite/lite-project-get-started.png" alt-text="Screenshot with an overview of the custom voice lite record, train, test, and deploy workflow.":::


## Record and build a custom voice lite model

Record at least 20 voice samples (up to 50) with provided scripts online. Voice samples recorded here are used to create a synthetic version of your voice.

> [!NOTE]
> Custom voice training is currently only available in some regions. See footnotes in the [regions](regions.md#regions) table for more information.

Here are some tips to help you record your voice samples:
- Use a good microphone. Increase the clarity of your samples by using a high-quality microphone. Speak about 8 inches away from the microphone to avoid mouth noises.
- Avoid background noise. Record in a quiet room without background noise or echoing.
- Relax and speak naturally. Allow yourself to express emotions as you read the sentences.
- Record in one take. To keep a consistent energy level, record all sentences in one session.
- Pronounce each word correctly, and speak clearly. 

To record and build a custom voice lite model, follow these steps in [Speech Studio](https://aka.ms/speechstudio/customvoice):

1. Select **Custom voice** > Your project name > **Record and build**. 
1. Select **Get started**. 
1. Read the Voice talent terms of use carefully. Select the checkbox to acknowledge the terms of use.
1. Select **Accept**
1. Press the microphone icon to start the noise check. This noise check takes only a few seconds, and you don't need to speak during it. 
1. If noise was detected, you can select **Check again** to repeat the noise check. If no noise was detected, you can select **Done** to proceed to the next step. 
    :::image type="content" source="media/custom-voice/lite/cnv-record-noise-check.png" alt-text="Screenshot of the noise check results when noise was detected.":::
1. Review the recording tips and select **Got it**. For the best results, go to a quiet area without background noise before recording your voice samples.
1. Press the microphone icon to start recording.
    :::image type="content" source="media/custom-voice/lite/cnv-record-sample.png" alt-text="Screenshot of the record sample dashboard.":::
1. Press the stop icon to stop recording.
1. Review quality metrics. After recording each sample, check its quality metric before continuing to the next one.
1. Record more samples. Although you can create a model with just 20 samples, it's recommended that you record up to 50 to get better quality.
1. Select **Train model** to start the training process. 

The training process takes approximately one compute hour. You can check the progress of the training process in the **Review model** page.

## Review model

To review the custom voice lite model and listen to your own synthetic voice, follow these steps:

1. Select **Custom voice** > Your project name > **Review model**. Here you can review the voice model name, model language, sample data size, and training progress. The voice name is composed of the word "Neural" appended to your project name.
1. Select the voice model name to review the model details and listen to the sample text to speech results.
1. Select the play icon to hear your voice speak each script. 
    :::image type="content" source="media/custom-voice/lite/lite-review-model.png" alt-text="Screenshot of the review sample output dashboard.":::

## Submit verbal statement

A verbal statement recorded by the voice talent is required before you can [deploy the model](#deploy-model) for your business use. 

To submit the voice talent verbal statement, follow these steps in [Speech Studio](https://aka.ms/speechstudio/customvoice):

1. Select **Custom voice** > Your project name > **Deploy model** > **Manage your voice talent**.
    :::image type="content" source="media/custom-voice/lite/lite-voice-talent-consent.png" alt-text="Screenshot of the record voice talent consent dashboard.":::
1. Select the model.
1. Enter the voice talent name and company name.
1. Read and record the statement. Select the microphone icon to start recording. Select the stop icon to stop recording.
1. Select **Submit** to submit the statement.
1. Check the processing status in the script table at the bottom of the dashboard. Once the status is **Succeeded**, you can [deploy the model](#deploy-model).

## Deploy model

To deploy your custom voice lite model and use it in your applications, you must get the full access to custom voice. Request access on the [intake form](https://aka.ms/customneural). Within approximately 10 business days, you receive an email with the approval status. A [verbal statement](#submit-verbal-statement) recorded by the voice talent is also required before you can deploy the model for your business use.

To deploy a custom voice lite model, follow these steps in [Speech Studio](https://aka.ms/speechstudio/customvoice):

1. Select **Custom voice** > Your project name > **Deploy model** > **Deploy model**.
1. Select a voice model name and then select **Next**.
1. Enter a name and description for your endpoint and then select **Next**.
1. Select the checkbox to agree to the terms of use and then select **Next**.
1. Select **Deploy** to deploy the model.

From here, you can use the custom voice lite model similarly as you would use a professional voice model. For example, you can [suspend or resume](professional-voice-deploy-endpoint.md) an endpoint after it's created, to limit spend and conserve resources that aren't in use. You can also access the voice in the [Audio Content Creation](how-to-audio-content-creation.md) tool in the [Speech Studio](https://aka.ms/speechstudio/audiocontentcreation).

## Related content

* [Fine-tune a professional voice](professional-voice-create-project.md) 
* [Try the text to speech quickstart](get-started-text-to-speech.md)
* [Learn more about speech synthesis](how-to-speech-synthesis.md)
