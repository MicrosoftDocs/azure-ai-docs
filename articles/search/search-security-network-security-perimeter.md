---
title: Add a Search Service to a Network Security Perimeter
titleSuffix: Azure AI Search
description: Learn how to add an Azure AI Search service to a network security perimeter for a secure connection.
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 01/16/2026
---

# Add a search service to a network security perimeter

A [network security perimeter](/azure/private-link/network-security-perimeter-concepts) is a logical network boundary around your platform as a service (PaaS) resources that you deploy outside of a virtual network. It establishes a perimeter for controlling public network access to resources like Azure AI Search, [Azure Storage](/azure/storage/common/storage-network-security-perimeter), and [Azure OpenAI](/azure/ai-foundry/openai/how-to/network-security-perimeter).

This article explains how to join an Azure AI Search service to a network security perimeter to control network access to your search service. By joining a network security perimeter, you can:

* Log all access to your search service in context with other Azure resources in the same perimeter.
* Block any data exfiltration from a search service to other services outside the perimeter.
* Allow access to your search service by using the inbound and outbound access capabilities of the network security perimeter.

You can add a search service to a network security perimeter in the Azure portal, as described in this article. Alternatively, you can use the [Azure Virtual Network Manager REST API](/rest/api/networkmanager/) to join a search service, and use the [Search Management REST APIs](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2025-05-01&preserve-view=true) to view and synchronize the configuration settings.

## Prerequisites

* An existing network security perimeter. You can [create one to associate with your search service](/azure/private-link/create-network-security-perimeter-portal).

* [Azure AI Search](search-create-service-portal.md), any billable tier, in any region.

## Limitations

* For search services within a network security perimeter, indexers must use a [system or user-assigned managed identity](search-how-to-managed-identities.md) and have a role assignment that permits read access to data sources.

* Supported indexer data sources are currently limited to [Azure Blob Storage](search-how-to-index-azure-blob-storage.md), [Azure Cosmos DB for NoSQL](./search-how-to-index-cosmosdb-sql.md), and [Azure SQL Database](search-how-to-index-sql-database.md).

