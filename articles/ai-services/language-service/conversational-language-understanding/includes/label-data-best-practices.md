---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
## Clearly label utterances 

* Ensure that the concepts that your entities refer to are well defined and separable. Check if you can easily determine the differences reliably. If you can't, this lack of distinction might indicate difficulty for the learned component.
* Ensure that some aspect of your data can provide a signal for differences when there's a similarity between entities.

    For example, if you built a model to book flights, a user might use an utterance like "I want a flight from Boston to Seattle." The *origin city* and *destination city* for such utterances would be expected to be similar. A signal to differentiate *origin city* might be that the word *from* often precedes it.

* Ensure that you label all instances of each entity in both your training and testing data. One approach is to use the search function to find all instances of a word or phrase in your data to check if they're correctly labeled.
* Ensure that you label test data for entities without [learned components](../concepts/entity-components.md#learned-component) and also for the entities with them. This practice helps to ensure that your evaluation metrics are accurate.
