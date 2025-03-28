---
title: Authentication in Azure AI Translator service
titleSuffix: Azure AI services
description: "There are several ways to authenticate a request to Azure AI Translator resource In this article, you'll learn about each method, and how to make a request."
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 03/26/2025
ms.author: lajanuar
---

# Authentication

Each request to an Azure AI service must include an authentication header. This header passes along a resource key or authentication token, which is used to validate your subscription for a service or group of services. In this article, you'll learn ways to authenticate a request and the requirements for each.

* Authenticate with a [single-service]() or [multi-service]() resource key.
* Authenticate with a [bearer token]().
* Authenticate with [Microsoft Entra ID]().
## Authentication

Subscribe to Translator or [multi-service](https://azure.microsoft.com/pricing/details/cognitive-services/) in Azure AI services, and use your key (available in the Azure portal) to authenticate.

There are three headers that you can use to authenticate your subscription. This table describes how each is used:

|Headers|Description|
|:----|:----|
|Ocp-Apim-Subscription-Key|*Use with Azure AI services subscription if you're passing your secret key*.<br/>The value is the Azure secret key for your subscription to Translator.|
|Authorization|*Use with Azure AI services subscription if you're passing an authentication token.*<br/>The value is the Bearer token: `Bearer <token>`.|
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

A successful request returns the encoded access token as plain text in the response body. The valid token is passed to the Translator service as a bearer token in the Authorization.

```http
Authorization: Bearer <Base64-access_token>
```

An authentication token is valid for 10 minutes. The token should be reused when making multiple calls to the Translator. However, if your program makes requests to the Translator over an extended period of time, then your program must request a new access token at regular intervals (for example, every 8 minutes).

<a name='authentication-with-azure-active-directory-azure-ad'></a>

## Authentication with Microsoft Entra ID

 Translator v3.0 supports Microsoft Entra authentication, Microsoft's cloud-based identity and access management solution.  Authorization headers enable the Translator service to validate that the requesting client is authorized to use the resource and to complete the request.

### **Prerequisites**

* A brief understanding of how to [**authenticate with Microsoft Entra ID**](../../../authentication.md?tabs=powershell#authenticate-with-azure-active-directory).

* A brief understanding of how to [**authorize access to managed identities**](../../../authentication.md?tabs=powershell#authorize-access-to-managed-identities).
