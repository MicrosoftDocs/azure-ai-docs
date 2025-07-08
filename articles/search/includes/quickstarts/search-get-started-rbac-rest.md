---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/08/2025
---

In this quickstart, you use role-based access control (RBAC) and Microsoft Entra ID to connect to Azure AI Search from your local system. You then use REST in Visual Studio Code to interact with your search service.

We recommend keyless connections for granular permissions and identity-based authentication, which eliminate the need for hard-coded API keys in your code. However, if you prefer key-based connections, see [Connect to Azure AI Search using keys](../../search-security-api-keys.md).

<!-- This quickstart is a prerequisite for other quickstarts that use Microsoft Entra ID with role assignments. -->

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any region or tier.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

[!INCLUDE [Setup](./search-get-started-rbac-setup.md)]

## Set up authentication

Before you establish a keyless connection to your Azure AI Search service, you must use the Azure CLI to authenticate your identity and generate a Microsoft Entra ID token. You specify this token in the next section.

To set up authentication:

1. On your local system, open a command-line tool.

1. Sign in to the subscription whose ID you obtained in [Get service information](#get-service-information).

   ```azurecli
   az login
   ```

1. Generate an access token.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
    ```

1. Make a note of the token.

## Connect to Azure AI Search

You can use the REST Client extension to send requests to Azure AI Search. For request authentication, include an `Authorization` header with the Microsoft Entra ID token you previously generated.

To use REST for keyless connections:

1. On your local system, open Visual Studio Code.

1. Create a `.rest` or `.http` file.

1. Paste the following placeholders into the file.

   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
   @token = PUT-YOUR-PERSONAL-IDENTITY-TOKEN-HERE
   ```

1. Replace `@baseUrl` with the value you obtained in [Get service information](#get-service-information).

1. Replace `@token` with the value you obtained in [Set up authentication](#set-up-authentication).

1. Make a REST call to authenticate with your token and connect to your search service.

   ```http
   POST https://{{baseUrl}}/indexes/hotels-sample-index/docs/search?api-version=2024-07-01 HTTP/1.1
      Content-type: application/json
      Authorization: Bearer {{token}}
    
      {
         "queryType": "simple",
         "search": "beach access",
         "filter": "",
         "select": "HotelName,Description,Category,Tags",
         "count": true
      }
   ```

### Troubleshoot 401 errors

+ Revisit [Configure role-based access](#configure-role-based-access). Your search service must have **Role-based access control** or **Both** enabled. Policies at the subscription or resource group level might also override your role assignments.

+ Revisit [Set up authentication](#set-up-authentication). You must sign in to the correct subscription for your search service.

+ Make sure your endpoint and token variables don't have surrounding quotes or extra spaces.

+ Make sure your token doesn't have the `@` symbol in the request header. For example, if the variable is `@token`, the reference in the request should be `{{token}}`.

If all else fails, restart your device to remove cached tokens and then repeat the steps in this quickstart, starting with [Set up authentication](#set-up-authentication).
