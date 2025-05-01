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
> You can [download the source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart/v11) to start with a finished project or follow these steps to create your own.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An Azure AI Search service. [Create a service](../../search-create-service-portal.md) if you don't have one. For this quickstart, you can use a free service.

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:

- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign both of the `Search Service Contributor` and `Search Index Data Contributor` roles to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**. For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Retrieve resource information

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Set up

1. Create a new folder `full-text-quickstart` to contain the application and open Visual Studio Code in that folder with the following command:

    ```shell
    mkdir full-text-quickstart && cd full-text-quickstart
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

1. Install the Azure AI Search client library ([Azure.Search.Documents](/dotnet/api/overview/azure/search.documents-readme)) for .NET with:

    ```console
    dotnet add package Azure.Search.Documents
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) package with:

    ```console
    dotnet add package Azure.Identity
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

## Create, load, and query a search index

In the prior [set up](#set-up) section, you created a new console application and installed the Azure AI Search client library. 

In this section, you add code to create a search index, load it with documents, and run queries. You run the program to see the results in the console. For a detailed explanation of the code, see the [explaining the code](#explaining-the-code) section.

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```csharp
Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");
DefaultAzureCredential credential = new();
```

#### [API key](#tab/api-key)

```csharp
Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");
AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
```
---

1. In *Program.cs*, paste the following code. Edit the `serviceName` and `apiKey` variables with your search service name and admin API key.

    ```csharp
    using System;
    using Azure;
    using Azure.Identity;
    using Azure.Search.Documents;
    using Azure.Search.Documents.Indexes;
    using Azure.Search.Documents.Indexes.Models;
    using Azure.Search.Documents.Models;
    
    namespace AzureSearch.Quickstart
    
    {
        class Program
        {
            static void Main(string[] args)
            {    
                // Your search service endpoint
                Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");
    
                // Use the recommended keyless credential instead of the AzureKeyCredential credential.
                DefaultAzureCredential credential = new();
                //AzureKeyCredential credential = new AzureKeyCredential("Your search service admin key");
    
                // Create a SearchIndexClient to send create/delete index commands
                SearchIndexClient searchIndexClient = new SearchIndexClient(serviceEndpoint, credential);
    
                // Create a SearchClient to load and query documents
                string indexName = "hotels-quickstart";
                SearchClient searchClient = new SearchClient(serviceEndpoint, indexName, credential);
    
                // Delete index if it exists
                Console.WriteLine("{0}", "Deleting index...\n");
                DeleteIndexIfExists(indexName, searchIndexClient);
    
                // Create index
                Console.WriteLine("{0}", "Creating index...\n");
                CreateIndex(indexName, searchIndexClient);
    
                SearchClient ingesterClient = searchIndexClient.GetSearchClient(indexName);
    
                // Load documents
                Console.WriteLine("{0}", "Uploading documents...\n");
                UploadDocuments(ingesterClient);
    
                // Wait 2 secondsfor indexing to complete before starting queries (for demo and console-app purposes only)
                Console.WriteLine("Waiting for indexing...\n");
                System.Threading.Thread.Sleep(2000);
    
                // Call the RunQueries method to invoke a series of queries
                Console.WriteLine("Starting queries...\n");
                RunQueries(searchClient);
    
                // End the program
                Console.WriteLine("{0}", "Complete. Press any key to end this program...\n");
                Console.ReadKey();
            }
    
            // Delete the hotels-quickstart index to reuse its name
            private static void DeleteIndexIfExists(string indexName, SearchIndexClient searchIndexClient)
            {
                searchIndexClient.GetIndexNames();
                {
                    searchIndexClient.DeleteIndex(indexName);
                }
            }
            // Create hotels-quickstart index
            private static void CreateIndex(string indexName, SearchIndexClient searchIndexClient)
            {
                FieldBuilder fieldBuilder = new FieldBuilder();
                var searchFields = fieldBuilder.Build(typeof(Hotel));
    
                var definition = new SearchIndex(indexName, searchFields);
    
                var suggester = new SearchSuggester("sg", new[] { "HotelName", "Category", "Address/City", "Address/StateProvince" });
                definition.Suggesters.Add(suggester);
    
                searchIndexClient.CreateOrUpdateIndex(definition);
            }
    
            // Upload documents in a single Upload request.
            private static void UploadDocuments(SearchClient searchClient)
            {
                IndexDocumentsBatch<Hotel> batch = IndexDocumentsBatch.Create(
                    IndexDocumentsAction.Upload(
                        new Hotel()
                        {
                            HotelId = "1",
                            HotelName = "Secret Point Motel",
                            Description = "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
                            DescriptionFr = "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.",
                            Category = "Boutique",
                            Tags = new[] { "pool", "air conditioning", "concierge" },
                            ParkingIncluded = false,
                            LastRenovationDate = new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero),
                            Rating = 3.6,
                            Address = new Address()
                            {
                                StreetAddress = "677 5th Ave",
                                City = "New York",
                                StateProvince = "NY",
                                PostalCode = "10022",
                                Country = "USA"
                            }
                        }),
                    IndexDocumentsAction.Upload(
                        new Hotel()
                        {
                            HotelId = "2",
                            HotelName = "Twin Dome Motel",
                            Description = "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
                            DescriptionFr = "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
                            Category = "Boutique",
                            Tags = new[] { "pool", "free wifi", "concierge" },
                            ParkingIncluded = false,
                            LastRenovationDate = new DateTimeOffset(1979, 2, 18, 0, 0, 0, TimeSpan.Zero),
                            Rating = 3.60,
                            Address = new Address()
                            {
                                StreetAddress = "140 University Town Center Dr",
                                City = "Sarasota",
                                StateProvince = "FL",
                                PostalCode = "34243",
                                Country = "USA"
                            }
                        }),
                    IndexDocumentsAction.Upload(
                        new Hotel()
                        {
                            HotelId = "3",
                            HotelName = "Triple Landscape Hotel",
                            Description = "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
                            DescriptionFr = "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
                            Category = "Resort and Spa",
                            Tags = new[] { "air conditioning", "bar", "continental breakfast" },
                            ParkingIncluded = true,
                            LastRenovationDate = new DateTimeOffset(2015, 9, 20, 0, 0, 0, TimeSpan.Zero),
                            Rating = 4.80,
                            Address = new Address()
                            {
                                StreetAddress = "3393 Peachtree Rd",
                                City = "Atlanta",
                                StateProvince = "GA",
                                PostalCode = "30326",
                                Country = "USA"
                            }
                        }),
                    IndexDocumentsAction.Upload(
                        new Hotel()
                        {
                            HotelId = "4",
                            HotelName = "Sublime Cliff Hotel",
                            Description = "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace.",
                            DescriptionFr = "Le sublime Cliff Hotel est situé au coeur du centre historique de sublime dans un quartier extrêmement animé et vivant, à courte distance de marche des sites et monuments de la ville et est entouré par l'extraordinaire beauté des églises, des bâtiments, des commerces et Monuments. Sublime Cliff fait partie d'un Palace 1800 restauré avec amour.",
                            Category = "Boutique",
                            Tags = new[] { "concierge", "view", "24-hour front desk service" },
                            ParkingIncluded = true,
                            LastRenovationDate = new DateTimeOffset(1960, 2, 06, 0, 0, 0, TimeSpan.Zero),
                            Rating = 4.60,
                            Address = new Address()
                            {
                                StreetAddress = "7400 San Pedro Ave",
                                City = "San Antonio",
                                StateProvince = "TX",
                                PostalCode = "78216",
                                Country = "USA"
                            }
                        })
                    );
    
                try
                {
                    IndexDocumentsResult result = searchClient.IndexDocuments(batch);
                }
                catch (Exception)
                {
                    // If for some reason any documents are dropped during indexing, you can compensate by delaying and
                    // retrying. This simple demo just logs the failed document keys and continues.
                    Console.WriteLine("Failed to index some of the documents: {0}");
                }
            }
    
            // Run queries, use WriteDocuments to print output
            private static void RunQueries(SearchClient searchClient)
            {
                SearchOptions options;
                SearchResults<Hotel> response;
    
                // Query 1
                Console.WriteLine("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");
    
                options = new SearchOptions()
                {
                    IncludeTotalCount = true,
                    Filter = "",
                    OrderBy = { "" }
                };
    
                options.Select.Add("HotelId");
                options.Select.Add("HotelName");
                options.Select.Add("Rating");
    
                response = searchClient.Search<Hotel>("*", options);
                WriteDocuments(response);
    
                // Query 2
                Console.WriteLine("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");
    
                options = new SearchOptions()
                {
                    Filter = "Rating gt 4",
                    OrderBy = { "Rating desc" }
                };
    
                options.Select.Add("HotelId");
                options.Select.Add("HotelName");
                options.Select.Add("Rating");
    
                response = searchClient.Search<Hotel>("hotels", options);
                WriteDocuments(response);
    
                // Query 3
                Console.WriteLine("Query #3: Limit search to specific fields (pool in Tags field)...\n");
    
                options = new SearchOptions()
                {
                    SearchFields = { "Tags" }
                };
    
                options.Select.Add("HotelId");
                options.Select.Add("HotelName");
                options.Select.Add("Tags");
    
                response = searchClient.Search<Hotel>("pool", options);
                WriteDocuments(response);
    
                // Query 4 - Use Facets to return a faceted navigation structure for a given query
                // Filters are typically used with facets to narrow results on OnClick events
                Console.WriteLine("Query #4: Facet on 'Category'...\n");
    
                options = new SearchOptions()
                {
                    Filter = ""
                };
    
                options.Facets.Add("Category");
    
                options.Select.Add("HotelId");
                options.Select.Add("HotelName");
                options.Select.Add("Category");
    
                response = searchClient.Search<Hotel>("*", options);
                WriteDocuments(response);
    
                // Query 5
                Console.WriteLine("Query #5: Look up a specific document...\n");
    
                Response<Hotel> lookupResponse;
                lookupResponse = searchClient.GetDocument<Hotel>("3");
    
                Console.WriteLine(lookupResponse.Value.HotelId);
    
    
                // Query 6
                Console.WriteLine("Query #6: Call Autocomplete on HotelName...\n");
    
                var autoresponse = searchClient.Autocomplete("sa", "sg");
                WriteDocuments(autoresponse);
    
            }
    
            // Write search results to console
            private static void WriteDocuments(SearchResults<Hotel> searchResults)
            {
                foreach (SearchResult<Hotel> result in searchResults.GetResults())
                {
                    Console.WriteLine(result.Document);
                }
    
                Console.WriteLine();
            }
    
            private static void WriteDocuments(AutocompleteResults autoResults)
            {
                foreach (AutocompleteItem result in autoResults.Results)
                {
                    Console.WriteLine(result.Text);
                }
    
                Console.WriteLine();
            }
        }
    }
    ```

1. In the same folder, create a new file named *Hotel.cs* and paste the following code. This code defines the structure of a hotel document. 

    ```csharp
    using System;
    using System.Text.Json.Serialization;
    using Azure.Search.Documents.Indexes;
    using Azure.Search.Documents.Indexes.Models;
    
    namespace AzureSearch.Quickstart
    {
        public partial class Hotel
        {
            [SimpleField(IsKey = true, IsFilterable = true)]
            public string HotelId { get; set; }
    
            [SearchableField(IsSortable = true)]
            public string HotelName { get; set; }
    
            [SearchableField(AnalyzerName = LexicalAnalyzerName.Values.EnLucene)]
            public string Description { get; set; }
    
            [SearchableField(AnalyzerName = LexicalAnalyzerName.Values.FrLucene)]
            [JsonPropertyName("Description_fr")]
            public string DescriptionFr { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string Category { get; set; }
    
            [SearchableField(IsFilterable = true, IsFacetable = true)]
            public string[] Tags { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public bool? ParkingIncluded { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public DateTimeOffset? LastRenovationDate { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public double? Rating { get; set; }
    
            [SearchableField]
            public Address Address { get; set; }
        }
    }
    ```

1. Create a new file named *Hotel.cs* and paste the following code to define the structure of a hotel document. Attributes on the field determine how it's used in an application. For example, the `IsFilterable` attribute must be assigned to every field that supports a filter expression.

    ```csharp
    using System;
    using System.Text.Json.Serialization;
    using Azure.Search.Documents.Indexes;
    using Azure.Search.Documents.Indexes.Models;
    
    namespace AzureSearch.Quickstart
    {
        public partial class Hotel
        {
            [SimpleField(IsKey = true, IsFilterable = true)]
            public string HotelId { get; set; }
    
            [SearchableField(IsSortable = true)]
            public string HotelName { get; set; }
    
            [SearchableField(AnalyzerName = LexicalAnalyzerName.Values.EnLucene)]
            public string Description { get; set; }
    
            [SearchableField(AnalyzerName = LexicalAnalyzerName.Values.FrLucene)]
            [JsonPropertyName("Description_fr")]
            public string DescriptionFr { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string Category { get; set; }
    
            [SearchableField(IsFilterable = true, IsFacetable = true)]
            public string[] Tags { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public bool? ParkingIncluded { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public DateTimeOffset? LastRenovationDate { get; set; }
    
            [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public double? Rating { get; set; }
    
            [SearchableField]
            public Address Address { get; set; }
        }
    }
    ```

1. Create a new file named *Address.cs* and paste the following code to define the structure of an address document.

    ```csharp
    using Azure.Search.Documents.Indexes;
    
    namespace AzureSearch.Quickstart
    {
        public partial class Address
        {
            [SearchableField(IsFilterable = true)]
            public string StreetAddress { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string City { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string StateProvince { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string PostalCode { get; set; }
    
            [SearchableField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
            public string Country { get; set; }
        }
    }
    ```

1. Create a new file named *Hotel.Methods.cs* and paste the following code to define a `ToString()` override for the `Hotel` class. 

    ```csharp
    using System;
    using System.Text;
    
    namespace AzureSearch.Quickstart
    {
        public partial class Hotel
        {
            public override string ToString()
            {
                var builder = new StringBuilder();
    
                if (!String.IsNullOrEmpty(HotelId))
                {
                    builder.AppendFormat("HotelId: {0}\n", HotelId);
                }
    
                if (!String.IsNullOrEmpty(HotelName))
                {
                    builder.AppendFormat("Name: {0}\n", HotelName);
                }
    
                if (!String.IsNullOrEmpty(Description))
                {
                    builder.AppendFormat("Description: {0}\n", Description);
                }
    
                if (!String.IsNullOrEmpty(DescriptionFr))
                {
                    builder.AppendFormat("Description (French): {0}\n", DescriptionFr);
                }
    
                if (!String.IsNullOrEmpty(Category))
                {
                    builder.AppendFormat("Category: {0}\n", Category);
                }
    
                if (Tags != null && Tags.Length > 0)
                {
                    builder.AppendFormat("Tags: [ {0} ]\n", String.Join(", ", Tags));
                }
    
                if (ParkingIncluded.HasValue)
                {
                    builder.AppendFormat("Parking included: {0}\n", ParkingIncluded.Value ? "yes" : "no");
                }
    
                if (LastRenovationDate.HasValue)
                {
                    builder.AppendFormat("Last renovated on: {0}\n", LastRenovationDate);
                }
    
                if (Rating.HasValue)
                {
                    builder.AppendFormat("Rating: {0}\n", Rating);
                }
    
                if (Address != null && !Address.IsEmpty)
                {
                    builder.AppendFormat("Address: \n{0}\n", Address.ToString());
                }
    
                return builder.ToString();
            }
        }
    }
    ```

1. Create a new file named *Address.Methods.cs* and paste the following code to define a `ToString()` override for the `Address` class.

    ```csharp
    using System;
    using System.Text;
    using System.Text.Json.Serialization;
    
    namespace AzureSearch.Quickstart
    {
        public partial class Address
        {
            public override string ToString()
            {
                var builder = new StringBuilder();
    
                if (!IsEmpty)
                {
                    builder.AppendFormat("{0}\n{1}, {2} {3}\n{4}", StreetAddress, City, StateProvince, PostalCode, Country);
                }
    
                return builder.ToString();
            }
    
            [JsonIgnore]
            public bool IsEmpty => String.IsNullOrEmpty(StreetAddress) &&
                                   String.IsNullOrEmpty(City) &&
                                   String.IsNullOrEmpty(StateProvince) &&
                                   String.IsNullOrEmpty(PostalCode) &&
                                   String.IsNullOrEmpty(Country);
        }
    }
    ```

1. Build and run the application with the following command:

    ```shell
    dotnet run
    ```

Output includes messages from [Console.WriteLine](/dotnet/api/system.console.writeline), with the addition of query information and results.


## Explaining the code

In the previous sections, you created a new console application and installed the Azure AI Search client library. You added code to create a search index, load it with documents, and run queries. You ran the program to see the results in the console. 

In this section, we explain the code you added to the console application.

### Create a search client

In *Program.cs*, you created two clients:
- [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient) creates the index.
- [SearchClient](/dotnet/api/azure.search.documents.searchclient) loads and queries an existing index. 

Both clients need the search service endpoint and credentials described previously in the [resource information](#retrieve-resource-information) section.

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```csharp
Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");
DefaultAzureCredential credential = new();
```

#### [API key](#tab/api-key)

```csharp
Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");
AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
```
---

```csharp
static void Main(string[] args)
{
    // Your search service endpoint
    Uri serviceEndpoint = new Uri($"https://<Put your search service NAME here>.search.windows.net/");

    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    DefaultAzureCredential credential = new();
    //AzureKeyCredential credential = new AzureKeyCredential("Your search service admin key");

    // Create a SearchIndexClient to send create/delete index commands
    SearchIndexClient searchIndexClient = new SearchIndexClient(serviceEndpoint, credential);

    // Create a SearchClient to load and query documents
    string indexName = "hotels-quickstart";
    SearchClient searchClient = new SearchClient(serviceEndpoint, indexName, credential);
    
    // REDACTED FOR BREVITY . . . 
}
```

### Create an index

This quickstart builds a Hotels index that you load with hotel data and execute queries against. In this step, you define the fields in the index. Each field definition includes a name, data type, and attributes that determine how the field is used.

In this example, synchronous methods of the *Azure.Search.Documents* library are used for simplicity and readability. However, for production scenarios, you should use asynchronous methods to keep your app scalable and responsive. For example, you would use [CreateIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindexasync) instead of [CreateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindex).

#### Define the structures

You created two helper classes, *Hotel.cs* and *Address.cs*, to define the structure of a hotel document and its address. The `Hotel` class includes fields for a hotel ID, name, description, category, tags, parking, renovation date, rating, and address. The `Address` class includes fields for street address, city, state/province, postal code, and country/region.

In the *Azure.Search.Documents* client library, you can use [SearchableField](/dotnet/api/azure.search.documents.indexes.models.searchablefield) and [SimpleField](/dotnet/api/azure.search.documents.indexes.models.simplefield) to streamline field definitions. Both are derivatives of a [SearchField](/dotnet/api/azure.search.documents.indexes.models.searchfield) and can potentially simplify your code:

+ `SimpleField` can be any data type, is always non-searchable (ignored for full text search queries), and is retrievable (not hidden). Other attributes are off by default, but can be enabled. You might use a `SimpleField` for document IDs or fields used only in filters, facets, or scoring profiles. If so, be sure to apply any attributes that are necessary for the scenario, such as `IsKey = true` for a document ID. For more information, see [SimpleFieldAttribute.cs](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/src/Indexes/SimpleFieldAttribute.cs) in source code.

+ `SearchableField` must be a string, and is always searchable and retrievable. Other attributes are off by default, but can be enabled. Because this field type is searchable, it supports synonyms and the full complement of analyzer properties. For more information, see the [SearchableFieldAttribute.cs](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/src/Indexes/SearchableFieldAttribute.cs) in source code.

Whether you use the basic `SearchField` API or either one of the helper models, you must explicitly enable filter, facet, and sort attributes. For example, [IsFilterable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfilterable), [IsSortable](/dotnet/api/azure.search.documents.indexes.models.searchfield.issortable), and [IsFacetable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfacetable) must be explicitly attributed, as shown in the previous sample.

#### Create the search index

In *Program.cs*, you create a [SearchIndex](/dotnet/api/azure.search.documents.indexes.models.searchindex) object, and then call the [CreateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindex) method to express the index in your search service. The index also includes a [SearchSuggester](/dotnet/api/azure.search.documents.indexes.models.searchsuggester) to enable autocomplete on the specified fields.

```csharp
// Create hotels-quickstart index
private static void CreateIndex(string indexName, SearchIndexClient searchIndexClient)
{
    FieldBuilder fieldBuilder = new FieldBuilder();
    var searchFields = fieldBuilder.Build(typeof(Hotel));

    var definition = new SearchIndex(indexName, searchFields);

    var suggester = new SearchSuggester("sg", new[] { "HotelName", "Category", "Address/City", "Address/StateProvince" });
    definition.Suggesters.Add(suggester);

    searchIndexClient.CreateOrUpdateIndex(definition);
}
```

### Load documents

Azure AI Search searches over content stored in the service. In this step, you load JSON documents that conform to the hotel index you created.

In Azure AI Search, search documents are data structures that are both inputs to indexing and outputs from queries. As obtained from an external data source, document inputs might be rows in a database, blobs in Blob storage, or JSON documents on disk. In this example, we're taking a shortcut and embedding JSON documents for four hotels in the code itself.

When uploading documents, you must use an [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1) object. An `IndexDocumentsBatch` object contains a collection of [Actions](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1.actions), each of which contains a document and a property telling Azure AI Search what action to perform ([upload, merge, delete, and mergeOrUpload](/azure/search/search-what-is-data-import#indexing-actions)).

In *Program.cs*, you create an array of documents and index actions, and then pass the array to `IndexDocumentsBatch`. The following documents conform to the hotels-quickstart index, as defined by the hotel class.

```csharp
// Upload documents in a single Upload request.
private static void UploadDocuments(SearchClient searchClient)
{
    IndexDocumentsBatch<Hotel> batch = IndexDocumentsBatch.Create(
        IndexDocumentsAction.Upload(
            new Hotel()
            {
                HotelId = "1",
                HotelName = "Stay-Kay City Hotel",
                Description = "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
                DescriptionFr = "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.",
                Category = "Boutique",
                Tags = new[] { "pool", "air conditioning", "concierge" },
                ParkingIncluded = false,
                LastRenovationDate = new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero),
                Rating = 3.6,
                Address = new Address()
                {
                    StreetAddress = "677 5th Ave",
                    City = "New York",
                    StateProvince = "NY",
                    PostalCode = "10022",
                    Country = "USA"
                }
            }),
        // REDACTED FOR BREVITY
}
```

Once you initialize the [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1) object, you can send it to the index by calling [IndexDocuments](/dotnet/api/azure.search.documents.searchclient.indexdocuments) on your [SearchClient](/dotnet/api/azure.search.documents.searchclient) object.

You load documents using SearchClient in `Main()`, but the operation also requires admin rights on the service, which is typically associated with SearchIndexClient. One way to set up this operation is to get SearchClient through `SearchIndexClient` (`searchIndexClient` in this example).

```csharp
SearchClient ingesterClient = searchIndexClient.GetSearchClient(indexName);

// Load documents
Console.WriteLine("{0}", "Uploading documents...\n");
UploadDocuments(ingesterClient);
```

Because we have a console app that runs all commands sequentially, we add a 2-second wait time between indexing and queries.

```csharp
// Wait 2 seconds for indexing to complete before starting queries (for demo and console-app purposes only)
Console.WriteLine("Waiting for indexing...\n");
System.Threading.Thread.Sleep(2000);
```

The 2-second delay compensates for indexing, which is asynchronous, so that all documents can be indexed before the queries are executed. Coding in a delay is typically only necessary in demos, tests, and sample applications.

### Search an index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

This section adds two pieces of functionality: query logic, and results. For queries, use the [Search](/dotnet/api/azure.search.documents.searchclient.search) method. This method takes search text (the query string) and other [options](/dotnet/api/azure.search.documents.searchoptions).

The [SearchResults](/dotnet/api/azure.search.documents.models.searchresults-1) class represents the results.

In *Program.cs*, the `WriteDocuments` method prints search results to the console.

```csharp
// Write search results to console
private static void WriteDocuments(SearchResults<Hotel> searchResults)
{
    foreach (SearchResult<Hotel> result in searchResults.GetResults())
    {
        Console.WriteLine(result.Document);
    }

    Console.WriteLine();
}

private static void WriteDocuments(AutocompleteResults autoResults)
{
    foreach (AutocompleteItem result in autoResults.Results)
    {
        Console.WriteLine(result.Text);
    }

    Console.WriteLine();
}
```

#### Query example 1

The `RunQueries` method executes queries and returns results. Results are Hotel objects. This sample shows the method signature and the first query. This query demonstrates the `Select` parameter that lets you compose the result using selected fields from the document.

```csharp
// Run queries, use WriteDocuments to print output
private static void RunQueries(SearchClient searchClient)
{
    SearchOptions options;
    SearchResults<Hotel> response;
    
    // Query 1
    Console.WriteLine("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");

    options = new SearchOptions()
    {
        IncludeTotalCount = true,
        Filter = "",
        OrderBy = { "" }
    };

    options.Select.Add("HotelId");
    options.Select.Add("HotelName");
    options.Select.Add("Address/City");

    response = searchClient.Search<Hotel>("*", options);
    WriteDocuments(response);
    // REDACTED FOR BREVITY
}
```

#### Query example 2

In the second query, search on a term, add a filter that selects documents where *Rating* is greater than 4, and then sort by Rating in descending order. Filter is a boolean expression that is evaluated over [IsFilterable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfilterable) fields in an index. Filter queries either include or exclude values. As such, there's no relevance score associated with a filter query.

```csharp
// Query 2
Console.WriteLine("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");

options = new SearchOptions()
{
    Filter = "Rating gt 4",
    OrderBy = { "Rating desc" }
};

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Rating");

response = searchClient.Search<Hotel>("hotels", options);
WriteDocuments(response);
```

#### Query example 3
The third query demonstrates `searchFields`, used to scope a full text search operation to specific fields.

```csharp
// Query 3
Console.WriteLine("Query #3: Limit search to specific fields (pool in Tags field)...\n");

options = new SearchOptions()
{
    SearchFields = { "Tags" }
};

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Tags");

response = searchClient.Search<Hotel>("pool", options);
WriteDocuments(response);
```

#### Query example 4

The fourth query demonstrates `facets`, which can be used to structure a faceted navigation structure.

```csharp
// Query 4
Console.WriteLine("Query #4: Facet on 'Category'...\n");

options = new SearchOptions()
{
    Filter = ""
};

options.Facets.Add("Category");

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Category");

response = searchClient.Search<Hotel>("*", options);
WriteDocuments(response);
```

#### Query example 5

In the fifth query, return a specific document. A document lookup is a typical response to `OnClick` event in a result set.

```csharp
// Query 5
Console.WriteLine("Query #5: Look up a specific document...\n");

Response<Hotel> lookupResponse;
lookupResponse = searchClient.GetDocument<Hotel>("3");

Console.WriteLine(lookupResponse.Value.HotelId);
```

#### Query example 6

The last query shows the syntax for autocomplete, simulating a partial user input of *sa* that resolves to two possible matches in the sourceFields associated with the suggester you defined in the index.

```csharp
// Query 6
Console.WriteLine("Query #6: Call Autocomplete on HotelName that starts with 'sa'...\n");

var autoresponse = searchClient.Autocomplete("sa", "sg");
WriteDocuments(autoresponse);
```

#### Summary of queries

The previous queries show multiple [ways of matching terms in a query](/azure/search/search-query-overview#types-of-queries): full-text search, filters, and autocomplete.

Full text search and filters are performed using the [SearchClient.Search](/dotnet/api/azure.search.documents.searchclient.search) method. A search query can be passed in the `searchText` string, while a filter expression can be passed in the [Filter](/dotnet/api/azure.search.documents.searchoptions.filter) property of the [SearchOptions](/dotnet/api/azure.search.documents.searchoptions) class. To filter without searching, just pass `"*"` for the `searchText` parameter of the [Search](/dotnet/api/azure.search.documents.searchclient.search) method. To search without filtering, leave the `Filter` property unset, or don't pass in a `SearchOptions` instance at all.

