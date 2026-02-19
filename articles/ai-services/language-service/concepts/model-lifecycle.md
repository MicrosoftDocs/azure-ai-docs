---
title: Model Lifecycle for Azure Language service models
titleSuffix: Foundry Tools
description: This article describes the timelines for models and model versions used by Language service features.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 01/30/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Model lifecycle

Azure Language features are powered by machine learning models that undergo continuous improvement and refinement. New model versions are released regularly to enhance prediction accuracy, expand language support, and improve overall output quality.

As part of this iterative development process, older model versions are deprecated and eventually retired according to a defined lifecycle policy. This article provides detailed information about model versioning, deprecation timelines, and retirement procedures to help you plan for updates and maintain compatibility in your production applications.

## Prebuilt features

Prebuilt (also referred to as pretrained) features in Azure Language are powered by models trained on large datasets and are ready to use without added customization. These models provide out-of-the-box natural language processing capabilities for common scenarios.

Prebuilt models are updated continuously to improve prediction accuracy, expand language coverage, and enhance output quality. By default, all API requests are automatically routed to the latest Generally Available (GA) model version.

### Choose the model version used on your data

We recommend using the **latest** model version to ensure optimal accuracy and access to the most recent improvements. However, as models evolve, prediction outputs may change between versions. Deprecated model versions are no longer accepted in API requests after their retirement date.

> [!IMPORTANT]
> Preview model versions don't maintain a minimum retirement period and may be deprecated at any time without advance notice.

By default, API and SDK requests are processed using the latest Generally Available model version. To specify an alternative version, use the optional **modelVersion** parameter in your request. Specifying a preview model version for production workloads isn't recommended.

> [!NOTE]
> If you're using a model version that isn't listed in the following table, that version is retired according to the expiration policy.

## Model versions

The following table provides a comprehensive reference of supported model versions for each prebuilt feature, including Generally Available (GA), preview, and deprecated versions:

| Feature | Supported generally available (GA) version | Latest supported preview versions | Other supported versions | Deprecated versions |
| --- | --- | --- | --- | --- |
| **Sentiment Analysis and opinion mining** | **latest** | | | |
| **Language Detection** | **latest** | | | |
| **Entity Linking** | **latest** | | | |
| **Named Entity Recognition (NER)** | **2025-11-01** (latest) | **2025-11-15-preview** | &bullet; **2025-02-01**</br>&bullet; **2023-09-01** | &bullet; **2025-08-01-preview**</br>&bullet; **2024-05-01** |
| **Personally Identifiable Information (PII) detection** | **2025-11-01** (latest) | **2025-11-15-preview** | &bullet; **2025-02-01**</br>&bullet; **2023-09-01** | &bullet; **2025-08-01-preview**</br>&bullet; **2024-05-01** |
| **PII detection for conversations** | **2025-02-01** (latest) | **2025-11-01-preview** | &bullet; **2022-05-15**</br>&bullet; **2022-05-15-preview** | &bullet; **2024-11-01-preview**</br>&bullet; **2023-04-15-preview** |
| **Question answering** | **latest** | | | |
| **Text Analytics for health** | **latest** | **2023-04-15-preview** | | |
| **Key phrase extraction** | **latest** | | | |
| **Summarization** | **latest**. **Note**: **2025-06-10** is only available for **issue** and **resolution** aspects in conversation summarization. | | | |

## Custom features

Custom features in Azure Language involve two distinct lifecycle phases: **training** and **deployment**. Each phase has its own configuration version and expiration timeline. New training configurations are released periodically to incorporate AI improvements, and older configurations are retired according to a defined schedule.

### Expiration timeline

The following table lists the supported training configuration versions and their corresponding expiration dates for each custom feature:

| Feature | Supported Training Config Versions | Training Config Expiration | Deployment Expiration |
| --- | --- | --- | --- |
| Conversational language understanding | **2022-09-01** (latest) | August 26, 2025 | August 26, 2026 |
| Orchestration workflow | **2022-09-01** (latest) | October 22, 2025 | October 22, 2026 |
| Custom named entity recognition | **2022-05-01** (latest) | October 22, 2025 | October 22, 2026 |
| Custom text classification | **2022-05-01** (latest) | October 22, 2025 | October 22, 2026 |

