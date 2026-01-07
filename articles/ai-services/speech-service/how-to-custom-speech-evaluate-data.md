---
title: Test accuracy of a custom speech model - Speech service
titleSuffix: Foundry Tools
description: In this article, you learn how to quantitatively measure and improve the quality of our speech to text model or your custom model.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/19/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio-cli-rest
show_latex: true
no-loc: [$$, '\times', '\over']
#Customer intent: As a developer, I want to test the accuracy of a custom speech model so that I can evaluate whether it meets my requirements.
---

# Test accuracy of a custom speech model

This article shows you how to quantitatively measure and improve the accuracy of the base speech to text model or your own custom models. To test accuracy, you need [audio and human-labeled transcript data](how-to-custom-speech-test-and-train.md#audio--human-labeled-transcript-data-for-training-or-testing). Provide 30 minutes to 5 hours of representative audio. 

[!INCLUDE [service-pricing-advisory](includes/service-pricing-advisory.md)]

## Create a test

> [!TIP]
> Bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry portal, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).

You can test the accuracy of your custom model by creating a test. A test requires a collection of audio files and their corresponding transcriptions. You can compare a custom model's accuracy with a speech to text base model or another custom model. After you [get](#get-test-results) the test results, [evaluate the word error rate (WER)](#evaluate-word-error-rate-wer) compared to speech recognition results.

After you [upload training and testing datasets](how-to-custom-speech-upload-data.md), you can create a test.

::: zone pivot="ai-foundry-portal"

To test your fine-tuned custom speech model, follow these steps:

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the custom speech fine-tuning task (by model name) that you [started as described in the how to start custom speech fine-tuning article](./how-to-custom-speech-create-project.md).
1. Select **Test models** > **+ Create test**. 

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-test-model.png" alt-text="Screenshot of the page with an option to test your custom speech model." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-test-model.png":::

1. In the **Create a new test** wizard, select the test type. For an accuracy (quantitative) test, select **Evaluate accuracy (Audio + transcript data)**. Then select **Next**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-test-model-select-type.png" alt-text="Screenshot of the page with an option to select the test type." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-test-model-select-type.png":::

1. Select the data that you want to use for testing. Then select **Next**.
1. Select up to two models to evaluate and compare accuracy. In this example, select the model that you trained and the base model. Then select **Next**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-test-model-select-models.png" alt-text="Screenshot of the page with an option to select up to two models to evaluate and compare accuracy." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-test-model-select-models.png":::

1. Enter a name and description for the test. Then select **Next**.
1. Review the settings and select **Create test**. You're taken back to the **Test models** page. The status of the data is **Processing**.

    :::image type="content" source="./media/custom-speech/ai-foundry/new-fine-tune-test-model-status-processing.png" alt-text="Screenshot of the page that shows the status of the test as processing." lightbox="./media/custom-speech/ai-foundry/new-fine-tune-test-model-status-processing.png":::

::: zone-end

::: zone pivot="speech-studio"

Follow these steps to create an accuracy test:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Test models**.
1. Select **Create new test**.
1. Select **Evaluate accuracy** > **Next**. 
1. Select one audio + human-labeled transcription dataset, and then select **Next**. If there aren't any datasets available, cancel the setup, and then go to the **Speech datasets** menu to [upload datasets](how-to-custom-speech-upload-data.md).
    
    > [!NOTE]
    > It's important to select an acoustic dataset that's different from the one you used with your model. This approach can provide a more realistic sense of the model's performance.

1. Select up to two models to evaluate, and then select **Next**.
1. Enter the test name and description, and then select **Next**.
1. Review the test details, and then select **Save and close**.

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To create a test, use the `spx csr evaluation create` command. Construct the request parameters according to the following instructions:

- Set the `project` property to the ID of an existing project. The `project` property is recommended so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the required `model1` property to the ID of a model that you want to test.
- Set the required `model2` property to the ID of another model that you want to test. If you don't want to compare two models, use the same model for both `model1` and `model2`.
- Set the required `dataset` property to the ID of a dataset that you want to use for the test.
- Set the `language` property, otherwise the Speech CLI sets "en-US" by default. This parameter should be the locale of the dataset contents. The locale can't be changed later. The Speech CLI `language` property corresponds to the `locale` property in the JSON request and response.
- Set the required `name` property. This parameter is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). The Speech CLI `name` property corresponds to the `displayName` property in the JSON request and response.

