---
title: What is Azure AI Content Safety? 
titleSuffix: Azure AI services
description: Learn how to use Content Safety to track, flag, assess, and filter inappropriate material in user-generated content.
#services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: overview
ms.date: 09/04/2024
ms.author: pafarley
keywords: content safety, Azure AI Content Safety, online content safety, content filtering software, content moderation service, content moderation
ms.custom: references_regions, build-2023, build-2023-dataai
#Customer intent: As a developer of content management software, I want to find out whether Azure AI Content Safety is the right solution for my moderation needs.
---

# What is Azure AI Content Safety? 

Azure AI Content Safety is an AI service that detects harmful user-generated and AI-generated content in applications and services. Azure AI Content Safety includes text and image APIs that allow you to detect material that is harmful. The interactive Content Safety Studio allows you to view, explore, and try out sample code for detecting harmful content across different modalities.

Content filtering software can help your app comply with regulations or maintain the intended environment for your users.

This documentation contains the following article types:  
* **[Concepts](concepts/harm-categories.md)** provide in-depth explanations of the service functionality and features.  
* **[Quickstarts](./quickstart-text.md)** are getting-started instructions to guide you through making requests to the service.  
* **[How-to guides](./how-to/use-blocklist.md)** contain instructions for using the service in more specific or customized ways.  

## Where it's used

The following are a few scenarios in which a software developer or team would require a content moderation service:

- User prompts submitted to a generative AI service. 
- Content produced by generative AI models.
- Online marketplaces that moderate product catalogs and other user-generated content.
- Gaming companies that moderate user-generated game artifacts and chat rooms.
- Social messaging platforms that moderate images and text added by their users.
- Enterprise media companies that implement centralized moderation for their content.
- K-12 education solution providers filtering out content that is inappropriate for students and educators.

> [!IMPORTANT]
> You cannot use Azure AI Content Safety to detect illegal child exploitation images.

## Product features

This service makes several different types of analysis available. The following table describes the currently available APIs.

| Feature    | Functionality    | Concepts guide | Get started |
| :- | :-- | --| --| 
| [Prompt Shields](/rest/api/contentsafety/text-operations/detect-text-jailbreak) | Scans text for the risk of a User input attack on a Large Language Model. | [Prompt Shields concepts](/azure/ai-services/content-safety/concepts/jailbreak-detection)|[Quickstart](./quickstart-jailbreak.md) |
| [Groundedness detection](/rest/api/contentsafety/text-groundedness-detection-operations/detect-groundedness-options) (preview) | Detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. | [Groundedness detection concepts](/azure/ai-services/content-safety/concepts/groundedness)|[Quickstart](./quickstart-groundedness.md) |
| [Protected material text detection](/rest/api/contentsafety/text-operations/detect-text-protected-material) | Scans AI-generated text for known text content (for example, song lyrics, articles, recipes, selected web content). | [Protected material concepts](/azure/ai-services/content-safety/concepts/protected-material)|[Quickstart](./quickstart-protected-material.md)|
| Custom categories (standard) API (preview)    | Lets you create and train your own custom content categories and scan text for matches. | [Custom categories concepts](/azure/ai-services/content-safety/concepts/custom-categories)|[Quickstart](./quickstart-custom-categories.md) |
| Custom categories (rapid) API (preview) | Lets you define emerging harmful content patterns and scan text and images for matches. | [Custom categories concepts](/azure/ai-services/content-safety/concepts/custom-categories)| [How-to guide](./how-to/custom-categories-rapid.md) |
| [Analyze text](/rest/api/contentsafety/text-operations/analyze-text) API   | Scans text for sexual content, violence, hate, and self harm with multi-severity levels. | [Harm categories](/azure/ai-services/content-safety/concepts/harm-categories)| [Quickstart](/azure/ai-services/content-safety/quickstart-text) |
| [Analyze image](/rest/api/contentsafety/image-operations/analyze-image) API  | Scans images for sexual content, violence, hate, and self harm with multi-severity levels. | [Harm categories](/azure/ai-services/content-safety/concepts/harm-categories)| [Quickstart](/azure/ai-services/content-safety/quickstart-image) |


## Content Safety Studio