* Currently, within the perimeter, indexer connections to Azure PaaS for data retrieval is the primary use case. For outbound skills-driven API calls to Foundry Tools, Azure OpenAI, or the Microsoft Foundry model catalog, or for inbound calls from Foundry for "chat with your data" scenarios, you must [configure inbound and outbound rules](#add-an-inbound-access-rule) to allow the requests through the perimeter. If you require private connections for [structure-aware chunking](search-how-to-semantic-chunking.md) and vectorization, you should [create a shared private link](search-indexer-howto-access-private.md) and a private network.

## Assign a search service to a network security perimeter

By using Azure Network Security Perimeter, administrators can define a logical network isolation boundary for PaaS resources, such as Azure Storage and Azure SQL Database, that are deployed outside virtual networks. It restricts communication to resources within the perimeter, and it allows non-perimeter public traffic through inbound and outbound access rules.

You can add Azure AI Search to a network security perimeter so that all indexing and query requests occur within the security boundary.

1. In the Azure portal, find the network security perimeter service for your subscription.

1. From the left pane, select **Settings** > **Associated resources**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-resources.png" alt-text="Screenshot of the network security perimeter left-hand menu." border="true":::

1. Select **Add** > **Associate resources with an existing profile**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-associate-resource.png" alt-text="Screenshot of network security perimeter associate resource button." border="true":::

1. Select the profile you created when you created the network security perimeter for **Profile**.

1. Select **Add**, and then select your search service.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-associate-select-resource.png" alt-text="Screenshot of network security perimeter associate resource button with the select resource screen." border="true":::

1. Select **Associate** in the lower-left corner to create the association.

<a id="network-security-perimeter-access-modes"></a>

### Network security perimeter access modes

Network security perimeter supports two different access modes for associated resources:

| Mode | Description |
|--|--|
| Learning mode | This is the default access mode. In learning mode, network security perimeter logs all traffic to the search service that would be denied if the perimeter was in enforced mode. This access mode allows network administrators to understand the existing access patterns of the search service before implementing enforcement of access rules. |
| Enforced mode | In enforced mode, network security perimeter logs and denies all traffic that isn't explicitly allowed by access rules. |

#### Network security perimeter and search service networking settings

The `publicNetworkAccess` setting determines search service association with a network security perimeter.

* In learning mode, the `publicNetworkAccess` setting controls public access to the resource.

* In enforced mode, the network security perimeter rules override the `publicNetworkAccess` setting. For example, if a search service with a `publicNetworkAccess` setting of `enabled` is associated with a network security perimeter in enforced mode, access to the search service is still controlled by network security perimeter access rules.

#### Change the network security perimeter access mode

1. Go to your network security perimeter resource in the Azure portal.

1. From the left pane, select **Settings** > **Associated resources**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-resources.png" alt-text="Screenshot of the network security perimeter left-hand menu." border="true":::

1. Find your search service in the table.

1. Select the three dots at the end of the row, and then select **Change access mode**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-resource-change-access-mode.png" alt-text="Screenshot of the change access mode button in the network security perimeter portal." border="true":::

1. Select your desired access mode, and then select **Apply**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-resource-change-access-mode-apply.png" alt-text="Screenshot of the change access mode button in the network security perimeter portal with the access modes displayed." border="true":::

## Enable logging network access

1. Go to your network security perimeter resource in the Azure portal.

1. From the left pane, select **Monitoring** > **Diagnostic settings**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-diagnostic-settings.png" alt-text="Screenshot of left-hand menu in the network security perimeter portal." border="true":::

1. Select **Add diagnostic setting**.

1. Enter any name, such as "diagnostic," for **Diagnostic setting name**.

1. Under **Logs**, select **allLogs**. **allLogs** ensures all inbound and outbound network access to resources in your network security perimeter is logged.

1. Under **Destination details**, select **Archive to a storage account** or **Send to Log Analytics workspace**. The storage account must be in the same region as the network security perimeter. You can either use an existing storage account or create a new one. A Log Analytics workspace can be in a different region than the one used by the network security perimeter. You can also select any of the other applicable destinations.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-diagnostic-settings-filled-out.png" alt-text="Screenshot of a filled out diagnostic settings in the network security perimeter portal." border="true":::

1. Select **Save** to create the diagnostic setting and start logging network access.

### Reading network access logs

#### Log Analytics workspace

The `network-security-perimeterAccessLogs` table contains all the logs for every log category, such as `network-security-perimeterPublicInboundResourceRulesAllowed`. Each log contains a record of the network security perimeter network access that matches the log category.

Here's an example of the `network-security-perimeterPublicInboundResourceRulesAllowed` log format:

| Column Name | Meaning | Example Value |
|--|--|--|
| ResultDescription | Name of the network access operation. | POST /indexes/my-index/docs/search |
| Profile | Which network security perimeter the search service was associated with. | defaultProfile |
| ServiceResourceId | Resource ID of the search service. | `search-service-resource-id` |
| Matched Rule | JSON description of the rule that the log matched. | `{ "accessRule": "IP firewall" }` |
| SourceIPAddress | Source IP of the inbound network access, if applicable. | 1.1.1.1 |
| AccessRuleVersion | Version of the network-security-perimeter access rules used to enforce the network access rules. | 0 |

#### Storage Account

The storage account has containers for every log category, such as `insights-logs-network-security-perimeterpublicinboundperimeterrulesallowed`. The folder structure inside the container matches the resource ID of the network security perimeter and the time the logs were taken. Each line on the JSON log file contains a record of the network security perimeter network access that matches the log category.

For example, the inbound perimeter rules allowed category log uses the following format:

```json
"properties": {
    "ServiceResourceId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/network-security-perimeter/providers/Microsoft.Search/searchServices/network-security-perimeter-search",
    "Profile": "defaultProfile",
    "MatchedRule": {
        "AccessRule": "myaccessrule"
    },
    "Source": {
        "IpAddress": "255.255.255.255",
    }
}
```

## Add an access rule for your search service

A network security perimeter profile specifies rules that allow or deny access through the perimeter.

Within the perimeter, all resources have mutual access at the network level. You must still set up authentication and authorization, but at the network level, connection requests from inside the perimeter are accepted.

For resources outside of the network security perimeter, you must specify inbound and outbound access rules. Inbound rules specify which connections to allow in, and outbound rules specify which requests are allowed out.

A search service accepts inbound requests from apps like the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), Azure Machine Learning prompt flow, and any app that sends indexing or query requests. A search service sends outbound requests during indexer-based indexing and skillset execution. This section explains how to set up inbound and outbound access rules for Azure AI Search scenarios.

   > [!NOTE]
   > When you authenticate access by using [managed identities and role assignments](/entra/identity/managed-identities-azure-resources/overview), any service associated with a network security perimeter implicitly allows inbound and outbound access to any other service associated with the same network security perimeter. You only need to create access rules when you allow access outside of the network security perimeter or for access authenticated by using API keys.

### Add an inbound access rule

Inbound access rules can allow the internet and resources outside the perimeter to connect with resources inside the perimeter.

Network security perimeter supports two types of inbound access rules:

* IP address ranges. IP addresses or ranges must be in the Classless Inter-Domain Routing (CIDR) format. An example of CIDR notation is 192.0.2.0/24, which represents the IPs that range from 192.0.2.0 to 192.0.2.255. This type of rule allows inbound requests from any IP address within the range.