Here's an example Speech CLI command that creates a test:

```azurecli-interactive
spx csr evaluation create --api-version v3.2 --project aaaabbbb-0000-cccc-1111-dddd2222eeee --dataset bbbbcccc-1111-dddd-2222-eeee3333ffff --model1 ccccdddd-2222-eeee-3333-ffff4444aaaa --model2 ddddeeee-3333-ffff-4444-aaaa5555bbbb --name "My Evaluation" --description "My Evaluation Description"
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/eeeeffff-4444-aaaa-5555-bbbb6666cccc",
  "model1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "model2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "dataset": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "transcription2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "transcription1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/dda6e880-6ccd-49dc-b277-137565cbaa38/files"
  },
  "properties": {
    "wordErrorRate1": -1.0,
    "sentenceErrorRate1": -1.0,
    "sentenceCount1": -1,
    "wordCount1": -1,
    "correctWordCount1": -1,
    "wordSubstitutionCount1": -1,
    "wordDeletionCount1": -1,
    "wordInsertionCount1": -1,
    "wordErrorRate2": -1.0,
    "sentenceErrorRate2": -1.0,
    "sentenceCount2": -1,
    "wordCount2": -1,
    "correctWordCount2": -1,
    "wordSubstitutionCount2": -1,
    "wordDeletionCount2": -1,
    "wordInsertionCount2": -1
  },
  "lastActionDateTime": "2024-07-14T21:31:14Z",
  "status": "NotStarted",
  "createdDateTime": "2024-07-14T21:31:14Z",
  "locale": "en-US",
  "displayName": "My Evaluation",
  "description": "My Evaluation Description",
  "customProperties": {
    "testingKind": "Evaluation"
  }
}
```

The top-level `self` property in the response body is the evaluation's URI. Use this URI to get details about the project and test results. You also use this URI to update or delete the evaluation.

For Speech CLI help with evaluations, run the following command:

```azurecli-interactive
spx help csr evaluation
```

::: zone-end

::: zone pivot="rest-api"

To create a test, use the [Evaluations_Create](/rest/api/speechtotext/evaluations/create) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the `project` property to the ID of an existing project. The `project` property is recommended so that you can also manage fine-tuning for custom speech in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). To get the project ID, see [Get the project ID for the REST API](./how-to-custom-speech-create-project.md#get-the-project-id-for-the-rest-api) documentation.
- Set the `testingKind` property to `Evaluation` within `customProperties`. If you don't specify `Evaluation`, the test is treated as a quality inspection test. Whether the `testingKind` property is set to `Evaluation` or `Inspection`, or not set, you can access the accuracy scores via the API, but not in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
- Set the required `model1` property to the URI of a model that you want to test.
- Set the required `model2` property to the URI of another model that you want to test. If you don't want to compare two models, use the same model for both `model1` and `model2`.
- Set the required `dataset` property to the URI of a dataset that you want to use for the test.
- Set the required `locale` property. This property should be the locale of the dataset contents. The locale can't be changed later.
- Set the required `displayName` property. This property is the name that is displayed in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

Make an HTTP POST request using the URI as shown in the following example. Replace `YourSpeechResoureKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "model1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "model2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "dataset": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "displayName": "My Evaluation",
  "description": "My Evaluation Description",
  "customProperties": {
    "testingKind": "Evaluation"
  },
  "locale": "en-US"
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations"
```

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/eeeeffff-4444-aaaa-5555-bbbb6666cccc",
  "model1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "model2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "dataset": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "transcription2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "transcription1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/dda6e880-6ccd-49dc-b277-137565cbaa38/files"
  },
  "properties": {
    "wordErrorRate1": -1.0,
    "sentenceErrorRate1": -1.0,
    "sentenceCount1": -1,
    "wordCount1": -1,
    "correctWordCount1": -1,
    "wordSubstitutionCount1": -1,
    "wordDeletionCount1": -1,
    "wordInsertionCount1": -1,
    "wordErrorRate2": -1.0,
    "sentenceErrorRate2": -1.0,
    "sentenceCount2": -1,
    "wordCount2": -1,
    "correctWordCount2": -1,
    "wordSubstitutionCount2": -1,
    "wordDeletionCount2": -1,
    "wordInsertionCount2": -1
  },
  "lastActionDateTime": "2024-07-14T21:31:14Z",
  "status": "NotStarted",
  "createdDateTime": "2024-07-14T21:31:14Z",
  "locale": "en-US",
  "displayName": "My Evaluation",
  "description": "My Evaluation Description",
  "customProperties": {
    "testingKind": "Evaluation"
  }
}
```

The top-level `self` property in the response body is the evaluation's URI. Use this URI to [get](/rest/api/speechtotext/evaluations/get) details about the evaluation's project and test results. You also use this URI to [update](/rest/api/speechtotext/evaluations/update) or [delete](/rest/api/speechtotext/evaluations/delete) the evaluation.

::: zone-end

## Get test results

Get the test results and [evaluate](#evaluate-word-error-rate-wer) the word error rate (WER) compared to speech recognition results.

::: zone pivot="ai-foundry-portal"

When the test status is **Succeeded**, you can view the results. Select the test to view the results.

::: zone-end

::: zone pivot="speech-studio"

Follow these steps to get test results:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select **Custom speech** > Your project name > **Test models**.
1. Select the link by test name.
1. After the test completes, as indicated by the status set to *Succeeded*, you see results that include the WER number for each tested model.

This page lists all the utterances in your dataset and the recognition results, alongside the transcription from the submitted dataset. You can toggle various error types, including insertion, deletion, and substitution. By listening to the audio and comparing recognition results in each column, you can decide which model meets your needs and determine where more training and improvements are required.

::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To get test results, use the `spx csr evaluation status` command. Construct the request parameters according to the following instructions:

- Set the required `evaluation` property to the ID of the evaluation that you want to get test results.

Here's an example Speech CLI command that gets test results:

```azurecli-interactive
spx csr evaluation status --api-version v3.2 --evaluation aaaabbbb-6666-cccc-7777-dddd8888eeee
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

