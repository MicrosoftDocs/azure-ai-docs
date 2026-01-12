---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/19/2025
---

All it takes to get started are a handful of audio files and the associated transcriptions. See if custom voice supports your [language](../../../../language-support.md?tabs=tts) and [region](../../../../regions.md#regions).

## Start fine-tuning

In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), you can fine-tune some Foundry Tools models. To fine-tune a professional voice model, follow these steps:

1. Go to your Microsoft Foundry project in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). If you need to create a project, see [Create a Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Foundry Tools models." lightbox="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png":::
 
1. In the wizard, select **Custom voice (professional voice fine-tuning)**.
1. Select **Next**.
1. Follow the instructions provided by the wizard to create your fine-tuning workspace. 

## Continue fine-tuning

Go to the Azure Speech in Foundry Tools documentation to learn how to continue fine-tuning your professional voice model:
* [Add voice talent consent](../../../../professional-voice-create-consent.md)
* [Add training datasets](../../../../professional-voice-create-training-set.md)
* [Train your voice model](../../../../professional-voice-train-voice.md)
* [Deploy your professional voice model as an endpoint](../../../../professional-voice-deploy-endpoint.md)

## View fine-tuned models

After fine-tuning, you can access your custom voice models and deployments from the **Fine-tuning** page. 

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**. You can view the status of your fine-tuning tasks and the models that were created.
    
    :::image type="content" source="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to view fine-tuned Foundry Tools models." lightbox="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png":::

## Next step

> [!div class="nextstepaction"]
> [Add voice talent consent to the professional voice project.](../../../../professional-voice-create-consent.md)

