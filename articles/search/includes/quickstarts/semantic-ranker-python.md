---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 11/20/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, use a Jupyter notebook and the [**azure-search-documents**](/python/api/overview/azure/search-documents-readme) library in the Azure SDK for Python to learn about semantic ranking.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with Python 3.10 or later and the [Python extension](https://code.visualstudio.com/docs/languages/python) for this quickstart.

> [!TIP]
> You can [download a finished notebook](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Ranking) to start with a finished project or follow these steps to create your own.

We recommend a virtual environment for this quickstart:

1. Start Visual Studio Code.

1. Open the **semantic-ranking-quickstart.ipynb** file or create a new notebook.

1. Open the Command Palette by using **Ctrl+Shift+P**.

1. Search for **Python: Create Environment**.

1. Select **`Venv.`**

1. Select a Python interpreter. Choose 3.10 or later.

It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

### Install packages and set environment variables

1. Install packages, including [azure-search-documents](/python/api/azure-search-documents).

    ```python
   ! pip install -r requirements.txt --quiet
    ```

1. Rename `sample.env` to `.env`, and provide your search service endpoint. You can get the endpoint from the Azure portal on the search service **Overview** page.

    ```python
    AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
    AZURE_SEARCH_INDEX_NAME=hotels-sample-index
    ```

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI or Azure PowerShell to log in: `az login` or `az connect`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Update the index

In this section, you update a search index to include a semantic configuration. The code gets the index definition from the search service and adds a semantic configuration.

1. Open the [semantic-ranking-quickstart.ipynb](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Semantic-Ranking/semantic-ranking-quickstart.ipynb) file in Visual Studio Code or create a new file.

1. Provide the variables used in the solution.

    ```python
    # Provide variables
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    import os
    
    load_dotenv(override=True) # Take environment variables from .env.
    
    # The following variables from your .env file are used in this notebook
    search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    index_name = os.getenv("AZURE_SEARCH_INDEX", "hotels-sample-index")
    ```

1. Create a SearchIndexClient and get the existing hotels-sample-index.

    ```python
    from azure.search.documents.indexes import SearchIndexClient
    from azure.identity import DefaultAzureCredential
    import os
    
    # Initialize the client (similar to what you already have)
    search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    credential = DefaultAzureCredential()
    index_name = "hotels-sample-index"  # or use your existing index_name variable
    
    # Create the SearchIndexClient
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    
    try:
        # Get the existing index schema
        index = index_client.get_index(index_name)
        
        print(f"Index name: {index.name}")
        print(f"Number of fields: {len(index.fields)}")
        
        # Print field details
        for field in index.fields:
            print(f"Field: {field.name}, Type: {field.type}, Searchable: {field.searchable}")
        
        # Access semantic configuration if it exists
        if index.semantic_search and index.semantic_search.configurations:
            for config in index.semantic_search.configurations:
                print(f"Semantic config: {config.name}")
                if config.prioritized_fields.title_field:
                    print(f"Title field: {config.prioritized_fields.title_field.field_name}")
        else:
            print("No semantic configuration exists for this index")
    
    except Exception as ex:
        print(f"Error retrieving index: {ex}")
    ```

1. Run the code.

1. Output is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say "No semantic configuration exists for this index".

1. Add a semantic configuration to an existing hotels-sample-index on your search service. No search documents are deleted by this operation and your index is still operational after the configuration is added.

    ```python
    # Add semantic configuration to hotels-sample-index and display updated index details
    from azure.search.documents.indexes.models import (
        SemanticConfiguration,
        SemanticField,
        SemanticPrioritizedFields,
        SemanticSearch
    )
    
    try:
        # Get the existing index
        existing_index = index_client.get_index(index_name)
        
        # Create a new semantic configuration
        new_semantic_config = SemanticConfiguration(
            name="semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="HotelName"),
                keywords_fields=[SemanticField(field_name="Tags")],
                content_fields=[SemanticField(field_name="Description")]
            )
        )
        
        # Add semantic configuration to the index
        if existing_index.semantic_search is None:
            existing_index.semantic_search = SemanticSearch(configurations=[new_semantic_config])
        else:
            # Check if configuration already exists
            config_exists = any(config.name == "semantic-config" 
                              for config in existing_index.semantic_search.configurations)
            if not config_exists:
                existing_index.semantic_search.configurations.append(new_semantic_config)
        
        # Update the index
        result = index_client.create_or_update_index(existing_index)
        
        # Get the updated index and display detailed information
        updated_index = index_client.get_index(index_name)
        
        print("Semantic configurations:")
        print("-" * 40)
        if updated_index.semantic_search and updated_index.semantic_search.configurations:
            for config in updated_index.semantic_search.configurations:
                print(f"  Configuration: {config.name}")
                if config.prioritized_fields.title_field:
                    print(f"    Title field: {config.prioritized_fields.title_field.field_name}")
                if config.prioritized_fields.keywords_fields:
                    keywords = [kf.field_name for kf in config.prioritized_fields.keywords_fields]
                    print(f"    Keywords fields: {', '.join(keywords)}")
                if config.prioritized_fields.content_fields:
                    content = [cf.field_name for cf in config.prioritized_fields.content_fields]
                    print(f"    Content fields: {', '.join(content)}")
                print()
        else:
            print("  No semantic configurations found")
        
        print("✅ Semantic configuration successfully added!")
        
    except Exception as ex:
        print(f"❌ Error adding semantic configuration: {ex}")
    ```

1. Run the code.

1. Output is the semantic configuration you just added.

## Run semantic queries

Once the index has a semantic configuration, you can run queries that include semantic parameters.

1. Create a SearchClient and a query request that includes the semantic query type and the semantic configuration. This is the minimum requirement for invoking semantic ranking.

    ```python
    # Set up the search client
    search_client = SearchClient(endpoint=search_endpoint,
                          index_name=index_name,
                          credential=credential)
    
    # Runs a semantic query (runs a BM25-ranked query, rescoring and promoting the most semantically relevant matches to the top)
    results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
        search_text="walking distance to live music", 
        select='HotelId,HotelName,Description', query_caption='extractive')
    
    for result in results:
        print(result["@search.reranker_score"])
        print(result["HotelId"])
        print(result["HotelName"])
        print(f"Description: {result['Description']}")
    ```

1. Run the code.

1. Output should consist of 13 documents, ordered by the `"@search.reranker_score"`.

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions.

1. Add `captions` to the query.

    ```python
    # Runs a semantic query that returns captions
    results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
        search_text="walking distance to live music", 
        select='HotelName,HotelId,Description', query_caption='extractive')
    
    for result in results:
        print(result["@search.reranker_score"])
        print(result["HotelId"])
        print(result["HotelName"])
        print(f"Description: {result['Description']}")
    
        captions = result["@search.captions"]
        if captions:
            caption = captions[0]
            if caption.highlights:
                print(f"Caption: {caption.highlights}\n")
            else:
                print(f"Caption: {caption.text}\n")
    ```

1. Run the code.

1. Output should include a new caption element alongside search field. Captions are the most relevant passages in a  result. If your index includes larger chunks of text, a caption is helpful for extracting the most interesting sentences.

    ```bash
    2.613231658935547
    24
    Uptown Chic Hotel
    Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
    Caption: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
    ```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

1. Add `answers` to the query.

    ```python
    # Run a semantic query that returns semantic answers  
    results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
     search_text="what's a good hotel for people who like to read",
     select='HotelName,Description,Category', query_caption='extractive', query_answer="extractive",)
    
    semantic_answers = results.get_answers()
    for answer in semantic_answers:
        if answer.highlights:
            print(f"Semantic Answer: {answer.highlights}")
        else:
            print(f"Semantic Answer: {answer.text}")
        print(f"Semantic Answer Score: {answer.score}\n")
    
    for result in results:
        print(result["@search.reranker_score"])
        print(result["HotelName"])
        print(f"Description: {result['Description']}")
    
        captions = result["@search.captions"]
        if captions:
            caption = captions[0]
            if caption.highlights:
                print(f"Caption: {caption.highlights}\n")
            else:
                print(f"Caption: {caption.text}\n")
    ```

1. Run the code.

1. Output should look similar to the following example, where the best answer to question is pulled from one of the results.

    Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

    ```bash
    Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    Semantic Answer Score: 0.9829999804496765
    
    2.124817371368408
    1
    Stay-Kay City Hotel
    Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
    Caption: This classic hotel is<em> fully-refurbished </em>and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
    
    2.0705394744873047
    16
    Double Sanctuary Resort
    Description: 5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
    Caption: <em>5 star Luxury Hotel </em>-<em> Biggest </em>Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
    
    2.041472911834717
    38
    Lakeside B & B
    Description: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    Caption: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    
    2.084540843963623
    Double Sanctuary Resort
    Description: 5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
    Caption: <em>5 star Luxury Hotel </em>-<em> Biggest </em>Rooms in the<em> city. #1 </em>Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
    
    ...
    ```
