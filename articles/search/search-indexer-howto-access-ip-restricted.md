---
title: Connect Through Firewalls
titleSuffix: Azure AI Search
description: Configure IP firewall rules to allow data access by an Azure AI Search indexer.
manager: nitinme
author: arv100kri
ms.author: arjagann
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/29/2026
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-image-nochange
  - dev-focus
ai-usage: ai-assisted
---

# Configure IP firewall rules to allow indexer connections from Azure AI Search

Azure AI Search makes external, outbound calls during indexer processing for content and skills, and for agentic retrieval requests that include calls to large language models (LLMs). If the target Azure resource uses IP firewall rules to filter incoming calls, you must create an inbound rule in your firewall that admits requests from Azure AI Search.

This article explains how to find the IP address of your search service and configure an inbound IP rule on an Azure Storage account. While specific to Azure Storage, this approach also works for other Azure resources that use IP firewall rules for data access, such as Azure Cosmos DB and Azure SQL.

## Prerequisites

+ [Azure AI Search service](search-create-service-portal.md) (Basic tier or higher). You can't set firewall rules on the Free tier.
+ An existing target Azure resource protected by a firewall.
+ **Contributor** or **Owner** role on the search service.

> [!NOTE]
> + Applicable to Azure Storage only. To define IP firewall rules, your storage account and search service must be in different regions. If your setup doesn't permit different regions, try the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md) or [resource instance rule](/azure/storage/common/storage-network-security#grant-access-from-azure-resource-instances) instead.
>
> + For private connections from indexers to any supported Azure resource, we recommend setting up a [shared private link](search-indexer-howto-access-private.md). Private connections travel the Microsoft backbone network, bypassing the public internet completely.

## Get a search service IP address

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Overview**.

1. Copy the fully qualified domain name (FQDN) of your search service, which should look like `my-search-service.search.windows.net`.

   :::image type="content" source="media/search-get-started-rest/get-endpoint.png" alt-text="Screenshot of the search service Overview page." border="true" lightbox="media/search-get-started-rest/get-endpoint.png":::

1. Look up the IP address of the search service by performing an `nslookup` (or a `ping`) of the FQDN on a command prompt. Make sure you remove the `https://` prefix.

1. Copy the IP address for use in the next step. In the following example, the IP address that you copy is `150.0.0.1`.

   ```bash
   nslookup my-search-service.search.windows.net
   Server:  server.example.org
   Address:  10.50.10.50
    
   Non-authoritative answer:
   Name:    <name>
   Address:  150.0.0.1
   aliases:  my-search-service.search.windows.net
   ```

   The IP address in the `Address` field under "Non-authoritative answer" (150.0.0.1 in this example) is the value you need for the firewall rule.

## Allow access from your client IP address

Client applications that push indexing and query requests to the search service must be represented in an IP range. On Azure, you can generally determine the IP address by pinging the FQDN of a service. For example, `ping <your-search-service-name>.search.windows.net` returns the IP address of a search service.

Add your client IP address to allow access to the service from the Azure portal on your current computer.

1. In the Azure portal, select your search service.

1. From the left pane, select **Settings** > **Networking**.

1. On the **Firewall and virtual networks** tab, set **Public network access** to **Selected IP addresses**.

   :::image type="content" source="media\service-configure-firewall\azure-portal-firewall.png" alt-text="Screenshot of the option to allow public network access from selected IP addresses in the Azure portal." border="true":::

1. Under **IP Firewall**, select **Add your client IP address**.

   :::image type="content" source="media\service-configure-firewall\azure-portal-firewall-all.png" alt-text="Screenshot of the option to add your client IP address in the Azure portal." border="true":::

1. Save your changes.

## Get the Azure portal IP address

If you're using the [legacy Import data wizard](search-import-data-portal.md) in the Azure portal to create an indexer that pulls from Azure Cosmos DB or Azure SQL, you must grant the Azure portal IP address inbound access to your SQL Azure virtual machine. For more information, see [Allow access from the Azure portal IP address](service-configure-firewall.md#allow-access-from-the-azure-portal-ip-address).

