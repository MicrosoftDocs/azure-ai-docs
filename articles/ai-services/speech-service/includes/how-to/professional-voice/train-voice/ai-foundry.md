---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/19/2025
ms.custom: include
---

In this article, you learn how to fine-tune a professional voice through the Microsoft Foundry portal.

> [!IMPORTANT]
> Professional voice fine-tuning is currently only available in some regions. After your voice model is trained in a supported region, you can [copy the professional voice model](#copy-your-voice-model-to-another-project) to a Microsoft Foundry resource in another region as needed. For more information, see the footnotes in the [Speech service table](../../../../regions.md#regions).

Training duration varies depending on how much data you use. It takes about 10 compute hours on average to fine-tune a professional voice. With a Microsoft Foundry standard (S0) resource, you can train four voices simultaneously. If you reach the limit, wait until at least one of your voice models finishes training, and then try again.

> [!NOTE]
> Although the total number of hours required per [training method](#choose-a-training-method) varies, the same unit price applies to each. For more information, see the [custom neural training pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

## Choose a training method

After you validate your data files, use them to build your custom voice model. When you create a custom voice, you can choose to train it with one of the following methods:

- [Neural](?tabs=neural#train-your-custom-voice-model): Create a voice in the same language as your training data.

- [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model): Create an HD voice in the same language of your training data. Azure neural HD voices are LLM-based, optimized for dynamic conversations. Learn more about neural HD voices [here](../../../../high-definition-voices.md).

- [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model): Create a voice that speaks multiple languages using the single-language training data. For example, with the `en-US` primary training data, you can create a voice that speaks `en-US`, `de-DE`, `zh-CN` etc. secondary languages.

  The primary language of the training data and the secondary languages must be in the [languages that are supported](../../../../language-support.md?tabs=tts#professional-voice) for multilingual voice training. You don't need to prepare training data in the secondary languages.

- [Neural - multi style](?tabs=multistyle#train-your-custom-voice-model): Create a custom voice that speaks in multiple styles and emotions, without adding new training data. Multiple style voices are useful for video game characters, conversational chatbots, audiobooks, content readers, and more.

  To create a multiple style voice, you need to prepare a set of general training data, at least 300 utterances. Select one or more of the preset target speaking styles. You can also create multiple custom styles by providing style samples, of at least 100 utterances per style, as extra training data for the same voice. The supported preset styles vary according to different languages. See [available preset styles across different languages](?tabs=multistyle#available-preset-styles-across-different-languages).

- [Neural - cross lingual](?tabs=crosslingual#train-your-custom-voice-model): Create a voice that speaks a different language from your training data. For example, with the `zh-CN` training data, you can create a voice that speaks `en-US`.

  The language of the training data and the target language must both be one of the [languages that are supported](../../../../language-support.md?tabs=tts#professional-voice) for cross lingual voice training. You don't need to prepare training data in the target language, but your test script must be in the target language.

The language of the training data must be one of the [languages that are supported](../../../../language-support.md?tabs=tts) for custom voice, cross-lingual, or multiple style training.

## Train your custom voice model

To create a custom voice in Microsoft Foundry portal, follow these steps for one of the following methods:

# [Neural](#tab/neural)

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Train model** > **+ Train model**. 
1. Select **Neural** as the [training method](#choose-a-training-method) for your model. To use a different training method, see [Neural - cross lingual](?tabs=crosslingual#train-your-custom-voice-model), [Neural - multi style](?tabs=multistyle#train-your-custom-voice-model), [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model), or [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model).

   :::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-train-neural.png" alt-text="Screenshot that shows how to select neural training." lightbox="../../../../media/custom-voice/professional-voice/cnv-train-neural.png":::

1. Select a version of the training recipe for your model. The latest version is selected by default. The supported features and training time can vary by version. Normally, we recommend the latest version. In some cases, you can choose an earlier version to reduce training time. See [Bilingual training](#bilingual-training) for more information about bilingual training and differences between locales.
   
1. Select **Next**.
1. Select the data that you want to use for training. Duplicate audio names are removed from the training. Make sure that the data you select doesn't contain the same audio names across multiple *.zip* files.

   You can select only successfully processed datasets for training. If you don't see your training set in the list, check your data processing status.

1. Select a speaker file with the voice talent statement that corresponds to the speaker in your training data.
1. Select **Next**.
1. Select a test script and then select **Next**. 
    - Each training generates 100 sample audio files automatically to help you test the model with a default script.
    - Alternatively, you can select **Add my own test script** and provide your own test script with up to 100 utterances to test the model at no extra cost. The generated audio files are a combination of the automatic test scripts and custom test scripts. For more information, see [test script requirements](#test-script-requirements).

1. Enter a **Voice model name**. Choose a name carefully. The model name is used as the voice name in your [speech synthesis request](../../../../professional-voice-deploy-endpoint.md#use-your-custom-voice) by the SDK and SSML input. Only letters, numbers, and a few punctuation characters are allowed. Use different names for different neural voice models.
1. Optionally, enter the **Description** to help you identify the model. A common use of the description is to record the names of the data that you used to create the model.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the terms of use.
1. Select **Train** to start training the model.

### Bilingual training

[!INCLUDE [Bilingual training](./bilingual-training.md)]

# [Neural - HD Voice](#tab/hdvoice)

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Train model** > **+ Train model**. 
1. Select **Neural - HD** as the [training method](#choose-a-training-method) for your model. To use a different training method, see [Neural](?tabs=neural#train-your-custom-voice-model), [Neural - cross lingual](?tabs=crosslingual#train-your-custom-voice-model), [Neural - multi style](?tabs=multistyle#train-your-custom-voice-model), or [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model).

   :::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-train-neural-hd-voice.png" alt-text="Screenshot that shows how to select neural HD training." lightbox="../../../../media/custom-voice/professional-voice/cnv-train-neural-hd-voice.png":::

1. Select a version of the training recipe for your model. The latest version is selected by default. The supported features and training time can vary by version. Normally, we recommend the latest version. In some cases, you can choose an earlier version to reduce training time.
1. Select the data that you want to use for training. Duplicate audio names are removed from the training. Make sure that the data you select doesn't contain the same audio names across multiple *.zip* files.

   You can select only successfully processed datasets for training. Check your data processing status if you don't see your training set in the list.

1. Select a speaker file with the voice talent statement that corresponds to the speaker in your training data.
1. Select **Next**.
1. Select a test script and then select **Next**. 
    - Each training generates 100 sample audio files automatically to help you test the model with a default script.
    - Alternatively, you can select **Add my own test script** and provide your own test script with up to 100 utterances to test the model at no extra cost. The generated audio files are a combination of the automatic test scripts and custom test scripts. For more information, see [test script requirements](#test-script-requirements).

1. Enter a **Voice model name**. Choose a name carefully. The model name is used as the voice name in your [speech synthesis request](../../../../professional-voice-deploy-endpoint.md#use-your-custom-voice) by the SDK and SSML input. Only letters, numbers, and a few punctuation characters are allowed. Use different names for different neural voice models.
1. Optionally, enter the **Description** to help you identify the model. A common use of the description is to record the names of the data that you used to create the model.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the terms of use.
1. Select **Train** to start training the model.

# [Neural - multilingual](#tab/multilingual)

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Train model** > **+ Train model**. 
1. Select **Neural - multilingual** as the [training method](#choose-a-training-method) for your model. To use a different training method, see [Neural](?tabs=neural#train-your-custom-voice-model), [Neural - cross lingual](?tabs=crosslingual#train-your-custom-voice-model), [Neural - multi style](?tabs=multistyle#train-your-custom-voice-model), or [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model).

   :::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-train-neural-multi-lingual.png" alt-text="Screenshot that shows how to select neural multilingual training." lightbox="../../../../media/custom-voice/professional-voice/cnv-train-neural-multi-lingual.png":::

1. Select a version of the training recipe for your model. The latest version is selected by default. The supported features and training time can vary by version. Normally, we recommend the latest version. In some cases, you can choose an earlier version to reduce training time.
1. Select the **Additional language** that your voice speaks. You can select one or more secondary languages for a voice model and the voice speaks languages you selected from training data.
1. Select the data that you want to use for training. Duplicate audio names are removed from the training. Make sure that the data you select doesn't contain the same audio names across multiple *.zip* files.

   You can select only successfully processed datasets for training. Check your data processing status if you don't see your training set in the list.

1. Select a speaker file with the voice talent statement that corresponds to the speaker in your training data.
1. Select **Next**.
1. Select a test script and then select **Next**. 
    - Each training generates 100 sample audio files automatically to help you test the model with a default script.
    - Alternatively, you can select **Add my own test script** and provide your own test script with up to 100 utterances to test the model at no extra cost. The generated audio files are a combination of the automatic test scripts and custom test scripts. For more information, see [test script requirements](#test-script-requirements).

1. Enter a **Voice model name**. Choose a name carefully. The model name is used as the voice name in your [speech synthesis request](../../../../professional-voice-deploy-endpoint.md#use-your-custom-voice) by the SDK and SSML input. Only letters, numbers, and a few punctuation characters are allowed. Use different names for different neural voice models.
1. Optionally, enter the **Description** to help you identify the model. A common use of the description is to record the names of the data that you used to create the model.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the terms of use.
1. Select **Train** to start training the model.

# [Neural - multi style](#tab/multistyle)

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Train model** > **+ Train model**. 
1. Select **Neural - multi style** as the [training method](#choose-a-training-method) for your model. To use a different training method, see [Neural](?tabs=neural#train-your-custom-voice-model), [Neural - cross lingual](?tabs=crosslingual#train-your-custom-voice-model), [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model), or [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model).

   :::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-train-neural-multi-style.png" alt-text="Screenshot that shows how to select neural multi style training." lightbox="../../../../media/custom-voice/professional-voice/cnv-train-neural-multi-style.png":::

1. Select a version of the training recipe for your model. The latest version is selected by default. The supported features and training time can vary by version. Normally, we recommend the latest version. In some cases, you can choose an earlier version to reduce training time.
1. Select **Next**.
1. Select one or more preset speaking styles to train.
1. Select the data that you want to use for training. Duplicate audio names are removed from the training. Make sure that the data you select doesn't contain the same audio names across multiple *.zip* files.

   You can select only successfully processed datasets for training. Check your data processing status if you don't see your training set in the list.

1. Select **Next**.

1. Optionally, you can add other custom speaking styles. The maximum number of custom styles varies by languages: `English (United States)` allows up to 10 custom styles, `Chinese (Mandarin, Simplified)` allows up to four custom styles, and `Japanese (Japan)` allows up to five custom styles.

   1. Select **+ Add a custom style** and enter a custom style name of your choice. This name is used by your application within the `style` element of [Speech Synthesis Markup Language (SSML)](../../../../speech-synthesis-markup-voice.md#use-speaking-styles-and-roles). 
   1. Select style samples as training data. Ensure that the training data for custom speaking styles comes from the same speaker as the data used to create the default style.

1. Select **Next**.
1. Select a speaker file with the voice talent statement that corresponds to the speaker in your training data.
1. Select **Next**.
1. Select a test script and then select **Next**. 
    - Each training generates 100 sample audio files automatically to help you test the model with a default script.
    - Alternatively, you can select **Add my own test script** and provide your own test script with up to 100 utterances to test the model at no extra cost. The generated audio files are a combination of the automatic test scripts and custom test scripts. For more information, see [test script requirements](#test-script-requirements).

1. Enter a **Voice model name**. Choose a name carefully. The model name is used as the voice name in your [speech synthesis request](../../../../professional-voice-deploy-endpoint.md#use-your-custom-voice) by the SDK and SSML input. Only letters, numbers, and a few punctuation characters are allowed. Use different names for different neural voice models.
1. Optionally, enter the **Description** to help you identify the model. A common use of the description is to record the names of the data that you used to create the model.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the terms of use.
1. Select **Train** to start training the model.

### Available preset styles across different languages

The following table summarizes the different preset styles according to different languages.

[!INCLUDE [Speaking styles](./voice-styles-by-locale.md)]

# [Neural - cross lingual](#tab/crosslingual)

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Train model** > **+ Train model**. 
1. Select **Neural - Cross lingual** as the [training method](#choose-a-training-method) for your model. To use a different training method, see [Neural](?tabs=neural#train-your-custom-voice-model), [Neural - multi style](?tabs=multistyle#train-your-custom-voice-model), [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model), or [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model).

   :::image type="content" source="../../../../media/custom-voice/professional-voice/cnv-train-neural-cross-lingual.png" alt-text="Screenshot that shows how to select neural cross lingual training." lightbox="../../../../media/custom-voice/professional-voice/cnv-train-neural-cross-lingual.png":::

1. Select a version of the training recipe for your model. The latest version is selected by default. The supported features and training time can vary by version. Normally, we recommend the latest version. In some cases, you can choose an earlier version to reduce training time.
1. Select the **Primary target language** that your voice speaks. The voice speaks a different language from your training data. You can select only one target language for a voice model.
1. Select **Next**.
1. Select the data that you want to use for training. Duplicate audio names are removed from the training. Make sure that the data you select doesn't contain the same audio names across multiple *.zip* files.

   You can select only successfully processed datasets for training. Check your data processing status if you don't see your training set in the list.

1. Select a speaker file with the voice talent statement that corresponds to the speaker in your training data.
1. Select **Next**.
1. Select a test script and then select **Next**. 
    - Each training generates 100 sample audio files automatically to help you test the model with a default script.
    - Alternatively, you can select **Add my own test script** and provide your own test script with up to 100 utterances to test the model at no extra cost. The generated audio files are a combination of the automatic test scripts and custom test scripts. For more information, see [test script requirements](#test-script-requirements).

1. Enter a **Voice model name**. Choose a name carefully. The model name is used as the voice name in your [speech synthesis request](../../../../professional-voice-deploy-endpoint.md#use-your-custom-voice) by the SDK and SSML input. Only letters, numbers, and a few punctuation characters are allowed. Use different names for different neural voice models.
1. Optionally, enter the **Description** to help you identify the model. A common use of the description is to record the names of the data that you used to create the model.
1. Select the checkbox to accept the terms of use and then select **Next**.
1. Review the settings and select the box to accept the terms of use.
1. Select **Train** to start training the model.

---

## Monitor the training process

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

## Rename your model

You have to clone your model to rename it. You can't rename the model directly. 

1. Select the model.
1. Select **Clone model** to create a clone of the model with a new name in the current project.
1. Enter the new name on the **Clone voice model** window.
1. Select **Submit**. The text *Neural* is automatically added as a suffix to your new model name.

## Test your voice model

After your voice model is successfully built, you can use the generated sample audio files to test it before you deploy it.

> [!NOTE]
> [Neural - multilingual](?tabs=multilingual#train-your-custom-voice-model) and [Neural - HD Voice](?tabs=hdvoice#train-your-custom-voice-model) do not support this type of testing.

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

Unlike the [training transcription files](../../../../how-to-custom-voice-training-data.md#transcription-data-for-individual-utterances--matching-transcript), the test script should exclude the utterance ID, which is the filename of each utterance. Otherwise, these IDs are spoken.

Here's an example set of utterances in one *.txt* file:

```text
This is the waistline, and it's falling.
We have trouble scoring.
It was Janet Maslin.
```

Each paragraph of the utterance results in a separate audio. If you want to combine all sentences into one audio, make them a single paragraph.

> [!NOTE]
> The generated audio files are a combination of the automatic test scripts and custom test scripts.

### Update engine version for your voice model

Azure text to speech engines are updated from time to time to capture the latest language model that defines the pronunciation of the language. After you train your voice, you can apply your voice to the new language model by updating to the latest engine version.

- When a new engine is available, you're prompted to update your neural voice model.
- Go to the model details page and follow the on-screen instructions to install the latest engine.
- Alternatively, select **Install the latest engine** later to update your model to the latest engine version. You're not charged for engine update. The previous versions are still kept.
- You can check all engine versions for the model from the **Engine version** list, or remove one if you don't need it anymore.

The updated version is automatically set as default. But you can change the default version by selecting a version from the drop-down list and selecting **Set as default**.

If you want to test each engine version of your voice model, you can select a version from the list, then select **DefaultTests** under **Testing** to listen to the sample audio files. If you want to upload your own test scripts to further test your current engine version, first make sure the version is set as default, then follow the steps in [Test your voice model](#test-your-voice-model).

Updating the engine creates a new version of the model at no extra cost. After you update the engine version for your voice model, you need to deploy the new version to [create a new endpoint](../../../../professional-voice-deploy-endpoint.md#add-a-deployment-endpoint). You can only deploy the default version.

After you create a new endpoint, you need to [transfer the traffic to the new endpoint in your product](../../../../professional-voice-deploy-endpoint.md#switch-to-a-new-voice-model-in-your-product).

To learn more about the capabilities and limits of this feature, and the best practice to improve your model quality, see [Characteristics and limitations for using custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note).

## Copy your voice model to another project

> [!NOTE]
> In this context "project" refers to a fine-tuning task rather than a Microsoft Foundry project. 

After training you can copy your voice model to another project for the same region or another region. 

For example, you can copy a professional voice model that was trained in one region, to a project for another region. Professional voice fine-tuning is currently only [available in some regions](../../../../regions.md#regions). 

To copy your custom voice model to another project:

1. On the **Train model** tab, select a voice model that you want to copy, and then select **Copy to project**.
1. Select the **Subscription**, **Target region**, **Connected AI Service resource** (Foundry resource), and **Target fine-tuning task** where you want to copy the model. 
1. Select **Copy to** to copy the model.
1. Select **View model** under the notification message for the successful copying.

Navigate to the project where you copied the model to [deploy the model copy](../../../../professional-voice-deploy-endpoint.md).

## Next steps

> [!div class="nextstepaction"]
> [Deploy the professional voice endpoint](../../../../professional-voice-deploy-endpoint.md)

