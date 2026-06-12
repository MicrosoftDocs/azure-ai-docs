---
title: Add a Search Service to a Network Security Perimeter
description: Learn how to add an Azure AI Search service to a network security perimeter for a secure connection.
ms.date: 06/08/2026
ms.service: azure-ai-search
ms.topic: how-to
ms.custom:
  - ignite-2024
ai-usage: ai-assisted
---

# Add a search service to a network security perimeter

A [network security perimeter](/azure/private-link/network-security-perimeter-concepts) is a logical network boundary around your platform as a service (PaaS) resources that you deploy outside of a virtual network. It establishes a perimeter for controlling public network access to resources like Azure AI Search, [Azure Storage](/azure/storage/common/storage-network-security-perimeter), and [Azure OpenAI in Microsoft Foundry Models](/azure/ai-foundry/openai/how-to/network-security-perimeter).

This article explains how to join an Azure AI Search service to a network security perimeter to control network access to your search service. By joining a network security perimeter, you can:

- Log all access to your search service in context with other Azure resources in the same perimeter.
- Block any data exfiltration from a search service to other services outside the perimeter.
- Allow access to your search service by using the inbound and outbound access capabilities of the network security perimeter.

You can add a search service to a network security perimeter in the Azure portal, as described in this article. Alternatively, use the [Search Management REST APIs](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2025-05-01&preserve-view=true) to view and synchronize the configuration settings.

## Prerequisites

- An existing network security perimeter. You can [create one to associate with your search service](/azure/private-link/create-network-security-perimeter-portal).

- [Azure AI Search](search-create-service-portal.md), any billable tier, in any region.

- Azure role assignments: **Network Security Perimeter Contributor** on the perimeter (or its resource group or subscription) to create and manage the perimeter, profiles, access rules, and associations. **Search Service Contributor** (or **Contributor**) on the search service to associate it with a perimeter. For more information, see [What is a network security perimeter?](/azure/private-link/network-security-perimeter-concepts).

- If you plan to use indexers, configure the search service with a [system- or user-assigned managed identity](search-how-to-managed-identities.md) and assign the identity an appropriate data-plane role on each data source.

## Limitations

- Supported indexer data sources are currently limited to [Azure Blob Storage](search-how-to-index-azure-blob-storage.md), [Azure Cosmos DB for NoSQL](search-how-to-index-cosmosdb-sql.md), and [Azure SQL Database](search-how-to-index-sql-database.md).

