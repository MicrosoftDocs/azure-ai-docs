---
title: "Retrieval-Augmented Generation (RAG) Evaluators for Generative AI"
description: "Learn about Retrieval-Augmented Generation evaluators for assessing relevance, groundedness, and response completeness in generative AI systems."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 02/25/2026
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
---

# Retrieval-Augmented Generation (RAG) evaluators
[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

A Retrieval-Augmented Generation (RAG) system tries to generate the most relevant answer consistent with grounding documents in response to a user's query. A user's query triggers a search retrieval in the corpus of grounding documents to provide grounding context for the AI model to generate a response.

| Evaluator | Best practice | Use when | Purpose | Output |
|--|--|--|--|--|
| Document Retrieval | Process evaluation | Retrieval quality is a bottleneck for your RAG, and you have query relevance labels (ground truth) for precise search quality metrics for debugging and parameter optimization | Measures search quality metrics (Fidelity, NDCG, XDCG, Max Relevance, Holes) by comparing retrieved documents against ground truth labels | Composite: Fidelity, NDCG, XDCG, Max Relevance, Holes (with Pass/Fail) |
| Retrieval | Process evaluation | You want to assess textual quality of retrieved context, but you don't have ground truths | Measures how relevant the retrieved context chunks are to addressing a query using an LLM judge | Binary: Pass/Fail based on threshold (1-5 scale) |
| Groundedness | System evaluation | You want a well-rounded groundedness definition that works with agent inputs, and bring your own GPT models as the LLM-judge | Measures how well the generated response aligns with the given context without fabricating content (precision aspect) | Binary: Pass/Fail based on threshold (1-5 scale) |
| Groundedness Pro (preview) | System evaluation | You want a strict groundedness definition powered by Azure AI Content Safety and use our service model | Detects if the response is strictly consistent with the context using the Azure AI Content Safety service | Binary: True/False |
| Relevance | System evaluation | You want to assess how well the RAG response addresses the query but don't have ground truths | Measures the accuracy, completeness, and direct relevance of the response to the query | Binary: Pass/Fail based on threshold (1-5 scale) |
| Response Completeness | System evaluation | You want to ensure the RAG response doesn't miss critical information (recall aspect) from your ground truth | Measures how completely the response covers the expected information compared to ground truth | Binary: Pass/Fail based on threshold (1-5 scale) |

Think about *groundedness* and *response completeness* as:

- Groundedness focuses on the *precision* aspect of the response. It doesn't contain content outside of the grounding context.
- Response completeness focuses on the *recall* aspect of the response. It doesn't miss critical information compared to the expected response or ground truth.

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

RAG evaluators assess how well AI systems retrieve and use context to generate grounded responses. Each evaluator requires specific data mappings and parameters:

| Evaluator | Required inputs | Required parameters |
|-----------|-----------------|---------------------|
| Groundedness | (`response`, `context`) OR (`query`, `response`) | `deployment_name` |
| Groundedness Pro (preview) | `query`, `response`, `context` | *(none)* |
| Relevance | `query`, `response` | `deployment_name` |
| Response Completeness | `ground_truth`, `response` | `deployment_name` |
| Retrieval | `query`, `context` | `deployment_name` |
| Document Retrieval | `retrieval_ground_truth`, `retrieved_documents` | *(none)* |

### Example input

Your test dataset should contain the fields referenced in your data mappings:

```jsonl
{"query": "What are the store hours?", "context": "Our store is open Monday-Friday 9am-6pm and Saturday 10am-4pm.", "response": "The store is open weekdays from 9am to 6pm and Saturdays from 10am to 4pm."}
{"query": "What is the return policy?", "context": "Items can be returned within 30 days with original receipt for full refund.", "response": "You can return items within 30 days if you have your receipt."}
```

### Configuration example

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_items}}` references agent responses generated or retrieved during evaluation. Use this when evaluating with an agent target or agent response data source. For agent evaluation, `context` is optional if the response contains tool calls—the evaluator can extract context from tool call results.

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "groundedness",
        "evaluator_name": "builtin.groundedness",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {
            "context": "{{item.context}}",
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

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example output

These evaluators return scores on a 1-5 Likert scale (1 = very poor, 5 = excellent). The default pass threshold is 3. Scores at or above the threshold are considered passing. Key output fields:

```json
{
    "type": "azure_ai_evaluator",
    "name": "Groundedness",
    "metric": "groundedness",
    "score": 4,
    "label": "pass",
    "reason": "The response is well-grounded in the provided context without fabricating content.",
    "threshold": 3,
    "passed": true
}
```

## Document retrieval

Because of its upstream role in RAG, the retrieval quality is important. If the retrieval quality is poor and the response requires corpus-specific knowledge, there's less chance your language model gives you a satisfactory answer. The most precise measurement is to use the `document_retrieval` evaluator to evaluate retrieval quality and optimize your search parameters for RAG.

- Document retrieval evaluator measures how well the RAG retrieves the correct documents from the document store. As a composite evaluator useful for RAG scenario with ground truth, it computes a list of useful search quality metrics for debugging your RAG pipelines:

  | Metric | Category | Description |
  |--|--|--|
  | Fidelity | Search Fidelity | How well the top n retrieved chunks reflect the content for a given query: number of good documents returned out of the total number of known good documents in a dataset |
  | NDCG | Search NDCG | How good are the rankings to an ideal order where all relevant items are at the top of the list |
  | XDCG | Search XDCG | How good the results are in the top-k documents regardless of scoring of other index documents |
  | Max Relevance N | Search Max Relevance | Maximum relevance in the top-k chunks |
  | Holes | Search Label Sanity | Number of documents with missing query relevance judgments, or ground truth |

- To optimize your RAG in a scenario called *parameter sweep*, you can use these metrics to calibrate the search parameters for the optimal RAG results. Generate different retrieval results for various search parameters such as search algorithms (vector, semantic), top_k, and chunk sizes you're interested in testing. Then use `document_retrieval` to find the search parameters that yield the highest retrieval quality.

### Document retrieval example

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

### Document retrieval output

The `document_retrieval` evaluator returns multiple metrics for retrieval quality:

```python
[
    {
        "type": "azure_ai_evaluator",
        "name": "Document Retrieval",
        "metric": "ndcg@3",
        "score": 0.646,
        "label": "pass",
        "passed": true
    },
    {
        "type": "azure_ai_evaluator",
        "name": "Document Retrieval",
        "metric": "fidelity",
        "score": 0.019,
        "label": "fail",
        "passed": false
    },
    # more metrics...
]
```

## Related content

- [More examples for quality evaluators](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [How to run agent evaluation](../../observability/how-to/evaluate-agent.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)
