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

## Agent Framework

[Microsoft Agent Framework](/agent-framework/overview/agent-framework-overview) is an open-source SDK (Python and .NET) for building agents and multi-agent systems in code. It's the recommended path for [code-based agents](../agents/overview.md#code-based-agents) on Microsoft Foundry, and it's cloud-provider-agnostic so the same code can run in your own process or be packaged as a Foundry-managed Hosted agent.

### How it connects to Foundry

Agent Framework calls the **Foundry Responses API** through the `FoundryChatClient` provider. The `FoundryChatClient` targets your project endpoint:

```
{project_endpoint}/openai/v1/responses
```

Going through the project endpoint — instead of a resource-level OpenAI endpoint — gives your agent:

- Foundry models from the catalog (Azure OpenAI and Foundry direct models) through one API.
- Platform tools beyond the OpenAI tool set, including file search, code interpreter, memory, web search, MCP servers, SharePoint, WorkIQ, and Fabric IQ.
- Project-scoped data, On-Behalf-Of (OBO) tool authentication, and the project's tracing, content filters, and identity configuration.

### When to use it

Use Agent Framework when you want your agent definition (instructions, tools, model) to live in your application code and ship in the same release cycle as the app, rather than as a portal-defined [prompt agent](../agents/quickstarts/prompt-agent.md) or a [workflow agent](../agents/concepts/workflow.md).

The same Agent Framework code supports two hosting modes — they're additive, not alternatives:

- **Self-hosted** — Run the agent in your own process or infrastructure. You manage the endpoint, scaling, and lifecycle; Foundry provides the models, platform tools, and API. Best for local iteration and integrating with existing code. See [Quickstart: Use the Foundry Responses API](../agents/quickstarts/responses-api.md).
- **Hosted agent (preview)** — Package the same code as a container and deploy it to Foundry. You get a managed endpoint, automatic scaling on isolated Micro VMs, a dedicated Microsoft Entra agent identity, session-level state, and end-to-end observability. See [Deploy your first Hosted agent](../agents/quickstarts/quickstart-hosted-agent.md).

Start self-hosted while you iterate, then graduate the same codebase to a Hosted agent when you need a managed, network-addressable endpoint that other apps or agents can call.

For a full comparison of agent types and hosting choices, see [What is Microsoft Foundry Agent Service?](../agents/overview.md).

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

#### Language Endpoints

| Foundry Tool | Endpoint |
| --- | --- |
| Text analysis| `https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com`|

> [!IMPORTANT]
> On March 20, 2027, Azure Language Studio will retire and migrate to Microsoft Foundry; all capabilities and future enhancements will be available in Microsoft Foundry.
>
> On March 31, 2029, the following Azure Language capabilities will retire (end of support). Before that date, users should migrate existing workloads and onboard new projects to [Microsoft Foundry models](../concepts/foundry-models-overview.md) for enhanced natural language understanding and simplified application integration:
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
