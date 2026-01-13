---
title: Model lifecycle of custom speech - Speech service
titleSuffix: Foundry Tools
description: Custom speech provides base models for training and lets you create custom models from your data. This article describes the timelines for models and for endpoints that use these models.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/29/2025
ms.reviewer: heikora
zone_pivot_groups: foundry-speech-studio-cli-rest
#Customer intent: As a developer, I want to understand the lifecycle of custom speech models and endpoints so that I can plan for the expiration of my models.
---

# Custom speech model lifecycle

You can use a custom speech model for some time after you deploy it to your custom endpoint. But when new base models are made available, the older models are expired. You must periodically recreate and train your custom model from the latest base model to take advantage of the improved accuracy and quality.

Here are some key terms related to the model lifecycle:

* **Training**: Taking a base model and customizing it to your domain/scenario by using text data and/or audio data. In some contexts such as the REST API properties, training is also referred to as **adaptation**.
* **Transcription**: Using a model and performing speech recognition (decoding audio into text).
* **Endpoint**: A specific deployment of either a base model or a custom model that only you can access. 

> [!NOTE]
> Endpoints used by `F0` Speech resources are deleted after seven days.

## Expiration timeline

Here are timelines for model adaptation and transcription expiration:

- Training is available for one year after the quarter when Microsoft created the base model.
- Transcription with a base model is available for two years after the quarter when Microsoft created the base model.
- Transcription with a custom model is available for two years after the quarter when you created the custom model.

In this context, quarters end on January 15, April 15, July 15, and October 15. 

## What to do when a model expires

When a custom model or base model expires, it's no longer available for transcription. You can change the model that is used by your custom speech endpoint without downtime.

|Transcription route  |Expired model result  |Recommendation  |
|---------|---------|---------|
|Custom endpoint|Speech recognition requests fall back to the most recent base model for the same [locale](language-support.md?tabs=stt). You get results, but recognition might not accurately transcribe your domain data.  |Update the endpoint's model as described in the [Deploy a custom speech model](how-to-custom-speech-deploy-model.md) guide. |
|Batch transcription |[Batch transcription](batch-transcription.md) requests for expired models fail with a 4xx error. |In each [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit) REST API request body, set the `model` property to a base model or custom model that isn't expired. Otherwise don't include the `model` property to always use the latest base model. |

## Get base model expiration dates

> [!TIP]
> Bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry portal, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).

The last date that you could use the base model for training was shown when you created the custom model. For more information, see [Train a custom speech model](how-to-custom-speech-train-model.md).

Follow these instructions to get the transcription expiration date for a base model:

::: zone pivot="ai-foundry-portal"

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.
1. Select the custom model that you want to check from the **Model name** column.
1. Select **Deploy models**.
1. The expiration date for the model is shown in the **Expiration** column. This date is the last date that you can use the model for transcription.

::: zone-end

::: zone pivot="speech-studio"

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Deploy models**.
1. The expiration date for the model is shown in the **Expiration** column. This date is the last date that you can use the model for transcription.

    :::image type="content" source="media/custom-speech/custom-speech-model-expiration.png" alt-text="Screenshot of the deploy models page that shows the transcription expiration date.":::


::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To get the training and transcription expiration dates for a base model, use the `spx csr model status` command. Construct the request parameters according to the following instructions:

- Set the `url` property to the URI of the base model that you want to get. You can run the `spx csr list --base` command to get available base models for all locales.

Here's an example Speech CLI command to get the training and transcription expiration dates for a base model:

```azurecli-interactive
spx csr model status --api-version v3.2 --model https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/aaaabbbb-0000-cccc-1111-dddd2222eeee
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

In the response, take note of the date in the `adaptationDateTime` property. This property is the last date that you can use the base model for training. Also take note of the date in the `transcriptionDateTime` property. This date is the last date that you can use the base model for transcription.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff",
  "datasets": [],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/1aae1070-7972-47e9-a977-87e3b05c457d/manifest"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2023-01-15T00:00:00Z",
      "transcriptionDateTime": "2024-01-15T00:00:00Z"
    }
  },
  "lastActionDateTime": "2022-05-06T10:52:02Z",
  "status": "Succeeded",
  "createdDateTime": "2021-10-13T00:00:00Z",
  "locale": "en-US",
  "displayName": "20210831 + Audio file adaptation",
  "description": "en-US base model"
}
```

For Speech CLI help with models, run the following command:

```azurecli-interactive
spx help csr model
```

::: zone-end

::: zone pivot="rest-api"

To get the training and transcription expiration dates for a base model, use the [Models_GetBaseModel](/rest/api/speechtotext/models/get-base-model) operation of the [Speech to text REST API](rest-speech-to-text.md). You can make a [Models_ListBaseModels](/rest/api/speechtotext/models/list-base-models) request to get available base models for all locales.

Make an HTTP GET request using the model URI as shown in the following example. Replace `BaseModelId` with your model ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/BaseModelId" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

