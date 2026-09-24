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

In this article, you learn how to fine-tune a professional voice through the Microsoft Foundry portal.

> [!IMPORTANT]
> Professional voice fine-tuning is currently only available in some regions. After your voice model is trained in a supported region, you can [copy the professional voice model](#copy-your-voice-model-to-another-project) to a Microsoft Foundry resource in another region as needed. For supported training locations, check the **Custom voice training** column and footnotes in the [Text to speech regions table](../../../../regions.md?tabs=tts#regions).

Training duration varies depending on how much data you use. It takes about 10 compute hours on average to fine-tune a professional voice. With a Microsoft Foundry standard (S0) resource, you can train four voices simultaneously. If you reach the limit, wait until at least one of your voice models finishes training, and then try again.

> [!NOTE]
> Although the total number of hours required per [training method](#choose-a-training-method) varies, the same unit price applies to each. For more information, see the [custom neural training pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

## Choose a training method

# [Foundry (new)](#tab/foundry-new)

On the **Training data** step of **Customize a model**, select one of these training methods:

- **Neural - HD**: Create an HD voice in the same language as your training data. HD voices are LLM-based and optimized for dynamic conversations. For more information, see [High-definition voices](../../../../high-definition-voices.md).
- **Neural - Default**: Create a voice in the same language as your training data.
- **Neural - Multi lingual**: Create a voice that speaks multiple languages from single-language training data.
- **Neural - Multi style**: Create a voice that speaks in multiple styles and emotions.

After you select a method, select a recipe **Version**. The portal evaluates whether your datasets are eligible for that method and version.

# [Foundry (classic)](#tab/foundry-classic)

After you validate your data files, use them to build your custom voice model.
In Foundry (classic), choose one of these training methods:

- [Neural - HD Voice](?tabs=foundry-classic%2Chdvoice#train-your-custom-voice-model): Create an HD voice in the same language of your training data. Azure neural HD voices are LLM-based, optimized for dynamic conversations. Learn more about [high-definition voices](../../../../high-definition-voices.md).

- [Neural](?tabs=foundry-classic%2Cneural#train-your-custom-voice-model): Create a voice in the same language as your training data.

- [Neural - multilingual](?tabs=foundry-classic%2Cmultilingual#train-your-custom-voice-model): Create a voice that speaks multiple languages using the single-language training data. For example, with the `en-US` primary training data, you can create a voice that speaks `en-US`, `de-DE`, `zh-CN` and other secondary languages.

  The primary language of the training data and the secondary languages must be in the [languages that are supported](../../../../language-support.md?tabs=tts#professional-voice) for multilingual voice training. You don't need to prepare training data in the secondary languages.

- [Neural - multi style](?tabs=foundry-classic%2Cmultistyle#train-your-custom-voice-model): Create a custom voice that speaks in multiple styles and emotions, without adding new training data. Multiple style voices are useful for video game characters, conversational chatbots, audiobooks, content readers, and more.

  To create a multiple style voice, you need to prepare a set of general training data, at least 300 utterances. Select one or more of the preset target speaking styles. You can also create multiple custom styles by providing style samples, of at least 100 utterances per style, as extra training data for the same voice. The supported preset styles vary according to different languages. See [available preset styles across different languages](?tabs=foundry-classic%2Cmultistyle#available-preset-styles-across-different-languages).

> [!NOTE]
> Neural - cross lingual retires on August 25, 2026. Voice models that you create by using this retired method aren't affected.

The language of the training data must be one of the [languages that are supported](../../../../language-support.md?tabs=tts) for custom voice or multiple style training.

---

## Train your custom voice model

To create a custom voice in the Microsoft Foundry portal, follow these steps for one of the following methods:

# [Foundry (new)](#tab/foundry-new)

[!INCLUDE [Foundry (new) train](./foundry-new-train.md)]

# [Foundry (classic)](#tab/foundry-classic)

In the Microsoft Foundry (classic) portal, select a training method below and follow the corresponding steps.

[!INCLUDE [Foundry (classic) training methods](./foundry-classic-training-methods.md)]

---

## Monitor the training process

# [Foundry (new)](#tab/foundry-new)

1. [!INCLUDE [foundry-sign-in](../../../../../../foundry/includes/foundry-sign-in.md)]
1. Select **Build** from the upper-right menu.
1. Select **Services** in the left pane.
1. Select the **Customizations** tab to view your Professional Voice customization jobs and their status.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-customizations-status.png" alt-text="Screenshot of a succeeded Professional Voice customization job in the new Foundry portal." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-customizations-status.png":::

1. To stop a model that's still training, select its name, and then select **Cancel training**. You aren't charged for canceled training.
1. After the status changes to **Succeeded**, select the model name to open its **Details** page. The page displays the training and deployment status, task parameters, model attributes, training data, engine version, creation time, and model ID.

### Troubleshoot training

If training fails, review the reported error before starting another job. For data-related errors, [review your dataset's validation results](../../../../professional-voice-create-training-set.md?tabs=foundry-new&pivots=ai-foundry-portal#review-data-issues) and correct the affected recordings or transcripts. If you can't resolve the failure, [contact support](/azure/ai-services/cognitive-services-support-options).

# [Foundry (classic)](#tab/foundry-classic)

The **Train model** table displays a new entry that corresponds to this newly created model. The status reflects the process of converting your data to a voice model, as described in this table:

| State | Meaning |
|:----- |:------- |
| Processing | Your voice model is being created. |
| Succeeded  | Your voice model has been created and can be deployed. |
| Failed     | Your voice model has failed in training. The cause of the failure might be, for example, unseen data problems or network issues. |
| Canceled   | The training for your voice model was canceled. |

While the model status is **Processing**, you can select the model and then select **Cancel training** to cancel training. You're not charged for this canceled training.

:::image type="content" source="../../../../media/custom-voice/professional-voice/training-status-processing.png" alt-text="Screenshot that shows how to cancel training for a model." lightbox="../../../../media/custom-voice/professional-voice/training-status-processing.png":::

After you finish training the model successfully, you can review the model details and [Test your voice model](#test-your-voice-model).

### Rename your model

You have to clone your model to rename it. You can't rename the model directly. 

1. Select the model.
1. Select **Clone model** to create a clone of the model with a new name in the current project.
1. Enter the new name on the **Clone voice model** window.
1. Select **Submit**. The text *Neural* is automatically added as a suffix to your new model name.

### Test your voice model

After your voice model is successfully built, you can use the generated sample audio files to test it before you deploy it.

> [!NOTE]
> [Neural - multilingual](?tabs=foundry-classic%2Cmultilingual#train-your-custom-voice-model) and [Neural - HD Voice](?tabs=foundry-classic%2Chdvoice#train-your-custom-voice-model) don't support this type of testing.

The quality of the voice depends on many factors, such as:

- The size of the training data.
- The quality of the recording.
- The accuracy of the transcript file.
- How well the recorded voice in the training data matches the personality of the designed voice for your intended use case.

Select **DefaultTests** under **Testing** to listen to the sample audio files. The default test samples include 100 sample audio files generated automatically during training to help you test the model. In addition to these 100 audio files provided by default, your own test script utterances are also added to **DefaultTests** set. This addition is at most 100 utterances. You're not charged for the testing with **DefaultTests**.

If you want to upload your own test scripts to further test your model, select **Add test scripts** to upload your own test script.

Before you upload test script, check the [Test script requirements](#test-script-requirements). You're charged for the extra testing with the batch synthesis based on the number of billable characters. See [Azure Speech in Foundry Tools pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

Under **Add test scripts**, select **Browse for a file** to select your own script, then select **Add** to upload it.

### Test script requirements

The test script must be a *.txt* file that is less than 1 MB. Supported encoding formats include ANSI/ASCII, UTF-8, UTF-8-BOM, UTF-16-LE, or UTF-16-BE.

Unlike the [training transcription files](../../../../how-to-custom-voice-training-data.md#transcription-data-for-individual-utterances-and-matching-transcript), the test script should exclude the utterance ID, which is the filename of each utterance. Otherwise, these IDs are spoken.

Here's an example set of utterances in one *.txt* file:

```text
This is the waistline, and it's falling.
We have trouble scoring.
It was Janet Maslin.
```

Each paragraph of the utterance results in a separate audio. If you want to combine all sentences into one audio, make them a single paragraph.

> [!NOTE]
> The generated audio files are a combination of the automatic test scripts and custom test scripts.

---

## Update engine version for your voice model

Azure text to speech engines are updated from time to time to capture the latest language model that defines the pronunciation of the language. After you train your voice, you can apply your voice to the new language model by updating to the latest engine version.

# [Foundry (new)](#tab/foundry-new)

1. Select **Build** > **Services** > **Customizations**.
1. Select the name of the Professional Voice model.
1. When the model details page indicates that a new engine is available, select **Install the latest engine**.
1. In the **Install the latest engine** dialog, select **Confirm**. The update creates a new engine version at no extra cost and keeps the existing versions.

The new engine version becomes the default version. To use another installed version as the default, select the **Engine version** value on the model details page, select the version, and then select **Done**.

:::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-engine-version.png" alt-text="Screenshot of the Engine version dialog in the new Foundry portal." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-engine-version.png":::

# [Foundry (classic)](#tab/foundry-classic)

- When a new engine is available, you're prompted to update your neural voice model.
- Go to the model details page and follow the on-screen instructions to install the latest engine.
- Alternatively, select **Install the latest engine** later to update your model to the latest engine version. You're not charged for engine update. The previous versions are still kept.
- You can check all engine versions for the model from the **Engine version** list, or remove one if you don't need it anymore.

The updated version is automatically set as default. But you can change the default version by selecting a version from the drop-down list and selecting **Set as default**.

If you want to test each engine version of your voice model, you can select a version from the list, then select **DefaultTests** under **Testing** to listen to the sample audio files. If you want to upload your own test scripts to further test your current engine version, first make sure the version is set as default, then follow the steps in [Test your voice model](#test-your-voice-model).

---

Updating the engine creates a new version of the model at no extra cost. After you update the engine version for your voice model, you need to deploy the new version to [create a new endpoint](../../../../professional-voice-deploy-endpoint.md#add-a-deployment-endpoint). You can only deploy the default version.

After you create a new endpoint, you need to [transfer the traffic to the new endpoint in your product](../../../../professional-voice-deploy-endpoint.md#switch-to-a-new-voice-model-in-your-product).

To learn more about the capabilities and limits of this feature, and the best practice to improve your model quality, see [Characteristics and limitations for using custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note).

## Copy your voice model to another project

# [Foundry (new)](#tab/foundry-new)

After training, you can copy your voice model to another Microsoft Foundry project in the same region or another region. For example, you can train a Professional Voice model in a [supported training region](../../../../regions.md?tabs=tts#regions) and copy it to a Foundry resource and project in another region.

1. Select **Build** > **Services** > **Customizations**.
1. Select the row for the model that you want to copy. In the model details pane, select **Copy to**.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-model-actions.png" alt-text="Screenshot of the Customizations model list and model details pane, with the selected model name and Copy to action outlined." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-model-actions.png":::

1. In the **Copy speech model** dialog, select the **Subscription**, **Resource group**, **Target foundry resource**, and **Target foundry project**.

   :::image type="content" source="../../../../media/custom-voice/professional-voice/foundry-new-copy-model.png" alt-text="Screenshot of the Copy speech model dialog in the new Foundry portal." lightbox="../../../../media/custom-voice/professional-voice/foundry-new-copy-model.png":::

1. Select **Copy**. The copied model appears in the target project's **Customizations** list after the copy operation finishes.

# [Foundry (classic)](#tab/foundry-classic)

In Foundry (classic), *project* refers to a fine-tuning task. After training,
you can copy your voice model to another fine-tuning task in the same region or
another region.

1. On the **Train model** tab, select a voice model that you want to copy, and then select **Copy to project**.
1. Select the **Subscription**, **Target region**, **Connected AI Service resource** (Foundry resource), and **Target fine-tuning task** where you want to copy the model. 
1. Select **Copy to** to copy the model.
1. Select **View model** under the notification message for the successful copying.

Navigate to the fine-tuning task where you copied the model to
[deploy the model copy](../../../../professional-voice-deploy-endpoint.md).

---

## Next steps

> [!div class="nextstepaction"]
> [Deploy the professional voice endpoint](../../../../professional-voice-deploy-endpoint.md)
