---
title: "Quickstart: Use use protected material detection for text with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
---


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [cURL](https://curl.haxx.se/) installed

## Analyze text for protected material detection

The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys that come with your resource.
1. Optionally, replace the `"text"` field in the body with your own text you'd like to analyze.
    > [!TIP]
    > See [Input requirements](../../overview.md#input-requirements) for maximum text length limitations. Protected material detection is meant to be run on LLM completions, not user prompts.

```shell
curl --location --request POST '<endpoint>/contentsafety/text:detectProtectedMaterial?api-version=2024-09-01' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "text": "Kiss me out of the bearded barley Nightly beside the green, green grass Swing, swing, swing the spinning step You wear those shoes and I will wear that dress Oh, kiss me beneath the milky twilight Lead me out on the moonlit floor Lift your open hand Strike up the band and make the fireflies dance Silver moon's sparkling So, kiss me Kiss me down by the broken tree house Swing me upon its hanging tire Bring, bring, bring your flowered hat We'll take the trail marked on your father's map."
}'
```
The below fields must be included in the url:

| Name      |Required?  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. The current version is: api-version=2024-09-01. Example: `<endpoint>/contentsafety/text:detectProtectedMaterial?api-version=2024-09-01` |String |

The parameters in the request body are defined in this table:

| Name        | Required?     | Description  | Type    |
| :---------- | ----------- | :------------ | ------- |
| **text**    | Required | This is the raw text to be checked. Other non-ascii characters can be included. | String  |

See the following sample request body:
```json
{
  "text": "string"
}
```

Open a command prompt window and run the cURL command.

### Interpret the API response

You should see the protected material detection results displayed as JSON data in the console output. For example:

```json
{
  "protectedMaterialAnalysis": {
    "detected": true
  }
}
```

The JSON fields in the output are defined here:

| Name     | Description   | Type   |
| :------------- | :--------------- | ------ |
| **protectedMaterialAnalysis**   | Each output class that the API predicts. | String |
| **detected** | Whether protected material was detected or not.  | Boolean |

## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../multi-service-resource.md?pivots=azcli#clean-up-resources)

