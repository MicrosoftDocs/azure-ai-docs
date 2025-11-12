---
title: Move a search service across regions
titleSuffix: Azure AI Search
description: Learn how to move your Azure AI Search resources from one region to another in the Azure cloud.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/29/2025
ms.update-cycle: 365-days
ms.custom:
  - subject-moving-resources
  - ignite-2023
  - sfi-image-nochange
---

# Move your Azure AI Search service to another Azure region

Occasionally, customers ask about moving a search service to another region. Currently, there's no built-in mechanism or tooling to help with that task, but this article can help you understand the manual steps for recreating indexes and other objects on a new search service in a different region.

> [!NOTE]
> In the Azure portal, all services have an **Export template** command. In the case of Azure AI Search, this command produces a basic definition of a service (name, location, tier, replica, and partition count), but does not recognize the content of your service, nor does it carry over keys, roles, or logs. Although the command exists, we don't recommend using it for moving a search service.

## Prerequisites

+ Ensure that the services and features that your account uses are supported in the target region.

+ For preview features, ensure that your subscription is approved for the target region.

## Prepare and move

1. Identify dependencies and related services to understand the full impact of relocating a service, in case you need to move more than just Azure AI Search.

   Azure Storage is used for logging, creating a knowledge store, and is a commonly used external data source for AI enrichment and indexing. Foundry Tools are used to power built-in skills during AI enrichment. Both Foundry Tools and your search service are required to be in the same region if you're using AI enrichment.

1. Create an inventory of all objects on the service so that you know what to move: indexes, synonym maps, indexers, data sources, skillsets. If you enabled logging, create and archive any reports you might need for a historical record.

1. Check pricing and availability in the new region to ensure availability of Azure AI Search plus any related services in the new region. Most features are available in all regions, but some preview features have restricted availability.

1. Create a service in the new region and republish from source code any existing indexes, synonym maps, indexers, data sources, and skillsets. Remember that service names must be unique so you can't reuse the existing name. Check each skillset to see if connections to Foundry Tools are still valid in terms of the same-region requirement. Also, if knowledge stores are created, check the connection strings for Azure Storage if you're using a different service.

1. Reload indexes and knowledge stores, if applicable. You'll either use application code to push JSON data into an index, or rerun indexers to pull documents in from external sources. 

1. Enable logging, and if you're using them, re-create security roles.

1. Update client applications and test suites to use the new service name and API keys, and test all applications.

## Discard or clean up

Delete the old service once the new service is fully tested and operational. Deleting the service automatically deletes all content associated with the service.

## Next steps

The following links can help you locate more information when completing the steps outlined above.

+ [Azure AI Search pricing and regions](https://azure.microsoft.com/pricing/details/search/)
+ [Choose a tier](search-sku-tier.md)
+ [Create a search service](search-create-service-portal.md)
+ [Load search documents](search-what-is-data-import.md)
+ [Enable logging](monitor-azure-cognitive-search.md)