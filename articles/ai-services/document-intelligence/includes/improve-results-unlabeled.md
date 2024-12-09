---
author: laujan
ms.service: azure-ai-document-intelligence
ms.topic: include
ms.date: 08/21/2023
ms.author: lajanuar
---

Examine the `"confidence"` values for each key/value result under the `"pageResults"` node. You should also look at the confidence scores in the `"readResults"` node, which correspond to the text read operation. The confidence of the read results doesn't affect the confidence of the key/value extraction results, so you should check both.

- If the confidence scores for the read operation are low, try to improve the quality of your input documents. For more information, see [Input requirements](../model-overview.md#input-requirements).
- If the confidence scores for the key/value extraction operation are low, ensure that the documents being analyzed are of the same type as documents used in the training set. If the documents in the training set have variations in appearance, consider splitting them into different folders and training one model for each variation.

The confidence scores you target depends on your use case, but generally it's a good practice to target a score of 80 percent or higher. For more sensitive cases, like reading medical records or billing statements, we recommend a score of 100 percent.