* Subscriptions. This type of rule allows inbound access authenticated by using any managed identity from the subscription.

To add an inbound access rule in the Azure portal:

1. Go to your network security perimeter resource in the Azure portal.

1. From the left pane, select **Settings** > **Profiles**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-profiles.png" alt-text="Screenshot of the left hand menu with profiles selected." border="true":::

1. Select the profile you're using with your network security perimeter.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-select-profile.png" alt-text="Screenshot of selecting the profile from network security perimeter." border="true":::

1. From the left pane, select **Settings** > **Inbound access rules**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-inbound-access-rules.png" alt-text="Screenshot of the left hand menu with inbound access rules selected." border="true":::

1. Select **Add**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-access-rule.png" alt-text="Screenshot of add inbound network security perimeter access rule button." border="true":::

1. Enter or select the following values:

   | Setting | Value |
   | ------- | ----- |
   | Rule name | The name for the inbound access rule, such as `MyInboundAccessRule`. |
   | Source type | Valid values are **IP address ranges** or **Subscriptions**. |
   | Allowed sources | If you selected **IP address ranges**, enter the IP address range in CIDR format that you want to allow inbound access from. Azure IP ranges are available at [this link](https://www.microsoft.com/download/details.aspx?id=56519). If you selected **Subscriptions**, use the subscription you want to allow inbound access from. |

1. Select **Add** to create the inbound access rule.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-inbound-access-rule-filled-out.png" alt-text="Screenshot of add inbound network security perimeter access rule screen filled out." border="true":::

### Add an outbound access rule

A search service makes outbound calls during indexer-based indexing and skillset execution. If your indexer data sources, Foundry Tools, or custom skill logic is outside of the network security perimeter, you should create an outbound access rule that allows your search service to make the connection.

Currently, Azure AI Search can only connect to Azure Storage or Azure Cosmos DB within the security perimeter. If your indexers use other data sources, you need an outbound access rule to support that connection.

The network security perimeter supports outbound access rules based on the Fully Qualified Domain Name (FQDN) of the destination. For example, you can allow outbound access from any service associated with your network security perimeter to an FQDN such as `mystorageaccount.blob.core.windows.net`.

To add an outbound access rule in the Azure portal:

1. Go to your network security perimeter resource in the Azure portal.

1. From the left pane, select **Settings** > **Profiles**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-profiles.png" alt-text="Screenshot of the left hand menu with profiles option selected." border="true":::

1. Select the profile you're using with your network security perimeter.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-select-profile.png" alt-text="Screenshot of selecting the profile from network security perimeter." border="true":::

1. From the left pane, select **Settings** > **Outbound access rules**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-select-outbound-access-rules.png" alt-text="Screenshot of selecting the outbound access rules in the left-hand menu." border="true":::

1. Select **Add**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-outbound-access-rule.png" alt-text="Screenshot of adding the outbound access rule in network security perimeter." border="true":::

1. Enter or select the following values:

   | Setting | Value |
   | ------- | ----- |
   | Rule name | The name for the outbound access rule, such as "MyOutboundAccessRule." |
   | Destination type | Leave as **FQDN**. |
   | Allowed destinations | Enter a comma-separated list of FQDNs you want to allow outbound access to. |

1. Select **Add** to create the outbound access rule.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-outbound-access-rule-filled-out.png" alt-text="Screenshot of adding the outbound access rule in network security perimeter with filled out options." border="true":::

## Test your connection through network security perimeter

To test your connection through network security perimeter, you need access to a web browser, either on a local computer with an internet connection or an Azure VM.

1. Change your network security perimeter association to [enforced mode](#network-security-perimeter-access-modes) to start enforcing network security perimeter requirements for network access to your search service.

1. Decide if you want to use a local computer or an Azure VM.
   1. If you're using a local computer, you need to know your public IP address.
   1. If you're using an Azure VM, you can either use [private link](/azure/private-link/private-link-overview) or [check the IP address using the Azure portal](/azure/virtual-network/ip-services/virtual-network-network-interface-addresses).

1. Using the IP address, create an [inbound access rule](#add-an-inbound-access-rule) for that IP address to allow access. You can skip this step if you're using private link.

1. Finally, try navigating to the search service in the Azure portal. If you can view the indexes successfully, then the network security perimeter is configured correctly.

## View and manage network security perimeter configuration

Use the [Network Security Perimeter Configuration REST APIs](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2025-05-01&preserve-view=true) to review and reconcile perimeter configurations.

Be sure to use the 2025-05-01 REST API version, which is the latest stable version of the Search Management REST APIs. For more information, see [Manage your Azure AI Search service using REST APIs](search-manage-rest.md).

## Related content

* [Use Azure role-based access control in Azure AI Search](search-security-rbac.md)
