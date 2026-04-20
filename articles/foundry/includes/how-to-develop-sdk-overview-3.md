---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: dantaylo
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Using the Agent Framework for local orchestration

Microsoft Agent Framework is an open-source SDK for building multi-agent systems in code (for example, .NET and Python) with a cloud-provider-agnostic interface.

Use Agent Framework when you want to define and orchestrate agents locally. Pair it with the Foundry SDK when you want those agents to run against Foundry models or when you want Agent Framework to orchestrate agents hosted in Foundry.

For more information, see the [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview).

## Foundry Tools SDKs

Foundry Tools (formerly Azure AI Services) are prebuilt point solutions with dedicated SDKs. Use the following endpoints to work with Foundry Tools.

### Which endpoint should you use?

Choose an endpoint based on your needs:

Use the Azure AI Services endpoint to access Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token Foundry Tools.

Foundry Tools endpoint: `https://<your-resource-name>.cognitiveservices.azure.com/`

> [!NOTE]
> Endpoints use either your resource name or a custom subdomain. If your organization set up a custom subdomain, replace `your-resource-name` with `your-custom-subdomain` in all endpoint examples.

If your workloads use retiring Azure AI Language features—for example, sentiment analysis, key phrase extraction, summarization, entity linking, CLU, or CQA—plan to migrate to Microsoft Foundry alternatives. For new development, consider using the Foundry SDK or the OpenAI-compatible endpoint as described earlier in this article. See [Migrate from Language Studio to Microsoft Foundry](/azure/ai-services/language-service/migration-studio-to-foundry).

For Speech and Translation Foundry Tools, use the endpoints in the following tables. Replace placeholders with your resource information.

#### Speech Endpoints

| Foundry Tool | Endpoint |
| --- | --- |
|Speech to Text (Standard)|`https://<YOUR-RESOURCE-REGION>.stt.speech.microsoft.com`|
|Text to Speech (Neural)|`https://<YOUR-RESOURCE-REGION>.tts.speech.microsoft.com`|
|Custom Voice|`https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/`|

#### Translation Endpoints

| Foundry Tool | Endpoint |
| --- | --- |
|Text Translation|`https://api.cognitive.microsofttranslator.com/`|
|Document Translation|`https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/`|

The following sections include quickstart links for the Foundry Tools SDKs and reference information.

> [!IMPORTANT]
> On March 20, 2027, Azure Language Studio will retire and migrate to Microsoft Foundry; all capabilities and future enhancements will be available in Microsoft Foundry.
>
> On March 31, 2029, the following Azure Language capabilities will retire (end of support). Before that date, users should migrate existing workloads and onboard new projects to [Microsoft Foundry models](https://review.learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview) for enhanced natural language understanding and simplified application integration:
>
> - Key Phrase Extraction
> - Sentiment Analysis and Opinion Mining
> - Custom Text Classification
> - Conversational Language Understanding (CLU)
> - Custom Question Answering (CQA)
> - Orchestration Workflow
> - Summarization (extractive and abstractive, for documents and conversations)
> - Entity Linking
>
> Core features with continued support: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
>
> For migration options, see [Migrate from Language Studio to Microsoft Foundry](/azure/ai-services/language-service/migration-studio-to-foundry).

<!-- ::: zone pivot="programming-language-cpp"
[!INCLUDE [C++ include](sdk/cpp.md)]
::: zone-end -->

::: zone pivot="programming-language-csharp"
[!INCLUDE [C# include](sdk/csharp.md)]
::: zone-end

<!-- ::: zone pivot="programming-language-go"
[!INCLUDE [Go include](sdk/go.md)]
::: zone-end -->

::: zone pivot="programming-language-java"
[!INCLUDE [Java include](sdk/java.md)]
::: zone-end

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript include](sdk/javascript.md)]
::: zone-end

<!-- ::: zone pivot="programming-language-objectivec"
[!INCLUDE [ObjectiveC include](sdk/objective-c.md)]
::: zone-end -->

::: zone pivot="programming-language-python"
[!INCLUDE [Python include](sdk/python.md)]
::: zone-end

<!-- ::: zone pivot="programming-language-swift"
[!INCLUDE [Swift include](sdk/swift.md)]
::: zone-end -->
