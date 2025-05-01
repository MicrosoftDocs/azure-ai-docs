---
title: "Groundedness detection in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about groundedness in large language model (LLM) responses, and how to detect outputs that deviate from source material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: conceptual
ms.date: 10/16/2024
ms.author: pafarley
---

#  Groundedness detection

The Groundedness detection API detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungroundedness refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials.

## Key terms

- **Retrieval Augmented Generation (RAG)**: RAG is a technique for augmenting LLM knowledge with other data. LLMs can reason about wide-ranging topics, but their knowledge is limited to the public data that was available at the time they were trained. If you want to build AI applications that can reason about private data or data introduced after a model’s cutoff date, you need to provide the model with that specific information. The process of bringing the appropriate information and inserting it into the model prompt is known as Retrieval Augmented Generation (RAG). For more information, see [Retrieval-augmented generation (RAG)](https://python.langchain.com/docs/tutorials/rag/).
- **Groundedness and Ungroundedness in LLMs**: This refers to the extent to which the model's outputs are based on provided information or reflect reliable sources accurately. A grounded response adheres closely to the given information, avoiding speculation or fabrication. In groundedness measurements, source information is crucial and serves as the grounding source.

## Groundedness detection options

The following options are available for Groundedness detection in Azure AI Content Safety:

- **Domain Selection**: Users can choose an established domain to ensure more tailored detection that aligns with the specific needs of their field. The current available domains are `MEDICAL` and `GENERIC`.
- **Task Specification**: This feature lets you select the task you're doing, such as QnA (question & answering) and Summarization, with adjustable settings according to the task type.
- **Speed vs Interpretability**: There are two modes that trade off speed with result interpretability.
   - Non-Reasoning mode: Offers fast detection capability; easy to embed into online applications.
   - Reasoning mode: Offers detailed explanations for detected ungrounded segments; better for understanding and mitigation.

##  Use cases

Groundedness detection supports text-based Summarization and QnA tasks to ensure that the generated summaries or answers are accurate and reliable. Here are some examples of each use case:

**Summarization tasks**:
- Medical summarization: In the context of medical news articles, Groundedness detection can be used to ensure that the summary doesn't contain fabricated or misleading information, guaranteeing that readers obtain accurate and reliable medical information.
- Academic paper summarization: When the model generates summaries of academic papers or research articles, the function can help ensure that the summarized content accurately represents the key findings and contributions without introducing false claims.

**QnA tasks**:
- Customer support chatbots: In customer support, the function can be used to validate the answers provided by AI chatbots, ensuring that customers receive accurate and trustworthy information when they ask questions about products or services.
- Medical QnA: For medical QnA, the function helps verify the accuracy of medical answers and advice provided by AI systems to healthcare professionals and patients, reducing the risk of medical errors.
- Educational QnA: In educational settings, the function can be applied to QnA tasks to confirm that answers to academic questions or test prep queries are factually accurate, supporting the learning process.


## Groundedness correction

The groundedness detection API includes a correction feature that automatically corrects any detected ungroundedness in the text based on the provided grounding sources. When the correction feature is enabled, the response includes a `corrected Text` field that presents the corrected text aligned with the grounding sources.

###  Use cases

Below, see several common scenarios that illustrate how and when to apply these features to achieve the best outcomes.

#### Summarization in medical contexts

You're summarizing medical documents, and it’s critical that the names of patients in the summaries are accurate and consistent with the provided grounding sources.

Example API Request:

```json
{
  "domain": "Medical",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
}
```

**Expected outcome:**

The correction feature detects that `Kevin` is ungrounded because it conflicts with the grounding source `Jane`. The API returns the corrected text: `"The patient name is Jane."`

#### Question and answer (QnA) task with customer support data

You're implementing a QnA system for a customer support chatbot. It’s essential that the answers provided by the AI align with the most recent and accurate information available.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "QnA",
  "qna": {
    "query": "What is the current interest rate?"
  },
  "text": "The interest rate is 5%.",
  "groundingSources": [
    "As of July 2024, the interest rate is 4.5%."
  ],
}
```
**Expected outcome:**

The API detects that `5%` is ungrounded because it does not match the provided grounding source `4.5%`. The response includes the correction text: `"The interest rate is 4.5%."`


#### Content creation with historical data

You're creating content that involves historical data or events, where accuracy is critical to maintaining credibility and avoiding misinformation.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "Summarization",
  "text": "The Battle of Hastings occurred in 1065.",
  "groundingSources": [
    "The Battle of Hastings occurred in 1066."
  ],
}
```
**Expected outcome:**

The API detects the ungrounded date `1065` and corrects it to `1066` based on the grounding source. The response includes the corrected text: `"The Battle of Hastings occurred in 1066."`


#### Internal documentation summarization

You're summarizing internal documents where product names, version numbers, or other specific data points must remain consistent.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "Summarization",
  "text": "Our latest product is SuperWidget v2.1.",
  "groundingSources": [
    "Our latest product is SuperWidget v2.2."
  ],
}
```

**Expected outcome:**

The correction feature identifies `SuperWidget v2.1` as ungrounded and updates it to `SuperWidget v2.2` in the response. The response returns the corrected text: `"Our latest product is SuperWidget v2.2."`

## Best practices

Adhere to the following best practices when setting up RAG systems to get the best performance out of the groundedness detection API:
- When dealing with product names or version numbers, use grounding sources directly from internal release notes or official product documentation to ensure accuracy.
- For historical content, cross-reference your grounding sources with trusted academic or historical databases to ensure the highest level of accuracy.
- In a dynamic environment like finance, always use the most recent and reliable grounding sources to ensure your AI system provides accurate and timely information.
- Always ensure that your grounding sources are accurate and up-to-date, particularly in sensitive fields like healthcare. This minimizes the risk of errors in the summarization process.

## Limitations

### Language availability

Currently, the Groundedness detection API supports English language content. While our API doesn't restrict the submission of non-English content, we can't guarantee the same level of quality and accuracy in the analysis of other language content. We recommend that users submit content primarily in English to ensure the most reliable and accurate results from the API.

### Text length limitations

See [Input requirements](../overview.md#input-requirements) for maximum text length limitations.

### Region availability

To use this API, you must create your Azure AI Content Safety resource in the supported regions. See [Region availability](/azure/ai-services/content-safety/overview#region-availability).

### Rate limitations

See [Query rates](/azure/ai-services/content-safety/overview#query-rates).

If you need a higher rate, [contact us](mailto:contentsafetysupport@microsoft.com) to request it.

## Next steps

Follow the quickstart to get started using Azure AI Content Safety to detect groundedness.

> [!div class="nextstepaction"]
> [Groundedness detection quickstart](../quickstart-groundedness.md)
