---
title: Create a custom speech project - Speech service
titleSuffix: Azure AI services
description: Learn about how to create a project for custom speech. 
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/19/2024
ms.author: eur
zone_pivot_groups: speech-studio-cli-rest
#Customer intent: As a developer, I want to learn how to create a project for custom speech so that I can train and deploy a custom model.
---

# Create a custom speech project

Custom speech projects contain models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might create a project for English in the United States.

## Create a project

::: zone pivot="speech-studio"

To create a custom speech project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you will train a custom model with audio data, choose a Speech resource region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#speech-service) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. You'll see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 

::: zone-end

::: zone pivot="speech-cli"

To create a project, use the `spx csr project create` command. Construct the request parameters according to the following instructions:

- Set the required `language` parameter. The locale of the project and the contained datasets should be the same. The locale can't be changed later. The Speech CLI `language` parameter corresponds to the `locale` property in the JSON request and response.
- Set the required `name` parameter. This is the name that is displayed in the Speech Studio. The Speech CLI `name` parameter corresponds to the `displayName` property in the JSON request and response.

Here's an example Speech CLI command that creates a project:

```azurecli-interactive
spx csr project create --api-version v3.2 --name "My Project" --description "My Project Description" --language "en-US"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52",
  "links": {
    "evaluations": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/evaluations",
    "datasets": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/datasets",
    "models": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/models",
    "endpoints": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/endpoints",
    "transcriptions": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/transcriptions"
  },
  "properties": {
    "datasetCount": 0,
    "evaluationCount": 0,
    "modelCount": 0,
    "transcriptionCount": 0,
    "endpointCount": 0
  },
  "createdDateTime": "2024-07-14T17:15:55Z",
  "locale": "en-US",
  "displayName": "My Project",
  "description": "My Project Description"
}
```

The top-level `self` property in the response body is the project's URI. Use this URI to get details about the project's evaluations, datasets, models, endpoints, and transcriptions. You also use this URI to update or delete a project.

For Speech CLI help with projects, run the following command:

```azurecli-interactive
spx help csr project
```

::: zone-end

::: zone pivot="rest-api"

To create a project, use the [Projects_Create](/rest/api/speechtotext/projects/create) operation of the [Speech to text REST API](rest-speech-to-text.md). Construct the request body according to the following instructions:

- Set the required `locale` property. This should be the locale of the contained datasets. The locale can't be changed later.
- Set the required `displayName` property. This is the project name that is displayed in the Speech Studio.

Make an HTTP POST request using the URI as shown in the following [Projects_Create](/rest/api/speechtotext/projects/create) example. Replace `YourSubscriptionKey` with your Speech resource key, replace `YourServiceRegion` with your Speech resource region, and set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSubscriptionKey" -H "Content-Type: application/json" -d '{
  "displayName": "My Project",
  "description": "My Project Description",
  "locale": "en-US"
} '  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/v3.2/projects"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52",
  "links": {
    "evaluations": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/evaluations",
    "datasets": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/datasets",
    "models": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/models",
    "endpoints": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/endpoints",
    "transcriptions": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/projects/0198f569-cc11-4099-a0e8-9d55bc3d0c52/transcriptions"
  },
  "properties": {
    "datasetCount": 0,
    "evaluationCount": 0,
    "modelCount": 0,
    "transcriptionCount": 0,
    "endpointCount": 0
  },
  "createdDateTime": "2024-07-14T17:15:55Z",
  "locale": "en-US",
  "displayName": "My Project",
  "description": "My Project Description"
}
```

The top-level `self` property in the response body is the project's URI. Use this URI to [get](/rest/api/speechtotext/projects/get) details about the project's evaluations, datasets, models, endpoints, and transcriptions. You also use this URI to [update](/rest/api/speechtotext/projects/update) or [delete](/rest/api/speechtotext/projects/delete) a project.

::: zone-end

## Choose your model

There are a few approaches to using custom speech models:
- The base model provides accurate speech recognition out of the box for a range of [scenarios](overview.md#speech-scenarios). Base models are updated periodically to improve accuracy and quality. We recommend that if you use base models, use the latest default base models. If a required customization capability is only available with an older model, then you can choose an older base model. 
- A custom model augments the base model to include domain-specific vocabulary shared across all areas of the custom domain.
- Multiple custom models can be used when the custom domain has multiple areas, each with a specific vocabulary.

One recommended way to see if the base model suffices is to analyze the transcription produced from the base model and compare it with a human-generated transcript for the same audio. You can compare the transcripts and obtain a [word error rate (WER)](how-to-custom-speech-evaluate-data.md#evaluate-word-error-rate-wer) score. If the WER score is high, training a custom model to recognize the incorrectly identified words is recommended.

Multiple models are recommended if the vocabulary varies across the domain areas. For instance, Olympic commentators report on various events, each associated with its own vernacular. Because each Olympic event vocabulary differs significantly from others, building a custom model specific to an event increases accuracy by limiting the utterance data relative to that particular event. As a result, the model doesn't need to sift through unrelated data to make a match. Regardless, training still requires a decent variety of training data. Include audio from various commentators who have different accents, gender, age, etcetera. 

## Model stability and lifecycle

A base model or custom model deployed to an endpoint using custom speech is fixed until you decide to update it. The speech recognition accuracy and quality remain consistent, even when a new base model is released. This allows you to lock in the behavior of a specific model until you decide to use a newer model.

Whether you train your own model or use a snapshot of a base model, you can use the model for a limited time. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

## Next steps

* [Training and testing datasets](./how-to-custom-speech-test-and-train.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
* [Train a model](how-to-custom-speech-train-model.md)
