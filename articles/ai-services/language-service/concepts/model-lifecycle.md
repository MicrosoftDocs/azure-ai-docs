---
title: Model Lifecycle of Language service models
titleSuffix: Foundry Tools
description: This article describes the timelines for models and model versions used by Language service features.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 01/26/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Model lifecycle

Language features utilize AI models. We update Azure Language with new model versions to improve accuracy, support, and quality. As models become older, they're retired. Use this article for information on that process, and what you can expect for your applications.

## Prebuilt features

Our standard (not customized) Language features are built on AI models that we call pretrained or prebuilt models.

We regularly update Azure Language with new model versions to improve model accuracy, support, and quality.

By default, all API requests use the latest Generally Available (GA) model.

### Choose the model-version used on your data

We recommend using the **latest** model version to utilize the latest and highest quality models. As our models improve, it's possible that some of your model results may change. Model versions may be deprecated, so we no longer accept specified GA model versions in your implementation.

Preview models used for preview features don't maintain a minimum retirement period and may be deprecated at any time.

By default, API and SDK requests use the latest Generally Available model. To use a model in preview, you can use an optional parameter **modelVersion** to select the preview version of the model to be used (not recommended for GA models).

> [!NOTE]
> If you're using a model version that isn't listed in the table, then it was subjected to the expiration policy.

## Model versions

Use the following table to find which model versions support each feature:

| Feature | Supported generally available (GA) version | Latest supported preview versions | Other supported versions | Deprecated versions |
| --- | --- | --- | --- | --- |
| **Sentiment Analysis and opinion mining** | **latest** | | | |
| **Language Detection** | **latest** | | | |
| **Entity Linking** | **latest** | | | |
| **Named Entity Recognition (NER)** | **2025-11-01** (latest) | **2025-11-15-preview** | **2025-02-01**</br>**2023-09-01** | **2025-08-01-preview**</br> **2024-05-01** |
| **Personally Identifiable Information (PII) detection** | **2025-11-01** (latest) | **2025-11-15-preview** | **2025-02-01**</br> **2023-09-01** | **2025-08-01-preview**</br> **2024-05-01** |
| **PII detection for conversations** | **2025-02-01** (latest) | **2025-11-01-preview** | **2022-05-15**</br> **2022-05-15-preview** | **2024-11-01-preview**</br> **2023-04-15-preview** |
| **Question answering** | **latest** | | | |
| **Text Analytics for health** | **latest** | **2023-04-15-preview** | | |
| **Key phrase extraction** | **latest** | | | |
| **Summarization** | **latest**. **Note**: **2025-06-10** is only available for **issue** and **resolution** aspects in conversation summarization. | | | |

## Custom features

For custom features, there are two key parts of the AI implementation: training and deployment. New configurations are released regularly with regular AI improvements, so older and less accurate configurations are retired.

### Expiration timeline

Use the following table to find which model versions support each feature:

| Feature | Supported Training Config Versions | Training Config Expiration | Deployment Expiration |
| --- | --- | --- | --- |
| Conversational language understanding | **2022-09-01** (latest)** | August 26, 2025 | August 26, 2026 |
| Orchestration workflow | **2022-09-01** (latest)** | October 22, 2025 | October 22, 2026 |
| Custom named entity recognition | **2022-05-01** (latest)** | October 22, 2025 | October 22, 2026 |
| Custom text classification | **2022-05-01** (latest)** | October 22, 2025 | October 22, 2026 |

** *For latest training configuration versions, the posted expiration dates are subject to availability of a newer model version. If no newer model versions are available, the expiration date may be extended.*

Training configurations are typically available for **six months** after its release. If you assigned a trained configuration to a deployment, this deployment expires after **twelve months** from the training config expiration. If your models are about to expire, you can retrain and redeploy your models with the latest training configuration version.

> [!TIP]
> We recommend that you use the latest supported configuration version.

After the **training config expiration** date, you have to use another supported training configuration version to submit any training or deployment jobs. After the **deployment expiration** date, your deployed model is unavailable to be used for prediction.

After training config version expires, API calls returns an error when called or used if called with an expired configuration version. By default, training requests use the latest available training configuration version. To change the configuration version, use the **trainingConfigVersion** parameter when submitting a training job and assign the version you want.

## API versions

When you're making API calls to the following features, you need to specify the **API-VERISON** you want to use to complete your request. We recommend that you use the latest available API version.

If you're using [Language Studio](https://aka.ms/languageStudio) for your projects, you use the latest API version available. Other API versions are only available through the REST APIs and client libraries.

Use the following table to find which API versions support each feature:

| Feature | Supported versions | Latest Generally Available version | Latest preview version |
| --- | --- | --- | --- |
| Custom text classification | **2022-05-01**</br> **2022-10-01-preview**</br> **2023-04-01** | **2022-05-01** | **2022-10-01-preview** |
| Conversational language understanding | **2022-05-01**</br> **2022-10-01-preview**</br> **2023-04-01** | **2023-04-01** | **2022-10-01-preview** |
| Custom named entity recognition | **2022-05-01**</br> **2022-10-01-preview**</br> **2023-04-01**</br> **2023-04-15**</br> **2023-04-15-preview** | **2023-04-15** | **2023-04-15-preview** |
| Orchestration workflow | **2022-05-01**</br> **2022-10-01-preview**</br> **2023-04-01** | **2023-04-01** | **2022-10-01-preview** |
| Named Entity Recognition (NER) | **2025-05-15-preview**</br> **2024-11-01 (GA)**</br>**2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |
| Personally Identifiable Information (PII) detection | **2025-05-15-preview**</br>**2024-11-01 (GA)**</br>**2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |
| PII detection for conversations | **2025-05-15-preview**</br>**2024-11-01 (GA)**</br>**2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |

## Next steps

[Azure Language in Foundry Tools overview](../overview.md)
