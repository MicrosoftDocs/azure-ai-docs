---
title: Attach Resource to Skillset for Billing
titleSuffix: Azure AI Search
description: Learn how to attach a Microsoft Foundry resource to an AI enrichment pipeline for billing purposes in Azure AI Search.
author: HeidiSteen 
ms.author: heidist 
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/04/2025
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - ignite-2024
  - sfi-image-nochange
---

# Attach a billable resource to a skillset in Azure AI Search

If you're using built-in skills for [AI enrichment](cognitive-search-concept-intro.md) in Azure AI Search, you can enrich a small number of documents for free, up to 20 transactions per index per day. For larger or more frequent workloads, you should attach a billable Microsoft Foundry resource to your [skillset](/rest/api/searchservice/skillsets/create).

Azure AI Search uses dedicated, internally hosted resources to execute built-in skills backed by Foundry Tools and requires a Foundry resource solely for billing purposes. The exception is the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md), which uses your resource for both billing and processing.

A Foundry resource provides access to multiple services within Foundry Tools. When you specify it in a skillset, Microsoft is able to charge you for using the following services:

+ [Azure Vision in Foundry Tools](/azure/ai-services/computer-vision/overview) for image analysis, optical character recognition (OCR), and multimodal embeddings.
+ [Azure Language in Foundry Tools](/azure/ai-services/language-service/overview) for language detection, entity recognition, sentiment analysis, and key phrase extraction.
+ [Azure Translator in Foundry Tools](/azure/ai-services/translator/translator-overview) for machine text translation.

Skillset processing is billed to the underlying service of each skill. Azure AI Search consolidates charges for Foundry Tools into a single Foundry resource. For example, if you use the [Image Analysis](cognitive-search-skill-image-analysis.md) and [Language Detection](cognitive-search-skill-language-detection.md) skills, charges for Azure Vision and Azure Language appear on the same bill for your Foundry resource. All other resources are billed independently.

To attach a Foundry resource, provide connection information in the skillset. You can use a key-based approach or keyless approach, which is currently in preview.

## Prerequisites

+ Connectivity over a public endpoint, unless your search service meets the creation date, tier, and region requirements for [private connections](search-indexer-howto-access-private.md) to a Foundry resource.

+ A [Foundry resource](/azure/ai-services/multi-service-resource) with the `AIServices` API kind. You can verify the API kind on the resource's **Overview** page in the Azure portal:

  :::image type="content" source="media/cognitive-search-attach-cognitive-services/ai-services-kind.png" alt-text="Screenshot of the API kind property in the Azure portal." border="true" lightbox="media/cognitive-search-attach-cognitive-services/ai-services-kind.png":::

