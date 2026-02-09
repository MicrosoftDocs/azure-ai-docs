---
title: What's new in Azure Language in Foundry Tools?
titleSuffix: Foundry Tools
description: Stay informed about recent releases and enhancements designed to help you get the most out of Azure Language capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: whats-new
ms.date: 02/09/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# What's new in Azure Language in Foundry Tools?

Stay informed about recent releases and enhancements designed to help you get the most out of Azure Language capabilities. Azure Language in Foundry Tools is updated on an ongoing basis. Bookmark this page and stay up to date with release notes, feature enhancements, and our newest documentation.

## February 2026

* **Text PII detection quality improvement**. Backend validation for the Phone Number entity type is updated to broaden detection coverage, resulting in improved recall across supported languages. This change is applied at the service level and requires no updates to your API calls or request parameters.

* **Orchestration workflow playground update**. The Foundry playground experience for orchestration workflow introduces a redesigned task-linking interface. The **Schema definition** page previously available in Language Studio is replaced by the **Configure orchestration** page, which provides a streamlined way to associate fine-tuning tasks with an orchestration workflow task. For more information, see the [Orchestration workflow quickstart](orchestration-workflow/quickstart.md).

* **Language Studio retirement**. Azure Language Studio is scheduled for retirement on **March 20, 2027**. After that date, the Language Studio portal is no longer accessible, but your existing projects, data, and service endpoints remain unaffected. All features and new enhancements are available in Microsoft Foundry. For step-by-step migration instructions, see [Migrate from Language Studio to Microsoft Foundry](migration-studio-to-foundry.md).

