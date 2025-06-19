---
title: 'Quickstart: Vector Search Using REST APIs'
titleSuffix: Azure AI Search
description: Learn how to call the Search REST APIs for vector workloads in Azure AI Search.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 06/19/2025
zone_pivot_groups: search-get-started-vector
---

# Quickstart: Vector search using REST

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to create, load, and query vectors.

In Azure AI Search, a [vector store](vector-store.md) has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. The [Create Index](/rest/api/searchservice/indexes/create-or-update) REST API creates the vector store.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](vector-search-integrated-vectorization.md) over your own content, try the [**Import and vectorize data wizard**](search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch) in your current subscription.
    - You can use a free search service for most of this quickstart, but we recommend the Basic tier or higher for larger data files.
    - To run the query example that invokes [semantic reranking](semantic-search-overview.md), your search service must be at the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

- [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

## Retrieve resource information

Requests to the search endpoint must be authenticated and authorized. You can use API keys or roles for this task. We recommend [using a keyless connection via Microsoft Entra ID](search-get-started-rbac.md).

Select the tab that corresponds to your preferred authentication method. Use the same method for all requests in this quickstart.

#### [Microsoft Entra ID](#tab/keyless)

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch).

1. On the **Overview** home page, find the URL. An example endpoint might look like `https://mydemo.search.windows.net`. 

   :::image type="content" source="media/search-get-started-rest/get-endpoint.png" lightbox="media/search-get-started-rest/get-endpoint.png" alt-text="Screenshot of the URL property on the overview page.":::

1. Follow the steps in the [keyless quickstart](./search-get-started-rbac.md) to get your Microsoft Entra token. 

    You get the token when you run the `az account get-access-token` command in step 3 of the previous quickstart.
    
    ```bash
    az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
    ```

#### [API key](#tab/api-key)


1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch).

1. On the **Overview** home page, find the URL. An example endpoint might look like `https://mydemo.search.windows.net`. 

   :::image type="content" source="media/search-get-started-rest/get-endpoint.png" lightbox="media/search-get-started-rest/get-endpoint.png" alt-text="Screenshot of the URL property on the overview page.":::

1. Select **Settings** > **Keys**. Either **API keys** or **Both** must be enabled. [Admin API keys](search-security-api-keys.md) are used to add, modify, and delete objects. There are two interchangeable admin keys. Copy either one.

   :::image type="content" source="media/search-get-started-rest/get-api-key.png" lightbox="media/search-get-started-rest/get-api-key.png" alt-text="Screenshot that shows the API keys in the Azure portal.":::

---

## Create or download the code file

You use one `.rest` or `.http` file to run all the requests in this quickstart. You can download the REST file that contains the code for this quickstart, or you can create a new file in Visual Studio Code and copy the code into it.

1. In Visual Studio Code, create a new file with a `.rest` or `.http` file extension. For example, `az-search-vector-quickstart.rest`. Copy and paste the raw contents of the [Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-vectors/az-search-vector-quickstart.rest](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors) file into this new file. 

1. At the top of the file, replace the placeholder value for `@baseUrl` with your search service URL. See the [Retrieve resource information](#retrieve-resource-information) section for instructions on how to find your search service URL.


   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
   ```

1. At the top of the file, replace the placeholder value for authentication. See the [Retrieve resource information](#retrieve-resource-information) section for instructions on how to get your Microsoft Entra token or API key.

    For the **recommended** keyless authentication via Microsoft Entra ID, you need to replace `@apiKey` with the `@token` variable.

   ```http
   @token = PUT-YOUR-MICROSOFT-ENTRA-TOKEN-HERE
   ```

    If you prefer to use an API key, replace `@apiKey` with the key you copied from the Azure portal.

    ```http
    @apiKey = PUT-YOUR-ADMIN-KEY-HERE
    ```

1. For the **recommended** keyless authentication via Microsoft Entra ID, you need to replace `api-key: {{apiKey}}` with `Authorization: Bearer {{token}}` in the request headers. Replace all instances of `api-key: {{apiKey}}` that you find in the file.

::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/search-get-started-vector-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST quickstart](includes/quickstarts/search-get-started-vector-rest.md)]

::: zone-end


## Next steps

As a next step, we recommend learning how to invoke REST API calls [without API keys](search-get-started-rbac.md).

You might also want to review the demo code for [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python), [C#](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet), or [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript).