The word error rates and more details are returned in the response body.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/eeeeffff-4444-aaaa-5555-bbbb6666cccc",
  "model1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "model2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "dataset": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "transcription2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "transcription1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/dda6e880-6ccd-49dc-b277-137565cbaa38/files"
  },
  "properties": {
    "wordErrorRate1": 0.028900000000000002,
    "sentenceErrorRate1": 0.667,
    "tokenErrorRate1": 0.12119999999999999,
    "sentenceCount1": 3,
    "wordCount1": 173,
    "correctWordCount1": 170,
    "wordSubstitutionCount1": 2,
    "wordDeletionCount1": 1,
    "wordInsertionCount1": 2,
    "tokenCount1": 165,
    "correctTokenCount1": 145,
    "tokenSubstitutionCount1": 10,
    "tokenDeletionCount1": 1,
    "tokenInsertionCount1": 9,
    "tokenErrors1": {
      "punctuation": {
        "numberOfEdits": 4,
        "percentageOfAllEdits": 20.0
      },
      "capitalization": {
        "numberOfEdits": 2,
        "percentageOfAllEdits": 10.0
      },
      "inverseTextNormalization": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      },
      "lexical": {
        "numberOfEdits": 12,
        "percentageOfAllEdits": 12.0
      },
      "others": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      }
    },
    "wordErrorRate2": 0.028900000000000002,
    "sentenceErrorRate2": 0.667,
    "tokenErrorRate2": 0.12119999999999999,
    "sentenceCount2": 3,
    "wordCount2": 173,
    "correctWordCount2": 170,
    "wordSubstitutionCount2": 2,
    "wordDeletionCount2": 1,
    "wordInsertionCount2": 2,
    "tokenCount2": 165,
    "correctTokenCount2": 145,
    "tokenSubstitutionCount2": 10,
    "tokenDeletionCount2": 1,
    "tokenInsertionCount2": 9,
    "tokenErrors2": {
      "punctuation": {
        "numberOfEdits": 4,
        "percentageOfAllEdits": 20.0
      },
      "capitalization": {
        "numberOfEdits": 2,
        "percentageOfAllEdits": 10.0
      },
      "inverseTextNormalization": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      },
      "lexical": {
        "numberOfEdits": 12,
        "percentageOfAllEdits": 12.0
      },
      "others": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      }
    }
  },
  "lastActionDateTime": "2024-07-14T21:31:22Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-14T21:31:14Z",
  "locale": "en-US",
  "displayName": "My Evaluation",
  "description": "My Evaluation Description",
  "customProperties": {
    "testingKind": "Evaluation"
  }
}
```

For Speech CLI help with evaluations, run the following command:

```azurecli-interactive
spx help csr evaluation
```

::: zone-end

::: zone pivot="rest-api"

To get test results, start by using the [Evaluations_Get](/rest/api/speechtotext/evaluations/get) operation of the [Speech to text REST API](rest-speech-to-text.md).

Make an HTTP GET request using the URI as shown in the following example. Replace `YourEvaluationId` with your evaluation ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/YourEvaluationId" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

The word error rates and more details are returned in the response body.

You receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/eeeeffff-4444-aaaa-5555-bbbb6666cccc",
  "model1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "model2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
  },
  "dataset": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/datasets/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "transcription2": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "transcription1": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/ffffaaaa-5555-bbbb-6666-cccc7777dddd"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/aaaabbbb-0000-cccc-1111-dddd2222eeee"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/evaluations/dda6e880-6ccd-49dc-b277-137565cbaa38/files"
  },
  "properties": {
    "wordErrorRate1": 0.028900000000000002,
    "sentenceErrorRate1": 0.667,
    "tokenErrorRate1": 0.12119999999999999,
    "sentenceCount1": 3,
    "wordCount1": 173,
    "correctWordCount1": 170,
    "wordSubstitutionCount1": 2,
    "wordDeletionCount1": 1,
    "wordInsertionCount1": 2,
    "tokenCount1": 165,
    "correctTokenCount1": 145,
    "tokenSubstitutionCount1": 10,
    "tokenDeletionCount1": 1,
    "tokenInsertionCount1": 9,
    "tokenErrors1": {
      "punctuation": {
        "numberOfEdits": 4,
        "percentageOfAllEdits": 20.0
      },
      "capitalization": {
        "numberOfEdits": 2,
        "percentageOfAllEdits": 10.0
      },
      "inverseTextNormalization": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      },
      "lexical": {
        "numberOfEdits": 12,
        "percentageOfAllEdits": 12.0
      },
      "others": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      }
    },
    "wordErrorRate2": 0.028900000000000002,
    "sentenceErrorRate2": 0.667,
    "tokenErrorRate2": 0.12119999999999999,
    "sentenceCount2": 3,
    "wordCount2": 173,
    "correctWordCount2": 170,
    "wordSubstitutionCount2": 2,
    "wordDeletionCount2": 1,
    "wordInsertionCount2": 2,
    "tokenCount2": 165,
    "correctTokenCount2": 145,
    "tokenSubstitutionCount2": 10,
    "tokenDeletionCount2": 1,
    "tokenInsertionCount2": 9,
    "tokenErrors2": {
      "punctuation": {
        "numberOfEdits": 4,
        "percentageOfAllEdits": 20.0
      },
      "capitalization": {
        "numberOfEdits": 2,
        "percentageOfAllEdits": 10.0
      },
      "inverseTextNormalization": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      },
      "lexical": {
        "numberOfEdits": 12,
        "percentageOfAllEdits": 12.0
      },
      "others": {
        "numberOfEdits": 1,
        "percentageOfAllEdits": 5.0
      }
    }
  },
  "lastActionDateTime": "2024-07-14T21:31:22Z",
  "status": "Succeeded",
  "createdDateTime": "2024-07-14T21:31:14Z",
  "locale": "en-US",
  "displayName": "My Evaluation",
  "description": "My Evaluation Description",
  "customProperties": {
    "testingKind": "Evaluation"
  }
}
```

