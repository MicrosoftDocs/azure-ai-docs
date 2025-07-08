---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/08/2025
---

In this quickstart, you use role-based access control (RBAC) and Microsoft Entra ID to connect to Azure AI Search from your local system. You then use Python in Visual Studio Code to interact with your search service.

We recommend keyless connections for granular permissions and identity-based authentication, which eliminate the need for hard-coded API keys in your code. However, if you prefer key-based connections, see [Connect to Azure AI Search using keys](../../search-security-api-keys.md).

<!-- This quickstart is a prerequisite for other quickstarts that use Microsoft Entra ID with role assignments. -->

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any region or tier.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://jupyter.org/install).

[!INCLUDE [Setup](./search-get-started-rbac-setup.md)]

## Set up authentication

Before you establish a keyless connection to your Azure AI Search service, you must use the Azure CLI to authenticate your identity with Microsoft Entra ID.

To set up authentication:

1. On your local system, open a command-line tool.

1. Sign in to the subscription whose ID you obtained in [Get service information](#get-service-information).

   ```azurecli
   az login
   ```

## Connect to Azure AI Search

You can use the Python extension and Jupyter package to send requests to your Azure AI Search service. For request authentication, use the `DefaultAzureCredential` class from the Azure Identity library.

To use Python for keyless connections:

1. On your local system, open Visual Studio Code.

1. Create a `.ipynb` file.

1. Create a code cell to install the `azure-identity` and `azure-search-documents` libraries.

   ```python
   pip install azure-identity azure-search-documents
   ```

1. Create another code cell to authenticate with `DefaultAzureCredential` and connect to your search service.

   ```python
   from azure.identity import DefaultAzureCredential
   from azure.search.documents import SearchClient
    
   service_endpoint = "PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE"
   index_name = "hotels-sample-index"
    
   credential = DefaultAzureCredential()
   client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    
   results = client.search("beach access")
   for result in results:
      print(result)
   ```

### Troubleshoot 401 errors

+ Revisit [Configure role-based access](#configure-role-based-access). Your search service must have **Role-based access control** or **Both** enabled. Policies at the subscription or resource group level might also override your role assignments.

+ Revisit [Set up authentication](#set-up-authentication). You must sign in to the correct subscription for your search service.

If all else fails, restart your device to remove cached tokens and then repeat the steps in this quickstart, starting with [Set up authentication](#set-up-authentication).
