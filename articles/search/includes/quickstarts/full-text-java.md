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
> You can [download the source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart) to start with a finished project or follow these steps to create your own.

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

The sample in this quickstart works with the Java Runtime. Install a Java Development Kit such as [Azul Zulu OpenJDK](https://www.azul.com/downloads/?package=jdk). The [Microsoft Build of OpenJDK](https://www.microsoft.com/openjdk) or your preferred JDK should also work.

1. Install [Apache Maven](https://maven.apache.org/install.html). Then run `mvn -v` to confirm successful installation.
1. Create a new `pom.xml` file in the root of your project, and copy the following code into it:

    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>azure.search.sample</groupId>
        <artifactId>azuresearchquickstart</artifactId>
        <version>1.0.0-SNAPSHOT</version>
        <build>
            <sourceDirectory>src</sourceDirectory>
            <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.7.0</version>
                <configuration>
                <source>1.8</source>
                <target>1.8</target>
                </configuration>
            </plugin>
            </plugins>
        </build>
        <dependencies>
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>4.11</version>
                <scope>test</scope>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-search-documents</artifactId>
                <version>11.7.3</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-core</artifactId>
                <version>1.53.0</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-identity</artifactId>
                <version>1.15.1</version>
            </dependency>
        </dependencies>
    </project>
    ```

1. Install the dependencies including the Azure AI Search client library ([Azure.Search.Documents](/java/api/overview/azure/search)) for Java and [Azure Identity client library for Java](https://mvnrepository.com/artifact/com.azure/azure-identity) with:

   ```console
   mvn clean dependency:copy-dependencies
   ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

## Create, load, and query a search index

In the prior [set up](#set-up) section, you installed the Azure AI Search client library and other dependencies. 

In this section, you add code to create a search index, load it with documents, and run queries. You run the program to see the results in the console. For a detailed explanation of the code, see the [explaining the code](#explaining-the-code) section.

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
```

#### [API key](#tab/api-key)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
```
---

1. Create a new file named *App.java* and paste the following code into *App.java*:

    ```java
    import java.util.Arrays;
    import java.util.ArrayList;
    import java.time.OffsetDateTime;
    import java.time.ZoneOffset;
    import java.time.LocalDateTime;
    import java.time.LocalDate;
    import java.time.LocalTime;
    import com.azure.core.util.Configuration;
    import com.azure.core.util.Context;
    import com.azure.identity.DefaultAzureCredential;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.azure.search.documents.SearchClient;
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.indexes.SearchIndexClient;
    import com.azure.search.documents.indexes.SearchIndexClientBuilder;
    import com.azure.search.documents.indexes.models.IndexDocumentsBatch;
    import com.azure.search.documents.models.SearchOptions;
    import com.azure.search.documents.indexes.models.SearchIndex;
    import com.azure.search.documents.indexes.models.SearchSuggester;
    import com.azure.search.documents.util.AutocompletePagedIterable;
    import com.azure.search.documents.util.SearchPagedIterable;
    
    public class App {
    
        public static void main(String[] args) {
            // Your search service endpoint
            "https://<Put your search service NAME here>.search.windows.net/";
    
            // Use the recommended keyless credential instead of the AzureKeyCredential credential.
            DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
            //AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
    
            // Create a SearchIndexClient to send create/delete index commands
            SearchIndexClient searchIndexClient = new SearchIndexClientBuilder()
                .endpoint(searchServiceEndpoint)
                .credential(credential)
                .buildClient();
            
            // Create a SearchClient to load and query documents
            String indexName = "hotels-quickstart-java";
            SearchClient searchClient = new SearchClientBuilder()
                .endpoint(searchServiceEndpoint)
                .credential(credential)
                .indexName(indexName)
                .buildClient();
    
            // Create Search Index for Hotel model
            searchIndexClient.createOrUpdateIndex(
                new SearchIndex(indexName, SearchIndexClient.buildSearchFields(Hotel.class, null))
                .setSuggesters(new SearchSuggester("sg", Arrays.asList("HotelName"))));
    
            // Upload sample hotel documents to the Search Index
            uploadDocuments(searchClient);
    
            // Wait 2 seconds for indexing to complete before starting queries (for demo and console-app purposes only)
            System.out.println("Waiting for indexing...\n");
            try
            {
                Thread.sleep(2000);
            }
            catch (InterruptedException e)
            {
            }
    
            // Call the RunQueries method to invoke a series of queries
            System.out.println("Starting queries...\n");
            RunQueries(searchClient);
    
            // End the program
            System.out.println("Complete.\n");
        }
    
        // Upload documents in a single Upload request.
        private static void uploadDocuments(SearchClient searchClient)
        {
            var hotelList = new ArrayList<Hotel>();
    
            var hotel = new Hotel();
            hotel.hotelId = "1";
            hotel.hotelName = "Stay-Kay City Hotel";
            hotel.description = "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.";
            hotel.descriptionFr = "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.";
            hotel.category = "Boutique";
            hotel.tags = new String[] { "pool", "air conditioning", "concierge" };
            hotel.parkingIncluded = false;
            hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(1970, 1, 18), LocalTime.of(0, 0)), ZoneOffset.UTC);
            hotel.rating = 3.6;
            hotel.address = new Address();
            hotel.address.streetAddress = "677 5th Ave";
            hotel.address.city = "New York";
            hotel.address.stateProvince = "NY";
            hotel.address.postalCode = "10022";
            hotel.address.country = "USA";
            hotelList.add(hotel);
    
            hotel = new Hotel();
            hotel.hotelId = "2";
            hotel.hotelName = "Old Century Hotel";
            hotel.description = "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.";
            hotel.descriptionFr = "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.";
            hotel.category = "Boutique";
            hotel.tags = new String[] { "pool", "free wifi", "concierge" };
            hotel.parkingIncluded = false;
            hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(1979, 2, 18), LocalTime.of(0, 0)), ZoneOffset.UTC);
            hotel.rating = 3.60;
            hotel.address = new Address();
            hotel.address.streetAddress = "140 University Town Center Dr";
            hotel.address.city = "Sarasota";
            hotel.address.stateProvince = "FL";
            hotel.address.postalCode = "34243";
            hotel.address.country = "USA";
            hotelList.add(hotel);
    
            hotel = new Hotel();
            hotel.hotelId = "3";
            hotel.hotelName = "Gastronomic Landscape Hotel";
            hotel.description = "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.";
            hotel.descriptionFr = "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.";
            hotel.category = "Resort and Spa";
            hotel.tags = new String[] { "air conditioning", "bar", "continental breakfast" };
            hotel.parkingIncluded = true;
            hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(2015, 9, 20), LocalTime.of(0, 0)), ZoneOffset.UTC);
            hotel.rating = 4.80;
            hotel.address = new Address();
            hotel.address.streetAddress = "3393 Peachtree Rd";
            hotel.address.city = "Atlanta";
            hotel.address.stateProvince = "GA";
            hotel.address.postalCode = "30326";
            hotel.address.country = "USA";
            hotelList.add(hotel);
    
            hotel = new Hotel();
            hotel.hotelId = "4";
            hotel.hotelName = "Sublime Palace Hotel";
            hotel.description = "Sublime Palace  Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace.";
            hotel.descriptionFr = "Le Sublime Palace Hotel est situé au coeur du centre historique de sublime dans un quartier extrêmement animé et vivant, à courte distance de marche des sites et monuments de la ville et est entouré par l'extraordinaire beauté des églises, des bâtiments, des commerces et Monuments. Sublime Palace fait partie d'un Palace 1800 restauré avec amour.";
            hotel.category = "Boutique";
            hotel.tags = new String[] { "concierge", "view", "24-hour front desk service" };
            hotel.parkingIncluded = true;
            hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(1960, 2, 06), LocalTime.of(0, 0)), ZoneOffset.UTC);
            hotel.rating = 4.60;
            hotel.address = new Address();
            hotel.address.streetAddress = "7400 San Pedro Ave";
            hotel.address.city = "San Antonio";
            hotel.address.stateProvince = "TX";
            hotel.address.postalCode = "78216";
            hotel.address.country = "USA";
            hotelList.add(hotel);
    
            var batch = new IndexDocumentsBatch<Hotel>();
            batch.addMergeOrUploadActions(hotelList);
            try
            {
                searchClient.indexDocuments(batch);
            }
            catch (Exception e)
            {
                e.printStackTrace();
                // If for some reason any documents are dropped during indexing, you can compensate by delaying and
                // retrying. This simple demo just logs failure and continues
                System.err.println("Failed to index some of the documents");
            }
        }
    
        // Write search results to console
        private static void WriteSearchResults(SearchPagedIterable searchResults)
        {
            searchResults.iterator().forEachRemaining(result ->
            {
                Hotel hotel = result.getDocument(Hotel.class);
                System.out.println(hotel);
            });
    
            System.out.println();
        }
    
        // Write autocomplete results to console
        private static void WriteAutocompleteResults(AutocompletePagedIterable autocompleteResults)
        {
            autocompleteResults.iterator().forEachRemaining(result ->
            {
                String text = result.getText();
                System.out.println(text);
            });
    
            System.out.println();
        }
    
        // Run queries, use WriteDocuments to print output
        private static void RunQueries(SearchClient searchClient)
        {
            // Query 1
            System.out.println("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");
    
            SearchOptions options = new SearchOptions();
            options.setIncludeTotalCount(true);
            options.setFilter("");
            options.setOrderBy("");
            options.setSelect("HotelId", "HotelName", "Address/City");
    
            WriteSearchResults(searchClient.search("*", options, Context.NONE));
    
            // Query 2
            System.out.println("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");
    
            options = new SearchOptions();
            options.setFilter("Rating gt 4");
            options.setOrderBy("Rating desc");
            options.setSelect("HotelId", "HotelName", "Rating");
    
            WriteSearchResults(searchClient.search("hotels", options, Context.NONE));
    
            // Query 3
            System.out.println("Query #3: Limit search to specific fields (pool in Tags field)...\n");
    
            options = new SearchOptions();
            options.setSearchFields("Tags");
    
            options.setSelect("HotelId", "HotelName", "Tags");
    
            WriteSearchResults(searchClient.search("pool", options, Context.NONE));
    
            // Query 4
            System.out.println("Query #4: Facet on 'Category'...\n");
    
            options = new SearchOptions();
            options.setFilter("");
            options.setFacets("Category");
            options.setSelect("HotelId", "HotelName", "Category");
    
            WriteSearchResults(searchClient.search("*", options, Context.NONE));
    
            // Query 5
            System.out.println("Query #5: Look up a specific document...\n");
    
            Hotel lookupResponse = searchClient.getDocument("3", Hotel.class);
            System.out.println(lookupResponse.hotelId);
            System.out.println();
    
             // Query 6
            System.out.println("Query #6: Call Autocomplete on HotelName that starts with 's'...\n");
    
            WriteAutocompleteResults(searchClient.autocomplete("s", "sg"));
        }
    }
    ```

1. Create a new file named *Hotel.java* and paste the following code into *Hotel.java*:

    ```java
    import com.azure.search.documents.indexes.SearchableField;
    import com.azure.search.documents.indexes.SimpleField;
    import com.fasterxml.jackson.annotation.JsonInclude;
    import com.fasterxml.jackson.annotation.JsonProperty;
    import com.fasterxml.jackson.core.JsonProcessingException;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.annotation.JsonInclude.Include;
    
    import java.time.OffsetDateTime;
    
    /**
     * Model class representing a hotel.
     */
    @JsonInclude(Include.NON_NULL)
    public class Hotel {
        /**
         * Hotel ID
         */
        @JsonProperty("HotelId")
        @SimpleField(isKey = true)
        public String hotelId;
    
        /**
         * Hotel name
         */
        @JsonProperty("HotelName")
        @SearchableField(isSortable = true)
        public String hotelName;
    
        /**
         * Description
         */
        @JsonProperty("Description")
        @SearchableField(analyzerName = "en.microsoft")
        public String description;
    
        /**
         * French description
         */
        @JsonProperty("DescriptionFr")
        @SearchableField(analyzerName = "fr.lucene")
        public String descriptionFr;
    
        /**
         * Category
         */
        @JsonProperty("Category")
        @SearchableField(isFilterable = true, isSortable = true, isFacetable = true)
        public String category;
    
        /**
         * Tags
         */
        @JsonProperty("Tags")
        @SearchableField(isFilterable = true, isFacetable = true)
        public String[] tags;
    
        /**
         * Whether parking is included
         */
        @JsonProperty("ParkingIncluded")
        @SimpleField(isFilterable = true, isSortable = true, isFacetable = true)
        public Boolean parkingIncluded;
    
        /**
         * Last renovation time
         */
        @JsonProperty("LastRenovationDate")
        @SimpleField(isFilterable = true, isSortable = true, isFacetable = true)
        public OffsetDateTime lastRenovationDate;
    
        /**
         * Rating
         */
        @JsonProperty("Rating")
        @SimpleField(isFilterable = true, isSortable = true, isFacetable = true)
        public Double rating;
    
        /**
         * Address
         */
        @JsonProperty("Address")
        public Address address;
    
        @Override
        public String toString()
        {
            try
            {
                return new ObjectMapper().writeValueAsString(this);
            }
            catch (JsonProcessingException e)
            {
                e.printStackTrace();
                return "";
            }
        }
    }
    ```

1. Create a new file named *Address.java* and paste the following code into *Address.java*:

    ```java
    import com.azure.search.documents.indexes.SearchableField;
    import com.fasterxml.jackson.annotation.JsonInclude;
    import com.fasterxml.jackson.annotation.JsonProperty;
    import com.fasterxml.jackson.annotation.JsonInclude.Include;
    
    /**
     * Model class representing an address.
     */
    @JsonInclude(Include.NON_NULL)
    public class Address {
        /**
         * Street address
         */
        @JsonProperty("StreetAddress")
        @SearchableField
        public String streetAddress;
    
        /**
         * City
         */
        @JsonProperty("City")
        @SearchableField(isFilterable = true, isSortable = true, isFacetable = true)
        public String city;
    
        /**
         * State or province
         */
        @JsonProperty("StateProvince")
        @SearchableField(isFilterable = true, isSortable = true, isFacetable = true)
        public String stateProvince;
    
        /**
         * Postal code
         */
        @JsonProperty("PostalCode")
        @SearchableField(isFilterable = true, isSortable = true, isFacetable = true)
        public String postalCode;
    
        /**
         * Country
         */
        @JsonProperty("Country")
        @SearchableField(isFilterable = true, isSortable = true, isFacetable = true)
        public String country;
    }
    ```


1. Run your new console application:

    ```console
    javac Address.java App.java Hotel.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" App
    ```

## Explaining the code

In the previous sections, you created a new console application and installed the Azure AI Search client library. You added code to create a search index, load it with documents, and run queries. You ran the program to see the results in the console. 

In this section, we explain the code you added to the console application.

### Create a search client

In *App.java* you created two clients:

- SearchIndexClient creates the index.
- SearchClient loads and queries an existing index.

Both clients need the search service endpoint and credentials described previously in the resource information section.

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
```

#### [API key](#tab/api-key)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
```
---

```java
public static void main(String[] args) {
    // Your search service endpoint
    String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";

    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
    //AzureKeyCredential credential = new AzureKeyCredential("Your search service admin key");

    // Create a SearchIndexClient to send create/delete index commands
    SearchIndexClient searchIndexClient = new SearchIndexClientBuilder()
        .endpoint(searchServiceEndpoint)
        .credential(credential)
        .buildClient();
    
    // Create a SearchClient to load and query documents
    String indexName = "hotels-quickstart-java";
    SearchClient searchClient = new SearchClientBuilder()
        .endpoint(searchServiceEndpoint)
        .credential(credential)
        .indexName(indexName)
        .buildClient();

    // Create Search Index for Hotel model
    searchIndexClient.createOrUpdateIndex(
        new SearchIndex(indexName, SearchIndexClient.buildSearchFields(Hotel.class, null))
        .setSuggesters(new SearchSuggester("sg", Arrays.asList("HotelName"))));

    // REDACTED FOR BREVITY . . . 
}
```


### Create an index

This quickstart builds a Hotels index that you load with hotel data and execute queries against. In this step, you define the fields in the index. Each field definition includes a name, data type, and attributes that determine how the field is used.

In this example, synchronous methods of the *Azure.Search.Documents* library are used for simplicity and readability. However, for production scenarios, you should use asynchronous methods to keep your app scalable and responsive. For example, you would use [CreateIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindexasync) instead of [CreateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindex).

#### Define the structures

You created two helper classes, *Hotel.java* and *Address.java*, to define the structure of a hotel document and its address. The Hotel class includes fields for a hotel ID, name, description, category, tags, parking, renovation date, rating, and address. The Address class includes fields for street address, city, state/province, postal code, and country/region.

In the Azure.Search.Documents client library, you can use [SearchableField](/java/api/com.azure.search.documents.indexes.searchablefield) and [SimpleField](/java/api/com.azure.search.documents.indexes.simplefield) to streamline field definitions.

* `SimpleField` can be any data type, is always non-searchable (ignored for full text search queries), and is retrievable (not hidden). Other attributes are off by default, but can be enabled. You might use a SimpleField for document IDs or fields used only in filters, facets, or scoring profiles. If so, be sure to apply any attributes that are necessary for the scenario, such as IsKey = true for a document ID.
* `SearchableField` must be a string, and is always searchable and retrievable. Other attributes are off by default, but can be enabled. Because this field type is searchable, it supports synonyms and the full complement of analyzer properties.

Whether you use the basic `SearchField` API or either one of the helper models, you must explicitly enable filter, facet, and sort attributes. For example, `isFilterable`, `isSortable`, and `isFacetable` must be explicitly attributed, as shown in the previous sample.

#### Create the search index

In `App.java`, you create a `SearchIndex` object in the `main` method, and then call the `createOrUpdateIndex` method to create the index in your search service. The index also includes a `SearchSuggester` to enable autocomplete on the specified fields.

```java
// Create Search Index for Hotel model
searchIndexClient.createOrUpdateIndex(
    new SearchIndex(indexName, SearchIndexClient.buildSearchFields(Hotel.class, null))
    .setSuggesters(new SearchSuggester("sg", Arrays.asList("HotelName"))));
```

### Load documents

Azure AI Search searches over content stored in the service. In this step, you load JSON documents that conform to the hotel index you created.

In Azure AI Search, search documents are data structures that are both inputs to indexing and outputs from queries. As obtained from an external data source, document inputs might be rows in a database, blobs in Blob storage, or JSON documents on disk. In this example, we're taking a shortcut and embedding JSON documents for four hotels in the code itself.

When uploading documents, you must use an [IndexDocumentsBatch](/java/api/com.azure.search.documents.indexes.models.indexdocumentsbatch) object. An `IndexDocumentsBatch` object contains a collection of [IndexActions](/java/api/com.azure.search.documents.models.indexaction), each of which contains a document and a property telling Azure AI Search what action to perform (upload, merge, delete, and mergeOrUpload).

In `App.java`, you create documents and index actions, and then pass them to `IndexDocumentsBatch`. The following documents conform to the hotels-quickstart index, as defined by the hotel class.

```java
private static void uploadDocuments(SearchClient searchClient)
{
    var hotelList = new ArrayList<Hotel>();

    var hotel = new Hotel();
    hotel.hotelId = "1";
    hotel.hotelName = "Stay-Kay City Hotel";
    hotel.description = "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.";
    hotel.descriptionFr = "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.";
    hotel.category = "Boutique";
    hotel.tags = new String[] { "pool", "air conditioning", "concierge" };
    hotel.parkingIncluded = false;
    hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(1970, 1, 18), LocalTime.of(0, 0)), ZoneOffset.UTC);
    hotel.rating = 3.6;
    hotel.address = new Address();
    hotel.address.streetAddress = "677 5th Ave";
    hotel.address.city = "New York";
    hotel.address.stateProvince = "NY";
    hotel.address.postalCode = "10022";
    hotel.address.country = "USA";
    hotelList.add(hotel);
    
    // REDACTED FOR BREVITY

    var batch = new IndexDocumentsBatch<Hotel>();
    batch.addMergeOrUploadActions(hotelList);
    try
    {
        searchClient.indexDocuments(batch);
    }
    catch (Exception e)
    {
        e.printStackTrace();
        // If for some reason any documents are dropped during indexing, you can compensate by delaying and
        // retrying. This simple demo just logs failure and continues
        System.err.println("Failed to index some of the documents");
    }
}
```

Once you initialize the `IndexDocumentsBatch` object, you can send it to the index by calling [indexDocuments](/java/api/com.azure.search.documents.searchclient#com-azure-search-documents-searchclient-indexdocuments(com-azure-search-documents-indexes-models-indexdocumentsbatch(-))) on your `SearchClient` object.

You load documents using SearchClient in `main()`, but the operation also requires admin rights on the service, which is typically associated with SearchIndexClient. One way to set up this operation is to get SearchClient through `SearchIndexClient` (`searchIndexClient` in this example).

```java
uploadDocuments(searchClient);
```

Because we have a console app that runs all commands sequentially, we add a 2-second wait time between indexing and queries.

```java
// Wait 2 seconds for indexing to complete before starting queries (for demo and console-app purposes only)
System.out.println("Waiting for indexing...\n");
try
{
    Thread.sleep(2000);
}
catch (InterruptedException e)
{
}
```

The 2-second delay compensates for indexing, which is asynchronous, so that all documents can be indexed before the queries are executed. Coding in a delay is typically only necessary in demos, tests, and sample applications.

### Search an index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

This section adds two pieces of functionality: query logic and results. For queries, use the Search method. This method takes search text (the query string) and other options.

In `App.java`, the `WriteDocuments` method prints search results to the console.

```java
// Write search results to console
private static void WriteSearchResults(SearchPagedIterable searchResults)
{
    searchResults.iterator().forEachRemaining(result ->
    {
        Hotel hotel = result.getDocument(Hotel.class);
        System.out.println(hotel);
    });

    System.out.println();
}

// Write autocomplete results to console
private static void WriteAutocompleteResults(AutocompletePagedIterable autocompleteResults)
{
    autocompleteResults.iterator().forEachRemaining(result ->
    {
        String text = result.getText();
        System.out.println(text);
    });

    System.out.println();
}
```

#### Query example 1

The `RunQueries` method executes queries and returns results. Results are Hotel objects. This sample shows the method signature and the first query. This query demonstrates the `Select` parameter that lets you compose the result using selected fields from the document.

```java
// Run queries, use WriteDocuments to print output
private static void RunQueries(SearchClient searchClient)
{
    // Query 1
    System.out.println("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");

    SearchOptions options = new SearchOptions();
    options.setIncludeTotalCount(true);
    options.setFilter("");
    options.setOrderBy("");
    options.setSelect("HotelId", "HotelName", "Address/City");

    WriteSearchResults(searchClient.search("*", options, Context.NONE));
}
```

#### Query example 2

In the second query, search on a term, add a filter that selects documents where Rating is greater than 4, and then sort by *Rating* in descending order. Filter is a boolean expression that is evaluated over `isFilterable` fields in an index. Filter queries either include or exclude values. As such, there's no relevance score associated with a filter query.

```java
// Query 2
System.out.println("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");

options = new SearchOptions();
options.setFilter("Rating gt 4");
options.setOrderBy("Rating desc");
options.setSelect("HotelId", "HotelName", "Rating");

WriteSearchResults(searchClient.search("hotels", options, Context.NONE));
```

#### Query example 3

The third query demonstrates `searchFields`, used to scope a full text search operation to specific fields.

```java
// Query 3
System.out.println("Query #3: Limit search to specific fields (pool in Tags field)...\n");

options = new SearchOptions();
options.setSearchFields("Tags");

options.setSelect("HotelId", "HotelName", "Tags");

WriteSearchResults(searchClient.search("pool", options, Context.NONE));
```

#### Query example 4

The fourth query demonstrates `facets`, which can be used to structure a faceted navigation structure.

```java
// Query 4
System.out.println("Query #4: Facet on 'Category'...\n");

options = new SearchOptions();
options.setFilter("");
options.setFacets("Category");
options.setSelect("HotelId", "HotelName", "Category");

WriteSearchResults(searchClient.search("*", options, Context.NONE));
```

#### Query example 5

In the fifth query, return a specific document.

```java
// Query 5
System.out.println("Query #5: Look up a specific document...\n");

Hotel lookupResponse = searchClient.getDocument("3", Hotel.class);
System.out.println(lookupResponse.hotelId);
System.out.println();
```

#### Query example 6

The last query shows the syntax for autocomplete, simulating a partial user input of *s* that resolves to two possible matches in the `sourceFields` associated with the suggester you defined in the index.

```java
// Query 6
System.out.println("Query #6: Call Autocomplete on HotelName that starts with 's'...\n");

WriteAutocompleteResults(searchClient.autocomplete("s", "sg"));
```

#### Summary of queries

The previous queries show multiple ways of matching terms in a query: full-text search, filters, and autocomplete.

Full text search and filters are performed using the [SearchClient.search](/java/api/com.azure.search.documents.searchclient#com-azure-search-documents-searchclient-search(java-lang-string)) method. A search query can be passed in the `searchText` string, while a filter expression can be passed in the `filter` property of the [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions) class. To filter without searching, just pass "*" for the `searchText` parameter of the `search` method. To search without filtering, leave the `filter` property unset, or don't pass in a `SearchOptions` instance at all.

