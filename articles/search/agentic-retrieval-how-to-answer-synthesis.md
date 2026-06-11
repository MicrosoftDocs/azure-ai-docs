---
title: Enable Answer Synthesis
description: Learn how to enable answer synthesis in a knowledge base or retrieve request in Azure AI Search. At query time, the knowledge base uses your deployed LLM to produce natural-language answers with citations to your knowledge sources.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Use answer synthesis for citation-backed responses in Azure AI Search (preview)

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

By default, a knowledge base in Azure AI Search performs *data extraction*, which returns raw grounding chunks from your knowledge sources. Data extraction is useful for retrieving specific information but lacks the context and reasoning necessary for complex queries.

You can instead enable *answer synthesis* (preview), which uses the LLM specified in your knowledge base to answer queries in natural language. Each answer includes citations to the retrieved sources and follows any instructions you provide, such as using bulleted lists.

You can set this property in a knowledge base or a retrieve request. The knowledge base setting establishes the default for all queries, while the retrieve request setting overrides the default on a query-by-query basis.

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that specifies an LLM.

+ Permissions to update knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ For outbound calls to the LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

:::zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

:::zone-end

:::zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

:::zone-end

:::zone pivot="rest"

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

:::zone-end

## Limitations and considerations

- The `minimal` retrieval reasoning effort disables LLM processing, so it's incompatible with answer synthesis in both knowledge base definitions and retrieve requests. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

- Answer synthesis incurs pay-as-you-go charges from Azure OpenAI, which are based on the number of input and output tokens. Charges appear under the LLM assigned to the knowledge base. For more information, see [Availability and pricing](agentic-retrieval-overview.md#availability-and-pricing).

## Enable answer synthesis in a knowledge base

This section demonstrates how to enable answer synthesis in an existing knowledge base. Although you can use this configuration for new knowledge bases, knowledge base creation is beyond the scope of this article.

:::zone pivot="csharp"

Set `OutputMode` to `"answerSynthesis"` on the `KnowledgeBase` definition. Optionally, set `AnswerInstructions` to customize the answer output. Our example instructs the knowledge base to `Use concise bulleted lists`.

```csharp
var aoaiParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel,
};

var knowledgeBase = new KnowledgeBase(
    name: knowledgeBaseName,
    knowledgeSources: new[] { new KnowledgeSourceReference(knowledgeSourceName) })
{
    Models = { new KnowledgeBaseAzureOpenAIModel(aoaiParams) },
    OutputMode = "answerSynthesis",
    AnswerInstructions = "Use concise bulleted lists",
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

Set `output_mode` to `"answerSynthesis"` on the `KnowledgeBase` definition. Optionally, set `answer_instructions` to customize the answer output. Our example instructs the knowledge base to `Use concise bulleted lists`.

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference,
)

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url=aoai_endpoint,
    deployment_name=aoai_gpt_deployment,
    model_name=aoai_gpt_model,
)

knowledge_base = KnowledgeBase(
    name=knowledge_base_name,
    models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
    knowledge_sources=[KnowledgeSourceReference(name=knowledge_source_name)],
    output_mode="answerSynthesis",
    answer_instructions="Use concise bulleted lists",
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_base(knowledge_base)
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

:::zone-end

:::zone pivot="rest"

Set `outputMode` to `"answerSynthesis"` on the knowledge base definition. Optionally, set `answerInstructions` to customize the answer output. Our example instructs the knowledge base to `Use concise bulleted lists`.

```http
### Enable answer synthesis in a knowledge base
PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{api-key}}

{
    "name": "{{knowledge-base-name}}",
    "knowledgeSources": [ ... // OMITTED FOR BREVITY ],
    "models": [ ... // OMITTED FOR BREVITY ],
    "outputMode": "answerSynthesis",
    "answerInstructions": "Use concise bulleted lists"
}
```

**Reference:** [Knowledge Base - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

## Enable answer synthesis in a retrieve request

For per-query control over the response format, you can enable answer synthesis at query time. This approach overrides the default output mode specified in the knowledge base.

:::zone pivot="csharp"

Set `OutputMode` to `"answerSynthesis"` on a `KnowledgeBaseRetrievalRequest`.

```csharp
var client = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri(searchEndpoint),
    knowledgeBaseName: knowledgeBaseName,
    credential: credential);

var request = new KnowledgeBaseRetrievalRequest();
request.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[]
        {
            new KnowledgeBaseMessageTextContent("What is healthcare?")
        }) { Role = "user" });
request.OutputMode = "answerSynthesis";

var result = await client.RetrieveAsync(request);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

Set `output_mode` to `"answerSynthesis"` on a `KnowledgeBaseRetrievalRequest`.

```python
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
)

agent_client = KnowledgeBaseRetrievalClient(
    endpoint=search_endpoint,
    credential=credential,
    knowledge_base_name=knowledge_base_name,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What is healthcare?")],
        )
    ],
    output_mode="answerSynthesis",
)

result = agent_client.retrieve(retrieval_request=request)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

Set `outputMode` to `"answerSynthesis"` on a retrieve request.

```http
### Enable answer synthesis in a retrieve request
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{api-key}}

{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is healthcare?"
                }
            ]
        }
    ],
    "outputMode": "answerSynthesis"
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

## Get a synthesized answer

When answer synthesis is enabled, the knowledge base returns a natural-language answer based on the instructions you optionally specified in the knowledge base. Citations to your knowledge sources are formatted as `[ref_id:<number>]`.

For example, if your instructions are `Use concise bulleted lists` and your query is `What is healthcare?`, the response might look like this:

```json
{
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "- Healthcare encompasses various services provided to patients and the general population ..."
        }
      ]
    }
  ]
}
```

The full `text` output is as follows:

```
"- Healthcare encompasses various services provided to patients and the general population, including primary health services, hospital care, dental care, mental health services, and alternative health services [ref_id:1].\n- It involves the delivery of safe, effective, patient-centered care through different modalities, such as in-person encounters, shared medical appointments, and group education sessions [ref_id:0].\n- Behavioral health is a significant aspect of healthcare, focusing on the connection between behavior and overall health, including mental health and substance use [ref_id:2].\n- The healthcare system aims to ensure quality of care, access to providers, and accountability for positive outcomes while managing costs effectively [ref_id:2].\n- The global health system is evolving to address complex health needs, emphasizing the importance of cross-sectoral collaboration and addressing social determinants of health [ref_id:4]."
```

Depending on your knowledge base's configuration, the response might include other information, such as activity logs and reference arrays. For more information, see [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Related content

- [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
- [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
- [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) (uses answer synthesis)
- [Python sample: Azure AI Search blob knowledge source](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb) (uses answer synthesis)