> [!NOTE]
> + If your Foundry resource is configured to use a private endpoint, Azure AI Search can [connect using a shared private link](search-indexer-howto-access-private.md). For more information, see [Shared private link resource limits](search-limits-quotas-capacity.md#shared-private-link-resource-limits).
>
> + The 2025-11-01-preview introduces support for the `AIServices` API kind. The previous `CognitiveServices` and classic Azure AI multi-service accounts continue to work, but for new skillsets, we recommend that you use `AIServices` and Foundry resources.

## Bill through a keyless connection

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

You can use a managed identity and permissions to attach a Foundry resource. The advantage of this approach is that billing is keyless and doesn't have region requirements.

As with keys, the details you provide about the resource are used for billing, not connections. All API requests made by Azure AI Search to Foundry Tools for built-in skills processing remain internal and managed by Microsoft.

To bill through a keyless connection:

1. On your Azure AI Search service, [configure a managed identity](search-how-to-managed-identities.md). Both system-assigned and user-assigned identities are supported.

1. On your Foundry resource, [assign the **Cognitive Services User** role](/azure/role-based-access-control/role-assignments-portal) to the managed identity of your search service.

1. Configure a skillset to use the managed identity. You can use the Azure portal, the latest preview version of [Skillsets - Create Or Update (REST API)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true), or an Azure SDK beta package that provides the syntax.

    + `@odata.type` is always `#Microsoft.Azure.Search.AIServicesByIdentity`.

    + `subdomainUrl` is the endpoint of your Foundry resource. You can use the `https://<resource-name>.services.ai.azure.com` or `https://<resource-name>.cognitiveservices.azure.com` format, both of which are available on the **Keys and Endpoint** page in the Azure portal.

    + Other properties are specific to the type of managed identity, as shown in the following REST API examples.

        ### [System-assigned managed identity](#tab/system-assigned)

        Here's a sample skillset configuration for a system-assigned managed identity. In this scenario, you must set `identity` to `null`.

        ```http
        POST https://[service-name].search.windows.net/skillsets/[skillset-name]?api-version=2025-11-01-preview
        api-key: [admin-key]
        Content-Type: application/json
    
        {
          "name": "my-skillset",
          "skills": [
            // Skills definition goes here
          ],
          "cognitiveServices": {
            "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity",
            "description": "A sample configuration for a system-assigned managed identity.",
            "subdomainUrl": "https://[resource-name].services.ai.azure.com",
            "identity": null
          }
        }
        ```

        ### [User-assigned managed identity](#tab/user-assigned)

        Here's a sample skillset configuration for a user-assigned managed identity. In this scenario, you must set `identity` to the resource ID of the user-assigned managed identity. To find an existing user-assigned managed identity, see [Manage user-assigned managed identities](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities).

        You must also set the `identity.@odata.type` and `identity.userAssignedIdentity` properties.

        ```http
        POST https://[service-name].search.windows.net/skillsets/[skillset-name]?api-version=2025-11-01-preview
        api-key: [admin-key]
        Content-Type: application/json
    
        { 
            "name": "my-skillset", 
            "skills":  
            [ 
              // Skills definition goes here
            ], 
            "cognitiveServices": { 
                "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity", 
                "description": "A sample configuration for a user-assigned managed identity.", 
                "subdomainUrl": "https://[resource-name].services.ai.azure.com",
                "identity": {   
                    "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",   
                    "userAssignedIdentity": ""/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{user-assigned-managed-identity-name}"" 
                }
            } 
        }
        ```

        ---

## Bill through a resource key

By default, Azure AI Search charges for transactions using the key of a Foundry resource. This approach is generally available. You can use the Azure portal, a stable REST API version, or an equivalent Azure SDK to add the key to a skillset.

There are two supported key types:

+ `#Microsoft.Azure.Search.CognitiveServicesByKey` calls the regional endpoint.
+ `#Microsoft.Azure.Search.AIServicesByKey` calls the subdomain. We recommend this type because it supports shared private links and doesn't have regional requirements relative to the search service.

Your Foundry resource must be in the same region as your search service. Choose an [Azure AI Search region that provides Foundry Tools integration](search-region-support.md), which is indicated by the **AI enrichment** column. For more information about the same-region requirement, see [How the key is used](#how-the-key-is-used).

If you don't specify the `cognitiveServices` property, your search service attempts to use the free enrichments available to your indexer each day. Execution of billable skills stops at 20 transactions per indexer invocation, and a "Time Out" message appears in the indexer execution history.

### [**Azure portal**](#tab/portal)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Create a Foundry resource in the same region as your search service.

1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

1. Copy one of the keys.

1. Add the key to a skillset definition.

   + If you're using an [import wizard](search-import-data-portal.md), select the Foundry resource. The wizard adds the resource key to your skillset definition.

   + For a new or existing skillset, provide the key in skillset definition.

   :::image type="content" source="media/cognitive-search-attach-cognitive-services/attach-existing2.png" alt-text="Screenshot of the key page." border="true":::

> [!NOTE]
> The portal automatically attaches the key of type `#Microsoft.Azure.Search.CognitiveServicesByKey`.

### [**REST**](#tab/cogkey-rest)

Use [Skillsets - Create Or Update (REST API)](/rest/api/searchservice/skillsets/create-or-update), specifying the `cognitiveServices` section in the body of the request.

```http
PUT https://[service-name].search.windows.net/skillsets/[skillset-name]?api-version=2025-09-01
api-key: [admin-key]
Content-Type: application/json
{
    "name": "my-skillset",
    "skills": 
    [
      // Skills definition goes here
    ],
    "cognitiveServices": {
        "@odata.type": "#Microsoft.Azure.Search.AIServicesByKey",
        "description": "A sample configuration for key-based billing.",
        "subdomainUrl": "https://[resource-name].services.ai.azure.com",
        "key": "{your-billable-resource-key}"
    }
}
```

### [**.NET SDK**](#tab/cogkey-csharp)

The following code snippet from [azure-search-dotnet-samples](https://github.com/Azure-Samples/azure-search-dotnet-samples/blob/main/tutorial-ai-enrichment/tutorial-ai-enrichment/Program.cs) is trimmed for brevity.

```csharp
IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
IConfigurationRoot configuration = builder.Build();

string searchServiceUri = configuration["SearchServiceUri"];
string adminApiKey = configuration["SearchServiceAdminApiKey"];
string cognitiveServicesKey = configuration["CognitiveServicesKey"];

SearchIndexerClient indexerClient = new SearchIndexerClient(new Uri(searchServiceUri), new AzureKeyCredential(adminApiKey));

// Create the skills
Console.WriteLine("Creating the skills...");
OcrSkill ocrSkill = CreateOcrSkill();
MergeSkill mergeSkill = CreateMergeSkill();

// Create the skillset
Console.WriteLine("Creating or updating the skillset...");
List<SearchIndexerSkill> skills = new List<SearchIndexerSkill>();
skills.Add(ocrSkill);
skills.Add(mergeSkill);

SearchIndexerSkillset skillset = CreateOrUpdateDemoSkillSet(indexerClient, skills, cognitiveServicesKey);
```

---

## Remove the key

Enrichments are billable operations. If you no longer need to call Foundry Tools, follow these instructions to remove the key and prevent use of the Foundry resource.

Without the key, the skillset reverts to the default allocation of 20 free transactions per indexer per day. Execution of billable skills stops at 20 transactions, and a "Time Out" message appears in the indexer execution history when the allocation is used.

### [**Azure portal**](#tab/portal-remove)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Under **Search management > Skillsets**, select a skillset from the list.

   :::image type="content" source="media/cognitive-search-attach-cognitive-services/select-skillset.png" alt-text="Screenshot of the skillset page." border="true" lightbox="media/cognitive-search-attach-cognitive-services/select-skillset.png":::

1. Scroll to the `"cognitiveServices"` section in the file.

1. Delete the key value from the JSON.

1. Save the skillset.

   :::image type="content" source="media/cognitive-search-attach-cognitive-services/remove-key-save.png" alt-text="Screenshot of the skillset JSON." border="true" lightbox="media/cognitive-search-attach-cognitive-services/remove-key-save.png":::

### [**REST**](#tab/cogkey-rest-remove)

1. Use [Skillsets - Get (REST API)](/rest/api/searchservice/skillsets/get) to retrieve the JSON definition of the skillset.

1. Use [Skillsets - Create Or Update (REST API)](/rest/api/searchservice/skillsets/create-or-update) to formulate an update request with the JSON definition.

1. Remove the key from the body of the JSON definition.

1. Send the request.

    ```http
    PUT https://[service-name].search.windows.net/skillsets/[skillset-name]?api-version=2025-09-01
    api-key: [admin-key]
    Content-Type: application/json

    {
        "name": "my-skillset",
        "skills": 
        [
          // Skills definition goes here
        ],
        "cognitiveServices": {
            "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
            "description": "An example of removing the key.",
            "key": ""
        }
    }
    ```

    Alternatively, you can set `cognitiveServices` to `null`:

    ```json
    "cognitiveServices": null,
    ```

---

<a name="same-region-requirement"></a>

## How the key is used

Billing goes into effect when API calls to a Foundry resource exceed 20 API calls per indexer per day. You can [reset the indexer](search-howto-run-reset-indexers.md) to reset the API count.

Keyless and key-based connections are used for billing, but not for connections related to enrichment operations.

For key-based connections, a search service [connects over the internal network](search-security-overview.md#internal-traffic) to a Foundry resource located in the [same physical region](search-region-support.md). Most regions that offer Azure AI Search also offer other Azure services. If you attempt AI enrichment in a region that doesn't have both services, you see this message: "Provided key isn't a valid CognitiveServices type key for the region of your search service."

For keyless connections, a search service authenticates using its identity and role assignment and targets a Foundry resource. The resource is specified as a fully qualified URI, and the URI includes a unique subdomain.

Indexers can be configured to run in a [private execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment) for dedicated processing using just the search nodes of your own search service. Even if you're using a private execution environment, Azure AI Search still uses its internally provisioned resources to perform all skill enrichments.

> [!NOTE]
> Some built-in skills, such as the [Text Translation skill](cognitive-search-skill-text-translation.md), are based on non-regional Foundry Tools services. If you use a non-regional skill, your request might be serviced in a different region than the Azure AI Search region. For more information about non-regional services, see the [product availability by region](https://aka.ms/allinoneregioninfo) page.

### Public connection requirements

Depending on when your search service was created, its pricing tier, and its region, billing for [built-in skills](cognitive-search-predefined-skills.md) can require a public connection from Azure AI Search to your Foundry resource. Disabling public network access breaks billing in some scenarios. Review the requirements for [connections through a shared private link](search-indexer-howto-access-private.md) to determine whether your search service requires a public connection.

If you can't use the public network, you can configure a [Custom Web API skill](cognitive-search-custom-skill-interface.md) implemented with an [Azure Function](cognitive-search-create-custom-skill-example.md) that supports [private endpoints](/azure/azure-functions/functions-create-vnet) and add your [Foundry resource to the same VNET](/azure/ai-services/cognitive-services-virtual-networks). In this scenario, you can call your Foundry resource directly from the custom skill using private endpoints.

### Key requirements special cases

[Custom Entity Lookup](cognitive-search-skill-custom-entity-lookup.md) is metered by Azure AI Search, but it requires a Foundry resource key to unlock transactions beyond 20 per indexer per day. For this skill only, the resource key unblocks the number of transactions but is unrelated to billing.

## Free enrichments

AI enrichment offers a small quantity of free processing of billable enrichments so that you can complete short exercises without having to attach an external resource. Free enrichments are 20 documents per indexer per day. You can [reset the indexer](search-howto-run-reset-indexers.md) to reset the counter if you want to repeat an exercise.

Some enrichments are always free:

+ Utility skills that don't call Foundry Tools (namely the [Conditional](cognitive-search-skill-conditional.md), [Document Extraction](cognitive-search-skill-document-extraction.md), [Shaper](cognitive-search-skill-shaper.md), [Text Merge](cognitive-search-skill-textmerger.md), and [Text Split](cognitive-search-skill-textsplit.md) skills) aren't billable.

+ Text extraction from PDF documents and other application files is nonbillable. Text extraction, which occurs during [document cracking](search-indexer-overview.md#document-cracking), isn't an AI enrichment, but it occurs during AI enrichment and is thus noted here.

## Billable enrichments

During AI enrichment, Azure AI Search calls APIs for [built-in skills](cognitive-search-predefined-skills.md) that are based on Azure Vision, Azure Language, and Azure Translator.

Billable built-in skills that make backend calls to external services include:

+ [Entity Linking](cognitive-search-skill-entity-linking-v3.md)
+ [Entity Recognition](cognitive-search-skill-entity-recognition-v3.md)
+ [Image Analysis](cognitive-search-skill-image-analysis.md)
+ [Key Phrase Extraction](cognitive-search-skill-keyphrases.md)
+ [Language Detection](cognitive-search-skill-language-detection.md)
+ [OCR](cognitive-search-skill-ocr.md)
+ [Personally Identifiable Information (PII) Detection](cognitive-search-skill-pii-detection.md)
+ [Sentiment](cognitive-search-skill-sentiment-v3.md)
+ [Text Translation](cognitive-search-skill-text-translation.md)
+ [Azure Vision multimodal embeddings](cognitive-search-skill-vision-vectorize.md)

A [query-time vectorizer](vector-search-how-to-configure-vectorizer.md) backed by the Azure Vision multimodal embedding model is also a billable enrichment.

Image extraction is an Azure AI Search operation that occurs when documents are cracked prior to enrichment. Image extraction is billable on all pricing tiers, except for 20 free daily extractions on the free tier. Image extraction costs apply to image files inside blobs, embedded images in other files (PDF and other app files), and images extracted using [Document Extraction](cognitive-search-skill-document-extraction.md). For image extraction pricing, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/).

> [!TIP]
> To lower the cost of skillset processing, enable [incremental enrichment](enrichment-cache-how-to-configure.md) to cache and reuse any enrichments that are unaffected by changes made to a skillset. Caching requires Azure Storage (see [pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)), but the cumulative cost of skillset execution is lower if existing enrichments can be reused, especially for skillsets that use image extraction and analysis.

## Example: Estimate costs

The prices shown in this section are hypothetical and used to illustrate the estimation process. Your costs could be lower. For the actual price of transactions, see [Foundry Tools pricing](https://azure.microsoft.com/pricing/details/cognitive-services).

To estimate the costs associated with Azure AI Search indexing, start with an idea of what an average document looks like so you can run some numbers. For example, you might approximate:

+ 1,000 PDFs
+ Six pages each
+ One image per page (6,000 images)
+ 3,000 characters per page

Assume a pipeline that consists of document cracking of each PDF, image and text extraction, OCR of images, and entity recognition of organizations.

1. For document cracking with text and image content, text extraction is currently free. For 6,000 images, assume $1 for every 1,000 images extracted. That's a cost of $6.00 for this step.

1. For OCR of 6,000 images in English, the OCR cognitive skill uses the best algorithm (DescribeText). Assuming a cost of $2.50 per 1,000 images to be analyzed, you would pay $15.00 for this step.

1. For entity extraction, you'd have a total of three text records per page. Each record is 1,000 characters. Three text records per page multiplied by 6,000 pages equal 18,000 text records. Assuming $2.00 per 1,000 text records, this step would cost $36.00.

Putting it all together, you'd pay about $57.00 to ingest 1,000 PDF documents of this type with the described skillset.

## Related content

+ [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [Create Skillset (REST)](/rest/api/searchservice/skillsets/create)
+ [How to map enriched fields](cognitive-search-output-field-mapping.md)
