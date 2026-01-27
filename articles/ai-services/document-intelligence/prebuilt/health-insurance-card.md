---
title: Health insurance card processing - Document Intelligence 
titleSuffix: Foundry Tools
description: Data extraction and analysis extraction using the health insurance card model
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: 'doc-intel-4.0.0 || >=doc-intel-3.0.0'
---


# Document Intelligence health insurance card model

**This content applies to:**![checkmark](../media/yes-icon.png) **v4.0** | **Previous versions:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru) ![blue-checkmark](../media/blue-yes-icon.png) [**v3.0 (GA)**](?view=doc-intel-3.0.0&preserve-view=tru)
::: moniker-end

::: moniker range="doc-intel-3.1.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)** | **Latest version:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0**](?view=doc-intel-4.0.0&preserve-view=true) | **Previous versions:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.0**](?view=doc-intel-3.0.0&preserve-view=true)
::: moniker-end

::: moniker range="doc-intel-3.0.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.0 (GA)** | **Latest versions:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0**](?view=doc-intel-4.0.0&preserve-view=true) ![purple-checkmark](../media/purple-yes-icon.png) [**v3.1**](?view=doc-intel-3.1.0&preserve-view=true)
::: moniker-end

The Document Intelligence health insurance card model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract key information from US health insurance cards. A health insurance card is a key document for care processing. It can be digitally analyzed for patient onboarding, financial coverage information, cashless payments, and insurance claim processing. The health insurance card model analyzes health card images; extracts key information such as insurer, member, prescription, and group number; and returns a structured JSON representation. Health insurance cards can be presented in various formats and quality including phone-captured images, scanned documents, and digital PDFs.

***Sample health insurance card processed using Document Intelligence Studio***

:::image type="content" source="../media/studio/health-insurance-card.png" alt-text="Screenshot of sample health insurance card processed in the Document Intelligence Studio.":::

## Development options

::: moniker range="doc-intel-4.0.0"


Document Intelligence v4.0: **2024-11-30** (GA) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Health insurance card model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**prebuilt-healthInsuranceCard.us**|
::: moniker-end

::: moniker range="doc-intel-3.1.0"

Document Intelligence v3.1 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Health insurance card model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)|**prebuilt-healthInsuranceCard.us**|
::: moniker-end

::: moniker range="doc-intel-3.0.0"

Document Intelligence v3.0 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Health insurance card model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)|**prebuilt-healthInsuranceCard.us**|
::: moniker-end

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

### Try Document Intelligence Studio

See how data is extracted from health insurance cards using the Document Intelligence Studio. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

> [!NOTE]
> Document Intelligence Studio is available with API version v3.0.

1. On the [Document Intelligence Studio home page](https://formrecognizer.appliedai.azure.com/studio), select **Health insurance cards**.

1. You can analyze the sample insurance card document or select the **➕ Add** button to upload your own sample.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

    > [!div class="nextstepaction"]
    > [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=healthInsuranceCard.us).

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extraction

For supported document extraction fields, *see* the [health insurance card model schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-11-30-ga/health-insurance-card.md) page in our GitHub sample repository.

### Migration guide and REST API v3.1

* Follow our [**Document Intelligence v3.1 migration guide**](../v3-1-migration-guide.md) to learn how to use the v3.1 version in your applications and workflows.

* Explore our [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP) to learn more about the v3.1 version and new capabilities.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
