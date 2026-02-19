---
author: PatrickFarley
reviewer: patrickfarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/21/2025
ms.author: pafarley
ms.reviewer: pafarley
---

### Standard voices

Use this table to determine *availability of neural voices* by region or endpoint:

| Region | Endpoint |
|--------|----------|
| Australia East | `https://australiaeast.tts.speech.microsoft.com/cognitiveservices/v1` |
| Brazil South | `https://brazilsouth.tts.speech.microsoft.com/cognitiveservices/v1` |
| Canada Central | `https://canadacentral.tts.speech.microsoft.com/cognitiveservices/v1` |
| Canada East | `https://canadaeast.tts.speech.microsoft.com/cognitiveservices/v1` |
| Central US | `https://centralus.tts.speech.microsoft.com/cognitiveservices/v1` |
| East Asia | `https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1` |
| East US | `https://eastus.tts.speech.microsoft.com/cognitiveservices/v1` |
| East US 2 | `https://eastus2.tts.speech.microsoft.com/cognitiveservices/v1` |
| France Central | `https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1` |
| Germany West Central | `https://germanywestcentral.tts.speech.microsoft.com/cognitiveservices/v1` |
| India Central | `https://centralindia.tts.speech.microsoft.com/cognitiveservices/v1` |
| Italy North | `https://italynorth.tts.speech.microsoft.com/cognitiveservices/v1` |
| Japan East | `https://japaneast.tts.speech.microsoft.com/cognitiveservices/v1` |
| Japan West | `https://japanwest.tts.speech.microsoft.com/cognitiveservices/v1` |
| Korea Central | `https://koreacentral.tts.speech.microsoft.com/cognitiveservices/v1` |
| North Central US | `https://northcentralus.tts.speech.microsoft.com/cognitiveservices/v1` |
| North Europe | `https://northeurope.tts.speech.microsoft.com/cognitiveservices/v1` |
| Norway East | `https://norwayeast.tts.speech.microsoft.com/cognitiveservices/v1` |
| Qatar Central | `https://qatarcentral.tts.speech.microsoft.com/cognitiveservices/v1` |
| South Africa North | `https://southafricanorth.tts.speech.microsoft.com/cognitiveservices/v1` |
| South Central US | `https://southcentralus.tts.speech.microsoft.com/cognitiveservices/v1` |
| Southeast Asia | `https://southeastasia.tts.speech.microsoft.com/cognitiveservices/v1` |
| Sweden Central | `https://swedencentral.tts.speech.microsoft.com/cognitiveservices/v1`|
| Switzerland North | `https://switzerlandnorth.tts.speech.microsoft.com/cognitiveservices/v1`|
| Switzerland West | `https://switzerlandwest.tts.speech.microsoft.com/cognitiveservices/v1`|
| UAE North | `https://uaenorth.tts.speech.microsoft.com/cognitiveservices/v1`|
| UK South | `https://uksouth.tts.speech.microsoft.com/cognitiveservices/v1` |
| UK West | `https://ukwest.tts.speech.microsoft.com/cognitiveservices/v1` |
| US Gov Arizona | `https://usgovarizona.tts.speech.azure.us/cognitiveservices/v1`|
| US Gov Virginia | `https://usgovvirginia.tts.speech.azure.us/cognitiveservices/v1`|
| West Central US | `https://westcentralus.tts.speech.microsoft.com/cognitiveservices/v1` |
| West Europe | `https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1` |
| West US | `https://westus.tts.speech.microsoft.com/cognitiveservices/v1` |
| West US 2 | `https://westus2.tts.speech.microsoft.com/cognitiveservices/v1` |
| West US 3 | `https://westus3.tts.speech.microsoft.com/cognitiveservices/v1` |

> [!TIP]
> For the current list of regions that support voices in preview, see the [Speech service regions table](../regions.md?tabs=tts).

### Custom voices

If you created a custom voice, use the endpoint that you created. You can also use the following endpoints. Replace `{deploymentId}` with the deployment ID for your custom voice model.

| Region | Training |Deployment |Endpoint |
|--------|----------|----------|----------|
| Australia East |Yes|Yes| `https://australiaeast.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Brazil South | No |Yes| `https://brazilsouth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Canada Central | No |Yes|`https://canadacentral.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Central US | No |Yes| `https://centralus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| East Asia | No |Yes| `https://eastasia.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| East US |Yes| Yes | `https://eastus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| East US 2 |Yes| Yes |`https://eastus2.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| France Central | No |Yes| `https://francecentral.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Germany West Central | No |Yes| `https://germanywestcentral.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| India Central |Yes| Yes | `https://centralindia.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Italy North | No |Yes| `https://italynorth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Japan East |Yes| Yes | `https://japaneast.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Japan West | No |Yes| `https://japanwest.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Korea Central |Yes|Yes| `https://koreacentral.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| North Central US | No |Yes| `https://northcentralus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| North Europe |Yes|Yes| `https://northeurope.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Norway East| No |Yes| `https://norwayeast.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| South Africa North | No |Yes| `https://southafricanorth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| South Central US |Yes|Yes| `https://southcentralus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Southeast Asia |Yes|Yes| `https://southeastasia.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Sweden Central | No |Yes| `https://swedencentral.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Switzerland North | No |Yes| `https://switzerlandnorth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| Switzerland West | No |Yes| `https://switzerlandwest.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| UAE North | No |Yes| `https://uaenorth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}`|
| UK South |Yes| Yes | `https://uksouth.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| West Central US | No |Yes| `https://westcentralus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| West Europe |Yes|Yes| `https://westeurope.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| West US |Yes|Yes| `https://westus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| West US 2 |Yes|Yes| `https://westus2.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |
| West US 3 | No |Yes| `https://westus3.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId={deploymentId}` |

> [!NOTE]
> The preceding regions are available for standard voice model hosting and real-time synthesis. Custom voice training is only available in some regions. But you can easily [copy a custom voice model](../professional-voice-train-voice.md) from these regions to other regions in the preceding list.

### Long Audio API

The Long Audio API is available in multiple regions with unique endpoints:

| Region | Endpoint |
|--------|----------|
| Australia East | `https://australiaeast.customvoice.api.speech.microsoft.com` |
| East US | `https://eastus.customvoice.api.speech.microsoft.com` |
| India Central | `https://centralindia.customvoice.api.speech.microsoft.com` |
| South Central US | `https://southcentralus.customvoice.api.speech.microsoft.com` |
| Southeast Asia | `https://southeastasia.customvoice.api.speech.microsoft.com` |
| UK South | `https://uksouth.customvoice.api.speech.microsoft.com` |
| West Europe | `https://westeurope.customvoice.api.speech.microsoft.com` |
