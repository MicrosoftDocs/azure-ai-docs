---
title: Quickstart keyless connection
titleSuffix: Azure AI Search
description: In this quickstart, learn how to switch from API keys to Microsoft Entra identities and role-based access control (RBAC).
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search

ms.topic: quickstart
ms.date: 11/28/2024
---

# Quickstart: Connect without keys

Configure Azure AI Search to use Microsoft Entra ID authentication and role-based access control (RBAC). Connect from your local system using your personal identity, using Jupyter notebooks or a REST client to interact with your search service.

If you stepped through other quickstarts that connect using API keys, this quickstart shows you how to switch to identity-based authentication so that you can avoid hard-coded keys in your example code.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).

- [Azure AI Search](search-create-service-portal.md), any region or tier, but you need Basic or higher to configure a system-assigned managed identity for Azure AI Search.

- A command line tool, such as the [Azure CLI](/cli/azure/install-azure-cli).

## Step 1: Get your Azure subscription and tenant IDs

This step is necessary if you have more than one subscription or tenant.

1. Get the Azure subscription and tenant for your search service:

   1. Sign into the [Azure portal](https://portal.azure.com) and navigate to your search service.

   1. Notice the subscription name and ID in **Overview** > **Essentials**.

   1. Now select the subscription name to confirm the parent management group (tenant ID) on the next page.

      :::image type="content" source="media/search-get-started-rbac/select-subscription-name.png" lightbox="media/search-get-started-rbac/select-subscription-name.png" alt-text="Screenshot of the portal page providing the subscription name":::

1. Switching to your local device and a command prompt, identify the active Azure subscription and tenant:

   ```azurecli
   az account show
   ```

1. If the active subscription is different from the information obtained in the previous step, change the subscription ID. Next, sign in to Azure using the tenant ID also found in the previous step:

   ```azurecli
    az account set --subscription <your-subscription-id>

    az login --tenant <your-tenant-id>
   ```

1. Verify your tenant ID:

   ```azurecli
   az account show --query tenantId --output tsv
   ```

## Step 2: Configure Azure AI Search for RBAC

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your Azure AI Search service.

1. Enable role-based access control (RBAC):

   1. Go to **Settings** > **Keys**.

   1. Choose **Role-based control** or **Both** if you need time to transition clients to role-based access control.

      If you choose **Role-based control**, make sure that you assign yourself *all* roles named in the next instruction or you won't be able to complete tasks in the portal or through a  local client.

1. Assign roles in the Azure portal:

   1. Navigate to your search service.

   1. Select **Access Control (IAM)** in the left navigation pane.

   1. Select **+ Add** > **Add role assignment**.

   1. Choose a role (Search Service Contributor, Search Index Data Contributor, Search Index Data Reader) and assign it to your Microsoft Entra user or group identity.

      Repeat for each role.

      You need all three roles for creating, loading, and querying objects on Azure AI Search. For more information, see [Connect using roles](search-security-rbac.md).

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
    index_name = "<your-index-name>"
    
    credential = DefaultAzureCredential()
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    
    results = client.search("search text")
    for result in results:
        print(result)
    ```

### Using a REST client

Several quickstarts and tutorials use a REST client, such as Visual Studio Code with the REST extension. Here's how you connect to Azure AI Search from Visual Studio Code.

1. Get a personal identity token:

   `az account get-access-token --scope https://search.azure.com/.default`

1. Extract the token from the output:

   `TOKEN=$(az account get-access-token --resource https://<your-search-service-name>.search.windows.net --query accessToken --output tsv)`

1. Provide the token in a request header:

   `az rest --method get --url "https://<your-search-service-name>.search.windows.net/indexes/<your-index-name>/docs?api-version=2021-04-30-Preview&search=*" --headers "Authorization=Bearer $TOKEN"`

1. Specify the authorization bearer token in a REST call:

   ```REST
    POST https://{{baseUrl}}/indexes/{{index-name}}/docs/search?api-version=2024-07-01 HTTP/1.1
      Content-type: application/json
      Authorization: Bearer {{token}}
    
        {
             "queryType": "simple",
             "search": "motel",
             "filter": "",
             "select": "HotelName,Description,Category,Tags",
             "count": true
         }
   ```

## Additional configuration

Configure a managed identity for outbound connections:

- [Configure a system-assigned or user-assigned managed identity](search-howto-managed-identities-data-sources.md) for your search service.
- [Use role assignments](keyless-connections.md) to authorize access to other Azure resources.

Network access configuration:

- [Set inbound rules](service-configure-firewall.md) to accept or reject requests to Azure AI Search based on IP address.