We recommend using the [Import data (new) wizard](search-get-started-portal.md), which doesn't have this limitation. 

## Get IP addresses for "AzureCognitiveSearch" service tag

You'll also need to create an inbound rule that allows requests from the [multitenant execution environment](search-indexer-securing-resources.md#network-access-and-indexer-execution-environments). This environment is managed by Microsoft and it's used to offload processing intensive jobs that could otherwise overwhelm your search service. This section explains how to get the range of IP addresses needed to create this inbound rule.

An IP address range is defined for each region that supports Azure AI Search. Specify the full range to ensure the success of requests originating from the multitenant execution environment. 

You can get this IP address range from the `AzureCognitiveSearch` service tag.

1. Use either the [discovery API](/azure/virtual-network/service-tags-overview#use-the-service-tag-discovery-api) or the [downloadable JSON file](/azure/virtual-network/service-tags-overview#discover-service-tags-by-using-downloadable-json-files). If the search service is the Azure Public cloud, download the [Azure Public JSON file](https://www.microsoft.com/download/details.aspx?id=56519).

1. Open the JSON file and search for "AzureCognitiveSearch". For a search service in WestUS2, the IP addresses for the multitenant indexer execution environment are:

    ```json
    {
    "name": "AzureCognitiveSearch.WestUS2",
    "id": "AzureCognitiveSearch.WestUS2",
    "properties": {
       "changeNumber": 1,
       "region": "westus2",
       "regionId": 38,
       "platform": "Azure",
       "systemService": "AzureCognitiveSearch",
       "addressPrefixes": [
          "20.42.129.192/26",
          "40.91.93.84/32",
          "40.91.127.116/32",
          "40.91.127.241/32",
          "51.143.104.54/32",
          "51.143.104.90/32",
          "2603:1030:c06:1::180/121"
       ],
       "networkFeatures": null
    }
    },
    ```

    Copy all IP addresses in the `addressPrefixes` array for your region.

1. For IP addresses having the "/32" suffix, drop the "/32" (40.91.93.84/32 becomes 40.91.93.84 in the rule definition). All other IP addresses can be used verbatim.

1. Copy all of the IP addresses for the region.

## Add IP addresses to IP firewall rules

After you get the necessary IP addresses, set up the inbound rules. The easiest way to add IP address ranges to a storage account's firewall rule is through the Azure portal. 

1. In the Azure portal, select your storage account. 

1. From the left pane, select **Security + networking** > **Networking**.

1. On the **Public access** tab, select **Manage**.

   :::image type="content" source="media\search-indexer-howto-secure-access\manage-network-access.png" alt-text="Screenshot of the button to manage public network access in the Azure portal." border="true":::

1. Under **Public network access scope**, select **Enable from selected networks**.

   :::image type="content" source="media\search-indexer-howto-secure-access\enable-selected-networks.png" alt-text="Screenshot of the option to enable access from selected networks in the Azure portal." border="true":::

1. Add the IP addresses you obtained previously, and then select **Save**. You should have rules for the search service, the Azure portal (optional), and all of the IP addresses for the "AzureCognitiveSearch" service tag for your region.

   It can take five to ten minutes for the firewall rules to update. After the update, indexers can access storage account data behind the firewall.

## Supplement network security with token authentication

Firewalls and network security are a first step in preventing unauthorized access to data and operations. Authorization should be your next step. 

We recommend role-based access, where Microsoft Entra ID users and groups are assigned to roles that determine read and write access to your service. For a description of built-in roles and instructions for creating custom roles, see [Connect to Azure AI Search using role-based access controls](search-security-rbac.md).

If you don't need key-based authentication, we recommend that you disable API keys and use role assignments exclusively.

## Related content

- [Configure Azure Storage firewalls](/azure/storage/common/storage-network-security)
- [Configure an IP firewall for Azure Cosmos DB](/azure/cosmos-db/how-to-configure-firewall)
- [Configure IP firewall for Azure SQL Server](/azure/azure-sql/database/firewall-configure)