::: zone-end


## Evaluate word error rate (WER)

The industry standard for measuring model accuracy is [word error rate (WER)](https://en.wikipedia.org/wiki/Word_error_rate). WER counts the number of incorrect words identified during recognition, and divides the sum by the total number of words provided in the human-labeled transcript (N). 

Incorrectly identified words fall into three categories:

* Insertion (I): Words that are incorrectly added in the hypothesis transcript
* Deletion (D): Words that are undetected in the hypothesis transcript
* Substitution (S): Words that were substituted between reference and hypothesis

In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) and [Speech Studio](https://speech.microsoft.com), the quotient is multiplied by 100 and shown as a percentage. The Speech CLI and REST API results aren't multiplied by 100.

$$
WER = {{I+D+S}\over N} \times 100
$$

Here's an example that shows incorrectly identified words, when compared to the human-labeled transcript:

![Screenshot showing an example of incorrectly identified words.](./media/custom-speech/custom-speech-dis-words.png)

The speech recognition result erred as follows:
* Insertion (I): Added the word "a" 
* Deletion (D): Deleted the word "are"
* Substitution (S): Substituted the word "Jones" for "John"

The word error rate from the previous example is 60%. 

If you want to replicate WER measurements locally, you can use the sclite tool from the [NIST Scoring Toolkit (SCTK)](https://github.com/usnistgov/SCTK).

## Resolve errors and improve WER

You can use the WER calculation from the machine recognition results to evaluate the quality of the model you're using with your app, tool, or product. A WER of 5-10% is considered good quality and is ready to use. A WER of 20% is acceptable, but you might want to consider more training. A WER of 30% or more signals poor quality and requires customization and training.

How the errors are distributed is important. When you encounter many deletion errors, it's usually because of weak audio signal strength. To resolve this problem, collect audio data closer to the source. Insertion errors mean that the audio was recorded in a noisy environment and crosstalk might be present, causing recognition problems. Substitution errors often occur when an insufficient sample of domain-specific terms is provided as either human-labeled transcriptions or related text.

By analyzing individual files, you can determine what type of errors exist and which errors are unique to a specific file. Understanding problems at the file level helps you target improvements.

## Evaluate token error rate (TER)

Besides [word error rate](#evaluate-word-error-rate-wer), you can also use the extended measurement of **Token Error Rate (TER)** to evaluate quality on the final end-to-end display format. In addition to the lexical format (`That will cost $900.` instead of `that will cost nine hundred dollars`), TER takes into account the display format aspects such as punctuation, capitalization, and ITN. For more information, see [Display output formatting with speech to text](display-text-format.md). 

TER counts the number of incorrect tokens identified during recognition, and divides the sum by the total number of tokens provided in the human-labeled transcript (N).

$$
TER = {{I+D+S}\over N} \times 100
$$

The formula for TER calculation is also similar to WER. The only difference is that TER is calculated based on the token level instead of word level.
* Insertion (I): Tokens that are incorrectly added in the hypothesis transcript
* Deletion (D): Tokens that are undetected in the hypothesis transcript
* Substitution (S): Tokens that were substituted between reference and hypothesis

In a real-world case, you can analyze both WER and TER results to get the desired improvements. 

> [!NOTE]
> To measure TER, make sure the [audio + transcript testing data](./how-to-custom-speech-test-and-train.md#audio--human-labeled-transcript-data-for-training-or-testing) includes transcripts with display formatting such as punctuation, capitalization, and ITN.

## Example scenario outcomes

Speech recognition scenarios vary by audio quality and language (vocabulary and speaking style). The following table examines four common scenarios:

| Scenario | Audio quality | Vocabulary | Speaking style |
|----------|---------------|------------|----------------|
| Call center | Low, 8&nbsp;kHz, could be two people on one audio channel, could be compressed | Narrow, unique to domain and products | Conversational, loosely structured |
| Voice assistant, such as Cortana, or a drive-through window | High, 16&nbsp;kHz | Entity-heavy (song titles, products, locations) | Clearly stated words and phrases |
| Dictation (instant message, notes, search) | High, 16&nbsp;kHz | Varied | Note-taking |
| Video closed captioning | Varied, including varied microphone use, added music | Varied, from meetings, recited speech, musical lyrics | Read, prepared, or loosely structured |

Different scenarios produce different quality outcomes. The following table examines how content from these four scenarios rates in the [WER](how-to-custom-speech-evaluate-data.md). The table shows which error types are most common in each scenario. The insertion, substitution, and deletion error rates help you determine what kind of data to add to improve the model.

| Scenario | Speech recognition quality | Insertion errors | Deletion errors | Substitution errors |
|--- |--- |--- |--- |--- |
| Call center | Medium<br>(<&nbsp;30%&nbsp;WER) | Low, except when other people talk in the background | Can be high. Call centers can be noisy, and overlapping speakers can confuse the model | Medium. Products and people's names can cause these errors |
| Voice assistant | High<br>(can be <&nbsp;10%&nbsp;WER) | Low | Low | Medium, due to song titles, product names, or locations |
| Dictation | High<br>(can be <&nbsp;10%&nbsp;WER) | Low | Low | High |
| Video closed captioning | Depends on video type (can be <&nbsp;50%&nbsp;WER) | Low | Can be high because of music, noises, microphone quality | Jargon might cause these errors |


## Next steps

* [Train a model](how-to-custom-speech-train-model.md)
* [Deploy a model](how-to-custom-speech-deploy-model.md)
