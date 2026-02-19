---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/20/2025
---

In this quickstart, you use role-based access control (RBAC) and Microsoft Entra ID to establish a keyless connection to your Azure AI Search service. You then use REST in Visual Studio Code to interact with your service.

Keyless connections provide enhanced security through granular permissions and identity-based authentication. We don't recommend hard-coded API keys, but if you prefer them, see [Connect to Azure AI Search using keys](../../search-security-api-keys.md).

<!-- This quickstart is a prerequisite for other quickstarts that use Microsoft Entra ID with role assignments. -->

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any region or tier.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

[!INCLUDE [Setup](./search-get-started-rbac-setup.md)]

## Sign in to Azure

Before you connect to your Azure AI Search service, use the Azure CLI to sign in to the subscription that contains your service.

To sign in:

1. On your local system, open a command-line tool.

1. Check the active subscription and tenant in your local environment.

   ```azurecli
   az account show
   ```

1. If the active subscription and tenant aren't valid for your search service, run the following commands to update their values. You can find the subscription ID on the search service **Overview** page in the Azure portal. To find the tenant ID, select the name of your subscription on the **Overview** page, and then locate the **Parent management group** value.

   ```azurecli
    az account set --subscription <your-subscription-id>

    az login --tenant <your-tenant-id>
   ```

## Get token

REST API calls require the inclusion of a Microsoft Entra ID token. You use this token to authenticate requests in the next section.

To get your token:

1. Using the same command-line tool, generate an access token.

   ```azurecli
   az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
   ```

1. Make a note of the token output.

## Connect to Azure AI Search

> [!NOTE]
> This section illustrates the basic REST pattern for keyless connections. For comprehensive guidance, see a specific quickstart or tutorial, such as [Quickstart: Agentic retrieval](../../search-get-started-agentic-retrieval.md).

You can use the REST Client extension in Visual Studio Code to send requests to your Azure AI Search service. For request authentication, include an `Authorization` header with the Microsoft Entra ID token you previously generated.

To connect using REST:

1. On your local system, open Visual Studio Code.

1. Create a `.rest` or `.http` file.

1. Paste the following variables and request into the file.

   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
   @token = PUT-YOUR-PERSONAL-IDENTITY-TOKEN-HERE

   ### List existing indexes
   GET {{baseUrl}}/indexes?api-version=2025-09-01  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}
   ```

1. Set `@baseUrl` to the value you obtained in [Get service information](#get-service-information).

1. Set `@token` to the value you obtained in [Get token](#get-token).

1. Under `### List existing indexes`, select **Send Request**.

   You should receive an `HTTP/1.1 200 OK` response, indicating a successful connection to your search service.

### Troubleshoot 401 errors

If you encounter a 401 error, follow these troubleshooting steps:

+ Revisit [Configure role-based access](#configure-role-based-access). Your search service must have **Role-based access control** or **Both** enabled. Policies at the subscription or resource group level might override your role assignments.

+ Revisit [Sign in to Azure](#sign-in-to-azure). You must sign in to the subscription that contains your search service.

+ Make sure your endpoint and token variables don't have surrounding quotes or extra spaces.

+ Make sure your token doesn't have the `@` symbol in the request header. For example, if the variable is `@token`, the reference in the request should be `{{token}}`.

+ If all else fails, restart your device to remove cached tokens and then repeat the steps in this quickstart, starting with [Sign in to Azure](#sign-in-to-azure).