- Indexer connections to Azure PaaS for data retrieval are the primary intra-perimeter use case. For other traffic, [configure inbound and outbound rules](#add-an-inbound-access-rule). For outbound calls to Microsoft Foundry resources, see [Outbound access to Microsoft Foundry resources](#outbound-access-to-microsoft-foundry-resources). [Shared private link](search-indexer-howto-access-private.md) is an alternative for specific resource types.

## Outbound access to Microsoft Foundry resources

A network security perimeter that includes both your search service and a [Microsoft Foundry resource](/azure/foundry/how-to/add-foundry-to-network-security-perimeter) provides a private channel for outbound calls between them. Because the perimeter operates at the resource and network layer, every search service feature that calls the Foundry resource uses the same allowed path, including:

- All skills that call a Foundry resource, such as the [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md), [GenAI prompt skill](cognitive-search-skill-genai-prompt.md), [Content Understanding skill](cognitive-search-skill-content-understanding.md), and other [Foundry resource skills](cognitive-search-predefined-skills.md#foundry-resource) for AI enrichment and billing.

- The [Azure OpenAI vectorizer](vector-search-vectorizer-azure-open-ai.md) at query time during [integrated vectorization](vector-search-integrated-vectorization.md).

- [Agentic retrieval](agentic-retrieval-overview.md) calls from a knowledge agent to a Foundry model deployment.

To enable the private channel:

1. Add both your search service and the Foundry resource to the same network security perimeter, or to perimeters that allow communication between them.

1. If both resources are in the same perimeter and the search service authenticates to the Foundry resource by using a managed identity, you don't need to add an outbound rule. Intra-perimeter traffic is allowed implicitly. If the resources are in different perimeters, or the search service authenticates with API keys, add an outbound FQDN access rule on the perimeter associated with your search service that targets the Foundry resource's hostname. For guidance on the Foundry side of the configuration, see [Add Microsoft Foundry to a network security perimeter](/azure/foundry/how-to/add-foundry-to-network-security-perimeter).

1. Validate access in two stages:

   1. With the perimeter in learning mode, run a skillset, vectorizer query, or agentic retrieval call that invokes the Foundry resource. Review the perimeter logs to confirm the expected access path.

   1. Switch to enforced mode and rerun the same operation. Confirm success in indexer execution history and in the perimeter's outbound allow logs.

Network security perimeter (NSP) support for `Microsoft.CognitiveServices` resources of kind `AIServices` (Microsoft Foundry) is generally available. NSP support for resources of kind `OpenAI` (Azure OpenAI Service) is in public preview. For the current support list, see [Onboarded private link resources](/azure/private-link/network-security-perimeter-concepts#onboarded-private-link-resources).

Shared private link to the Foundry resource remains supported as an alternative.

## Assign a search service to a network security perimeter

Associate your search service with a perimeter so that all indexing and query traffic is governed by perimeter rules.

> [!TIP]
> For automation, use the [Search Management REST APIs](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2025-05-01&preserve-view=true) instead of the portal. For more information, see [Manage your Azure AI Search service using REST APIs](search-manage-rest.md).

1. In the Azure portal, find the network security perimeter service for your subscription.

1. From the left pane, select **Settings** > **Associated resources**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-resources.png" alt-text="Screenshot of the network security perimeter left-hand menu." border="true":::

1. Select **Add** > **Associate resources with an existing profile**.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-associate-resource.png" alt-text="Screenshot of network security perimeter associate resource button." border="true":::

1. Select the profile you created when you created the network security perimeter for **Profile**.

1. Select **Add**, and then select your search service.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-associate-select-resource.png" alt-text="Screenshot of network security perimeter associate resource button with the select resource screen." border="true":::

1. Select **Associate** in the lower-left corner to create the association.

### Remove a search service from a network security perimeter

To disassociate a search service from a perimeter:

1. Go to your network security perimeter resource in the Azure portal.

1. From the left pane, select **Settings** > **Associated resources**.

1. Find your search service in the table, select the three dots at the end of the row, and then select **Remove association**.

1. Confirm the removal. After the association is removed, perimeter rules no longer apply to the search service, and the `publicNetworkAccess` setting on the search service again controls inbound traffic.

<a id="network-security-perimeter-access-modes"></a>

### Network security perimeter access modes

Network security perimeter supports two different access modes for associated resources:

| Mode | Description |
| --- | --- |
| Learning mode | This is the default access mode. In learning mode, network security perimeter logs all traffic to the search service that would be denied if the perimeter is in enforced mode. This access mode allows network administrators to understand the existing access patterns of the search service before implementing enforcement of access rules. |
| Enforced mode | In enforced mode, network security perimeter logs and denies all traffic that isn't explicitly allowed by access rules. |

#### Network security perimeter and search service networking settings

The `publicNetworkAccess` setting determines search service association with a network security perimeter.

- In learning mode, the `publicNetworkAccess` setting controls public access to the resource.

- In enforced mode, the network security perimeter rules override the `publicNetworkAccess` setting. For example, if a search service with a `publicNetworkAccess` setting of `enabled` is associated with a network security perimeter in enforced mode, access to the search service is still controlled by network security perimeter access rules.

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

1. Enter any name, such as `diagnostic`, for **Diagnostic setting name**.

1. Under **Logs**, select **allLogs**. **allLogs** ensures all inbound and outbound network access to resources in your network security perimeter is logged.

1. Under **Destination details**, select **Archive to a storage account** or **Send to Log Analytics workspace**. The storage account must be in the same region as the network security perimeter. You can either use an existing storage account or create a new one. A Log Analytics workspace can be in a different region than the one used by the network security perimeter. You can also select any of the other applicable destinations.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-diagnostic-settings-filled-out.png" alt-text="Screenshot of a filled out diagnostic settings in the network security perimeter portal." border="true":::

1. Select **Save** to create the diagnostic setting and start logging network access.

1. To verify logging is active, generate traffic to the search service (for example, run a query). Within about 10 minutes, query the `NSPAccessLogs` table in Log Analytics or check the corresponding `insights-logs-*` container in the storage account.

### Read network access logs

Network security perimeter logs are delivered to the destinations you selected in **Diagnostic settings**. The most common destinations are a Log Analytics workspace and a storage account.

#### Log Analytics workspace

The `NSPAccessLogs` table contains all the logs for every log category, such as `NspPublicInboundPerimeterRulesAllowed`. Each log contains a record of the network security perimeter network access that matches the log category.

Here's an example of the `NspPublicInboundPerimeterRulesAllowed` log format:

| Column name | Meaning | Example value |
| --- | --- | --- |
| ResultDescription | Name of the network access operation. | POST /indexes/my-index/docs/search |
| Profile | Which network security perimeter the search service was associated with. | defaultProfile |
| ServiceResourceId | Resource ID of the search service. | `search-service-resource-id` |
| Matched Rule | JSON description of the rule that the log matched. | `{ "accessRule": "IP firewall" }` |
| SourceIPAddress | Source IP of the inbound network access, if applicable. | 192.0.2.1 |
| AccessRuleVersion | Version of the network security perimeter access rules used to enforce the network access rules. | 0 |

#### Storage account

The storage account has containers for every log category, such as `insights-logs-nsppublicinboundperimeterrulesallowed`. The folder structure inside the container matches the resource ID of the network security perimeter and the time the logs were taken. Each line on the JSON log file contains a record of the network security perimeter network access that matches the log category.

For example, the inbound perimeter rules allowed category log uses the following format:

```json
"properties": {
    "ServiceResourceId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/network-security-perimeter/providers/Microsoft.Search/searchServices/network-security-perimeter-search",
    "Profile": "defaultProfile",
    "MatchedRule": {
        "AccessRule": "myaccessrule"
    },
    "Source": {
        "IpAddress": "192.0.2.1",
    }
}
```

## Add an access rule for your search service

A network security perimeter profile specifies rules that allow or deny access through the perimeter.

Within the perimeter, all resources have mutual access at the network level. You must still set up authentication and authorization, but at the network level, connection requests from inside the perimeter are accepted.

For resources outside of the network security perimeter, you must specify inbound and outbound access rules. Inbound rules specify which connections to allow in, and outbound rules specify which requests are allowed out.

A search service accepts inbound requests from apps like the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) and any app that sends indexing or query requests. A search service sends outbound requests during indexer-based indexing and skillset execution. This section explains how to set up inbound and outbound access rules for Azure AI Search scenarios.

> [!NOTE]
> When the search service authenticates by using a managed identity and Microsoft Entra-based [role assignments](/entra/identity/managed-identities-azure-resources/overview), traffic between resources in the same network security perimeter is allowed implicitly at the network level. If the search service authenticates with API keys, the perimeter can't identify the traffic as intra-perimeter, so you must add explicit inbound and outbound access rules even when both resources are in the same perimeter.

### Add an inbound access rule

Inbound access rules can allow the internet and resources outside the perimeter to connect with resources inside the perimeter.

Network security perimeter supports two types of inbound access rules:

- IP address ranges. IP addresses or ranges must be in the Classless Inter-Domain Routing (CIDR) format. An example of CIDR notation is 192.0.2.0/24, which represents the IPs that range from 192.0.2.0 to 192.0.2.255. This type of rule allows inbound requests from any IP address within the range.

- Subscriptions. This type of rule allows inbound access authenticated by using any managed identity from the subscription. The rule controls the network path only; the caller still needs an Azure RBAC role assignment on the search service.

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
   | Allowed sources | If you selected **IP address ranges**, enter the IP address range in CIDR format that you want to allow inbound access from. Download the [Azure IP Ranges and Service Tags file](https://www.microsoft.com/download/details.aspx?id=56519). If you selected **Subscriptions**, use the subscription you want to allow inbound access from. |

1. Select **Add** to create the inbound access rule.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-inbound-access-rule-filled-out.png" alt-text="Screenshot of add inbound network security perimeter access rule screen filled out." border="true":::

1. To verify the rule, switch the association to enforced mode in a test profile. Confirm matching requests appear in the `NspPublicInboundPerimeterRulesAllowed` log category and non-matching requests appear in the `NspPublicInboundPerimeterRulesDenied` category.

### Add an outbound access rule

A search service makes outbound calls during indexer-based indexing and skillset execution. If your indexer data sources, an attached Microsoft Foundry resource for [Foundry Tools billing skills](cognitive-search-predefined-skills.md#foundry-resource), or custom skill logic is outside the network security perimeter, create an outbound access rule that allows your search service to make the connection.

Within the security perimeter, indexers can connect to Azure Blob Storage, Azure Cosmos DB for NoSQL, and Azure SQL Database. If your indexers use other data sources, you need an outbound access rule to support that connection.

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
   | Rule name | The name for the outbound access rule, such as `MyOutboundAccessRule`. |
   | Destination type | Leave as **FQDN**. |
   | Allowed destinations | Enter a comma-separated list of FQDNs you want to allow outbound access to. |

1. Select **Add** to create the outbound access rule.

   :::image type="content" source="media/search-security-network-security-perimeter/portal-network-security-perimeter-add-outbound-access-rule-filled-out.png" alt-text="Screenshot of adding the outbound access rule in network security perimeter with filled out options." border="true":::

1. To verify the rule, switch the association to enforced mode in a test profile. Confirm matching outbound requests appear in the `NspPublicOutboundPerimeterRulesAllowed` log category.

## Test your connection through network security perimeter

To test your connection through network security perimeter, you need access to a web browser, either on a local computer with an internet connection or an Azure VM.

1. Change your network security perimeter association to [enforced mode](#network-security-perimeter-access-modes) to start enforcing network security perimeter requirements for network access to your search service.

1. Choose a client:

   1. For a local computer, get your public IP address.

   1. For an Azure VM, use [private link](/azure/private-link/private-link-overview) or [find the IP address in the Azure portal](/azure/virtual-network/ip-services/virtual-network-network-interface-addresses).

1. Create an [inbound access rule](#add-an-inbound-access-rule) for that IP address to allow access.

1. In the Azure portal, open your search service and view its indexes.

   - **Expected success:** The index list loads and you can run a test query. The inbound IP rule is working.

   - **If you see a 403 or "Public network access is disabled" error:** Your client IP or the Azure portal isn't covered by an inbound rule. Check the [inbound access rules](#add-an-inbound-access-rule).

## Troubleshoot common issues

| Symptom | Likely cause | Mitigation |
| --- | --- | --- |
| Indexer fails after switching to enforced mode. | The search service identity lacks a data-plane role on the data source, or the data source isn't supported within the perimeter. | Confirm the search service uses a [managed identity](search-how-to-managed-identities.md) and has the required role on the data source. For unsupported data sources, add an [outbound access rule](#add-an-outbound-access-rule). |
| Skill, vectorizer, or agentic retrieval calls to a Foundry resource are denied. | The Foundry resource is in a different perimeter, or the search service authenticates with API keys, so the channel isn't implicit. | Add both resources to the same perimeter and use managed identity, or add an outbound FQDN rule that targets the Foundry resource's hostname. For more information, see [Outbound access to Microsoft Foundry resources](#outbound-access-to-microsoft-foundry-resources). |
| Diagnostic logs don't appear in Log Analytics or Storage. | Ingestion latency, or the storage account isn't in the same region as the perimeter. | Wait up to 10 minutes after generating traffic, then query the `NSPAccessLogs` table or check the matching `insights-logs-*` storage container. Verify the storage account region. |
| Portal access to the search service is denied after enforcement. | Your client IP isn't covered by any inbound rule. | Add an [inbound access rule](#add-an-inbound-access-rule) for your client IP, or revert to learning mode while you finish configuration. |

## View and manage network security perimeter configuration

Use the [Network Security Perimeter Configuration REST APIs](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2025-05-01&preserve-view=true) to review and reconcile perimeter configurations on a search service.

For example, list the current perimeter configurations on a search service:

```azurecli
az rest --method get \
  --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service-name>/networkSecurityPerimeterConfigurations?api-version=2025-05-01"
```

If the configuration is out of sync with the perimeter, trigger a reconcile:

```azurecli
az rest --method post \
  --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service-name>/networkSecurityPerimeterConfigurations/<association-name>/reconcile?api-version=2025-05-01"
```

Use the latest stable version of the Search Management REST APIs. For more information, see [Manage your Azure AI Search service using REST APIs](search-manage-rest.md).

## Related content

- [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts)
- [Configure a search service to connect using a managed identity](search-how-to-managed-identities.md)
- [Make outbound connections through a shared private link](search-indexer-howto-access-private.md)
- [Add Microsoft Foundry to a network security perimeter](/azure/foundry/how-to/add-foundry-to-network-security-perimeter)
