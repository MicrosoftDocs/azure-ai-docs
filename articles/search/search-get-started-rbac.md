---
title: 'Quickstart: Keyless Connection'
titleSuffix: Azure AI Search
description: Learn how to switch from API keys to Microsoft Entra identities and role-based access control (RBAC).
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 03/04/2025
---

# Quickstart: Connect without keys

In this quickstart, you configure Azure AI Search to use Microsoft Entra ID authentication and role-based access control (RBAC) to connect from your local system without API keys. You then use Jupyter notebooks or a REST client to interact with your search service.

If you completed other quickstarts that connect using API keys, this quickstart shows you how to switch to identity-based authentication so that you can avoid hard-coded keys in your example code.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An [Azure AI Search service](search-create-service-portal.md) in any region or tier. However, to configure a managed identity for Azure AI Search, you need the Basic tier or higher.

- A command line tool, such as PowerShell or Bash, and the [Azure CLI](/cli/azure/install-azure-cli).

## Step 1: Get your Azure subscription and tenant IDs

You need this step if you have more than one subscription or tenant.

1. Get the Azure subscription and tenant for your search service:

   1. Sign into the [Azure portal](https://portal.azure.com) and navigate to your search service.

   1. Notice the subscription name and ID in **Overview** > **Essentials**.

   1. Now select the subscription name to show the parent management group (tenant ID) on the next page.

      :::image type="content" source="media/search-get-started-rbac/select-subscription-name.png" lightbox="media/search-get-started-rbac/select-subscription-name.png" alt-text="Screenshot of the Azure portal page providing the subscription name":::

1. You now know which subscription and tenant Azure AI Search is under. Switch to your local device and a command prompt, and identify the active Azure subscription and tenant on your device:

   ```azurecli
   az account show
   ```

1. If the active subscription and tenant differ from the information obtained in the previous step, change the subscription ID. Next, sign in to Azure using the tenant ID that you found in the previous step:

   ```azurecli
    az account set --subscription <your-subscription-id>

    az login --tenant <your-tenant-id>
   ```

## Step 2: Configure Azure AI Search for RBAC

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your Azure AI Search service.

1. Enable role-based access control (RBAC):

   1. Go to **Settings** > **Keys**.

   1. Choose **Role-based control** or **Both** if you need time to transition clients to role-based access control.

      If you choose **Role-based control**, make sure that you assign yourself *all* roles named in the next instruction or you won't be able to complete tasks in the Azure portal or through a  local client.

1. Assign roles in the Azure portal:

   1. Navigate to your search service.

   1. Select **Access Control (IAM)** in the left pane.

   1. Select **+ Add** > **Add role assignment**.

   1. Choose a role (**Search Service Contributor**, **Search Index Data Contributor**, **Search Index Data Reader**) and assign it to your Microsoft Entra user or group identity.

      Repeat for each role.

      You need **Search Service Contributor** plus **Search Index Data Contributor** to create, load, and query objects on Azure AI Search. For more information, see [Connect using roles](search-security-rbac.md).

> [!TIP]
> Later, if you get authentication failure errors, recheck the settings in this section. There could be policies at the subscription or resource group level that override any API settings you specify.

## Step 3: Connect from your local system

If you haven't yet signed in to Azure:

```azurecli
az login
```

### Using Python and Jupyter notebooks

1. Install the Azure Identity and Azure Search libraries:

    ```python
    pip install azure-identity azure-search-documents
    ```

1. Authenticate and connect to Azure AI Search:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.search.documents import SearchClient
    
    service_endpoint = "https://<your-search-service-name>.search.windows.net"
    index_name = "hotels-sample-index"
    
    credential = DefaultAzureCredential()
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    
    results = client.search("beach access")
    for result in results:
        print(result)
    ```

### Using a REST client

Several quickstarts and tutorials use a REST client, such as Visual Studio Code with the REST extension. Here's how you connect to Azure AI Search from Visual Studio Code.

You should have a `.rest` or `.http` file, similar to the one described in [Quickstart: Vector search](search-get-started-vector.md).

1. Generate an access token.

   ```azurecli
   az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
   ```

1. At the top of your file, set variables used for the connection, pasting the full search service endpoint and the access token you got in the previous step. Your variables should look similar to the following example. Notice the values aren't quote-enclosed.

    ```REST
    @baseUrl = https://contoso.search.search.windows.net
    @token = <a long GUID>
    ```

1. Specify the authorization bearer token in a REST call:

   ```REST
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

- Check the active subscription and tenant (`az account show`) and make sure it's valid for your search service.

- Check the search service **Settings** > **Keys** options in the Azure portal and confirm the service is configured for **Both"** or **Role-based access control**.

- For the REST client only: Check the token and endpoint specified in your file and make sure there's no surrounding quotes or extra spaces.

If all else fails, restart your device to remove any cached tokens, and then repeat the steps in this section, starting with `az login`.

## Additional configuration

Configure a managed identity for outbound connections:

- [Configure a system-assigned or user-assigned managed identity](search-howto-managed-identities-data-sources.md) for your search service.

- [Use role assignments](keyless-connections.md) to authorize access to other Azure resources.

Network access configuration:

- [Set inbound rules](service-configure-firewall.md) to accept or reject requests to Azure AI Search based on IP address.
