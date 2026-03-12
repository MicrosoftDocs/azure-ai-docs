---
title: Custom Skill Interface
titleSuffix: Azure AI Search
description: Integrate a custom skill with an AI enrichment pipeline in Azure AI Search through a web interface that defines compatible inputs and outputs in a skillset.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 02/27/2026
ms.update-cycle: 365-days
---

# Add a custom skill to an Azure AI Search enrichment pipeline

An [AI enrichment pipeline](cognitive-search-concept-intro.md) can include both [built-in skills](cognitive-search-predefined-skills.md) and [custom skills](cognitive-search-custom-skill-web-api.md) that you create and publish. Your custom code executes outside the search service (for example, as an Azure function), but accepts inputs and sends outputs to the skillset just like any other skill. Your data is processed in the [geography](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

Custom skills might sound complex, but they can be simple to implement. If you have existing packages that provide pattern matching or classification models, content extracted from blobs can be passed to those models for processing. Because AI enrichment is Azure-based, your model should also be hosted on Azure. Common hosting options include [Azure Functions](cognitive-search-create-custom-skill-example.md) or [containers](https://github.com/Microsoft/SkillsExtractorCognitiveSearch).

If you're building a custom skill, this article describes the interface you use to integrate the skill into the pipeline. The primary requirement is the ability to accept inputs and emit outputs in ways that are consumable within the [skillset](cognitive-search-defining-skillset.md) as a whole. As such, the focus of this article is on the input and output formats that the enrichment pipeline requires.

## Benefits of custom skills

Building a custom skill gives you a way to insert transformations unique to your content. For example, you could build custom classification models to differentiate business and financial contracts and documents, or add a speech recognition skill to reach deeper into audio files for relevant content. For a step-by-step example, see [Example: Creating a custom skill for AI enrichment](cognitive-search-create-custom-skill-example.md).

## Set the endpoint and timeout interval

The interface for a custom skill is specified through the [Custom Web API skill](cognitive-search-custom-skill-web-api.md).

```json
"@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
"description": "This skill has a 230-second timeout",
"uri": "https://[your custom skill uri goes here]",
"authResourceId": "[for managed identity connections, your app's client ID goes here]",
"timeout": "PT230S",
```

The URI is the HTTPS endpoint of your function or app. When setting the URI, make sure the URI is secure (HTTPS). If your code is hosted in an Azure function app, the URI should include an [API key in the header or as a URI parameter](/azure/azure-functions/functions-bindings-http-webhook-trigger#api-key-authorization) to authorize the request. 

If instead your function or app uses Azure managed identities and Azure roles for authentication and authorization, the custom skill can include an authentication token on the request. The following points describe the requirements for this approach:

+ The search service, which sends the request on the indexer's behalf, must be [configured to use a managed identity](search-how-to-managed-identities.md) (either system or user-assigned) so that the caller can be authenticated by Microsoft Entra ID.

+ Your function or app must be [configured for Microsoft Entra ID](/azure/app-service/configure-authentication-provider-aad).

+ Your [custom skill definition](cognitive-search-custom-skill-web-api.md) must include an `authResourceId` property. This property takes an application (client) ID, in a [supported format](/azure/active-directory/develop/security-best-practices-for-app-registration#application-id-uri): `api://<appId>`.

By default, the connection to the endpoint times out if a response isn't returned within a 30-second window (`PT30S`). The indexing pipeline is synchronous, and indexing produces a timeout error if a response isn't received in that time frame. You can increase the interval to a maximum value of 230 seconds by setting the `timeout` parameter (`PT230S`).

## Format web API inputs

The web API must accept an array of records to process. Within each record, provide a property bag as input to your web API.

Suppose you want to create a basic enricher that identifies the first date mentioned in contract text. In this example, the custom skill accepts a single input, "contractText." The skill also has a single output, which is the contract date. To make the enricher more interesting, return "contractDate" in the shape of a multipart complex type.

Your Web API should be ready to receive a batch of input records. Each member of the "values" array represents the input for a particular record. Each record is required to have the following elements:

+ A "recordId" member that's the unique identifier for a particular record. When your enricher returns results, it must provide this "recordId" so that the caller can match record results to inputs.

+ A "data" member, which is a bag of input fields for each record.

The resulting Web API request might look like this:

```json
{
    "values": [
      {
        "recordId": "a1",
        "data":
           {
             "contractText": 
                "This is a contract that was issued on November 3, 2023 and that involves... "
           }
      },
      {
        "recordId": "b5",
        "data":
           {
             "contractText": 
                "In the City of Seattle, WA on February 5, 2018 there was a decision made..."
           }
      },
      {
        "recordId": "c3",
        "data":
           {
             "contractText": null
           }
      }
    ]
}
```

In practice, your code can be called with hundreds or thousands of records instead of only the three shown here.

## Format web API outputs

The output format is a set of records containing a "recordId" and a property bag. This particular example has only one output, but you can return more than one property. As a best practice, consider returning error and warning messages if a record couldn't be processed.

```json
{
  "values": 
  [
      {
        "recordId": "b5",
        "data" : 
        {
            "contractDate":  { "day" : 5, "month": 2, "year" : 2018 }
        }
      },
      {
        "recordId": "a1",
        "data" : {
            "contractDate": { "day" : 3, "month": 11, "year" : 2023 }                    
        }
      },
      {
        "recordId": "c3",
        "data" : 
        {
        },
        "errors": [ { "message": "contractText field required "}   ],  
        "warnings": [ {"message": "Date not found" }  ]
      }
    ]
}
```

## Add a custom skill to a skillset

When you create a web API enricher, you can define HTTP headers and parameters as part of the request. The following snippet shows how request parameters and optional HTTP headers can be included in the skillset definition. Setting an HTTP header is useful if you need to pass configuration settings to your code.

```json
{
    "skills": [
      {
        "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
        "name": "myCustomSkill",
        "description": "This skill calls an Azure function, which in turn calls TA sentiment",
        "uri": "https://indexer-e2e-webskill.azurewebsites.net/api/DateExtractor?language=en",
        "context": "/document",
        "httpHeaders": {
            "DateExtractor-Api-Key": "foo"
        },
        "inputs": [
          {
            "name": "contractText",
            "source": "/document/content"
          }
        ],
        "outputs": [
          {
            "name": "contractDate",
            "targetName": "date"
          }
        ]
      }
  ]
}
```

## Watch this video

For a video introduction and demo, watch the following demo.

> [!VIDEO https://www.youtube.com/embed/fHLCE-NZeb4?version=3]

## Next steps

This article covered the interface requirements necessary for integrating a custom skill into a skillset. Continue with these links to learn more about custom skills and skillset composition.

+ [Power Skills: a repository of custom skills](https://github.com/Azure-Samples/azure-search-power-skills)
+ [Example: Creating a custom skill for AI enrichment](cognitive-search-create-custom-skill-example.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [Create Skillset (REST)](/rest/api/searchservice/skillsets/create)
+ [How to map enriched fields](cognitive-search-output-field-mapping.md)
