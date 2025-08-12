---
title: Image Analysis SDK Overview
titleSuffix: Azure AI services
description: This page gives you an overview of the Azure AI Image Analysis SDK.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: overview
ms.date: 07/28/2025
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
ms.custom: devx-track-csharp
---

# Image Analysis SDK overview

The Image Analysis SDK provides a convenient way to access the Image Analysis service using [version 4.0 of the REST API](https://aka.ms/vision-4-0-ref).

> [!IMPORTANT]
> **Breaking Changes in SDK version 1.0.0-beta.1**
>
> The Image Analysis SDK was rewritten in version 1.0.0-beta.1 to better align with other Azure SDKs. All APIs are changed. See the updated [quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40), [samples](#github-samples), and [how-to-guides](/azure/ai-services/computer-vision/how-to/call-analyze-image-40) for information on how to use the new SDK.
>
> Major changes:
> - The SDK now calls the generally available [Computer Vision REST API (2023-10-01)](/rest/api/computervision/operation-groups?view=rest-computervision-2023-10-01&preserve-view=true), instead of the preview [Computer Vision REST API (2023-04-01-preview)](/rest/api/computervision/operation-groups?view=rest-computervision-2023-04-01-preview&preserve-view=true).
> - Support for JavaScript was added.
> - C++ is no longer supported.
> - Image Analysis with a custom model, and Image Segmentation (background removal) are no longer supported in the SDK, because the [Computer Vision REST API (2023-10-01)](/rest/api/computervision/operation-groups?view=rest-computervision-2023-10-01&preserve-view=true) doesn't yet support them. To use either feature, call the [Computer Vision REST API (2023-04-01-preview)](/rest/api/computervision/operation-groups?view=rest-computervision-2023-04-01-preview&preserve-view=true) directly (using the `Analyze` and `Segment` operations respectively).

## Supported languages

The Image Analysis SDK supports the following languages and platforms:

| Programming language | Quickstart | API Reference | Platform support |
|----------------------|------------|-----------|------------------|
| C# | [quickstart](../quickstarts-sdk/image-analysis-client-library-40.md?pivots=programming-language-csharp)  | [reference](https://aka.ms/azsdk/image-analysis/ref-docs/csharp) | Windows, Linux, macOS |
| Python | [quickstart](../quickstarts-sdk/image-analysis-client-library-40.md?pivots=programming-language-python) | [reference](https://aka.ms/azsdk/image-analysis/ref-docs/python) | Windows, Linux, macOS |
| Java | [quickstart](../quickstarts-sdk/image-analysis-client-library-40.md?pivots=programming-language-java) | [reference](https://aka.ms/azsdk/image-analysis/ref-docs/java) | Windows, Linux, macOS |
| JavaScript | [quickstart](../quickstarts-sdk/image-analysis-client-library-40.md?pivots=programming-language-js) | [reference](https://aka.ms/azsdk/image-analysis/ref-docs/js) | Windows, Linux, macOS |


## GitHub samples

Numerous code samples are available in the SDK repositories on GitHub.
- [C#](https://aka.ms/azsdk/image-analysis/samples/csharp)
- [Python](https://aka.ms/azsdk/image-analysis/samples/python)
- [Java](https://aka.ms/azsdk/image-analysis/samples/java)
- [JavaScript](https://aka.ms/azsdk/image-analysis/samples/js)


## Help and support

If you need assistance using the Image Analysis SDK or would like to report a bug or suggest new features, open a GitHub issue in the respective SDK repo. The SDK development team monitors these issues.
- [C#](https://github.com/Azure/azure-sdk-for-net/issues)
- [Python](https://github.com/Azure/azure-sdk-for-python/issues)
- [Java](https://github.com/Azure/azure-sdk-for-java/issues)
- [JavaScript](https://github.com/Azure/azure-sdk-for-js/issues)

Before you create a new issue:
* Make sure you first scan to see if a similar issue already exists.
* Find the sample closest to your scenario and run it to see if you see the same issue in the sample code.


## Next steps

- [Install the Image Analysis SDK](./install-sdk.md)
- [Follow the Image Analysis Quickstart](../quickstarts-sdk/image-analysis-client-library-40.md)
