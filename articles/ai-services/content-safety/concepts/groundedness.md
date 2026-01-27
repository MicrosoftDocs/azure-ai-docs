---
title: "Groundedness detection in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about groundedness in large language model (LLM) responses, and how to detect outputs that deviate from source material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 11/21/2025
ms.author: pafarley
---

#  Groundedness detection

[!INCLUDE [groundedness-detection-overview](../includes/groundedness-detection-overview.md)]

## Groundedness detection options

The following options are available for Groundedness detection in Azure AI Content Safety:

- **Domain Selection**: Users can choose an established domain to ensure more tailored detection that aligns with the specific needs of their field. The current available domains are `MEDICAL` and `GENERIC`.
- **Task Specification**: This feature lets you select the task you're doing, such as QnA (question & answering) and Summarization, with adjustable settings according to the task type.
- **Speed vs Interpretability**: There are two modes that trade off speed with result interpretability.
   - Non-Reasoning mode: Offers fast detection capability; easy to embed into online applications.
   - Reasoning mode: Offers detailed explanations for detected ungrounded segments; better for understanding and mitigation.

## Groundedness correction

The groundedness detection API includes a correction feature that automatically corrects any detected ungroundedness in the text based on the provided grounding sources. When the correction feature is enabled, the response includes a `corrected Text` field that presents the corrected text aligned with the grounding sources.


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

## Next step

Follow the quickstart to get started using Azure AI Content Safety to detect groundedness.

> [!div class="nextstepaction"]
> [Groundedness detection quickstart](../quickstart-groundedness.md)