In the response, take note of the date in the `adaptationDateTime` property. This date is the last date that you can use the base model for training. Also take note of the date in the `transcriptionDateTime` property. This date is the last date that you can use the base model for transcription.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff",
  "datasets": [],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/1aae1070-7972-47e9-a977-87e3b05c457d/manifest"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2023-01-15T00:00:00Z",
      "transcriptionDateTime": "2024-01-15T00:00:00Z"
    }
  },
  "lastActionDateTime": "2022-05-06T10:52:02Z",
  "status": "Succeeded",
  "createdDateTime": "2021-10-13T00:00:00Z",
  "locale": "en-US",
  "displayName": "20210831 + Audio file adaptation",
  "description": "en-US base model"
}
```

::: zone-end


## Get custom model expiration dates

::: zone pivot="ai-foundry-portal"

Follow these instructions to get the transcription expiration date for a custom model:

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.
1. Select the custom model that you want to check from the **Model name** column.
1. Select **Deploy models**.
1. The expiration date for the model is shown in the **Expiration** column. This date is the last date that you can use the model for transcription.

::: zone-end

::: zone pivot="speech-studio"

Follow these instructions to get the transcription expiration date for a custom model:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Train custom models**.
1. The expiration date the custom model is shown in the **Expiration** column. This date is the last date that you can use the custom model for transcription. Base models aren't shown on the **Train custom models** page. 

    :::image type="content" source="media/custom-speech/custom-speech-custom-model-expiration.png" alt-text="Screenshot of the train custom models page that shows the transcription expiration date.":::

You can also follow these instructions to get the transcription expiration date for a custom model:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech). 
1. Select **Custom speech** > Your project name > **Deploy models**.
1. The expiration date for the model is shown in the **Expiration** column. This date is the last date that you can use the model for transcription.

    :::image type="content" source="media/custom-speech/custom-speech-model-expiration.png" alt-text="Screenshot of the deploy models page that shows the transcription expiration date.":::


::: zone-end

::: zone pivot="speech-cli"

Before proceeding, make sure that you have the [Speech CLI](./spx-basics.md) installed and configured.

To get the transcription expiration date for your custom model, use the `spx csr model status` command. Construct the request parameters according to the following instructions:

- Set the `url` property to the URI of the model that you want to get. Replace `YourModelId` with your model ID and replace `YourServiceRegion` with your Speech resource region.

Here's an example Speech CLI command to get the transcription expiration date for your custom model:

```azurecli-interactive
spx csr model status --api-version v3.2 --model https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.1/models/YourModelId
```

> [!IMPORTANT]
> You must set `--api-version v3.2`. The Speech CLI uses the REST API, but doesn't yet support versions later than `v3.2`.

In the response, take note of the date in the `transcriptionDateTime` property. This date is the last date that you can use your custom model for transcription. The `adaptationDateTime` property isn't applicable, since custom models aren't used to train other custom models.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/ccccdddd-2222-eeee-3333-ffff4444aaaa",
  "baseModel": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "datasets": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/datasets/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
    }
  ],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/86c4ebd7-d70d-4f67-9ccc-84609504ffc7/manifest",
    "copyTo": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/86c4ebd7-d70d-4f67-9ccc-84609504ffc7:copyto"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/projects/eeeeffff-4444-aaaa-5555-bbbb6666cccc"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2023-01-15T00:00:00Z",
      "transcriptionDateTime": "2024-07-15T00:00:00Z"
    }
  },
  "lastActionDateTime": "2022-05-21T13:21:01Z",
  "status": "Succeeded",
  "createdDateTime": "2022-05-22T16:37:01Z",
  "locale": "en-US",
  "displayName": "My Model",
  "description": "My Model Description"
}
```

For Speech CLI help with models, run the following command:

```azurecli-interactive
spx help csr model
```

::: zone-end

::: zone pivot="rest-api"

To get the transcription expiration date for your custom model, use the [Models_GetCustomModel](/rest/api/speechtotext/models/get-custom-model) operation of the [Speech to text REST API](rest-speech-to-text.md). 

Make an HTTP GET request using the model URI as shown in the following example. Replace `YourModelId` with your model ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.1/models/YourModelId" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

In the response, take note of the date in the `transcriptionDateTime` property. This date is the last date that you can use your custom model for transcription. The `adaptationDateTime` property isn't applicable, since custom models aren't used to train other custom models.

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/ccccdddd-2222-eeee-3333-ffff4444aaaa",
  "baseModel": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/base/bbbbcccc-1111-dddd-2222-eeee3333ffff"
  },
  "datasets": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/datasets/ddddeeee-3333-ffff-4444-aaaa5555bbbb"
    }
  ],
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/86c4ebd7-d70d-4f67-9ccc-84609504ffc7/manifest",
    "copyTo": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/models/86c4ebd7-d70d-4f67-9ccc-84609504ffc7:copyto"
  },
  "project": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/projects/eeeeffff-4444-aaaa-5555-bbbb6666cccc"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2023-01-15T00:00:00Z",
      "transcriptionDateTime": "2024-07-15T00:00:00Z"
    }
  },
  "lastActionDateTime": "2022-05-21T13:21:01Z",
  "status": "Succeeded",
  "createdDateTime": "2022-05-22T16:37:01Z",
  "locale": "en-US",
  "displayName": "My Model",
  "description": "My Model Description"
}
```

::: zone-end

## Related content

- [Train a model](how-to-custom-speech-train-model.md)
- [Custom speech overview](custom-speech-overview.md)
