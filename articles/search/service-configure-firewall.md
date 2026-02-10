---
title: Configure network access
titleSuffix: Azure AI Search
description: Configure IP control policies to restrict network access to your Azure AI Search service to specific IP addresses.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/29/2026
ms.custom:
  - ignite-2023
  - sfi-image-nochange
  - dev-focus
ai-usage: ai-assisted
---

# Configure network access and firewall rules for Azure AI Search

This article explains how to restrict network access to a search service's public endpoint. You can configure IP firewall rules to allow only specific IP addresses, ranges, or subnets, and optionally enable exceptions for trusted Azure services.

To block *all* data plane access to the public endpoint, use [private endpoints](service-create-private-endpoint.md) instead.

## Prerequisites

+ + [Azure AI Search service](search-create-service-portal.md) (Basic tier or higher). Firewall configuration isn't supported on the Free tier.

+ **Owner** or **Contributor** role on the search service resource.
+ You can also use the [Management REST API](/rest/api/searchmanagement/), [Azure PowerShell](/powershell/module/az.search), or the [Azure CLI](/cli/azure/search) instead of the Azure portal.

## Configure network access in the Azure portal

1. Sign in to Azure portal and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. Under **Settings**, select **Networking** on the leftmost pane. If you don't see this option, check your service tier. Networking options are available on the Basic tier and higher.

1. Choose **Selected IP addresses**. Avoid the **Disabled** option unless you're configuring a [private endpoint](service-create-private-endpoint.md).

   :::image type="content" source="media/service-configure-firewall/azure-portal-firewall.png" alt-text="Screenshot showing the network access options in the Azure portal." lightbox="media/service-configure-firewall/azure-portal-firewall.png" :::

