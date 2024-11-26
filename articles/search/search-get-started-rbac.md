---
title: Quickstart RBAC
titleSuffix: Azure AI Search
description: In this quickstart, learn how to switch from API keys to Microsoft Entra identities and role-based access control (RBAC).
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search

ms.topic: quickstart
ms.date: 11/26/2024
---

# Quickstart: Connect to Azure AI Search using role-based access control (RBAC)

Here are the comprehensive instructions for configuring Azure AI Search to use Microsoft Entra ID authentication and roles, including steps for connecting from your local system, running Jupyter notebooks, or using a REST client.

If you followed other quickstarts that connect using key-based authentication, these steps to switch to identity-based authentication and avoid hard-coded API keys in your example code.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).

- [Azure AI Search](search-create-service-portal.md), any region or tier, but it needs to be Basic or higher to configure a system-assigned managed identity for Azure AI Search.

- A command line tool, such as the [Azure CLI](/cli/azure/install-azure-cli).

## Step 1: Set Up Your Azure Subscription and Tenant

Follow these steps if you have more than one Azure subscription or tenant. The active subscription and tenant must be valid for your search service.

1. Get the Azure subscription and tenant for your search service:

   1. Sign into the Azure portal and navigate to your search service.

   1. Notice the subscription name and ID in **Overview** > **Essentials**.

   1. Select the subscription name to view the parent management group (tenant ID).

1. Identify the active Azure subscription and tenant on your local device:

   `az account show`

1. Set your Azure subscription to the subscription and tenant:

   `az account set --subscription <your-subscription-id>`

   `az login --tenant <your-tenant-id>`

1. Check your tenant ID:

   `az account show --query tenantId --output tsv`

## Step 2: Configure Azure AI Search for Microsoft Entra ID Authentication

1. Sign in to the Azure portal and navigate to your Azure AI Search service.

1. Enable role-based access control (RBAC):

   1. Go to **Settings** > **Keys**.

   1. Choose **Role-based control** or **Both** if you need time to transition clients to role-based access control1.

1. Assign roles in the Azure portal:

   1. Navigate to your search service.

   1. Select **Access Control (IAM)** in the left navigation pane.

   1. Select **+ Add** > **Add role assignment**.

   1. Choose a role (e.g., Search Service Contributor, Search Index Data Contributor, Search Index Data Reader) and assign it to the appropriate Microsoft Entra user or group identity2. These three roles provide comprehensive permissions for creating, loading, and querying objects on Azure AI Search.

## Step 3: Connect from Your Local System

### Using Python Notebooks

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

### Using a REST Client

Several quickstarts and tutorials use a REST client, such as Visual Studio Code with the REST extension. Here's how you connect to Azure AI Search from Visual Studio Code.

1. Get a personal identity token:

   `az account get-access-token --resource https://<your-search-service-name>.search.windows.net`

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

## Additional Configuration

Configure a managed identity for outbound connections:

- Assign a system-assigned or user-assigned managed identity to your search service.
- Use role assignments to authorize access to other Azure resources.

Network access configuration:

- Set up inbound rules to accept or reject requests to Azure AI Search based on IP address.
