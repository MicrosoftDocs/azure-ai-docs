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

After you successfully created and [fine-tuned](../../../../professional-voice-train-voice.md) your professional voice model, you deploy it to a custom voice endpoint. 

> [!NOTE]
> You can create up to 50 endpoints with a standard (S0) Speech resource, each with its own custom voice.

To use your fine-tuned professional voice, you must specify the voice model name, use the custom URI directly in an HTTP request, and use the same Speech resource to pass through the authentication of the text to speech service.

## Add a deployment endpoint

To create a professional voice endpoint:

To deploy an endpoint, follow these steps:
1. Sign in to the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Deploy model** > **Deploy model**. 
1. Select a voice model that you want to associate with this endpoint and then select **Next**.  
1. Enter a **Endpoint name** and **Description** for your custom endpoint.
1. Select **Endpoint type** according to your scenario. If your resource is in a supported region, the default setting for the endpoint type is *High performance*. Otherwise, if the resource is in an unsupported region, the only available option is *Fast resume*.
   - **High performance**: Optimized for scenarios with real-time and high-volume synthesis requests, such as conversational AI, call-center bots. It takes around 5 minutes to deploy or resume an endpoint. For information about regions where the *High performance* endpoint type is supported, see the footnotes in the [regions](../../../../regions.md#regions) table. 
   - **Fast-resume**: Optimized for audio content creation scenarios with less frequent synthesis requests. Easy and quick to deploy or resume an endpoint in under a minute. The fast-resume endpoint type is supported in all [regions](../../../../regions.md#regions) where text to speech is available.
1. Select **Next**.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the model hosting costs.
1. Select **Deploy** to create your endpoint.

After your endpoint is deployed, the endpoint name appears as a link. Select the link to display information specific to your endpoint, such as the endpoint key, endpoint URL, and sample code. When the status of the deployment is **Succeeded**, the endpoint is ready for use.

## Test your custom voice

Once your custom voice endpoint has been deployed, you can try out your custom voice directly in the portal.

1. Select **Deploy model** > **Deploy model**. 
1. Select **Test endpoint**. 

:::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-endpoint-test.png" alt-text="Screenshot of a page to test an endpoint." lightbox="../../../../media/custom-voice/professional-voice/cnv-endpoint-test.png":::

## Use your custom voice

The custom endpoint is functionally identical to the standard endpoint that's used for text to speech requests. 

One difference is that the `EndpointId` must be specified to use the custom voice via the Speech SDK. You can start with the [text to speech quickstart](../../../../get-started-text-to-speech.md) and then update the code with the `EndpointId` and `SpeechSynthesisVoiceName`. For more information, see [use a custom endpoint](../../../../how-to-speech-synthesis.md#use-a-custom-endpoint).

To use a custom voice via [Speech Synthesis Markup Language (SSML)](../../../../speech-synthesis-markup-voice.md#use-voice-elements), specify the model name as the voice name. This example uses the `YourCustomVoiceName` voice. 

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="YourCustomVoiceName">
        This is the text that is spoken. 
    </voice>
</speak>
```

## Switch to a new voice model in your product

Once you updated your voice model to the latest engine version, or if you want to switch to a new voice in your product, you need to redeploy the new voice model to a new endpoint. Redeploying new voice model on your existing endpoint isn't supported. After deployment, switch the traffic to the newly created endpoint. We recommend that you transfer the traffic to the new endpoint in a test environment first to ensure that the traffic works well, and then transfer to the new endpoint in the production environment. During the transition, you need to keep the old endpoint. If there are some problems with the new endpoint during transition, you can switch back to your old endpoint. If the traffic has been running well on the new endpoint for about 24 hours (recommended value), you can delete your old endpoint. 

> [!NOTE]
> If your voice name is changed and you're using Speech Synthesis Markup Language (SSML), be sure to use the new voice name in SSML.

## Suspend and resume an endpoint

You can suspend or resume an endpoint to limit spend and conserve resources that aren't in use. You aren't charged while the endpoint is suspended. When you resume an endpoint, you can continue to use the same endpoint URL in your application to synthesize speech. 

> [!NOTE]
> The Suspend operation completes almost immediately. The Resume operation completes in about the same amount of time as a new deployment. 

This section describes how to suspend or resume a custom voice endpoint in the Microsoft Foundry portal.

### Suspend endpoint

To suspend and deactivate your endpoint:
1. Sign in to the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Deploy model**. 
1. Select the endpoint you want to suspend and then select **Suspend**. 

   :::image type="content" source="../../../../media/custom-voice/professional-voice/suspend-resume.png" alt-text="Screenshot of page to suspend or resume an endpoint." lightbox="../../../../media/custom-voice/professional-voice/suspend-resume.png":::

1. In the dialog box that appears, select **Suspend**. After the endpoint is suspended, the status changes from **Succeeded** to **Suspended**. 

### Resume endpoint

1. To resume and activate your endpoint, select **Resume** from the **Deploy model** tab in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. In the dialog box that appears, select **Submit**. After you successfully reactivate the endpoint, the status will change from **Suspended** to **Succeeded**.

## Next steps

- Learn more about custom voice in the [overview](../../../../custom-neural-voice.md).
- Learn more about custom avatar in the [overview](../../../../text-to-speech-avatar/what-is-text-to-speech-avatar.md).