1. Under **IP Firewall**, select **Add your client IP address**. This step creates an inbound rule for the public IP address of your personal device to Azure AI Search. See [Allow access from the Azure portal IP address](#allow-access-from-the-azure-portal-ip-address) for details.

   :::image type="content" source="media/service-configure-firewall/azure-portal-firewall-all.png" alt-text="Screenshot showing how to configure the IP firewall in the Azure portal." lightbox="media/service-configure-firewall/azure-portal-firewall-all.png":::

1. Add other client IP addresses for other devices and services that send requests to a search service.

   Specify IP addresses and ranges in the CIDR format. An example of CIDR notation is 8.8.8.0/24, which represents the IPs that range from 8.8.8.0 to 8.8.8.255.

   To get the public IP addresses of Azure services, see [Azure IP Ranges and Service Tags](https://www.microsoft.com/download/details.aspx?id=56519). If your search client is hosted within an Azure function, see [IP addresses in Azure Functions](/azure/azure-functions/ip-addresses).

1. Under **Exceptions**, select **Allow Azure services on the trusted services list to access this search service**. 
 
   :::image type="content" source="media/service-configure-firewall/exceptions.png" alt-text="Screenshot showing the exceptions checkbox on the network configuration page." lightbox="media/service-configure-firewall/exceptions.png":::

   The trusted service list includes:

   + `Microsoft.CognitiveServices` for Azure OpenAI and Foundry Tools
   + `Microsoft.MachineLearningServices` for Azure Machine Learning

   When you enable this exception, you take a dependency on Microsoft Entra ID authentication, managed identities, and role assignments. Any Foundry Tool or AML feature that has a valid role assignment on your search service can bypass the firewall. See [Grant access to trusted services](#grant-access-to-trusted-azure-services) for more details.

1. **Save** your changes.

After you enable the IP access control policy for your Azure AI Search service, all requests to the data plane from machines outside the allowed list of IP address ranges are rejected.

When requests originate from IP addresses that aren't in the allowed list, a generic **403 Forbidden** response is returned with no other details.

> [!IMPORTANT]
> It can take several minutes for changes to take effect. Wait at least 15 minutes before troubleshooting any problems related to network configuration.

## Allow access from the Azure portal IP address

The Azure portal uses your client IP address for a direct connection to Azure AI Search. If your client is in the allowed IP list, you can use almost all portal capabilities with no extra configuration required. However, there's an exception for the legacy Import data wizard when you *import from either Azure Cosmos DB or Azure SQL*. 

This scenario requires a separate IP address for the connection:

+ Identify the IP address used by the legacy wizard for this connection.

+ Add a firewall rule on [Azure Cosmos DB](/azure/cosmos-db/how-to-configure-firewall) or [Azure SQL](/azure/azure-sql/database/firewall-configure) to accept connections from the IP address.

This section explains how to get the IP address used by the wizard.

1. Open a command line tool

1. Perform `nslookup` (or `ping`) on:

   + `stamp2.ext.search.windows.net`, which is the domain of the traffic manager for the Azure public cloud.
   + `stamp2.ext.search.azure.us` for Azure Government cloud.

For nslookup, the IP address is visible in the "Non-authoritative answer" portion of the response. In the following example, the IP address that you should copy is `52.252.175.48`.

```bash
$ nslookup stamp2.ext.search.windows.net
Server:  ZenWiFi_ET8-0410
Address:  192.168.50.1

Non-authoritative answer:
Name:    azsyrie.northcentralus.cloudapp.azure.com
Address:  52.252.175.48
Aliases:  stamp2.ext.search.windows.net
          azs-ux-prod.trafficmanager.net
          azspncuux.management.search.windows.net
```

The IP address in the `Address` field (52.252.175.48 in this example) is the value to add to your firewall rules for legacy wizard connections.

**Reference:** [nslookup command](/windows-server/administration/windows-commands/nslookup)

> [!NOTE]
> You can use [ping](/windows-server/administration/windows-commands/ping) instead of nslookup for this task. For ping, the request times out, but the IP address is visible in the response. For example, in the message `"Pinging azsyrie.northcentralus.cloudapp.azure.com [52.252.175.48]"`, the IP address is `52.252.175.48`.
>
> If services run in different regions, they connect to different traffic managers. Regardless of the domain name, the IP address returned from the ping is the correct one to use when defining an inbound firewall rule for the Azure portal in your region.

## Grant access to trusted Azure services

Did you select the trusted services exception? If yes, your search service admits requests and responses from a trusted Azure resource without checking for an IP address. A trusted resource must have a managed identity (either system or user-assigned, but usually system). A trusted resource must have a role assignment on Azure AI Search that gives it permission to data and operations. 

The trusted service list for Azure AI Search includes:

+ `Microsoft.CognitiveServices` for Azure OpenAI and Foundry Tools
+ `Microsoft.MachineLearningServices` for Azure Machine Learning

Workflows for this network exception are requests originating from Microsoft Foundry or other AML features to Azure AI Search. The trusted services exception is typically for [Azure OpenAI On Your Data](/azure/ai-services/openai/concepts/use-your-data) scenarios for retrieval augmented generation (RAG) and playground environments.

### Trusted resources must have a managed identity

To set up managed identities for Azure OpenAI and Azure Machine Learning:

+ [How to configure Azure OpenAI in Foundry Models with managed identities](/azure/ai-services/openai/how-to/managed-identity)
+ [How to set up authentication between Azure Machine Learning and other services](/azure/machine-learning/how-to-identity-based-service-authentication).

To set up a managed identity for a Foundry resource:

1. [Find your Foundry resource](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/microsoft.cognitiveServices%2Faccounts).

1. From the left pane, select **Resource management** > **Identity**.

1. Set **System assigned** to **On**.

### Trusted resources must have a role assignment

Once your Azure resource has a managed identity, [assign roles on Azure AI Search](search-security-rbac-client-code.md) to grant permissions to data and operations. 

The trusted services are used for vectorization workloads: generating vectors from text and image content, and sending payloads back to the search service for query execution or indexing. Connections from a trusted service are used to deliver payloads to Azure AI search.

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).
1. On the leftmost pane, under **Access control (IAM)**, select **Identity**.
1. Select **Add** and then select **Add role assignment**.
1. On the **Roles** page:

   + Select **Search Index Data Contributor** to load a search index with vectors generated by an embedding model. Choose this role if you intend to use integrated vectorization during indexing.
   + Or, select **Search Index Data Reader** to provide queries containing a vector generated by an embedding model at query time. The embedding used in a query isn't written to an index, so no write permissions are required.

1. Select **Next**.
1. On the **Members** page, select **Managed identity** and **Select members**.
1. Filter by system-managed identity and then select the managed identity of your Foundry resource.

> [!NOTE]
> This article covers the trusted exception for admitting requests to your search service, but Azure AI Search is itself on the trusted services list of other Azure resources. Specifically, you can use the trusted service exception for [connections from Azure AI Search to Azure Storage](search-indexer-howto-access-trusted-service-exception.md).

## Limitations and considerations

Consider the following when configuring network access:

+ Some workflows require access to a public endpoint. Specifically, the [**Import data wizard**](search-import-data-portal.md) in the Azure portal connects to built-in (hosted) sample data and embedding models over a public endpoint. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

+ If you're in early stages of proof-of-concept testing with sample data, you might want to defer network access controls until you actually need them.

+ Network rules are scoped to data plane operations against the search service's public endpoint (creating or querying indexes, and all other actions described by the [Search REST APIs](/rest/api/searchservice/)).

+ For control plane operations that target service administration, refer to the [network protections supported by Azure Resource Manager](/security/benchmark/azure/baselines/azure-resource-manager-security-baseline).

## Next steps

Once a request is allowed through the firewall, it must be authenticated and authorized. You have two options:

+ [Key-based authentication](search-security-api-keys.md), where an admin or query API key is provided on the request. This option is the default.

+ [Role-based access control](search-security-rbac.md) using Microsoft Entra ID, where the caller is a member of a security role on a search service. This is the most secure option. It uses Microsoft Entra ID for authentication and role assignments on Azure AI Search for permissions to data and operations.

> [!div class="nextstepaction"]
> [Enable RBAC on your search service](search-security-enable-roles.md)