[Azure AI Content Safety Studio](https://contentsafety.cognitive.azure.com) is an online tool designed to handle potentially offensive, risky, or undesirable content using cutting-edge content moderation ML models. It provides templates and customized workflows, enabling users to choose and build their own content moderation system. Users can upload their own content or try it out with provided sample content.

Content Safety Studio not only contains out-of-the-box AI models but also includes **Microsoft's built-in terms blocklists** to flag profanities and stay up to date with new content trends. You can also upload your own blocklists to enhance the coverage of harmful content that's specific to your use case. 

Studio also lets you set up a **moderation workflow**, where you can continuously monitor and improve content moderation performance. It can help you meet content requirements from all kinds of industries like gaming, media, education, E-commerce, and more. Businesses can easily connect their services to the Studio and have their content moderated in real-time, whether user-generated or AI-generated.

All of these capabilities are handled by the Studio and its backend; customers don’t need to worry about model development. You can onboard your data for quick validation and monitor your KPIs accordingly, like technical metrics (latency, accuracy, recall), or business metrics (block rate, block volume, category proportions, language proportions, and more). With simple operations and configurations, customers can test different solutions quickly and find the best fit, instead of spending time experimenting with custom models or doing moderation manually. 

> [!div class="nextstepaction"]
> [Try Content Safety Studio](https://contentsafety.cognitive.azure.com)


### Content Safety Studio features

In Content Safety Studio, the following Azure AI Content Safety features are available:

* **[Moderate Text Content](https://contentsafety.cognitive.azure.com/text)**: With the text moderation tool, you can easily run tests on text content. Whether you want to test a single sentence or an entire dataset, our tool offers a user-friendly interface that lets you assess the test results directly in the portal. You can experiment with different sensitivity levels to configure your content filters and blocklist management, ensuring that your content is always moderated to your exact specifications. Plus, with the ability to export the code, you can implement the tool directly in your application, streamlining your workflow and saving time.

* **[Moderate Image Content](https://contentsafety.cognitive.azure.com/image)**: With the image moderation tool, you can easily run tests on images to ensure that they meet your content standards. Our user-friendly interface allows you to evaluate the test results directly in the portal, and you can experiment with different sensitivity levels to configure your content filters. Once you've customized your settings, you can easily export the code to implement the tool in your application.

* **[Monitor Online Activity](https://contentsafety.cognitive.azure.com/monitor)**: The powerful monitoring page allows you to easily track your moderation API usage and trends across different modalities. With this feature, you can access detailed response information, including category and severity distribution, latency, error, and blocklist detection. This information provides you with a complete overview of your content moderation performance, enabling you to optimize your workflow and ensure that your content is always moderated to your exact specifications. With our user-friendly interface, you can quickly and easily navigate the monitoring page to access the information you need to make informed decisions about your content moderation strategy. You have the tools you need to stay on top of your content moderation performance and achieve your content goals.

## Security

<a name='use-azure-active-directory-or-managed-identity-to-manage-access'></a>

### Use Microsoft Entra ID or Managed Identity to manage access

For enhanced security, you can use Microsoft Entra ID or Managed Identity (MI) to manage access to your resources.
* Managed Identity is automatically enabled when you create a Content Safety resource.
* Microsoft Entra ID is supported in both API and SDK scenarios. Refer to the general AI services guideline of [Authenticating with Microsoft Entra ID](/azure/ai-services/authentication?tabs=powershell#authenticate-with-azure-active-directory). You can also grant access to other users within your organization by assigning them the roles of **Cognitive Services Users** and **Reader**. To learn more about granting user access to Azure resources using the Azure portal, refer to the [Role-based access control guide](/azure/role-based-access-control/quickstart-assign-role-user-portal).

### Encryption of data at rest

Learn how Azure AI Content Safety handles the [encryption and decryption of your data](./how-to/encrypt-data-at-rest.md). Customer-managed keys (CMK), also known as Bring Your Own Key (BYOK), offer greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data.

## Pricing

Currently, Azure AI Content Safety has an **F0** and **S0** pricing tier. See the Azure [pricing page](https://aka.ms/content-safety-pricing) for more information.

## Service limits

> [!CAUTION]
> **Deprecation Notice**
>
> As part of Content Safety versioning and lifecycle management, we are announcing the deprecation of certain Public Preview and GA versions of our service APIs. Following our deprecation policy:
> * **Public Preview versions**: Each new Public Preview version will trigger the deprecation of the previous preview version after a 90-day period, provided no breaking changes are introduced.
> * **GA versions**: When a new GA version is released, the prior GA version will be deprecated after a 90-day period if compatibility is maintained.
>
> See the [What's new](./whats-new.md) page for upcoming deprecations.

### Input requirements

See the following list for the input requirements for each feature.

<!--
|  | Analyze text API | Analyze image API |  Prompt Shields<br> | Groundedness<br>detection (preview) | Protected material<br>detection |
|--|---|--|--|--|--|
| Input requirements:   | Default maximum length: 10K characters (split longer texts as needed). | Maximum image file size: 4 MB<br>Dimensions between 50x50 and 2048x2048 pixels.<br>Images can be in JPEG, PNG, GIF, BMP, TIFF, or WEBP formats. | Maximum prompt length: 10K characters.<br>Up to five documents with a total of 10D characters. | Maximum 55,000 characters for grounding sources per API call.<br>Maximum text and query length: 7,500 characters. | Default maximum: 1K characters.<br>Minimum: 111 characters (for scanning LLM completions, not user prompts). | -->

- **Analyze text API**: 
  - Default maximum length: 10K characters (split longer texts as needed).
- **Analyze image API**: 
  - Maximum image file size: 4 MB
  - Dimensions between 50 x 50 and 7200 x 7200 pixels.
  - Images can be in JPEG, PNG, GIF, BMP, TIFF, or WEBP formats.
- **Analyze multimodal API (preview)**:
  - Default maximum text length: 1K characters.
  - Maximum image file size: 4 MB
  - Dimensions between 50 x 50 and 7200 x 7200 pixels.
  - Images can be in JPEG, PNG, GIF, BMP, TIFF, or WEBP formats.
- **Prompt Shields API**: 
  - Maximum prompt length: 10K characters.
  - Up to five documents with a total of 10K characters.
- **Groundedness detection API (preview)**: 
  - Maximum length for grounding sources: 55,000 characters (per API call).
  - Maximum text and query length: 7,500 characters.
- **Protected material detection APIs**: 
  - Default maximum length: 1K characters.
  - Default minimum length: 110 characters (for scanning LLM completions, not user prompts).
- **Custom categories (standard) API (preview)**:
  - Maximum inference input length: 1K characters.


### Language support

[!INCLUDE [language-notice](includes/language-notice.md)]

For more information, see [Language support](/azure/ai-services/content-safety/language-support).

### Region availability

To use the Content Safety APIs, you must create your Azure AI Content Safety resource in a supported region. Currently, the Content Safety features are available in the following Azure regions with different API versions: 

| Region              | Custom Category    | Groundedness       | Image | Multimodal(Image with Tex) | Incident Response | Prompt Shield | Protected Material (Text) | Protected Material (Code) | Text | Unified API |
|--------------------|--------------------|--------------------|-------|-----------------|-------------------|---------------|---------------------------|---------------------------|------|-------------|
| Australia East                     | ✅                  |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Canada East                          |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Central US                             |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| East US                            | ✅                 |                  | ✅    | ✅              | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| East US 2                           |                    | ✅                 | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| France Central                        |                    | ✅                 | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Japan East                            |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| North Central US                      |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Poland Central                        |                    |                    | ✅    |                 |                   | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| South Central US                     |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| South India                           |                    |                    | ✅    |                 | ✅                 |               | ✅                         | ✅                         | ✅    | ✅           |
| Sweden Central                        |                    | ✅                 | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Switzerland North                     | ✅                 |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| Switzerland West                      |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    |             |
| UAE North                            |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    |             |
| UK South                             |                    | ✅                 | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| West Europe                          |                    |                    | ✅    | ✅              | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| West US                              |                    | ✅                 | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| West US 2                            |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| West US 3                            |                    |                    | ✅    |                 | ✅                 | ✅             | ✅                         | ✅                         | ✅    | ✅           |
| FairFax - USGovArizona|                                     |                    | ✅    |                 |                   | ✅             | ✅                         |                            | ✅    | ✅           |
| FairFax - USGovVirginia|                                   |                    | ✅    |                 |                   | ✅             | ✅                         |                            | ✅    | ✅           |

Feel free to [contact us](mailto:contentsafetysupport@microsoft.com) if your business needs other regions to be available.

### Query rates

Content Safety features have query rate limits in requests-per-second (RPS) or requests-per-10-seconds (RP10S) . See the following table for the rate limits for each feature.

|Pricing tier | Moderation APIs<br>(text and image) | Prompt Shields |  Protected material<br>detection | Groundedness<br>detection (preview) | Custom categories<br>(rapid) (preview) | Custom categories<br>(standard) (preview)|Multimodal |
|---|-|---|-|-|-|--|--|
| F0    | 5 RPS    | 5 RPS   | 5 RPS    | N/A | 5 RPS | 5 RPS|5 RPS|
| S0    | 1000 RP10S    | 1000 RP10S   | 1000 RP10S    | 50 RPS | 1000 RP10S | 5 RPS|10 RPS|

If you need a faster rate, please [contact us](mailto:contentsafetysupport@microsoft.com) to request it.


## Contact us

If you get stuck, [email us](mailto:contentsafetysupport@microsoft.com) or use the feedback widget at the bottom of any Microsoft Learn page.

## Next steps

Follow a quickstart to get started using Azure AI Content Safety in your application.

> [!div class="nextstepaction"]
> [Content Safety quickstart](./quickstart-text.md)