* **Foundry (classic) Language playground card is generally available**. The Language playground card in [Microsoft Foundry (classic)](https://ai.azure.com/) exits preview and is now generally available. You can access all Language authoring, testing, and deployment capabilities directly from the playground without any feature restrictions.

* **Updated LUIS migration guidance**. Migration documentation for **LUIS** (language understanding) is updated to reflect current Foundry workflows and Conversational Language Understanding (CLU) import procedures. If you're migrating from **LUIS**, see [Migrating to Azure Language in Foundry Tools](reference/migrate.md) for the latest instructions.

## January 2026

* **Orchestration workflow available in [Microsoft Foundry (classic)](https://ai.azure.com/)**. [Orchestration workflow](orchestration-workflow/quickstart.md) is now supported in Microsoft Foundry (classic).

  * The redesigned interface streamlines integration between [Conversational Language Understanding (CLU)](conversational-language-understanding/quickstart.md) and [Custom Question Answering (CQA)](question-answering/quickstart/sdk.md) projects. This capability enables efficient orchestration of user utterances across multiple conversational applications within a unified workflow.

  * Configure intent-based routing to direct user queries to the appropriate **CLU** or **CQA** project, improving response accuracy and reducing development complexity.

* **Azure AI Language capabilities fully available in [Microsoft Foundry (classic)](https://ai.azure.com/)**. All Azure AI Language capabilities are now accessible in Microsoft Foundry (classic), delivering a complete, unified development experience.

  * Language Studio authoring and testing capabilities—including project management, model training, and deployment workflows—are now fully integrated into the Foundry platform.

  * **Transition now** to Microsoft Foundry to take advantage of the full range of Language features, the latest enhancements, and a unified AI development platform. For step-by-step migration instructions, *see* [**Migrate from Azure Language Studio to Microsoft Foundry**](migration-studio-to-foundry.md).

## December 2025

* **Azure Language .NET SDK preview release**. New `.NET` SDK packages with support for the 2025-11-15-preview API are now available:

  * [Azure.AI.Language.Text 1.0.0-beta.4](https://www.nuget.org/packages/Azure.AI.Language.Text/1.0.0-beta.4)

  * [Azure.AI.Language.Conversation.Authoring 2.0.0-beta.5](https://www.nuget.org/packages/Azure.AI.Language.Conversations/2.0.0-beta.5)

* **Language Studio deprecation**. Azure Language Studio is scheduled for deprecation soon. All existing features, along with upcoming enhancements, are accessible through Microsoft Foundry. If you need guidance on exporting your projects from Language Studio, *see* [Export project](question-answering/how-to/migrate-knowledge-base.md#export-a-project).

## November 2025

**Azure Language integrates with Foundry Tools**. Azure Language now provides specialized tools and agents for building conversational AI applications in Foundry:

* [Azure Language MCP server](concepts/foundry-tools-agents.md#azure-language-mcp-server-preview). Connects AI agents to Azure Language services through the Model Context Protocol.
* [Azure Language Intent Routing agent](concepts/foundry-tools-agents.md#azure-language-intent-routing-agent-preview). Manages conversation flows by combining intent classification with answer delivery.
* [Azure Language Exact Question Answering agent](concepts/foundry-tools-agents.md#azure-language-exact-question-answering-agent-preview). Delivers consistent responses to frequently asked business questions.

**Azure Language capabilities now available in Foundry**. Several Azure Language capabilities are now available with the Foundry:

* [Conversational Language Understanding multi-turn conversations](conversational-language-understanding/concepts/multi-turn-conversations.md). Enable natural, context-aware dialogues through entity slot filling → Microsoft Foundry (new).
* [Language detection](conversational-language-understanding/concepts/multiple-languages.md). Automatically detect the language of user utterances in conversational applications → Microsoft Foundry (new).
* [PII detection for text](personally-identifiable-information/how-to/redact-text-pii.md). Detect and redact personally identifiable information in text documents → Microsoft Foundry (new).
* [Custom Named Entity Recognition](custom-named-entity-recognition/quickstart.md). You can test, train, and deploy custom NER models directly in the Foundry playground → Microsoft Foundry (classic).
* [PII detection for conversations](personally-identifiable-information/how-to/redact-conversation-pii.md). Identify and redact personally identifiable information in conversations → Microsoft Foundry (classic).

**Text PII detection enhancements (2025-11-15-preview API)**. The preview API introduces several new feature parameters for [PII detection](personally-identifiable-information/overview.md):

* **Anonymization**. The `syntheticReplacement` [redaction policy](personally-identifiable-information/how-to/redact-text-pii.md#redaction-policies) enables masking detected PII entities with synthetic replacement values. For example, "John Doe received a call from 424-878-9193" can be transformed into "Sam Johnson received a call from 401-255-6901."
* **Disable type-validation enforcement**. Disable [entity type validation](personally-identifiable-information/how-to/redact-text-pii.md#disableentityvalidation) to bypass strict validation when operational efficiency is prioritized over data integrity checks.
* **Confidence threshold score**. Set a minimum [confidence score](personally-identifiable-information/how-to/redact-text-pii.md#confidencescorethreshold-) threshold to control which entities appear in the output based on detection confidence.

**Entity Tags generally available**. [Entity Tags](named-entity-recognition/concepts/named-entity-categories.md) are now generally available, providing enhanced metadata and categorization for named entities.

**New preview model for PII detection**. The updated preview model introduces support for the following new entity types:

* [Airport](personally-identifiable-information/concepts/entity-categories.md#type-airport-preview)
* [City](personally-identifiable-information/concepts/entity-categories.md#type-city-preview)
* [Geopolitical Entity](personally-identifiable-information/concepts/entity-categories.md#type-geopolitical-entity-gpe-preview)
* [South Korea Drivers License Number](personally-identifiable-information/concepts/entity-categories.md#type-south-korea-drivers-license-number-preview)
* [South Korea Passport Number](personally-identifiable-information/concepts/entity-categories.md#type-south-korea-passport-number-preview)
* [South Korea Social Security Number](personally-identifiable-information/concepts/entity-categories.md#type-south-korea-social-security-number-preview)
* [Location](personally-identifiable-information/concepts/entity-categories.md#type-location-preview)
* [State](personally-identifiable-information/concepts/entity-categories.md#type-state-preview)
* [ZipCode](personally-identifiable-information/concepts/entity-categories.md#type-zipcode-preview)

**Model improvements**. Significant quality improvements for the following entity types:

* [Date Of Birth](personally-identifiable-information/concepts/entity-categories.md#type-date-of-birth-preview)
* [License Plate](personally-identifiable-information/concepts/entity-categories.md#type-license-plate-preview)
* [Sort Code](personally-identifiable-information/concepts/entity-categories.md#type-sort-code-preview)
* [VIN](personally-identifiable-information/concepts/entity-categories.md#type-vin-preview)

## October 2025

* **Summarization model 2025-06-10 generally available**. The [Summarization model](summarization/overview.md) version 2025-06-10 is now generally available. This model is fine-tuned using the [Phi open model family](https://azure.microsoft.com/products/phi), delivering enhanced performance for Issue and Resolution summary generation.

* **Expanded Azure Language in Foundry Tools MCP server capabilities**. The Model Context Protocol (MCP) server for Azure Language now provides eight added Natural Language Processing (NLP) tools: [Named Entity Recognition](named-entity-recognition/overview.md), [Text Analytics for health](text-analytics-for-health/overview.md), [Conversational Language Understanding](conversational-language-understanding/overview.md), [Custom Question Answering](question-answering/overview.md), [Language Detection](language-detection/overview.md), [Sentiment Analysis](sentiment-opinion-mining/overview.md), [Summarization](summarization/overview.md), and [Key Phrase Extraction](key-phrase-extraction/overview.md). These tools complement the existing PII Detection capability.

## September 2025

**Introducing CQA deploy-to-agent**. Custom Question Answering (CQA) projects can now be [deployed as intelligent agents](question-answering/how-to/deploy-agent.md) directly within the Foundry playground through a streamlined deployment experience.

* This feature enables users to transform fine-tuned CQA knowledge bases into production-ready agents with minimal configuration steps.
* The deployment process provides parity with CLU workflows and accelerates the agent development timeline within the unified Foundry environment.

**Custom Named Entity Recognition (NER) capabilities integrated into Language Playground**. Users can now access a testing playground for custom Named Entity Recognition (NER) within Foundry.

* This interactive interface allows training, deployment, testing, and fine-tuning for custom models while experimenting with custom NER capabilities in real-time.
* The playground accelerates the onboarding process and provides enhanced debugging capabilities for custom NER implementations. For more information, *see* [Quickstart: Custom named entity recognition](custom-named-entity-recognition/quickstart.md).

**New Python SDKs**. The new Python SDKs [**azure-ai-textanalytics 6.0.0b1**](https://pypi.org/project/azure-ai-textanalytics/6.0.0b1/) and [**azure-ai-textanalytics-authoring 1.0.0b1**](https://pypi.org/project/azure-ai-textanalytics-authoring/1.0.0b1/) are now available:

* **azure-ai-textanalytics 6.0.0b1** offers runtime APIs that enable users to utilize various prebuilt features within Azure Language, such as sentiment analysis, named entity recognition (NER), language detection, key phrase extraction, text PII detection, Text Analytics for health, and document summarization.<br><br>Additionally, the SDK can be used to access inference APIs for custom NER and text classification models. This release supports the latest `2025-05-15-preview` API, and previous versions. The `2025-05-15-preview` API introduces several new capabilities:

  * Added support for new entity types in [Named Entity Recognition (NER)](named-entity-recognition/concepts/named-entity-categories.md) and [Text PII detection](personally-identifiable-information/concepts/entity-categories.md): **DateOfBirth**, **BankAccountNumber**, **PassportNumber**, and **DriversLicenseNumber**.

  * Enhanced functionality allows users to define values to be excluded from the results produced by Text PII detection.

## August 2025

**Release of new Text PII and NER model (2025-08-01-preview)**. This new preview model version introduces broader functionality and expanded capabilities for Text personal information identification (PII) and named entity recognition (NER) services:

* **Expanded language support for DateOfBirth entity**. The **DateOfBirth** entity, which initially supported English only, now includes Tier 1 language coverage. This expansion supports French, German, Italian, Spanish, Portuguese, Brazilian Portuguese, and Dutch, ensuring broader international applicability.

* **Two new entity types added**:
  * **SortCode**: A financial identifier used in the UK and Ireland to specify the bank and branch associated with an account.
  * **LicensePlateNumber**: Support is now available for standard alphanumeric vehicle identification codes. At this time, license plates that consist exclusively of letters aren't supported.

* **Improved AI accuracy in financial entity recognition**. The **2025-08-01-preview** model is further optimized to minimize both false positives and false negatives in financial entity recognition, resulting in greater accuracy and reliability.

**New Python SDK release: azure-ai-language-conversations 2.0.0b1**. The latest Python SDK, **azure-ai-language-conversations 2.0.0b1**, is now available and supports the **2025-15-05-preview** REST API for conversation runtime.

* **Conversational Language Understanding (CLU) inference** now allows for seamless integration with advanced large-scale language models, providing real-time recognition of user intent without the need for extra model training.
* **Enhanced intent prediction capabilities** enable support for complex, multi-turn conversations. These advancements contribute to greater sophistication in conversational AI systems and, as a result, workflow automation processes are improved.

## July 2025

 **Expanded .NET SDK support for text and conversation authoring APIs**.

* [**Azure.AI.Language.Text.Authoring `1.0.0-beta.2`**](https://www.nuget.org/packages/Azure.AI.Language.Text.Authoring/1.0.0-beta.2) now supports project import with raw JSON string for custom NER and custom text classification.

* [**Azure.AI.Language.Conversation.Authoring `1.0.0-beta.2`**](https://www.nuget.org/packages/Azure.AI.Language.Conversations.Authoring/1.0.0-beta.2) introduces new authoring capabilities in the `2025-15-05-preview` API, including LLM-based CLU intent authoring, a quick-deploy feature, and multi-turn CLU model training with autogenerated synthetic data.

* [**Azure.AI.Language.Text.Authoring `1.0.0-beta.2`**](https://www.nuget.org/packages/Azure.AI.Language.Text.Authoring/1.0.0-beta.2) and [**Azure.AI.Language.Conversation.Authoring `1.0.0-beta.2`**](https://www.nuget.org/packages/Azure.AI.Language.Conversations.Authoring/1.0.0-beta.2) .NET SDK versions support the following [REST APIs](/rest/api/language/):

  * `2025-15-05-preview` (latest/default)
  * `2023-04-01`
  * `2023-04-15-preview`
  * `2024-11-15-preview`

## June 2025

**New version of the Conversational Language Understanding (CLU) training configuration**. This new version is aimed at minimizing over-predictions of the [None intent](conversational-language-understanding/concepts/none-intent.md)—particularly in multilingual contexts—is now available via the REST API using **trainingConfigVersion 2025-07-01-preview**. For more information, *see* [Train your model: request body data](conversational-language-understanding/how-to/train-model.md?tabs=rest-api#request-body).

**Updated [Build your conversational agent](https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator) accelerator project**. The update includes a new routing strategy—**TRIAGE_AGENT**. This strategy uses an agent hosted on Foundry Agent Service. It utilizes Conversational Language Understanding (CLU) and Custom Question Answering (CQA) as tools to triage user intent for downstream agent routing. Additionally, these tools help deliver precise answers to specific questions. For more information, *see* [TechCommunity Blog Post](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/announcing-azure-ai-language-new-features-to-accelerate-your-agent-development/4415216)

**[.NET SDKs](/dotnet/api/overview/azure/ai.textanalytics-readme?view=azure-dotnet&preserve-view=true) support**. The following `.NET SDK`s are now available, and support the latest REST API version **2025-15-05-preview**:

* [Azure.AI.Language.Text 1.0.0-beta.3](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/cognitivelanguage/Azure.AI.Language.Conversations/CHANGELOG.md) provides inference capabilities for a wide range of language processing tasks. These tasks include language detection, sentiment analysis, key phrase extraction, and named entity recognition (NER). The capabilities also include recognizing and linking personally identifiable information (PII) entities. Additionally, they offer text analytics for healthcare, custom named entity recognition (NER), and custom text classification. Both extractive and abstractive text summarization are also supported.

* [Azure.AI.Language.Conversation 2.0.0-beta.3](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/cognitivelanguage/Azure.AI.Language.Conversations/CHANGELOG.md) provides inference capabilities for conversational PII, conversational language understanding (CLU), and conversation summarization.

**Text PII GPU container is now available for integration**. You can access this container on the [Microsoft Artifact Registry](https://mcr.microsoft.com/artifact/mar/azure-cognitive-services/textanalytics/pii/) using the tag `gpu`.

## May 2025

**2025-05-15-preview release**. The latest API preview version includes updates for named entity recognition (NER) and PII detection:

* New entity type support for `DateOfBirth`, `BankAccountNumber`, `PassportNumber`, and `DriversLicenseNumber`.
* Improved AI quality for `PhoneNumber` entity type.

**New agent templates**. Azure Language now supports the following agent templates:

* [Intent routing](../../ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use.md): Detects user intent and provides precise answers, ideal for deterministic intent routing, and exact question answering with human oversight.
* [Exact question answering](../agents/concepts/agent-catalog.md): Delivers consistent, accurate responses to high-value predefined questions through deterministic methods.

**PII detection enhancements**. Azure Language introduces new customization and entity subtype features for PII detection:

* [Customize PII detection using your own regex](personally-identifiable-information/how-to/adapt-to-domain-pii.md#customizing-pii-detection-using-your-own-regex-only-available-for-text-pii-container) (Text PII container only).
* [Specify values to exclude from PII output](personally-identifiable-information/how-to/adapt-to-domain-pii.md#customizing-pii-output-by-specifying-values-to-exclude).
* [Use entity synonyms for tailored PII detection](personally-identifiable-information/how-to/adapt-to-domain-pii.md#api-schema-for-the-entitysynonyms-parameter).

**Enhanced CLU and CQA Capabilities in Foundry**. Foundry now offers enhanced capabilities for fine-tuning with custom conversational language understanding (CLU) and conversational question-and-answer (CQA) AI features:

* CLU and CQA authoring tools are now available in Foundry.
* CLU offers a quick deploy option powered by large language models (LLMs) for rapid deployment.
* CQA incorporates the QnA Maker scoring algorithm for more accurate responses.
* CQA enables exact match answering for precise query resolutions.

**For more updates, see our latest [TechCommunity Blog Post](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/announcing-azure-ai-language-new-features-to-accelerate-your-agent-development/4415216)**.

## April 2025

* Updated and improved model GA release for NER
* Expanded context window for [PII redaction](personally-identifiable-information/overview.md?tabs=text-pii) – This service update expands the window of detection the PII redaction service considers, enhancing quality and accuracy.
/python/api/azure-cognitiveservices-language-luis/index* Added prediction capability for custom models, including conversational language Understanding (CLU), custom named entity recognition (NER), and custom text classification, are now available in three new regions: Jio India Central, UK West, and Canada East.
* Scanned PDF PII. [Document input for PII redaction](personally-identifiable-information/how-to/redact-document-pii.md) now supports scanned PDFs, enabling PII detection and redaction in both digital and nondigital documents using `OCR`.

## March 2025

* Azure Language resource now can be deployed to three new regions, Jio India Central, UK West, and Canada East, for the following capabilities:
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
* More skills are available in [Foundry](https://ai.azure.com/?cid=learnDocs): Extract key phrase, Extract named entities, Analyze sentiment, and Detect language. More skills are yet to come.

## January 2025

* .NET SDK for Azure Language text analytics, [Azure.AI.Language.Text 1.0.0-beta.2](https://www.nuget.org/packages/Azure.AI.Language.Text/1.0.0-beta.2#readme-body-tab), is now available. This client library supports the latest REST API version, `2024-11-01`, and `2024-11-15-preview`, for the following features:
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

* Azure Language is moving to [Foundry](https://ai.azure.com/?cid=learnDocs). These skills are now available in Foundry playground: Extract health information, Extract PII from conversation, Extract PII from text, Summarize text, Summarize conversation, Summarize for call center. More skills follow.
* Runtime Container for Conversational Language Understanding (CLU) is available for on-premises connections.
* Both our [Text PII redaction service](personally-identifiable-information/overview.md?tabs=text-pii) and our Conversational PII service preview API (version 2024-11-15-preview) now support the option to mask detected sensitive entities with a label beyond just redaction characters. Customers can specify if personal data content such as names and phone numbers, that is, "John Doe received a call from 424-878-9192" are masked with a redaction character, that is, "******** received a call from ************" or masked with an entity label, that is, "`PERSON_1` received a call from `PHONENUMBER_1`." More on how to specify the redaction policy style for your outputs can be found in our [how-to guides](personally-identifiable-information/how-to-call.md).
* Native document support gating is removed with the latest API version, 2024-11-15-preview, allowing customers to access native document support for PII redaction and summarization. Key updates in this version include:
  * Increased Maximum File Size Limits (from 1 MB to 10 MB).
  * Enhanced PII Redaction Customization: Customers can now specify whether they want only the redacted document or both the redacted document and a JSON file containing the detected entities.
* Language detection is a built-in feature designed to identify the language in which a document is written. It provides a language code that corresponds to a wide array of languages. This feature includes not only standard languages but also their variants, dialects, and certain regional or cultural languages. Today the general availability of [script detection capability](language-detection/how-to/call-api.md#script-name-and-script-code), and 16 more languages support, which adds up to [139 total supported languages](language-detection/language-support.md) is announced.
* [Named Entity Recognition service](named-entity-recognition/overview.md), [Entity Resolution](named-entity-recognition/concepts/entity-resolutions.md) was upgraded to the Entity Metadata starting in API version 2023-04-15-preview. If you're calling the preview version of the API equal or newer than 2023-04-15-preview, check out the Entity Metadata article to use the resolution feature. The service now supports the ability to specify a list of entity tags to be included into the response or excluded from the response. If a piece of text is classified as more than one entity type, the overlapPolicy parameter allows customers to specify how the service handles the overlap. The `inferenceOptions` parameter enables users to modify the inference process, such as preventing detected entity values from being normalized and added to the metadata. Along with these optional input parameters, we support an updated output structure (with new fields tags, type, and metadata) to ensure enhanced user customization and deeper analysis Learn more on our documentation.
* Text Analytics for Health (TA4H) is a specialized tool designed to extract and categorize key medical details from unstructured sources. These sources include doctor's notes, discharge summaries, clinical documentation, and electronic health records. Today, we released support for Fast Healthcare Interoperability Resources (FHIR) structuring and temporal [assertion detection](text-analytics-for-health/concepts/assertion-detection.md) in the Generally Available API.

## October 2024

* Custom Language features enable you to deploy your project to multiple [resources within a single region](concepts/custom-features/multi-region-deployment.md) via the API.

## September 2024

* PII detection now has container support. See more details in the Azure Update post: [Announcing Text PII Redaction Container Release](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/announcing-text-pii-redaction-container-release/4264655).
* Custom sentiment analysis (preview) will be retired January 10, 2025. You can transition to other custom model training services, such as custom text classification in Azure Language. See more details in the Azure Update post: [Retirement: Announcing upcoming retirement of custom sentiment analysis (preview) in Azure Language (microsoft.com)](https://azure.microsoft.com/updates/v2/custom-sentiment-analysis-retirement).
* Custom text analytics for health (preview) will be retired on January 10, 2025. Transition to other custom model training services, such as custom named entity recognition in Azure Language, by that date. See more details in the Azure Update post: [Retirement: Announcing upcoming retirement of custom text analytics for health (preview) in Azure Language (microsoft.com)](https://azure.microsoft.com/updates/v2/custom-text-analytics-for-health-retirement).

## August 2024

* [CLU utterance limit in a project](conversational-language-understanding/service-limits.md#data-limits) increased from 25,000 to 50,000.
* [CLU new version of training configuration, version 2024-08-01-preview, is available now](conversational-language-understanding/concepts/best-practices.md#address-out-of-domain-utterances), which improves the quality of intent identification for out of domain utterances.

## July 2024

* [Conversational PII redaction](https://techcommunity.microsoft.com/blog/ai-azure-ai-services-blog/announcing-conversational-pii-detection-service-s-general/4162881) service in English-language contexts is now Generally Available (GA).
* Conversation Summarization now supports 12 added languages in preview as listed [here](summarization/language-support.md).
* Summarization Meeting or Conversation Chapter titles features support reduced length to focus on the key topics.
* Enable support for data augmentation for diacritics to generate variations of training data for diacritic variations used in some natural languages, which are especially useful for Germanic and Slavic languages.

## February 2024

* Expanded [language detection](./language-detection/how-to/call-api.md#script-name-and-script-code) support for added scripts according to the [ISO 15924 standard](https://wikipedia.org/wiki/ISO_15924) is now available starting in API version `2023-11-15-preview`.

## January 2024

* [Native document support](native-document-support/overview.md) is now available in `2023-11-15-preview` public preview.

## Related content

* See the [previous updates](./concepts/previous-updates.md) article for service updates not listed here.

* For a list of changes to the Azure Language library (`SDK`s), see the [release history](reference/release-history.md) article.
