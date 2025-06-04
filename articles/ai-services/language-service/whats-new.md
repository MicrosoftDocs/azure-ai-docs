---
title: What's new in Azure AI Language?
titleSuffix: Azure AI services
description: Find out about new releases and features for the Azure AI Language.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: whats-new
ms.date: 06/02/2025
ms.author: lajanuar
---

# What's new in Azure AI Language?

Azure AI Language is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

## May 2025

* **New agent templates**. Azure AI Language now supports the following agent templates:

    *   [Intent routing](../agents/concepts/agent-catalog.md) detects user intent and provides exact answering. Perfect for deterministically intent routing and exact question answering with human controls.
    *   [Exact question answering](../agents/concepts/agent-catalog.md) answers high-value predefined questions deterministically to ensure consistent and accurate responses.

* **Personally-identifiable-information updates**. Azure AI Language now offers PII detection customization and entity subtype support.

    *    [Customizing PII detection using your own regex](personally-identifiable-information/how-to/adapt-to-domain-pii.md#customizing-pii-detection-using-your-own-regex-only-available-for-text-pii-container) (only available for Text PII container)
    *   Support for customizing PII output by [specifying values to exclude](personally-identifiable-information/how-to/adapt-to-domain-pii.md#customizing-pii-output-by-specifying-values-to-exclude)
    *    Customizing PII detection using [entity synonyms](personally-identifiable-information/how-to/adapt-to-domain-pii.md#api-schema-for-the-entitysynoyms-parameter)
* [`2025-05-15-preview`](/rest/api/language/operation-groups?view=rest-language-2025-05-15-preview) release. This API preview version includes the following named entity recognition (NER) and personally identifiable information (PII) detection updates:

    * New entity type support for `DateOfBirth`, `BankAccountNumber`, `PassportNumber`, and `DriversLicenseNumber`
    * Enhanced AI quality for `PhoneNumber` entity type

To Learn more, see our latest [TechCommunity Blog Post](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/announcing-azure-ai-language-new-features-to-accelerate-your-agent-development/4415216).


## April 2025

* Updated and improved model GA release for NER
* Expanded context window for [PII redaction](personally-identifiable-information/overview.md?tabs=text-pii) – This service update expands the window of detection the PII redaction service considers, enhancing quality and accuracy.
* Added prediction capability for custom models, including conversational language Understanding (CLU), custom named entity recognition (NER), and custom text classification, are now available in three new regions: Jio India Central, UK West, and Canada East.
* Scanned PDF PII - [Document input for PII redaction](personally-identifiable-information/how-to/redact-document-pii.md) now supports scanned PDFs, enabling PII detection and redaction in both digital and nondigital documents using `OCR`.

## March 2025

* Azure AI Language resource now can be deployed to three new regions, Jio India Central, UK West, and Canada East, for the following capabilities:
    * Language detection
    * Sentiment analysis
    * Key phrase extraction
    * Named entity recognition (NER)
    * Personally identifiable information (PII) entity recognition
    * Entity linking
    * Text analytics for health
    * Extractive text summarization

* Back-end infrastructure for the Named entity recognition (NER) and Text Personally identifiable information (PII) entity recognition models is now updated with extended context window limits.

* Our [Conversational PII redaction](personally-identifiable-information/how-to/redact-conversation-pii.md?tabs=client-libraries) service is now powered by an upgraded GA model. This revised version enhances the quality and accuracy of Credit Card Number entities and Numeric Identification entities. These entities include Social Security numbers, Driver's license numbers, Policy numbers, Medicare Beneficiary Identifiers, and Financial account numbers.

## February 2025

* Document and text abstractive summarization is now powered by fine-tuned Phi-3.5-mini! Check out the [Announcing Blog](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/exciting-update-abstractive-summarization-in-azure-ai-language-now-powered-by-ph/4369025) for more information.
* More skills are available in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs): Extract key phrase, Extract named entities, Analyze sentiment, and Detect language. More skills are yet to come.

## January 2025

* .NET SDK for Azure AI Language text analytics, [Azure.AI.Language.Text 1.0.0-beta.2](https://www.nuget.org/packages/Azure.AI.Language.Text/1.0.0-beta.2#readme-body-tab), is now available. This client library supports the latest REST API version, `2024-11-01`, and `2024-11-15-preview`, for the following features:
    * Language detection
    * Sentiment analysis
    * Key phrase extraction
    * Named entity recognition (NER)
    * Personally identifiable information (PII) entity recognition
    * Entity linking
    * Text analytics for health
    * Custom named entity recognition (Custom NER)
    * Custom text classification
    * Extractive text summarization
    * Abstractive text summarization
* Custom sentiment analysis (preview), custom text analytics for health (preview) and custom summarization (preview) were retired on January 10, 2025, as Azure AI features are constantly evaluated based on customer demand and feedback. Based on the customers' feedback of these preview features, Microsoft is retiring this feature and prioritize new custom model features using the power of generative AI to better serve customers' needs.

## November 2024

* Azure AI Language is moving to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). These skills are now available in AI Foundry playground: Extract health information, Extract PII from conversation, Extract PII from text, Summarize text, Summarize conversation, Summarize for call center. More skills follow.
* Runtime Container for Conversational Language Understanding (CLU) is available for on-premises connections.
* Both our [Text PII redaction service](personally-identifiable-information/overview.md?tabs=text-pii) and our Conversational PII service preview API (version 2024-11-15-preview) now support the option to mask detected sensitive entities with a label beyond just redaction characters. Customers can specify if personal data content such as names and phone numbers, that is, "John Doe received a call from 424-878-9192" are masked with a redaction character, that is, "******** received a call from ************" or masked with an entity label, that is, "`PERSON_1` received a call from `PHONENUMBER_1`." More on how to specify the redaction policy style for your outputs can be found in our [how-to guides](personally-identifiable-information/how-to-call.md).
* Native document support gating is removed with the latest API version, 2024-11-15-preview, allowing customers to access native document support for PII redaction and summarization. Key updates in this version include:
    * Increased Maximum File Size Limits (from 1 MB to 10 MB).
    * Enhanced PII Redaction Customization: Customers can now specify whether they want only the redacted document or both the redacted document and a JSON file containing the detected entities.
* Language detection is a built-in feature designed to identify the language in which a document is written. It provides a language code that corresponds to a wide array of languages. This feature includes not only standard languages but also their variants, dialects, and certain regional or cultural languages. Today the general availability of [script detection capability](language-detection/how-to/call-api.md#script-name-and-script-code), and 16 more languages support, which adds up to [139 total supported languages](language-detection/language-support.md) is announced.
* [Named Entity Recognition service](named-entity-recognition/overview.md), [Entity Resolution](named-entity-recognition/concepts/entity-resolutions.md) was upgraded to the Entity Metadata starting in API version 2023-04-15-preview. If you're calling the preview version of the API equal or newer than 2023-04-15-preview, check out the Entity Metadata article to use the resolution feature. The service now supports the ability to specify a list of entity tags to be included into the response or excluded from the response. If a piece of text is classified as more than one entity type, the overlapPolicy parameter allows customers to specify how the service handles the overlap. The `inferenceOptions` parameter enables users to modify the inference process, such as preventing detected entity values from being normalized and added to the metadata. Along with these optional input parameters, we support an updated output structure (with new fields tags, type, and metadata) to ensure enhanced user customization and deeper analysis Learn more on our documentation.
* Text Analytics for Health (TA4H) is a specialized tool designed to extract and categorize key medical details from unstructured sources. These sources include doctor's notes, discharge summaries, clinical documentation, and electronic health records. Today, we released support for Fast Healthcare Interoperability Resources (FHIR) structuring and temporal [assertion detection](text-analytics-for-health/concepts/assertion-detection.md) in the Generally Available API.

## October 2024

* Custom language service features enable you to deploy your project to multiple [resources within a single region](concepts/custom-features/multi-region-deployment.md) via the API.

## September 2024

* PII detection now has container support. See more details in the Azure Update post: [Announcing Text PII Redaction Container Release](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/announcing-text-pii-redaction-container-release/4264655).
* Custom sentiment analysis (preview) will be retired January 10, 2025. You can transition to other custom model training services, such as custom text classification in Azure AI Language.  See more details in the Azure Update post: [Retirement: Announcing upcoming retirement of custom sentiment analysis (preview) in Azure AI Language (microsoft.com)](https://azure.microsoft.com/updates/v2/custom-sentiment-analysis-retirement).
* Custom text analytics for health (preview) will be retired on January 10, 2025. Transition to other custom model training services, such as custom named entity recognition in Azure AI Language, by that date.  See more details in the Azure Update post: [Retirement: Announcing upcoming retirement of custom text analytics for health (preview) in Azure AI Language (microsoft.com)](https://azure.microsoft.com/updates/v2/custom-text-analytics-for-health-retirement).

## August 2024
* [CLU utterance limit in a project](conversational-language-understanding/service-limits.md#data-limits) increased from 25,000 to 50,000.
* [CLU new version of training configuration, version 2024-08-01-preview, is available now](conversational-language-understanding/concepts/best-practices.md#address-out-of-domain-utterances), which improves the quality of intent identification for out of domain utterances.

## July 2024

* [Conversational PII redaction](https://techcommunity.microsoft.com/blog/ai-azure-ai-services-blog/announcing-conversational-pii-detection-service-s-general/4162881) service in English-language contexts is now Generally Available (GA).
* Conversation Summarization now supports 12 added languages in preview as listed [here](summarization/language-support.md).
* Summarization Meeting or Conversation Chapter titles features support reduced length to focus on the key topics.
* Enable support for data augmentation for diacritics to generate variations of training data for diacritic variations used in some natural languages which are especially useful for Germanic and Slavic languages.

## February 2024

* Expanded [language detection](./language-detection/how-to/call-api.md#script-name-and-script-code) support for added scripts according to the [ISO 15924 standard](https://wikipedia.org/wiki/ISO_15924) is now available starting in API version `2023-11-15-preview`.

## January 2024

* [Native document support](native-document-support/overview.md) is now available in `2023-11-15-preview` public preview.

## December 2023

* [Text Analytics for health](./text-analytics-for-health/overview.md) new model `2023-12-01` is now available.
* New Relation Type: `BodySiteOfExamination`
 * Quality enhancements to support radiology documents
 * Significant latency improvements
 * Various bug fixes: Improvements across NER, Entity Linking, Relations, and Assertion Detection

## November 2023

* [Named Entity Recognition Container](./named-entity-recognition/how-to/use-containers.md) is now Generally Available (GA).

## July 2023

* [Custom sentiment analysis](./sentiment-opinion-mining/overview.md) is now available in preview.

## May 2023

* [Custom Named Entity Recognition (NER) Docker containers](./custom-named-entity-recognition/how-to/use-containers.md) are now available for on-premises deployment.

## April 2023

* [Custom Text analytics for health](./custom-text-analytics-for-health/overview.md) is available in public preview, which enables you to build custom AI models to extract healthcare specific entities from unstructured text
* You can now use Azure OpenAI to automatically label or generate data during authoring. Learn more with the following links:
    * Autolabel your documents in [Custom text classification](./custom-text-classification/how-to/use-autolabeling.md) or [Custom named entity recognition](./custom-named-entity-recognition/how-to/use-autolabeling.md).
    * Generate suggested utterances in [Conversational language understanding](./conversational-language-understanding/how-to/tag-utterances.md#suggest-utterances-with-azure-openai).
* The latest model version (`2022-10-01`) for Language Detection now supports 6 more International languages and 12 Romanized Indic languages.

## March 2023

* New model version ('2023-01-01-preview') for Personally Identifiable Information (PII) detection with quality updates and new [language support](./personally-identifiable-information/language-support.md)

* New versions of the text analysis client library are available in preview:

    ### [C#](#tab/csharp)

    [**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.3.0-beta.2)

    [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.TextAnalytics_5.3.0-beta.2/sdk/textanalytics/Azure.AI.TextAnalytics/CHANGELOG.md)

    [**ReadMe**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.TextAnalytics_5.3.0-beta.2/sdk/textanalytics/Azure.AI.TextAnalytics/README.md)

    [**Samples**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.TextAnalytics_5.3.0-beta.2/sdk/textanalytics/Azure.AI.TextAnalytics/samples/README.md)

    ### [Java](#tab/java)

    [**Package (Maven)**](https://mvnrepository.com/artifact/com.azure/azure-ai-textanalytics/5.3.0-beta.2)

    [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md#530-beta2-2023-03-07)

    [**ReadMe**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/README.md)

    [**Samples**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/textanalytics/azure-ai-textanalytics/src/samples)

    ### [JavaScript](#tab/javascript)

    [**Package (npm)**](https://www.npmjs.com/package/@azure/ai-language-text/v/1.1.0-beta.2)

    [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/cognitivelanguage/ai-language-text/CHANGELOG.md)

    [**ReadMe**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cognitivelanguage/ai-language-text)

    [**Samples**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cognitivelanguage/ai-language-text/samples/v1-beta)

    ### [Python](#tab/python)

    [**Package (PyPi)**](https://pypi.org/project/azure-ai-textanalytics/5.3.0b2/)

    [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0b2/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md)

    [**ReadMe**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0b2/sdk/textanalytics/azure-ai-textanalytics/README.md)

    [**Samples**](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-textanalytics_5.3.0b2/sdk/textanalytics/azure-ai-textanalytics/samples)

    ---

## February 2023

* Conversational language understanding and orchestration workflow now available in the following regions in the sovereign cloud for China:
  * China East 2 (Authoring and Prediction)
  * China North 2 (Prediction)
* New model evaluation updates for Conversational language understanding and Orchestration workflow.
* New model version ('2023-01-01-preview') for Text Analytics for health featuring new [entity categories](./text-analytics-for-health/concepts/health-entity-categories.md) for social determinants of health.
* New model version ('2023-02-01-preview') for named entity recognition features improved accuracy and more [language support](./named-entity-recognition/language-support.md) with up to 79 languages.

## December 2022

* New version (v5.2.0-beta.1) of the text analysis client library is available in preview for C#/.NET:
    * [**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.3.0-beta.1)
    * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/CHANGELOG.md)
    * [**ReadMe**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/README.md)
    * [**Samples**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/textanalytics/Azure.AI.TextAnalytics/samples)
 * New model version (`2022-10-01`) released for Language Detection. The new model version comes with improvements in language detection quality on short texts.

## November 2022

* Expanded language support for:
    * [Opinion mining](./sentiment-opinion-mining/language-support.md)
* Conversational PII now supports up to 40,000 characters as document size.
* New versions of the text analysis client library are available in preview:

    * Java
        * [**Package (Maven)**](https://mvnrepository.com/artifact/com.azure/azure-ai-textanalytics/5.3.0-beta.1)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-textanalytics_5.3.0-beta.1/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-textanalytics_5.3.0-beta.1/sdk/textanalytics/azure-ai-textanalytics/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-java/tree/azure-ai-textanalytics_5.3.0-beta.1/sdk/textanalytics/azure-ai-textanalytics/src/samples)

    * JavaScript
        * [**Package (npm)**](https://www.npmjs.com/package/@azure/ai-language-text/v/1.1.0-beta.1)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/cognitivelanguage/ai-language-text/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/cognitivelanguage/ai-language-text/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cognitivelanguage/ai-language-text/samples/v1)

    * Python
        * [**Package (PyPi)**](https://pypi.org/project/azure-ai-textanalytics/5.3.0b1/)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0b1/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0b1/sdk/textanalytics/azure-ai-textanalytics/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-textanalytics_5.3.0b1/sdk/textanalytics/azure-ai-textanalytics/samples)

## October 2022

* The summarization feature now has the following capabilities:
    * [Document summarization](./summarization/overview.md):
        * Abstractive summarization, which generates a summary of a document that can't use the same words as presented in the document, but captures the main idea.
    * [Conversation summarization](./summarization/overview.md?tabs=document-summarization?tabs=conversation-summarization)
        * Chapter title summarization, which returns suggested chapter titles of input conversations.
        * Narrative summarization, which returns call notes, meeting notes or chat summaries of input conversations.
* Expanded language support for:
    * [Sentiment analysis](./sentiment-opinion-mining/language-support.md)
    * [Key phrase extraction](./key-phrase-extraction/language-support.md)
    * [Named entity recognition](./named-entity-recognition/language-support.md)
    * [Text Analytics for health](./text-analytics-for-health/language-support.md)
* [Multi-region deployment](./concepts/custom-features/multi-region-deployment.md) and [project asset versioning](./concepts/custom-features/project-versioning.md) for:
    * [Conversational language understanding](./conversational-language-understanding/overview.md)
    * [Orchestration workflow](./orchestration-workflow/overview.md)
    * [Custom text classification](./custom-text-classification/overview.md)
    * [Custom named entity recognition](./custom-named-entity-recognition/overview.md)
* [Regular expressions](./conversational-language-understanding/concepts/entity-components.md#regex-component) in conversational language understanding and [required components](./conversational-language-understanding/concepts/entity-components.md#required-components), offering an added ability to influence entity predictions.
* [Entity resolution](./named-entity-recognition/concepts/entity-resolutions.md) in named entity recognition
* New region support for:
    * [Conversational language understanding](./conversational-language-understanding/service-limits.md#regional-availability)
    * [Orchestration workflow](./orchestration-workflow/service-limits.md#regional-availability)
    * [Custom text classification](./custom-text-classification/service-limits.md#regional-availability)
    * [Custom named entity recognition](./custom-named-entity-recognition/service-limits.md#regional-availability)
* Document type as an input supported for [Text Analytics for health](./text-analytics-for-health/how-to/call-api.md) FHIR requests

## September 2022

* [Conversational language understanding](./conversational-language-understanding/overview.md) is available in the following regions:
  * Central India
  * Switzerland North
  * West US 2
* Text Analytics for Health now [supports more languages](./text-analytics-for-health/language-support.md) in preview: Spanish, French, German Italian, Portuguese and Hebrew. These languages are available when using a docker container to deploy the API service.
* The Azure.AI.TextAnalytics client library v5.2.0 are generally available and ready for use in production applications. For more information on Language service client libraries, see the [**Developer overview**](./concepts/developer-guide.md).
    * Java
        * [**Package (Maven)**](https://mvnrepository.com/artifact/com.azure/azure-ai-textanalytics/5.2.0)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/textanalytics/azure-ai-textanalytics/src/samples)
    * Python
        * [**Package (PyPi)**](https://pypi.org/project/azure-ai-textanalytics/5.2.0/)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics/samples)
    * C#/.NET
        * [**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.2.0)
        * [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/CHANGELOG.md)
        * [**ReadMe**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/README.md)
        * [**Samples**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/textanalytics/Azure.AI.TextAnalytics/samples)

## August 2022

* [Role-based access control](./concepts/role-based-access-control.md) for the Language service.

## July 2022

* New AI models for [sentiment analysis](./sentiment-opinion-mining/overview.md) and [key phrase extraction](./key-phrase-extraction/overview.md) based on [z-code models](https://www.microsoft.com/research/project/project-zcode/), providing:
    * Performance and quality improvements for the following 11 [languages](./sentiment-opinion-mining/language-support.md) supported by sentiment analysis: `ar`, `da`, `el`, `fi`, `hi`, `nl`, `no`, `pl`,  `ru`, `sv`, `tr`
    * Performance and quality improvements for the following 20 [languages](./key-phrase-extraction/language-support.md) supported by key phrase extraction: `af`, `bg`, `ca`, `hr`, `da`, `nl`, `et`, `fi`, `el`, `hu`, `id`, `lv`, `no`, `pl`, `ro`, `ru`, `sk`, `sl`, `sv`, `tr`

* Conversational PII is now available in all Azure regions supported by the Language service.

* A new version of the Language API (`2022-07-01-preview`) is available. It provides:
    * [Automatic language detection](./concepts/use-asynchronously.md#automatic-language-detection) for asynchronous tasks.
    * Text Analytics for health confidence scores are now returned in relations.

    To use this version in your REST API calls, use the following URL:

    ```http
    <your-language-resource-endpoint>/language/:analyze-text?api-version=2022-07-01-preview
    ```

## June 2022
* v1.0 client libraries for [conversational language understanding](./conversational-language-understanding/how-to/call-api.md?tabs=azure-sdk#send-a-conversational-language-understanding-request) and [orchestration workflow](./orchestration-workflow/how-to/call-api.md?tabs=azure-sdk#send-an-orchestration-workflow-request) are Generally Available for the following languages:
    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Language.Conversations_1.0.0/sdk/cognitivelanguage/Azure.AI.Language.Conversations)
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-language-conversations_1.0.0/sdk/cognitivelanguage/azure-ai-language-conversations)
* v1.1.0b1 client library for [conversation summarization](summarization/quickstart.md?tabs=conversation-summarization&pivots=programming-language-python) is available as a preview for:
    * [Python](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-language-conversations_1.1.0b1/sdk/cognitivelanguage/azure-ai-language-conversations/samples/README.md)
* There's a new endpoint URL and request format for making REST API calls to prebuilt Language service features. See the following quickstart guides and reference documentation for information on structuring your API calls. All text analytics `3.2-preview.2` API users can begin migrating their workloads to this new endpoint.
    * [Entity linking](./entity-linking/quickstart.md?pivots=rest-api)
    * [Language detection](./language-detection/quickstart.md?pivots=rest-api)
    * [Key phrase extraction](./key-phrase-extraction/quickstart.md?pivots=rest-api)
    * [Named entity recognition](./named-entity-recognition/quickstart.md?pivots=rest-api)
    * [PII detection](./personally-identifiable-information/quickstart.md?pivots=rest-api)
    * [Sentiment analysis and opinion mining](./sentiment-opinion-mining/quickstart.md?pivots=rest-api)
    * [Text analytics for health](./text-analytics-for-health/quickstart.md?pivots=rest-api)


## May 2022

* PII detection for conversations.
* Rebranded Text Summarization to Document summarization.
* Conversation summarization is now available in public preview.

* The following features are now Generally Available (GA):
    * Custom text classification
    * Custom Named Entity Recognition (NER)
    * Conversational language understanding
    * Orchestration workflow

* The following updates for custom text classification, custom Named Entity Recognition (NER), conversational language understanding, and orchestration workflow:
    * Data splitting controls.
    * Ability to cancel training jobs.
    * Custom deployments can be named. You can have up to 10 deployments.
    * Ability to swap deployments.
    * Auto labeling (preview) for custom named entity recognition
    * Enterprise readiness support
    * Training modes for conversational language understanding
    * Updated service limits
    * Ability to use free (F0) tier for Language resources
    * Expanded regional availability
    * Updated model life cycle to add training configuration versions



## April 2022

* Fast Healthcare Interoperability Resources (FHIR) support is available in the [Language REST API preview](text-analytics-for-health/quickstart.md?pivots=rest-api&tabs=language) for Text Analytics for health.

## March 2022

* Expanded language support for:
  * [Custom text classification](custom-text-classification/language-support.md)
  * [Custom Named Entity Recognition (NER)](custom-named-entity-recognition/language-support.md)
  * [Conversational language understanding](conversational-language-understanding/language-support.md)

## February 2022

* Model improvements for latest model-version for [text summarization](summarization/overview.md)

* Model `2021-10-01` is Generally Available (GA) for [Sentiment Analysis and Opinion Mining](sentiment-opinion-mining/overview.md), featuring enhanced modeling for emojis and better accuracy across all supported languages.

* [Question Answering](question-answering/overview.md): Active learning v2 incorporates a better clustering logic providing improved accuracy of suggestions. It considers user actions when suggestions are accepted or rejected to avoid duplicate suggestions, and improve query suggestions.

## December 2021

* The version 3.1-preview.x REST endpoints and 5.1.0-beta.x client library are retired. Upgrade to the General Available version of the API(v3.1). If you're using the client libraries, use package version 5.1.0 or higher. See the [migration guide](./concepts/migrate-language-service-latest.md) for details.

## November 2021

* Based on ongoing customer feedback, we increased the character limit per document for Text Analytics for health from 5,120 to 30,720.

* Azure AI Language release, with support for:

  * [Question Answering (now Generally Available)](question-answering/overview.md)
  * [Sentiment Analysis and opinion mining](sentiment-opinion-mining/overview.md)
  * [Key Phrase Extraction](key-phrase-extraction/overview.md)
  * [Named Entity Recognition (NER), Personally Identifying Information (PII)](named-entity-recognition/overview.md)
  * [Language Detection](language-detection/overview.md)
  * [Text Analytics for health](text-analytics-for-health/overview.md)
  * [Text summarization preview](summarization/overview.md)
  * [Custom Named Entity Recognition (Custom NER) preview](custom-named-entity-recognition/overview.md)
  * [Custom Text Classification preview](custom-text-classification/overview.md)
  * [Conversational Language Understanding preview](conversational-language-understanding/overview.md)

* Preview model version `2021-10-01-preview` for [Sentiment Analysis and Opinion mining](sentiment-opinion-mining/overview.md), which provides:

  * Improved prediction quality.
  * [Added language support](sentiment-opinion-mining/language-support.md?tabs=sentiment-analysis) for the opinion mining feature.
  * For more information, see the [project z-code site](https://www.microsoft.com/research/project/project-zcode/).
  * To use this [model version](sentiment-opinion-mining/how-to/call-api.md#specify-the-sentiment-analysis-model), you must specify it in your API calls, using the model version parameter.

* SDK support for sending requests to custom models:

  * Custom Named Entity Recognition
  * Custom text classification
  * Custom language understanding

## Next steps

* See the [previous updates](./concepts/previous-updates.md) article for service updates not listed here.
