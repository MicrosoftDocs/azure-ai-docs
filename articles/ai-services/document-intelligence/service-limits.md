---
title: Service quotas and limits - Document Intelligence
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Document Intelligence service Quotas and Limits
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 09/26/2024
ms.author: lajanuar
monikerRange: '<=doc-intel-4.0.0'
---


# Service quotas and limits

::: moniker range=">=doc-intel-3.0.0"
[!INCLUDE [applies to v4.0 v3.1 v3.0](includes/applies-to-v40-v31-v30.md)]
::: moniker-end

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](includes/applies-to-v21.md)]
::: moniker-end

This article contains both a quick reference and detailed description of Azure AI Document Intelligence service Quotas and Limits for all [pricing tiers](https://azure.microsoft.com/pricing/details/form-recognizer/). It also contains some best practices to avoid request throttling.

## Model usage

:::moniker range="doc-intel-4.0.0"
|Document types supported|Read|Layout|Prebuilt models|Custom models|Add-on capabilities|
|--|--|--|--|--|----|
| PDF | ✔️ | ✔️ | ✔️ | ✔️ |✔️|
| Images: `JPEG/JPG`, `PNG`, `BMP`, `TIFF`, `HEIF` | ✔️ | ✔️ | ✔️ | ✔️ |✔️|
| Microsoft Office: `DOCX`, `PPTX`, `XLS` | ✔️ | ✔️ | ✖️ | ✖️ |✖️|

✔️ = supported
✖️ = Not supported
:::moniker-end

:::moniker range="doc-intel-3.1.0"
|Document types supported|Read|Layout|Prebuilt models|Custom models|
|--|--|--|--|--|
| PDF | ✔️ | ✔️ | ✔️ | ✔️ |
| Images: `JPEG/JPG`, `PNG`, `BMP`, `TIFF`, `HEIF` | ✔️ | ✔️ | ✔️ | ✔️ |
| Microsoft Office: `DOCX`, `PPTX`, `XLS` | ✔️ | ✖️ | ✖️ | ✖️ |

✔️ = supported
✖️ = Not supported

## Billing

Document Intelligence billing is calculated monthly based on the model type and the number of pages analyzed. You can find usage metrics on the metrics dashboard in the Azure portal. The dashboard displays the number of pages that Azure AI Document Intelligence processes. You can check the estimated cost spent on the resource by using the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/). For detailed instructions, see [Check usage and estimate cost](how-to-guides/estimate-cost.md). Here are some details:

- When you submit a document for analysis, the service analyzes all pages unless you specify a page range by using the `pages` parameter in your request. When the service analyzes Microsoft Excel and PowerPoint documents through the read, OCR, or layout model, it counts each Excel worksheet and PowerPoint slide as one page.

- When the service analyzes PDF and TIFF files, it counts each page in the PDF file or each image in the TIFF file as one page with no maximum character limits.

- When the service analyzes Microsoft Word and HTML files that the read and layout models support, it counts pages in blocks of 3,000 characters each. For example, if your document contains 7,000 characters, the two pages with 3,000 characters each and one page with 1,000 characters add up to a total of three pages.

- The read and layout models don't support analysis of embedded or linked images in Microsoft Word, Excel, PowerPoint, and HTML files. Therefore, service doesn't count them as added images.

- Training a custom model is always free with Document Intelligence. Charges are incurred only when the service uses a model to analyze a document.

- Container pricing is the same as cloud service pricing.

- Document Intelligence offers a free tier (F0) where you can test all the Document Intelligence features.

- Document Intelligence has a commitment-based pricing model for large workloads.

- The Layout model is required to generate labels for your dataset for custom training. If the dataset that you use for custom training doesn't have label files available, the service generates them for you and bills you for layout model usage.

:::moniker-end

::: moniker range=">=doc-intel-3.0.0"

