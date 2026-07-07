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

   1. Select **+ Add a custom style** and enter a custom style name of your choice. This name is used by your application within the `style` element of [Speech Synthesis Markup Language (SSML)](../../../../speech-synthesis-markup-voice.md#use-speaking-styles-paralinguistics-and-roles). 
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
