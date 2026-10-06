---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 09/07/2026
ai-usage: ai-assisted
---

Set up your professional voice before you add voice talent consent and training data.

## Prerequisites

- Approved access to professional voice. Review the [limited-access requirements](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access?tabs=cnv) and [request access](https://aka.ms/customneural) if needed.
- For Foundry (new), an Azure subscription and a Foundry project associated with a Standard (S0) resource. See [Create a Microsoft Foundry project](/azure/foundry/how-to/create-projects?tabs=foundry).
- For Foundry (new), permission to use the project and manage Speech data, models, and deployments. Ask your administrator to review [Foundry access permissions](/azure/foundry/concepts/rbac-foundry) and [Speech resource permissions](../../../../role-based-access-control.md#roles-for-speech-resources).
- A [supported language](../../../../language-support.md?tabs=custom-tts#professional-voice) and a resource in a supported training region. In the [Text to speech regions table](../../../../regions.md?tabs=tts#regions), check **Custom voice training** and its footnotes.
- Written permission from the voice talent and a recording of their [consent statement](../../../../professional-voice-create-consent.md). Share the [disclosure for voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent) with them before recording.
- Audio recordings and, when required by your [data type](../../../../how-to-custom-voice-training-data.md), matching transcripts. Training eligibility depends on the selected [training method and version](../../../../professional-voice-train-voice.md#choose-a-training-method), not a single minimum that applies to every model.

## Start professional voice setup

# [Foundry (new)](#tab/foundry-new)

To start a professional voice customization in the new Microsoft Foundry portal, follow these steps:

> [!TIP]
> To start from **Build**, select **Services** > **Customizations**. This tab lists your draft customizations and trained models. Select **Create**, and then complete **Basic details** in this procedure.

1. [!INCLUDE [foundry-sign-in](../../../../../../foundry/includes/foundry-sign-in.md)]
1. Open the Foundry project associated with the resource you want to use for professional voice.
1. Select **Discover**.
1. On **Overview**, under **Experiment with prebuilt services**, select **Azure Speech**.
1. On the **Services** page, under **Customize**, select **Professional voice** to open the **Customize a model** page.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-discover-professional-voice.png" alt-text="Screenshot of Discover Services with the Professional voice card outlined under Customize." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-discover-professional-voice.png":::

1. On the **Basic details** step, fill in these settings:

   - **Select model**: Select **Azure Speech - Text to Speech** if it isn't already selected.
   - **Type**: Select **Professional voice** if it isn't already selected.
   - **Voice gender**: Select the gender of the voice talent.
   - **Training data language**: Select the language of your training data.
   - **Voice name**: Enter a name for your voice model.
   - **Description**: Optionally enter a description.

1. Select **Next**.

Keep the **Customize a model** page open and continue with [Add voice talent consent](../../../../professional-voice-create-consent.md) to register the voice talent.

### Resume an unfinished customization

If you leave the wizard before submitting training, return to your existing draft:

1. Open the same Foundry project.
1. Select **Build** > **Services** > **Customizations**.
1. Select the name of your customization with the **Draft** status to reopen **Customize a model**.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-resume-draft.png" alt-text="Screenshot of Build Services with the Customizations tab and a professional voice Draft row outlined." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-resume-draft.png":::

1. Review the saved settings and continue to the step you need.

# [Foundry (classic)](#tab/foundry-classic)

In the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs), you can fine-tune some Foundry Tools models. To fine-tune a professional voice model, follow these steps:

1. Go to your Microsoft Foundry project in the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs). If you need to create a project, see [Create a Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Foundry Tools models." lightbox="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png":::
 
1. In the wizard, select **Custom voice (professional voice fine-tuning)**.
1. Select **Next**.
1. Follow the instructions provided by the wizard to create your fine-tuning workspace. 

---

## Continue professional voice setup

Use the following Azure Speech in Foundry Tools articles to continue setting up your professional voice:
* [Add voice talent consent](../../../../professional-voice-create-consent.md)
* [Add training datasets](../../../../professional-voice-create-training-set.md)
* [Train your voice model](../../../../professional-voice-train-voice.md)
* [Deploy your professional voice model as an endpoint](../../../../professional-voice-deploy-endpoint.md)

## View professional voice models

# [Foundry (new)](#tab/foundry-new)

After training finishes, access your custom voice models and deployments from the **Customizations** tab.

1. [!INCLUDE [foundry-sign-in](../../../../../../foundry/includes/foundry-sign-in.md)]
1. Select **Build** from the upper-right menu.
1. Select **Services** in the left pane.
1. Select the **Customizations** tab to view the status of your customization jobs and the models that were created.
1. Select a model name to open the model details page, where you can view training status and manage deployments.

To [test your voice in the playground](../../../../professional-voice-deploy-endpoint.md?tabs=foundry-new&pivots=ai-foundry-portal#test-your-custom-voice), first deploy the model and wait for the deployment status to become **Succeeded**.

# [Foundry (classic)](#tab/foundry-classic)

1. Sign in to the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**. You can view the status of your fine-tuning tasks and the models that were created.
    
    :::image type="content" source="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to view fine-tuned Foundry Tools models." lightbox="../../../../media/custom-voice/professional-voice/fine-tune-azure-ai-services.png":::

---

## Next step

> [!div class="nextstepaction"]
> [Add voice talent consent for professional voice.](../../../../professional-voice-create-consent.md)