> [!div class="checklist"]
>
> * [**Document Intelligence SDKs**](quickstarts/get-started-sdks-rest-api.md)
> * [**Document Intelligence REST API**](quickstarts/get-started-sdks-rest-api.md)
> * [**Document Intelligence Studio v3.0**](quickstarts/try-document-intelligence-studio.md)
::: moniker-end

::: moniker range="doc-intel-2.1.0"

> [!div class="checklist"]
>
> * [**Document Intelligence SDKs**](quickstarts/get-started-sdks-rest-api.md)
> * [**Document Intelligence REST API**](quickstarts/get-started-sdks-rest-api.md)
> * [**Sample Labeling Tool v2.1**](https://fott-2-1.azurewebsites.net/)

::: moniker-end

|Quota|Free (F0)<sup>1</sup>|Standard (S0)|
|--|--|--|
| **Transactions Per Second limit** | 1 | 15 (default value) |
| Adjustable | No | Yes <sup>2</sup> |
| **Max document size** | 4 MB | 500 MB |
| Adjustable | No | No |
| **Max number of pages (Analysis)** | 2 | 2000 |
| Adjustable | No | No |
| **Max size of labels file** | 10 MB | 10 MB |
| Adjustable | No | No |
| **Max size of OCR json response** | 500 MB | 500 MB |
| Adjustable | No | No |
| **Max number of Template models** | 500 | 5000 |
| Adjustable | No | No |
| **Max number of Neural models** | 100 | 500 |
| Adjustable | No | No |

::: moniker range=">=doc-intel-4.0.0"

## Custom model usage

> [!div class="checklist"]
>
> * [**Custom template model**](train/custom-template.md)
> * [**Custom neural model**](train/custom-neural.md)
> * [**Custom generative model**](train/custom-generative-extraction.md)
> * [**Composed classification models**](train/custom-classifier.md)
> * [**Composed custom models**](train/composed-models.md)

|Quota|Free (F0) <sup>1</sup>|Standard (S0)|
|--|--|--|
| **Compose Model limit** | 5 | 500 (default value) |
| Adjustable | No | No |
| **Training dataset size * Neural and Generative** | 1 GB <sup>3</sup> | 1 GB (default value) |
| Adjustable | No | No |
| **Training dataset size * Template** | 50 MB <sup>4</sup> | 50 MB (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Template** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Neural and Generative** | 50,000 | 50,000 (default value) |
| Adjustable | No | No |
| **Custom neural model train** | 10 hours per month <sup>5</sup> | no limit (pay by the hour) |
| Adjustable | No |Yes <sup>3</sup>|
| **Max number of pages (Training) * Classifier** | 10,000 | 10,000 (default value) |
| Adjustable | No | No |
| **Max number of document types (classes) * Classifier** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Training dataset size * Classifier** | 1GB | 2GB (default value) |
| Adjustable | No | No |
| **Min number of samples per class * Classifier** | 5 | 5 (default value) |
| Adjustable | No | No |

::: moniker-end

::: moniker range="=doc-intel-3.0.0"

## Custom model usage

> [!div class="checklist"]
>
> * [**Custom template model**](train/custom-template.md)
> * [**Custom neural model**](train/custom-neural.md)
> * [**Composed classification models**](train/custom-classifier.md)
> * [**Composed custom models**](train/composed-models.md)

|Quota|Free (F0) <sup>1</sup>|Standard (S0)|
|--|--|--|
| **Compose Model limit** | 5 | 200 (default value) |
| Adjustable | No | No |
| **Training dataset size * Neural** | 1 GB <sup>3</sup> | 1 GB (default value) |
| Adjustable | No | No |
| **Training dataset size * Template** | 50 MB <sup>4</sup> | 50 MB (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Template** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Neural** | 50,000 | 50,000 (default value) |
| Adjustable | No | No |
| **Custom neural model train** | 10 per month | 20 per month |
| Adjustable | No |Yes <sup>3</sup>|
| **Max number of pages (Training) * Classifier** | 10,000 | 10,000 (default value) |
| Adjustable | No | No |
| **Max number of document types (classes) * Classifier** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Training dataset size * Classifier** | 1GB | 1GB (default value) |
| Adjustable | No | No |
| **Min number of samples per class * Classifier** | 5 | 5 (default value) |
| Adjustable | No | No |

::: moniker-end

::: moniker range="=doc-intel-3.1.0"

## Custom model usage

> [!div class="checklist"]
>
> * [**Custom template model**](train/custom-template.md)
> * [**Custom neural model**](train/custom-neural.md)
> * [**Composed classification models**](train/custom-classifier.md)
> * [**Composed custom models**](train/composed-models.md)

|Quota|Free (F0) <sup>1</sup>|Standard (S0)|
|--|--|--|
| **Compose Model limit** | 5 | 200 (default value) |
| Adjustable | No | No |
| **Training dataset size * Neural** | 1 GB <sup>3</sup> | 1 GB (default value) |
| Adjustable | No | No |
| **Training dataset size * Template** | 50 MB <sup>4</sup> | 50 MB (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Template** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Max number of pages (Training) * Neural** | 50,000 | 50,000 (default value) |
| Adjustable | No | No |
| **Custom neural model train** | 10 per month | 20 per month |
| Adjustable | No |Yes <sup>3</sup>|
| **Max number of pages (Training) * Classifier** | 10,000 | 10,000 (default value) |
| Adjustable | No | No |
| **Max number of document types (classes) * Classifier** | 500 | 500 (default value) |
| Adjustable | No | No |
| **Training dataset size * Classifier** | 1GB | 1GB (default value) |
| Adjustable | No | No |
| **Min number of samples per class * Classifier** | 5 | 5 (default value) |
| Adjustable | No | No |

::: moniker-end

::: moniker range="doc-intel-2.1.0"

## Custom model limits

> [!div class="checklist"]
>
> * [**Custom template model**](train/custom-template.md)
> * [**Composed custom models**](train/composed-models.md)

| Quota | Free (F0) <sup>1</sup> | Standard (S0) |
|--|--|--|
| **Compose Model limit** | 5 | 200 (default value) |
| Adjustable | No | No |
| **Training dataset size** | 50 MB | 50 MB (default value) |
| Adjustable | No | No |
| **Max number of pages (Training)** | 500 | 500 (default value) |
| Adjustable | No | No |

::: moniker-end

::: moniker range=">=doc-intel-2.1.0"

> <sup>1</sup> For **Free (F0)** pricing tier see also monthly allowances at the [pricing page](https://azure.microsoft.com/pricing/details/form-recognizer/).</br>
> <sup>2</sup> See [best practices](#example-of-a-workload-pattern-best-practice), and [adjustment instructions](#create-and-submit-support-request).</br>
> <sup>3</sup> Neural models training count is reset every calendar month. Open a support request to increase the monthly training limit.
::: moniker-end
::: moniker range=">=doc-intel-3.0.0"
> <sup>4</sup> This limit applies to all documents found in your training dataset folder prior to any labeling-related updates.
::: moniker-end
::: moniker range=">=doc-intel-4.0.0"
> <sup>5</sup> This limit applies for `v 4.0 (2024-07-31)` custom neural models only. Starting from `v 4.0`, we support training larger documents for longer durations (up to 10 hours for free, and incurring charges after). For more information, please refer to [custom nerual model page](train/custom-neural.md).
::: moniker-end

## Detailed description, Quota adjustment, and best practices

Before requesting a quota increase (where applicable), ensure that it's necessary. Document Intelligence service uses autoscaling to bring the required computational resources `on-demand`, keep the customer costs low, and deprovision unused resources by not maintaining an excessive amount of hardware capacity.

If your application returns Response Code 429 (*Too many requests*) and your workload is within the defined limits: most likely, the service is scaling up to your demand, but has yet to reach the required scale. Thus the service doesn't immediately have enough resources to serve the request. This state is transient and shouldn't last long.

### General best practices to mitigate throttling during autoscaling

To minimize issues related to throttling (Response Code 429), we recommend using the following techniques:

* Implement retry logic in your application
* Avoid sharp changes in the workload. Increase the workload gradually <br/>
*Example.* Your application is using Document Intelligence and your current workload is 10 TPS (transactions per second). The next second you increase the load to 40 TPS (that is four times more). The Service immediately starts scaling up to fulfill the new load, but likely it can't do it within a second, so some of the requests get Response Code 429.

The next sections describe specific cases of adjusting quotas.
Jump to [Document Intelligence: increasing concurrent request limit](#create-and-submit-support-request)

### Increasing transactions per second request limit

By default the number of transactions per second is limited to 15 transactions per second for a Document Intelligence resource. For the Standard pricing tier, this amount can be increased. Before submitting the request, ensure you're familiar with the material in [this section](#detailed-description-quota-adjustment-and-best-practices) and aware of these [best practices](#example-of-a-workload-pattern-best-practice).

Increasing the Concurrent Request limit does **not** directly affect your costs. Document Intelligence service uses "Pay only for what you use" model. The limit defines how high the Service can scale before it starts throttle your requests.

Existing value of Concurrent Request limit parameter is **not** visible via Azure portal, Command-Line tools, or API requests. To verify the existing value, create an Azure Support Request.

If you would like to increase your transactions per second, you can enable auto scaling on your resource. Follow this document to enable auto scaling on your resource * [enable auto scaling](../../ai-services/autoscale.md). You can also submit an increase TPS support request.

#### Have the required information ready

- Document Intelligence Resource ID
- Region

- Base model information:
  - Sign in to the [Azure portal](https://portal.azure.com)
  - Select the Document Intelligence Resource for which you would like to increase the transaction limit
  - Select -Properties- (-Resource Management- group)
  - Copy and save the values of the following fields:
    - Resource ID
    - Location (your endpoint Region)

#### Create and submit support request

Initiate the increase of transactions per second(TPS) limit for your resource by submitting the Support Request:

- Ensure you have the [required information](#have-the-required-information-ready)
- Sign in to the [Azure portal](https://portal.azure.com)
- Select the Document Intelligence Resource for which you would like to increase the TPS limit
- Select -New support request- (-Support + troubleshooting- group). A new window appears with autopopulated information about your Azure Subscription and Azure Resource
- Enter -Summary- (like "Increase Document Intelligence TPS limit")
- Select "Quota or usage validation" for problem type field.
- Select -Next: Solutions-
- Proceed further with the request creation
- Enter the following information in the -Description- field, under the Details tab:
  - a note, that the request is about Document Intelligence quota.
  - Provide a TPS expectation you would like to scale to  meet.
  - Azure resource information you [collected](#have-the-required-information-ready).
  - Complete entering the required information and select -Create- button in -Review + create- tab
  - Note the support request number in Azure portal notifications. Look for Support to contact you shortly for further processing.

## Example of a workload pattern best practice

This example presents the approach we recommend following to mitigate possible request throttling due to [Autoscaling being in progress](#detailed-description-quota-adjustment-and-best-practices). It isn't an *exact recipe*, but merely a template we invite to follow and adjust as necessary.

 Let us suppose that a Document Intelligence resource has the default limit set. Start the workload to submit your analyze requests. If you find that you're seeing frequent throttling with response code 429, start by implementing an exponential backoff on the GET analyze response request. By using a progressively longer wait time between retries for consecutive error responses, for example a  2-5-13-34 pattern of delays between requests. In general, we recommended not calling the get analyze response more than once every 2 seconds for a corresponding POST request.

If you find that you're being throttled on the number of POST requests for documents being submitted, consider adding a delay between the requests. If your workload requires a higher degree of concurrent processing, you then need to create a support request to increase your service limits on transactions per second.

Generally, we recommended testing the workload and the workload patterns before going to production.

## Next steps

> [!div class="nextstepaction"]
> [Learn about error codes and troubleshooting](v3-error-guide.md)
