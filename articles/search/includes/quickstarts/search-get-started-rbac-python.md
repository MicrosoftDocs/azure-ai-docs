---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/09/2025
---

In this quickstart, you use role-based access control (RBAC) and Microsoft Entra ID to establish a keyless connection to your Azure AI Search service. You then use Python in Visual Studio Code to interact with your service.

Keyless connections provide enhanced security through granular permissions and identity-based authentication. We don't recommend hard-coded API keys, but if you prefer them, see [Connect to Azure AI Search using keys](../../search-security-api-keys.md).

<!-- This quickstart is a prerequisite for other quickstarts that use Microsoft Entra ID with role assignments. -->

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any region or tier.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://jupyter.org/install).

[!INCLUDE [Setup](./search-get-started-rbac-setup.md)]

## Sign in to Azure

Before you connect to your Azure AI Search service, use the Azure CLI to sign in to the subscription that contains your service. This step establishes your Microsoft Entra identity, which `DefaultAzureCredential` uses to authenticate requests in the next section.

To sign in:

1. On your local system, open a command-line tool.

1. Check for the active tenant and subscription in your local environment.

   ```azurecli
   az account show
   ```

1. If the active subscription and tenant aren't valid for your search service, change the variables. You can check for the subscription ID on the search service overview page in the Azure portal. You can check for the tenant ID by clicking through to the subscription. In the Azure portal, the tenant ID is referred to as the **Parent management group**. Make a note of the values that are valid for your search service and run the following commands to update your local environment.

   ```azurecli
    az account set --subscription <your-subscription-id>

    az login --tenant <your-tenant-id>
   ```

## Connect to Azure AI Search

> [!NOTE]
> This section illustrates the basic Python pattern for keyless connections. For comprehensive guidance, see a specific quickstart or tutorial, such as [Quickstart: Use agentic retrieval in Azure AI Search](../../search-get-started-agentic-retrieval.md).

You can use Python notebooks in Visual Studio Code to send requests to your Azure AI Search service. For request authentication, use the `DefaultAzureCredential` class from the Azure Identity library.

To connect using Python:

1. On your local system, open Visual Studio Code.

1. Create a `.ipynb` file.

1. Create a code cell to install the `azure-identity` and `azure-search-documents` libraries.

   ```python
   pip install azure-identity azure-search-documents
   ```

1. Create another code cell to authenticate and connect to your search service.

   ```python
   from azure.identity import DefaultAzureCredential
   from azure.search.documents.indexes import SearchIndexClient
    
   service_endpoint = "PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE"
   credential = DefaultAzureCredential()
   client = SearchIndexClient(endpoint=service_endpoint, credential=credential)
    
   # List existing indexes
   indexes = client.list_indexes()
    
   for index in indexes:
      index_dict = index.as_dict()
      print(json.dumps(index_dict, indent=2))
   ```

1. Set `service_endpoint` to the value you obtained in [Get service information](#get-service-information).

1. Select **Run All** to run both code cells.

   The output should list the existing indexes (if any) on your search service, indicating a successful connection.

### Troubleshoot 401 errors

If you encounter a 401 error, follow these troubleshooting steps:

+ Revisit [Configure role-based access](#configure-role-based-access). Your search service must have **Role-based access control** or **Both** enabled. Policies at the subscription or resource group level might also override your role assignments.

+ Revisit [Sign in to Azure](#sign-in-to-azure). You must sign in to the subscription that contains your search service.

+ Make sure your endpoint variable has surrounding quotes.

+ If all else fails, restart your device to remove cached tokens and then repeat the steps in this quickstart, starting with [Sign in to Azure](#sign-in-to-azure).
