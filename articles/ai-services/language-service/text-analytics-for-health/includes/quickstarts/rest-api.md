---
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 11/18/2025
ms.service: azure-ai-language
ms.topic: include
ms.custom:
  - ignite-2024
  - build-2025
---
[Reference documentation](https://go.microsoft.com/fwlink/?linkid=2239169)

Use this quickstart to send language detection requests using the REST API. In the following example, you use cURL to identify medical [entities](../../concepts/health-entity-categories.md), [relations](../../concepts/relation-extraction.md), and [assertions](../../concepts/assertion-detection.md) that appear in text.


## Prerequisites

* The current version of [cURL](https://curl.haxx.se/)
* An Azure subscription - [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, [create a Foundry resource](../../../../../ai-services/multi-service-resource.md?pivots=azportal).
    * You need the key and endpoint from the resource you create to connect your application to the API. You paste your key and endpoint into the code later in the quickstart.
    * You can use the free pricing tier (`Free F0`) to try the service (providing 5,000 text records - 1,000 characters each) and upgrade later to the `Standard S` pricing tier for production. You can also start with the `Standard S` pricing tier, receiving the same initial quota for free (5,000 text records) before getting charged. For more information on pricing, visit [Language Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/language-service/).

> [!NOTE]
> * The following BASH examples use the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.
> * You can find language specific samples on [GitHub](https://github.com/Azure-Samples/cognitive-services-quickstart-code).
> * Go to the Azure portal and find the key and endpoint for Azure Language resource you created in the prerequisites. They are located on the resource's **key and endpoint** page, under **resource management**. Then replace the strings in the code below with your key and endpoint.
To call the API, you need the following information:

## Setting up

[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]



|parameter  |Description  |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your endpoint for accessing the API.        |
|`-H Content-Type: application/json`     | The content type for sending JSON data.          |
|`-H "Ocp-Apim-Subscription-Key:<key>`    | Specifies the key for accessing the API.        |
|`-d <documents>`     | The JSON containing the documents you want to send.         |

The following cURL commands are executed from a BASH shell. Edit these commands with your own resource name, resource key, and JSON values.




## Text Analytics for health

[!INCLUDE [REST API quickstart instructions](../../../includes/rest-api-instructions.md)]

[!INCLUDE [Sample request](request.md)]


> [!TIP]
> Fast Healthcare Interoperability Resources (FHIR) structuring is available using Azure Language REST API. The client libraries are not currently supported. [Learn more](../../how-to/call-api.md) on how to use FHIR structuring in your API call.
