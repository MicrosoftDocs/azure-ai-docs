---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 03/04/2025
---

[!INCLUDE [Full text introduction](full-text-intro.md)]

> [!TIP]
> You can download and run a [finished notebook](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An Azure AI Search service. [Create a service](../../search-create-service-portal.md) if you don't have one. For this quickstart, you can use a free service.
- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python), or an equivalent IDE with Python 3.10 or later. If you haven't installed a suitable version of Python, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign both of the `Search Service Contributor` and `Search Index Data Contributor` roles to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**. For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Retrieve resource information

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Set up your environment

You run the sample code in a Jupyter notebook. So, you need to set up your environment to run Jupyter notebooks.

1. Download or copy the [sample notebook from GitHub](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart).

1. Open the notebook in Visual Studio Code.

1. Create a new Python environment to use to install the packages you need for this tutorial. 

    > [!IMPORTANT]
    > Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global install of Python.

    # [Windows](#tab/windows)
    
    ```bash
    py -3 -m venv .venv
    .venv\scripts\activate
    ```
    
    # [Linux](#tab/linux)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    # [macOS](#tab/macos)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    ---

    It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

1. Install Jupyter notebooks and the IPython Kernel for Jupyter notebooks if you don't have them already.

    ```bash
    pip install jupyter
    pip install ipykernel
    python -m ipykernel install --user --name=.venv
    ```

1. Select the notebook kernel.

    1. In the top right corner of the notebook, select **Select Kernel**.
    1. If you see `.venv` in the list, select it. If you don't see it, select **Select Another Kernel** > **Python environments** > `.venv`.

## Create, load, and query a search index

In this section, you add code to create a search index, load it with documents, and run queries. You run the program to see the results in the console. For a detailed explanation of the code, see the [explaining the code](#explaining-the-code) section.

1. Make sure the notebook is open in the `.venv` kernel as described in the previous section.
1. Run the first code cell to install the required packages, including [azure-search-documents](/python/api/azure-search-documents). 

    ```python
    ! pip install azure-search-documents==11.6.0b1 --quiet
    ! pip install azure-identity --quiet
    ! pip install python-dotenv --quiet
    ```

1. Replace contents of the second code cell with the following code depending on your authentication method. 

    > [!NOTE]
    > The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

    #### [Microsoft Entra ID](#tab/keyless)
    
    ```python
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
    
    search_endpoint: str = "https://<Put your search service NAME here>.search.windows.net/"
    authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD
    credential = DefaultAzureCredential(authority=authority)

    index_name: str = "hotels-quickstart-python"
    ```
    
    #### [API key](#tab/api-key)
    
    ```python
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
    
    search_endpoint: str = "https://<Put your search service NAME here>.search.windows.net/"
    credential = AzureKeyCredential("Your search service admin key")

    index_name: str = "hotels-quickstart-python"
    ```
    ---

1. Remove the following two lines from the **Create an index** code cell. Credentials are already set in the previous code cell.

    ```python
    from azure.core.credentials import AzureKeyCredential
    credential = AzureKeyCredential(search_api_key)
    ```

1. Run the **Create an index** code cell to create a search index.
1. Run the remaining code cells sequentially to load documents and run queries.

## Explaining the code

### Create an index

`SearchIndexClient` is used to create and manage indexes for Azure AI Search. Each field is identified by a `name` and has a specified `type`. 

Each field also has a series of index attributes that specify whether Azure AI Search can search, filter, sort, and facet upon the field. Most of the fields are simple data types, but some, like `AddressType` are complex types that allow you to create rich data structures in your index. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create). 

### Create a documents payload and upload documents

Use an [index action](/python/api/azure-search-documents/azure.search.documents.models.indexaction) for the operation type, such as upload or merge-and-upload. Documents originate from the [HotelsData](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/hotels/HotelsData_toAzureSearch.JSON) sample on GitHub.

### Search an index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

Use the *search* method of the [search.client class](/python/api/azure-search-documents/azure.search.documents.searchclient).

The sample queries in the notebook are:
- Basic query: Executes an empty search (`search=*`), returning an unranked list (search score = 1.0) of arbitrary documents. Because there are no criteria, all documents are included in results.
- Term query: Adds whole terms to the search expression ("wifi"). This query specifies that results contain only those fields in the `select` statement. Limiting the fields that come back minimizes the amount of data sent back over the wire and reduces search latency.
- Filtered query: Add a filter expression, returning only those hotels with a rating greater than four, sorted in descending order.
- Fielded scoping: Add `search_fields` to scope query execution to specific fields.
- Facets: Generate facets for positive matches found in search results. There are no zero matches. If search results don't include the term *wifi*, then *wifi* doesn't appear in the faceted navigation structure.
- Look up a document: Return a document based on its key. This operation is useful if you want to provide drill through when a user selects an item in a search result.
- Autocomplete: Provide potential matches as the user types into the search box. Autocomplete uses a suggester (`sg`) to know which fields contain potential matches to suggester requests. In this quickstart, those fields are `Tags`, `Address/City`, `Address/Country`. To simulate autocomplete, pass in the letters *sa* as a partial string. The autocomplete method of [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient) sends back potential term matches.

### Remove the index

If you're finished with this index, you can delete it by running the **Clean up** code cell. Deleting unnecessary indexes frees up space for stepping through more quickstarts and tutorials.