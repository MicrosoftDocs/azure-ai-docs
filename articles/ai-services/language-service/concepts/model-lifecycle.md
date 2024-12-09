---
title: Model Lifecycle of Language service models
titleSuffix: Azure AI services
description: This article describes the timelines for models and model versions used by Language service features.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 01/16/2024
ms.author: jboback
---

# Model lifecycle

Language service features utilize AI models. We update the language service with new model versions to improve accuracy, support, and quality. As models become older, they are retired. Use this article for information on that process, and what you can expect for your applications.

## Prebuilt features

Our standard (not customized) language service features are built on AI models that we call pre-trained or prebuilt models.

We regularly update the language service with new model versions to improve model accuracy, support, and quality.

By default, all API requests will use the latest Generally Available (GA) model.

#### Choose the model-version used on your data

We recommend using the `latest` model version to utilize the latest and highest quality models. As our models improve, it’s possible that some of your model results may change. Model versions may be deprecated, so we no longer accept specified GA model versions in your implementation. 

Preview models used for preview features do not maintain a minimum retirement period and may be deprecated at any time.

By default, API and SDK requests will use the latest Generally Available model. You can use an optional parameter to select the version of the model to be used (not recommended).

> [!NOTE]
> If you are using a model version that is not listed in the table, then it was subjected to the expiration policy.

Use the table below to find which model versions are supported by each feature:

| Feature                                             | Supported generally available (GA) version     | Supported preview versions                  |
|-----------------------------------------------------|------------------------------------------------|---------------------------------------------|
| Sentiment Analysis and opinion mining               | `latest*`                                      |                                             |
| Language Detection                                  | `latest*`                                      |                                             |
| Entity Linking                                      | `latest*`                                      |                                             |
| Named Entity Recognition (NER)                      | `latest*`                                      | `2023-04-15-preview**`                      |
| Personally Identifiable Information (PII) detection | `latest*`                                      | `2023-04-15-preview**`                      | 
| PII detection for conversations                     | `latest*`                                      | `2023-04-15-preview**`                      |
| Question answering                                  | `latest*`                                      |                                             |
| Text Analytics for health                           | `latest*`                                      | `2022-08-15-preview`, `2023-01-01-preview**`|
| Key phrase extraction                               | `latest*`                                      |                                             | 
| Summarization                                       |  `latest*`                                     |                                             |


\* Latest Generally Available (GA) model version
\*\* Latest preview version


## Custom features

### Expiration timeline

For custom features, there are two key parts of the AI implementation: training and deployment. New configurations are released regularly with regular AI improvements, so older and less accurate configurations are retired. 

Use the table below to find which model versions are supported by each feature:

| Feature                                     | Supported Training Config Versions         | Training Config Expiration         | Deployment Expiration  |
|---------------------------------------------|--------------------------------------------|------------------------------------|------------------------|
| Conversational language understanding       | `2022-09-01` (latest)**                    | August 26, 2025                    | August 26, 2026        |
| Orchestration workflow                      | `2022-09-01` (latest)**                    | October 22, 2025                   | October 22, 2026       |
| Custom named entity recognition             | `2022-05-01` (latest)**                    | October 22, 2025                   | October 22, 2026       |
| Custom text classification                  | `2022-05-01` (latest)**                    | October 22, 2025                   | October 22, 2026       |

** *For latest training configuration versions, the posted expiration dates are subject to availability of a newer model version. If no newer model versions are available, the expiration date may be extended.*

Training configurations are typically available for **six months** after its release. If you've assigned a trained configuration to a deployment, this deployment expires after **twelve months** from the training config expiration. If your models are about to expire, you can retrain and redeploy your models with the latest training configuration version. 

> [!TIP]
> It's recommended to use the latest supported configuration version.

After the **training config expiration** date, you'll have to use another supported training configuration version to submit any training or deployment jobs. After the **deployment expiration** date, your deployed model will be unavailable to be used for prediction.

After training config version expires, API calls will return an error when called or used if called with an expired configuration version. By default, training requests use the latest available training configuration version. To change the configuration version, use the `trainingConfigVersion` parameter when submitting a training job and assign the version you want.



## API versions

When you're making API calls to the following features, you need to specify the `API-VERISON` you want to use to complete your request. It's recommended to use the latest available API versions.

If you're using [Language Studio](https://aka.ms/languageStudio) for your projects, you'll use the latest API version available. Other API versions are only available through the REST APIs and client libraries.

Use the following table to find which API versions are supported by each feature:

|Feature                               |Supported versions                                                                   |Latest Generally Available version                           |Latest preview version|
|--------------------------------------|-------------------------------------------------------------------------------------|----------------------------------|----------------------|
| Custom text classification           |`2022-05-01`, `2022-10-01-preview`, `2023-04-01`                                     |`2022-05-01`                      |`2022-10-01-preview`  |
| Conversational language understanding| `2022-05-01`, `2022-10-01-preview`, `2023-04-01`                                    |`2023-04-01`                      |`2022-10-01-preview`  |
| Custom named entity recognition      | `2022-05-01`, `2022-10-01-preview`, `2023-04-01`, `2023-04-15`, `2023-04-15-preview`|`2023-04-15`                      |`2023-04-15-preview`  |
| Orchestration workflow               | `2022-05-01`, `2022-10-01-preview`, `2023-04-01`                                    |`2023-04-01`                      |`2022-10-01-preview`  |

## Next steps

[Azure AI Language overview](../overview.md)