***For the latest training configuration versions, posted expiration dates are subject to the availability of a newer model version. If no newer model versions are released, the expiration date may be extended.***

Training configurations are typically supported for **six months** following their release date. Deployments created using a specific training configuration remain active for **twelve months** after the training configuration expiration date. To avoid service disruption, retrain and redeploy your models using the latest training configuration version before the expiration date.

> [!TIP]
> We recommend using the latest supported training configuration version to ensure optimal model performance and extended support.

**Training configuration expiration**: After the training configuration expiration date, you must use a supported configuration version to submit training or deployment jobs. Requests specifying an expired configuration version return an error.

**Deployment expiration**: After the deployment expiration date, the deployed model is no longer available for prediction requests.

By default, training requests use the latest available training configuration version. To specify a different version, include the **trainingConfigVersion** parameter in your training job request.

## API versions

For detailed information about request parameters and response schemas, see the [**Azure AI Language REST API reference**](/rest/api/language/).

When making API calls to Azure Language features, you must specify the **API-VERSION** parameter in your request. We recommend using the latest available API version to access the most recent features and improvements.

The following table lists the supported API versions for each feature:

| Feature | Supported versions | Latest Generally Available version | Latest preview version |
| --- | --- | --- | --- |
| Custom text </br>classification | &bullet; **2022-05-01**</br>&bullet; **2022-10-01-preview**</br>&bullet; **2023-04-01** | **2022-05-01** | **2022-10-01-preview** |
| Conversational language </br>understanding | &bullet; **2022-05-01**</br>&bullet; **2022-10-01-preview**</br>&bullet; **2023-04-01** | **2023-04-01** | **2022-10-01-preview** |
| Custom named entity </br>recognition | &bullet; **2022-05-01**</br>&bullet; **2022-10-01-preview**</br>&bullet; **2023-04-01**</br>&bullet; **2023-04-15**</br>&bullet; **2023-04-15-preview** | **2023-04-15** | **2023-04-15-preview** |
| Orchestration </br>workflow | &bullet; **2022-05-01**</br>&bullet; **2022-10-01-preview**</br>&bullet; **2023-04-01** | **2023-04-01** | **2022-10-01-preview** |
| Named Entity</br>Recognition | &bullet; **2025-05-15-preview**</br>&bullet; **2024-11-01 (GA)**</br>&bullet; **2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |
| `PII` detection </br>for text | &bullet; **2025-05-15-preview**</br>&bullet; **2024-11-01 (GA)**</br>&bullet; **2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |
| `PII` detection </br>for conversations | &bullet; **2025-05-15-preview**</br>&bullet; **2024-11-01 (GA)**</br>&bullet; **2024-11-15-preview** | **2024-11-01 (GA)** | **2025-05-15-preview** |

### Model version and API version comparison

Understanding the distinction between model versions and API versions is essential for managing your Azure Language implementations effectively.

| Aspect | API version | Model version |
| --- | --- | --- |
| **Definition** | Defines the service endpoint contract, including request/response schemas and available operations. | Specifies the underlying machine learning algorithm and trained weights used for predictions. |
| **REST call location** | Required `api-version` query parameter in the request URL. | Optional `modelVersion` parameter in the request body. |
| **Update frequency** | Released when interface changes or new features are introduced. | Released regularly to improve prediction accuracy and language coverage. |
| **Update impact** | Breaking changes require a new API version to maintain backward compatibility. | Updates typically enhance results without requiring API version changes. |
| **Default behavior** | Must be explicitly specified; SDK/client libraries default to a specific supported version. | Automatically defaults to the latest GA model version if not specified. |

## Related content

* [Azure Language overview](../overview.md)
* [Regional support for Azure Language](regional-support.md)
