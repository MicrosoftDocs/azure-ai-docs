---
title: Retrieval-Augmented Generation (RAG) Evaluators for Generative AI
titleSuffix: Microsoft Foundry
description: Learn about Retrieval-Augmented Generation evaluators for assessing relevance, groundedness, and response completeness in generative AI systems.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Retrieval-Augmented Generation (RAG) evaluators

[!INCLUDE [version-banner](../../includes/version-banner.md)]

A Retrieval-Augmented Generation (RAG) system tries to generate the most relevant answer consistent with grounding documents in response to a user's query. A user's query triggers a search retrieval in the corpus of grounding documents to provide grounding context for the AI model to generate a response.

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

It's important to evaluate:

- [Document Retrieval](#document-retrieval)
- [Retrieval](#retrieval)
- [Groundedness](#groundedness)
- [Groundedness Pro (preview)](#groundedness-pro)
- [Relevance](#relevance)
- [Response Completeness](#response-completeness)

These evaluators focus on three aspects:

- The relevance of the retrieval results to the user's query: use [Document Retrieval](#document-retrieval) if you have labels for query-specific document relevance, or query relevance judgement (qrels) for more accurate measurements. Use [Retrieval](#retrieval) if you only have the retrieved context, but you don't have such labels and have a higher tolerance for a less fine-grained measurement.
- The consistency of the generated response with respect to the grounding documents: use [Groundedness](#groundedness) if you want to customize the definition of groundedness in our open-source large language model-judge (LLM-judge) prompt. Use [Groundedness Pro (preview)](#groundedness-pro) if you want a straightforward definition.
- The relevance of the final response to the query: use [Relevance](#relevance) if you don't have ground truth. Use [Response Completeness](#response-completeness) if you have ground truth and don't want your response to miss critical information.

::: moniker-end

::: moniker range="foundry"

| Evaluator | Best practice | Use when | Purpose | Output |
|--|--|--|--|--|
| Document Retrieval | Process evaluation | Retrieval quality is a bottleneck for your RAG, and you have query relevance labels (ground truth) for precise search quality metrics for debugging and parameter optimization | Measures search quality metrics (Fidelity, NDCG, XDCG, Max Relevance, Holes) by comparing retrieved documents against ground truth labels | Composite: Fidelity, NDCG, XDCG, Max Relevance, Holes (with Pass/Fail) |
| Retrieval | Process evaluation | You want to assess textual quality of retrieved context, but you don't have ground truths | Measures how relevant the retrieved context chunks are to addressing a query using an LLM judge | Binary: Pass/Fail based on threshold (1-5 scale) |
| Groundedness | System evaluation | You want a well-rounded groundedness definition that works with agent inputs, and bring your own GPT models as the LLM-judge | Measures how well the generated response aligns with the given context without fabricating content (precision aspect) | Binary: Pass/Fail based on threshold (1-5 scale) |
| Groundedness Pro (preview) | System evaluation | You want a strict groundedness definition powered by Azure AI Content Safety and use our service model | Detects if the response is strictly consistent with the context using the Azure AI Content Safety service | Binary: True/False |
| Relevance | System evaluation | You want to assess how well the RAG response addresses the query but don't have ground truths | Measures the accuracy, completeness, and direct relevance of the response to the query | Binary: Pass/Fail based on threshold (1-5 scale) |
| Response Completeness | System evaluation | You want to ensure the RAG response doesn't miss critical information (recall aspect) from your ground truth | Measures how completely the response covers the expected information compared to ground truth | Binary: Pass/Fail based on threshold (1-5 scale) |

::: moniker-end

Think about *groundedness* and *response completeness* as:

- Groundedness focuses on the *precision* aspect of the response. It doesn't contain content outside of the grounding context.
- Response completeness focuses on the *recall* aspect of the response. It doesn't miss critical information compared to the expected response or ground truth.

::: moniker range="foundry-classic"

## Model configuration for AI-assisted evaluators

For reference in the following snippets, the AI-assisted quality evaluators, except for Groundedness Pro, use a model configuration for the LLM-judge:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get("AZURE_API_KEY"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

### Evaluator model support

The evaluators support AzureOpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other evaluators| Not Supported | Supported | -- |

For complex evaluation that requires refined reasoning, use a strong reasoning model like `4.1-mini` with a balance of reasoning performance and cost efficiency.

## Retrieval

Because of its upstream role in RAG, retrieval quality is critical. If retrieval quality is poor and the response requires corpus-specific knowledge, the language model is less likely to provide a satisfactory answer. `RetrievalEvaluator` measures the *textual quality* of retrieval results with a language model without requiring ground truth, also known as *query relevance judgment*.

This approach adds value compared to `DocumentRetrievalEvaluator`, which measures `ndcg`, `xdcg`, `fidelity`, and other classical information retrieval metrics that require ground truth. This metric focuses on how relevant the context chunks are to addressing a query and how the most relevant context chunks are surfaced at the top of the list. The context chunks are encoded as strings.

### Retrieval example

```python
from azure.ai.evaluation import RetrievalEvaluator

retrieval = RetrievalEvaluator(model_config=model_config, threshold=3)
retrieval(
    query="Where was Marie Curie born?", 
    context="Background: 1. Marie Curie was born in Warsaw. 2. Marie Curie was born on November 7, 1867. 3. Marie Curie is a French scientist. ",
)
```

### Retrieval output

The numerical score is based on a Likert scale (integer 1 to 5), where a higher score indicates better performance. Given a numerical threshold (a default is set), the evaluator also outputs *pass* if the score >= threshold, or *fail* otherwise. The reason field explains why the score is high or low.

```python
{
    "retrieval": 5.0,
    "gpt_retrieval": 5.0,
    "retrieval_reason": "The context contains relevant information that directly answers the query about Marie Curie's birthplace, with the most pertinent information placed at the top. Therefore, it fits the criteria for a high relevance score.",
    "retrieval_result": "pass",
    "retrieval_threshold": 3
}
```

::: moniker-end

::: moniker range="foundry"

## System evaluation

System evaluation examines the quality of the final response in your RAG workflow. These evaluators ensure that the AI-generated content is accurate, relevant, and complete based on the provided context and user query:

- Groundedness - Is the response grounded in the provided context without fabrication?
- Groundedness Pro - Does the response strictly adhere to the context (Azure AI Content Safety)?
- Relevance - Does the response accurately address the user's query?
- Response Completeness - Does the response cover all critical information from ground truth?

Examples:

- [Groundedness sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_groundedness.py)
- [Relevance sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_relevance.py)
- [Response completeness sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_response_completeness.py)

## Process evaluation

Process evaluation assesses the quality of the document retrieval step in RAG systems. The retrieval step is crucial for providing relevant context to the language model:

- Retrieval - How relevant are the retrieved context chunks to the query?
- Document Retrieval - How well does retrieval match ground truth labels (requires qrels)?

Examples:

- [Retrieval sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_retrieval.py)

For more examples, see [all quality evaluator samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations).

## Using RAG evaluators

To use RAG evaluators, configure them in your `testing_criteria`. Each evaluator requires specific data mappings:

| Evaluator | Required mappings |
|-----------|-------------------|
| Groundedness, Groundedness Pro | `query`, `context`, `response` |
| Relevance | `query`, `response` |
| Response Completeness | `response`, `ground_truth` |
| Retrieval | `query`, `context` |
| Document Retrieval | `retrieval_ground_truth`, `retrieval_documents` |

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_items}}` references response messages when evaluating with an agent/model target or agent response data source.

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on data sources.

### Configuration example

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "groundedness",
        "evaluator_name": "builtin.groundedness",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {
            "context": "{{item.context}}",
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "relevance",
        "evaluator_name": "builtin.relevance",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "retrieval",
        "evaluator_name": "builtin.retrieval",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {"query": "{{item.query}}", "context": "{{item.context}}"},
    },
]
```

### Output

These evaluators return scores on a 1-5 Likert scale (1 = very poor, 5 = excellent). The default pass threshold is 3. Scores at or above the threshold result in `passed: true`. The following shows a simplified example:

```json
{
    "type": "azure_ai_evaluator",
    "name": "groundedness",
    "score": 4,
    "passed": true,
    "reason": "The response is well-grounded in the provided context without fabricating content."
}
```

::: moniker-end

## Document retrieval

::: moniker range="foundry-classic"

Because of its upstream role in RAG, retrieval quality is critical. Poor retrieval quality reduces the likelihood of your language model providing a satisfactory answer, especially when the response requires corpus-specific knowledge. Use `DocumentRetrievalEvaluator` to evaluate retrieval quality and optimize your search parameters for RAG.

::: moniker-end

::: moniker range="foundry"

Because of its upstream role in RAG, the retrieval quality is important. If the retrieval quality is poor and the response requires corpus-specific knowledge, there's less chance your language model gives you a satisfactory answer. The most precise measurement is to use the `document_retrieval` evaluator to evaluate retrieval quality and optimize your search parameters for RAG.

::: moniker-end

- Document retrieval evaluator measures how well the RAG retrieves the correct documents from the document store. As a composite evaluator useful for RAG scenario with ground truth, it computes a list of useful search quality metrics for debugging your RAG pipelines:

  | Metric | Category | Description |
  |--|--|--|
  | Fidelity | Search Fidelity | How well the top n retrieved chunks reflect the content for a given query: number of good documents returned out of the total number of known good documents in a dataset |
  | NDCG | Search NDCG | How good are the rankings to an ideal order where all relevant items are at the top of the list |
  | XDCG | Search XDCG | How good the results are in the top-k documents regardless of scoring of other index documents |
  | Max Relevance N | Search Max Relevance | Maximum relevance in the top-k chunks |
  | Holes | Search Label Sanity | Number of documents with missing query relevance judgments, or ground truth |

::: moniker range="foundry-classic"

- To optimize your RAG in a scenario called *parameter sweep*, you can use these metrics to calibrate the search parameters for the optimal RAG results. Generate retrieval results for different search parameters, such as search algorithms (vector, semantic), top_k, and chunk sizes. Then use `DocumentRetrievalEvaluator` to identify the parameters that yield the highest retrieval quality.
::: moniker-end

::: moniker range="foundry"

- To optimize your RAG in a scenario called *parameter sweep*, you can use these metrics to calibrate the search parameters for the optimal RAG results. Generate different retrieval results for various search parameters such as search algorithms (vector, semantic), top_k, and chunk sizes you're interested in testing. Then use `document_retrieval` to find the search parameters that yield the highest retrieval quality.

::: moniker-end

### Document retrieval example

::: moniker range="foundry-classic"

```python
from azure.ai.evaluation import DocumentRetrievalEvaluator

# These query_relevance_labels are given by your human- or LLM-judges.
retrieval_ground_truth = [
    {
        "document_id": "1",
        "query_relevance_label": 4
    },
    {
        "document_id": "2",
        "query_relevance_label": 2
    },
    {
        "document_id": "3",
        "query_relevance_label": 3
    },
    {
        "document_id": "4",
        "query_relevance_label": 1
    },
    {
        "document_id": "5",
        "query_relevance_label": 0
    },
]
# The min and max of the label scores are inputs to document retrieval evaluator
ground_truth_label_min = 0
ground_truth_label_max = 4

# These relevance scores come from your search retrieval system
retrieved_documents = [
    {
        "document_id": "2",
        "relevance_score": 45.1
    },
    {
        "document_id": "6",
        "relevance_score": 35.8
    },
    {
        "document_id": "3",
        "relevance_score": 29.2
    },
    {
        "document_id": "5",
        "relevance_score": 25.4
    },
    {
        "document_id": "7",
        "relevance_score": 18.8
    },
]

document_retrieval_evaluator = DocumentRetrievalEvaluator(
    # Specify the ground truth label range
    ground_truth_label_min=ground_truth_label_min, 
    ground_truth_label_max=ground_truth_label_max,
    # Optionally override the binarization threshold for pass/fail output
    ndcg_threshold = 0.5,
    xdcg_threshold = 50.0,
    fidelity_threshold = 0.5,
    top1_relevance_threshold = 50.0,
    top3_max_relevance_threshold = 50.0,
    total_retrieved_documents_threshold = 50,
    total_ground_truth_documents_threshold = 50
)
document_retrieval_evaluator(retrieval_ground_truth=retrieval_ground_truth, retrieved_documents=retrieved_documents)   
```

::: moniker-end

::: moniker range="foundry"

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "document_retrieval",
        "evaluator_name": "builtin.document_retrieval",
        "initialization_parameters": {
            "ground_truth_label_min": 1,
            "ground_truth_label_max": 5,
        },
        "data_mapping": {
            "retrieval_ground_truth": "{{item.retrieval_ground_truth}}",
            "retrieval_documents": "{{item.retrieved_documents}}",
        },
    },
]
```

The `retrieval_ground_truth` contains human-labeled relevance scores per document:

```python
retrieval_ground_truth = [
    {"document_id": "1", "query_relevance_label": 4},
    {"document_id": "2", "query_relevance_label": 2},
]
```

The `retrieved_documents` contains scores from your search system:

```python
retrieved_documents = [
    {"document_id": "2", "relevance_score": 45.1},
    {"document_id": "6", "relevance_score": 35.8},
]
```

::: moniker-end

### Document retrieval output

All numerical scores have `high_is_better=True`, except for `holes` and `holes_ratio`, which have `high_is_better=False`. With a numerical threshold (default of 3), the evaluator outputs *pass* if the score is greater than or equal to the threshold, or *fail* otherwise.

::: moniker range="foundry-classic"

```python
{
    "ndcg@3": 0.6461858173,
    "xdcg@3": 37.7551020408,
    "fidelity": 0.0188438199,
    "top1_relevance": 2,
    "top3_max_relevance": 2,
    "holes": 30,
    "holes_ratio": 0.6000000000000001,
    "holes_higher_is_better": False,
    "holes_ratio_higher_is_better": False,
    "total_retrieved_documents": 50,
    "total_groundtruth_documents": 1565,
    "ndcg@3_result": "pass",
    "xdcg@3_result": "pass",
    "fidelity_result": "fail",
    "top1_relevance_result": "fail",
    "top3_max_relevance_result": "fail",
    # Omitting more fields ...
}
```

::: moniker-end

::: moniker range="foundry"

```python
{
    "ndcg@3": 0.6461858173,
    "xdcg@3": 37.7551020408,
    "fidelity": 0.0188438199,
    "top1_relevance": 2,
    "top3_max_relevance": 2,
    "holes": 30,
    "holes_ratio": 0.6000000000000001,
    "holes_higher_is_better": False,
    "holes_ratio_higher_is_better": False,
    "total_retrieved_documents": 50,
    "total_groundtruth_documents": 1565,
    "ndcg@3_result": "pass",
    "xdcg@3_result": "pass",
    "fidelity_result": "fail",
    "top1_relevance_result": "fail",
    "top3_max_relevance_result": "fail",
    # Omitting more fields ...
}
```

::: moniker-end

::: moniker range="foundry-classic"

## Groundedness

It's important to evaluate how grounded the response is in relation to the context. AI models might fabricate content or generate irrelevant responses. `GroundednessEvaluator` measures how well the generated response aligns with the given context, the grounding source, and doesn't fabricate content outside of it.

This metric captures the *precision* aspect of response alignment with the grounding source. A lower score means the response is irrelevant to the query or fabricates inaccurate content outside the context. This metric is complementary to `ResponseCompletenessEvaluator`, which captures the *recall* aspect of response alignment with the expected response.  

### Groundedness example

```python
from azure.ai.evaluation import GroundednessEvaluator

groundedness = GroundednessEvaluator(model_config=model_config, threshold=3)
groundedness(
    query="Is Marie Curie is born in Paris?", 
    context="Background: 1. Marie Curie is born on November 7, 1867. 2. Marie Curie is born in Warsaw.",
    response="No, Marie Curie is born in Warsaw."
)
```

### Groundedness output

The numerical score is on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default is 3), the evaluator outputs *pass* if the score is greater than or equal to the threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
    "groundedness": 5.0,  
    "gpt_groundedness": 5.0,
    "groundedness_reason": "The RESPONSE accurately answers the QUERY by confirming that Marie Curie was born in Warsaw, which is supported by the CONTEXT. It does not include any irrelevant or incorrect information, making it a complete and relevant answer. Thus, it deserves a high score for groundedness.",
    "groundedness_result": "pass", 
    "groundedness_threshold": 3
}
```

## Groundedness Pro

AI systems can generate irrelevant responses or fabricate content outside the given context. Powered by Azure AI Content Safety, `GroundednessProEvaluator` checks if the generated text response is accurate and consistent with the given context in a retrieval-augmented generation question-and-answering scenario. It ensures the response closely adheres to the context to answer the query, avoiding speculation or fabrication. It outputs a binary label.

### Groundedness Pro example

```python
from azure.ai.evaluation import GroundednessProEvaluator
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
load_dotenv()

# Using Microsoft Foundry Hub
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}

groundedness_pro = GroundednessProEvaluator(azure_ai_project=azure_ai_project), 
groundedness_pro(
    query="Is Marie Curie is born in Paris?", 
    context="Background: 1. Marie Curie is born on November 7, 1867. 2. Marie Curie is born in Warsaw.",
    response="No, Marie Curie is born in Warsaw."
)
```

### Groundedness Pro output

The label field returns `True` if all content in the response is completely grounded in the context, and `False` otherwise. Use the reason field to learn more about the judgment behind the score.

```python
{
    "groundedness_pro_reason": "All Contents are grounded",
    "groundedness_pro_label": True
}
```

## Relevance

AI models can generate irrelevant responses to a user query. It's important to evaluate the final response. To address this issue, use `RelevanceEvaluator`, which measures how effectively a response addresses a query. It assesses the accuracy, completeness, and direct relevance of the response based on the query. Higher scores mean better relevance.

### Relevance example

```python
from azure.ai.evaluation import RelevanceEvaluator

relevance = RelevanceEvaluator(model_config=model_config, threshold=3)
relevance(
    query="Is Marie Curie is born in Paris?", 
    response="No, Marie Curie is born in Warsaw."
)
```

### Relevance output

The numerical score is on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default is 3), the evaluator outputs *pass* if the score is greater than or equal to the threshold, or *fail* otherwise. The reason field helps you understand why the score is high or low.

```python
{
    "relevance": 4.0,
    "gpt_relevance": 4.0, 
    "relevance_reason": "The RESPONSE accurately answers the QUERY by stating that Marie Curie was born in Warsaw, which is correct and directly relevant to the question asked.",
    "relevance_result": "pass", 
    "relevance_threshold": 3
}
```

## Response completeness

AI systems can fabricate content or generate irrelevant responses outside the given context. Given a ground truth response, `ResponseCompletenessEvaluator` captures the *recall* aspect of response alignment with the expected response. This evaluator complements `GroundednessEvaluator`, which captures the *precision* aspect of response alignment with the grounding source.

### Response completeness example

```python
from azure.ai.evaluation import ResponseCompletenessEvaluator

response_completeness = ResponseCompletenessEvaluator(model_config=model_config, threshold=3)
response_completeness(
    response="Based on the retrieved documents, the shareholder meeting discussed the operational efficiency of the company and financing options.",
    ground_truth="The shareholder meeting discussed the compensation package of the company's CEO."
)
```

### Response completeness output

The numerical score on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), the evaluator also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
    "response_completeness": 1,
    "response_completeness_result": "fail",
    "response_completeness_threshold": 3,
    "response_completeness_reason": "The response does not contain any relevant information from the ground truth, which specifically discusses the CEO's compensation package. Therefore, it is considered fully incomplete."
}
```

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [More examples for quality evaluators](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)

::: moniker-end
