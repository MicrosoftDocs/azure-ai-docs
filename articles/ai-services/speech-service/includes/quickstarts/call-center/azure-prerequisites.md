---
author: PatrickFarley
ms.service: azure-ai-speech
ms.date: 09/29/2022
ms.topic: include
ms.author: pafarley
---

> [!div class="checklist"]
> * Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
> * <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry" title="Create a Microsoft Foundry resource" target="_blank">Create a multi-service resource</a> in the Azure portal. This quickstart only requires one Foundry Tools [multi-service resource](../../../../multi-service-resource.md?pivots=azportal). The sample code allows you to specify separate Language and Speech resource keys.
> * Get the resource key and region. After your Microsoft Foundry resource is deployed, select **Go to resource** to view and manage keys.

> [!IMPORTANT]
> This quickstart requires access to [conversation summarization](../../../../language-service/summarization/how-to/conversation-summarization.md). To get access, you must submit an [online request](https://aka.ms/applyforconversationsummarization/) and have it approved. 
> 
> The `--languageKey` and `--languageEndpoint` values in this quickstart must correspond to a resource that's in one of the regions supported by the [conversation summarization API](https://aka.ms/convsumregions): `eastus`, `northeurope`, and `uksouth`.
