---
title: Authentication and authorization in Azure Translator in Foundry Tools service
titleSuffix: Foundry Tools
description: "There are several ways to authenticate a request and authorize access to Azure Translator resource In this article, learn about each method, and how to make a request."
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Authentication and authorization

Each request to a Foundry Tool must include an authentication header. This header passes along a resource key or authentication token, which is used to validate your subscription for a service or group of services. In this article, you can explore ways to authenticate a request and the requirements for each.

* Authenticate with a [single-service regional](#authenticating-with-a-regional-resource), [single-service-global](#authenticating-with-a-global-resource) or [multi-service](#authenticating-with-a-multi-service-resource) resource key.
* Authenticate with a [bearer token](#authenticating-with-an-access-token).
* Authenticate with [Microsoft Entra ID](../../how-to/microsoft-entra-id-auth.md) is a cloud-based identity solution designed to manage user access and permissions for Microsoft services, resources, and applications. Microsoft Entra ID enables you to authenticate requests to your Azure resources without the need for passwords or keys. 

## Headers

Subscribe to Translator or [multi-service](https://azure.microsoft.com/pricing/details/cognitive-services/) in Foundry Tools, and use your key (available in the Azure portal) to authenticate.

There are three headers that you can use to authenticate your subscription. This table describes how each is used:

|Headers|Description|
|:----|:----|
|Ocp-Apim-Subscription-Key|*Use with Foundry Tools subscription if you're passing your secret key*.<br/>The value is the Azure secret key for your subscription to Translator.|
|Authorization|*Use with Foundry Tools subscription if you're passing an authentication token.*<br/>The value is the Bearer token: `Bearer <token>`.|
|Ocp-Apim-Subscription-Region|*Use with multi-service and regional translator resource.*<br/>The value is the region of the multi-service or regional translator resource. This value is optional when using a global translator resource.|

### Secret key

The first option is to authenticate using the `Ocp-Apim-Subscription-Key` header. Add the `Ocp-Apim-Subscription-Key: <YOUR_SECRET_KEY>` header to your request.

#### Authenticating with a global resource

When you use a [global translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation), you need to include one header to call the Translator.

|Headers|Description|
|:-----|:----|
|Ocp-Apim-Subscription-Key| The value is the Azure secret key for your subscription to Translator.|

Here's an example request to call the Translator using the global translator resource

 ```bash
// Pass secret key using headers
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=es" \
     -H "Ocp-Apim-Subscription-Key:<your-key>" \
     -H "Content-Type: application/json" \
     -d "[{'Text':'Hello, what is your name?'}]"
```

#### Authenticating with a regional resource

When you use a [regional translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation),
there are two headers that you need to call the Translator.

|Headers|Description|
|:-----|:----|
|Ocp-Apim-Subscription-Key| The value is the Azure secret key for your subscription to Translator.|
|Ocp-Apim-Subscription-Region| The value is the region of the translator resource. |

Here's an example request to call the Translator using the regional translator resource

 ```bash
// Pass secret key and region using headers
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=es" \
     -H "Ocp-Apim-Subscription-Key:<your-key>" \
     -H "Ocp-Apim-Subscription-Region:<your-region>" \
     -H "Content-Type: application/json" \
     -d "[{'Text':'Hello, what is your name?'}]"
```

#### Authenticating with a multi-service resource

A multi-service resource allows you to use a single API key to authenticate requests for multiple services.

When you use a multi-service secret key, you must include two authentication headers with your request. There are two headers that you need to call the Translator.

|Headers|Description|
|:-----|:----|
|Ocp-Apim-Subscription-Key| The value is the Azure secret key for your multi-service resource.|
|Ocp-Apim-Subscription-Region| The value is the region of the multi-service resource. |

Region is required for the multi-service Text API subscription. The region you select is the only region that you can use for text translation when using the multi-service key. It must be the same region you selected when you signed up for your multi-service subscription through the Azure portal.

If you pass the secret key in the query string with the parameter `Subscription-Key`, then you must specify the region with query parameter `Subscription-Region`.

### Authenticating with an access token

Alternatively, you can exchange your secret key for an access token. This token is included with each request as the `Authorization` header. To obtain an authorization token, make a `POST` request to the following URL:

| Resource type     | Authentication service URL                                |
|-----------------|-----------------------------------------------------------|
| Global          | `https://api.cognitive.microsoft.com/sts/v1.0/issueToken` |
| Regional or Multi-Service | `https://<your-region>.api.cognitive.microsoft.com/sts/v1.0/issueToken` |

Here are example requests to obtain a token given a secret key for a global resource:

 ```bash
// Pass secret key using header
curl --header 'Ocp-Apim-Subscription-Key: <your-key>' --data "" 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'

// Pass secret key using query string parameter
curl --data "" 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken?Subscription-Key=<your-key>'
```

And here are example requests to obtain a token given a secret key for a regional resource located in Central US:

 ```bash
// Pass secret key using header
curl --header "Ocp-Apim-Subscription-Key: <your-key>" --data "" "https://centralus.api.cognitive.microsoft.com/sts/v1.0/issueToken"

// Pass secret key using query string parameter
curl --data "" "https://centralus.api.cognitive.microsoft.com/sts/v1.0/issueToken?Subscription-Key=<your-key>"
```

A successful request returns the encoded access token as plain text in the response body. The valid token is passed to the Translator as a bearer token in the Authorization.

```bash
Authorization: Bearer <Base64-access_token>
```

An authentication token is valid for 10 minutes. The token should be reused when making multiple calls to the Translator. However, if your program makes requests to the Translator over an extended period of time, then your program must request a new access token at regular intervals (for example, every 8 minutes).

<a name='authentication-with-azure-active-directory-azure-ad'></a>

## Authentication with Microsoft Entra ID

 Translator v3.0 supports Microsoft Entra authentication, Microsoft's cloud-based identity and access management solution. Authorization headers enable the Translator to validate that the requesting client is authorized to use the resource and to complete the request.

### **Prerequisites**

* A brief understanding of how to [**authenticate with Microsoft Entra ID**](../../../authentication.md?tabs=powershell#authenticate-with-azure-active-directory).

* A brief understanding of how to [**authorize access to managed identities**](../../../authentication.md?tabs=powershell#authorize-access-to-managed-identities).

### **Microsoft Entra ID headers**

|Header|Value|
|:-----|:----|
|Authorization| The value is an access **bearer token** generated by Microsoft Entra ID.</br><ul><li> The bearer token provides proof of authentication and validates the client's authorization to use the resource.</li><li> An authentication token is valid for 10 minutes and should be reused when making multiple calls to Translator.</br></li>*See* [Sample request: 2. Get a token]( ../../../authentication.md?tabs=powershell#sample-request)</ul>|
|Ocp-Apim-Subscription-Region| The value is the region of the **translator resource**.</br><ul><li> This value is optional if the resource is global.</li></ul>|
|Ocp-Apim-ResourceId| The value is the Resource ID for your Translator resource instance.</br><ul><li>You find the Resource ID in the Azure portal at **Translator Resource  → Properties**. </li><li>Resource ID format: </br>/subscriptions/<**subscriptionId**>/resourceGroups/<**resourceGroupName**>/providers/Microsoft.CognitiveServices/accounts/<**resourceName**>/</li></ul>|

##### **Translator property page—Azure portal**

:::image type="content" source="../../media/managed-identities/resource-id-property.png" alt-text="Screenshot:Translator properties page in the Azure portal. ":::

> [!IMPORTANT]
> Assign [**Cognitive Services User**](/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-user) role to the service principal. By assigning this role, you're granting service principal access to the Translator resource.

### **Examples**

#### **Using the global endpoint**

 ```bash
 // Using headers, pass a bearer token generated by Azure AD, resource ID, and the region.

curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=es" \
     -H "Authorization: Bearer <Base64-access_token>"\
     -H "Ocp-Apim-ResourceId: <Resource ID>" \
     -H "Ocp-Apim-Subscription-Region: <your-region>" \
     -H "Content-Type: application/json" \
     -data-raw "[{'Text':'Hello, friend.'}]"
```

#### **Using your custom endpoint**

 ```bash
// Using headers, pass a bearer token generated by Azure AD.

curl -X POST https://<your-custom-domain>.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es \
     -H "Authorization: Bearer <Base64-access_token>"\
     -H "Content-Type: application/json" \
     -data-raw "[{'Text':'Hello, friend.'}]"
```

### **Examples using managed identities**

Translator v3.0 also supports authorizing access to managed identities. If a managed identity is enabled for a translator resource, you can pass the bearer token generated by managed identity in the request header.

#### **With the global endpoint**

 ```bash
// Using headers, pass a bearer token generated either by Azure AD or Managed Identities, resource ID, and the region.

curl -X POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=es \
     -H "Authorization: Bearer <Base64-access_token>"\
     -H "Ocp-Apim-ResourceId: <Resource ID>" \
     -H "Ocp-Apim-Subscription-Region: <your-region>" \
     -H "Content-Type: application/json" \
     -data-raw "[{'Text':'Hello, friend.'}]"
```

#### **With your custom endpoint**

 ```bash
//Using headers, pass a bearer token generated by Managed Identities.

curl -X POST https://<your-custom-domain>.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es \
     -H "Authorization: Bearer <Base64-access_token>"\
     -H "Content-Type: application/json" \
     -data-raw "[{'Text':'Hello, friend.'}]"
```
## Virtual Network support

The Translator is now available with Virtual Network (`VNET`) capabilities in all regions of the Azure public cloud. To enable Virtual Network, *See* [Configuring Foundry Tools virtual networks](../../../cognitive-services-virtual-networks.md?tabs=portal).

Once you turn on this capability, you must use the custom endpoint to call the Translator. You can't use the global translator endpoint ("api.cognitive.microsofttranslator.com") and you can't authenticate with an access token.

You can find the custom endpoint after you create a [translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) and allow access from selected networks and private endpoints.

1. Navigate to your Translator resource in the Azure portal.
1. Select **Networking** from the **Resource Management** section.
1. Under the **Firewalls and virtual networks** tab, choose **Selected Networks and Private Endpoints**.

   :::image type="content" source="../../media/virtual-network-setting-azure-portal.png" alt-text="Screenshot of the virtual network setting in the Azure portal.":::

1. Select **Save** to apply your changes.
1. Select **Keys and Endpoint** from the **Resource Management** section.
1. Select the **Virtual Network** tab.
1. Listed there are the endpoints for Text Translation and Document Translation.

   :::image type="content" source="../../media/virtual-network-endpoint.png" alt-text="Screenshot of the virtual network endpoint.":::

|Headers|Description|
|:-----|:----|
|Ocp-Apim-Subscription-Key| The value is the Azure secret key for your subscription to Translator.|
|Ocp-Apim-Subscription-Region| The value is the region of the translator resource. This value is optional if the resource is `global`|

Here's an example request to call the Translator using the custom endpoint

 ```bash
// Pass secret key and region using headers
curl -X POST "https://<your-custom-domain>.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es" \
     -H "Ocp-Apim-Subscription-Key:<your-key>" \
     -H "Ocp-Apim-Subscription-Region:<your-region>" \
     -H "Content-Type: application/json" \
     -d "[{'Text':'Hello, what is your name?'}]"
```

