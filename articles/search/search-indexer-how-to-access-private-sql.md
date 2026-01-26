---
title: Connect to SQL Managed Instance
titleSuffix: Azure AI Search
description: Configure an indexer connection to access content in an Azure SQL Managed instance that's protected through a private endpoint.
author: mattgotteiner
ms.author: magottei
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/23/2026
ms.update-cycle: 365-days
ms.custom: sfi-ropc-nochange
---

# Create a shared private link for a SQL managed instance from Azure AI Search

This article explains how to configure an indexer in Azure AI Search for a private connection to a SQL managed instance that runs within a virtual network. The private connection is through a [shared private link](search-indexer-howto-access-private.md) and Azure Private Link.

On a private connection to a managed instance, the fully qualified domain name (FQDN) of the instance must include the [DNS Zone](/azure/azure-sql/managed-instance/connectivity-architecture-overview#virtual-cluster-connectivity-architecture). Currently, only the Azure AI Search Management REST API provides a `dnsZonePrefix` parameter for accepting the DNS zone specification.

Although you can call the Management REST API directly, it's easier to use the Azure CLI `az rest` module to send Management REST API calls from a command line. This article uses the Azure CLI with REST to set up the private link.

> [!NOTE]
> This article refers to Azure portal for obtaining properties and confirming steps. However, when creating the shared private link for SQL Managed Instance, make sure you're using the REST API. Although the Networking tab lists `Microsoft.Sql/managedInstances` as an option, the Azure portal doesn't currently support the extended URL format used by SQL Managed Instance.

## Prerequisites

+ [Azure CLI](/cli/azure/install-azure-cli)

+ Azure AI Search, Basic or higher. If you're using [AI enrichment](cognitive-search-concept-intro.md) and skillsets, use Standard 2 (S2) or higher. See [Service limits](search-limits-quotas-capacity.md#shared-private-link-resource-limits) for details.

+ Azure SQL Managed Instance, configured to run in a virtual network.

+ You should have a minimum of Contributor permissions on both Azure AI Search and SQL Managed Instance.

+ Azure SQL Managed Instance connection string. Managed identity isn't currently supported with shared private link. Your connection string must include a user name and password.

> [!NOTE]
> Shared private links are billable through [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link/) and charges are invoiced based on usage.

## 1 - Retrieve connection information

In this section, get the DNS zone from the host name and a connection string.

1. In Azure portal, find the SQL managed instance object.

1. On the **Overview** tab, locate the Host property. Copy the *DNS zone* portion of the FQDN for the next step. The DNS zone is part of the domain name of the SQL Managed Instance. For example, if the FQDN of the SQL Managed Instance is `my-sql-managed-instance.a1b22c333d44.database.windows.net`, the DNS zone is `a1b22c333d44`.

1. On the **Connection strings** tab, copy the ADO.NET connection string for a later step. It's needed for the data source connection when testing the private connection.

For more information about connection properties, see [Create an Azure SQL Managed Instance](/azure/azure-sql/managed-instance/instance-create-quickstart?view=azuresql#retrieve-connection-details-to-sql-managed-instance&preserve-view=true).

## 2 - Create the body of the request

1. Using a text editor, create the JSON for the shared private link.

   ```json
   {
       "name": "{{shared-private-link-name}}",
       "properties": {
           "privateLinkResourceId": "/subscriptions/{{target-resource-subscription-ID}}/resourceGroups/{{target-resource-rg}}/providers/Microsoft.Sql/managedInstances/{{target-resource-name}}",
           "dnsZonePrefix": "a1b22c333d44",
           "groupId": "managedInstance",
           "requestMessage": "please approve"
       }
   }
   ```

   Provide a meaningful name for the shared private link. The shared private link appears alongside other private endpoints. A name like "shared-private-link-for-search" can remind you how it's used.

   Paste in the DNS zone name in "dnsZonePrefix" that you retrieved in an earlier step.

   Edit the "privateLinkResourceId", substitute valid for values for the placeholders. Provide a valid subscription ID, resource group name, and managed instance name.

1. Save the file locally as *create-pe.json* (or use another name, remembering to update the Azure CLI syntax in the next step).

1. In the Azure CLI, type `dir` to note the current location of the file.

## 3 - Create a shared private link

1. From the command line, sign into Azure using `az login`.

1. If you have multiple subscriptions, make sure you're using the one you intend to use: `az account show`.

   To set the subscription, use `az account set --subscription {{subscription ID}}`

1. Call the `az rest` command to use the [Management REST API](/rest/api/searchmanagement) of Azure AI Search. 

   Because shared private link support for SQL managed instances is still in preview, you need a preview version of the management REST API. Use `2021-04-01-preview` or a later preview API version for this step. We recommend using the latest preview API version.

   ```azurecli
   az rest --method put --uri https://management.azure.com/subscriptions/{{search-service-subscription-ID}}/resourceGroups/{{search service-resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}/sharedPrivateLinkResources/{{shared-private-link-name}}?api-version=2025-05-01-preview --body @create-pe.json
   ```

   Provide the subscription ID, resource group name, and service name of your Azure AI Search resource.

   Provide the same shared private link name that you specified in the JSON body.

   Provide a path to the *create-pe.json* file if you've navigated away from the file location. You can type `dir` at the command line to confirm the file is in the current directory.

1. Run the command.

When you complete these steps, you should have a shared private link that's provisioned in a pending state. **It takes several minutes to create the link**. Once it's created, the resource owner needs to approve the request before it's operational.

You can check the status of the shared private link in the Azure portal. On your search service page, under **Settings** > **Properties**, scroll down to find the shared private link resources and view the JSON value. When the provisioning state changes from *pending* to *succeeded*, you can continue on to the next step.

## 4 - Approve the private endpoint connection

On the SQL Managed Instance side, the resource owner must approve the private connection request you created. 

1. In the Azure portal, open the **Security** > **Private endpoint connections** of the managed instance.

1. Find the section that lists the private endpoint connections.

1. Select the connection, and then select **Approve**. It can take a few minutes for the status to be updated in the Azure portal.

After the private endpoint is approved, Azure AI Search creates the necessary DNS zone mappings in the DNS zone that's created for it.

## 5 - Check shared private link status

On the Azure AI Search side, you can confirm request approval by revisiting the Shared Private Access tab of the search service **Networking** page. Connection state should be approved.

   ![Screenshot of the Azure portal, showing an "Approved" shared private link resource.](media\search-indexer-howto-secure-access\new-shared-private-link-resource-approved.png)

## 6 - Configure the indexer to run in the private environment

You can now configure an indexer and its data source to use an outbound private connection to your managed instance.

This article assumes a [REST client](search-get-started-text.md) and uses the REST APIs.


1. [Create the data source definition](search-how-to-index-sql-database.md) as you would normally for Azure SQL. By default, a managed instance listens on port 3342, but on a virtual network it listens on 1433.

    Provide the connection string that you copied earlier with an Initial Catalog set to your database name.

    ```http
    POST https://myservice.search.windows.net/datasources?api-version=2025-09-01
     Content-Type: application/json
     api-key: admin-key
     {
         "name" : "my-sql-datasource",
         "description" : "A database for testing Azure AI Search indexes.",
         "type" : "azuresql",
         "credentials" : { 
             "connectionString" : "Server=tcp:contoso.a1b22c333d44.database.windows.net,1433;Persist Security Info=false; User ID=<your user name>; Password=<your password>;MultipleActiveResultsSets=False; Encrypt=True;Connection Timeout=30;Initial Catalog=<your database name>"
            },
         "container" : { 
             "name" : "Name of table or view to index",
             "query" : null (not supported in the Azure SQL indexer)
             },
         "dataChangeDetectionPolicy": null,
         "dataDeletionDetectionPolicy": null,
         "encryptionKey": null
     }
    ```

1. [Create the indexer definition](search-howto-create-indexers.md), setting the indexer `executionEnvironment` to "private".

   [Indexer execution](search-howto-run-reset-indexers.md#indexer-execution-environment) occurs in either a private execution environment that's specific to your search service, or a multitenant environment hosted by Microsoft and used to offload expensive skillset processing for multiple customers. **When connecting over a private endpoint, indexer execution must be private.**

   ```http
    POST https://myservice.search.windows.net/indexers?api-version=2025-09-01
     Content-Type: application/json
     api-key: admin-key
       {
        "name": "indexer",
        "dataSourceName": "my-sql-datasource",
        "targetIndexName": "my-search-index",
        "parameters": {
            "configuration": {
                "executionEnvironment": "private"
            }
        },
        "fieldMappings": []
        }
    ```

1. Run the indexer. If the indexer execution succeeds and the search index is populated, the shared private link is working.

You can monitor the status of the indexer in Azure portal or by using the [Indexer Status API](/rest/api/searchservice/indexers/get-status).

You can use [**Search explorer**](search-explorer.md) in Azure portal to check the contents of the index.

## 7 - Test the shared private link

If you ran the indexer in the previous step and successfully indexed content from your managed instance, then the test was successful. However, if the indexer fails or there's no content in the index, you can modify your objects and repeat testing by choosing any client that can invoke an outbound request from an indexer. 

An easy choice is [running an indexer](search-howto-run-reset-indexers.md) in Azure portal, but you can also try a [REST client](search-get-started-text.md) and REST APIs for more precision. Assuming that your search service isn't also configured for a private connection, the REST client connection to Azure AI Search can be over the public internet.

Here are some reminders for testing:

+ If you use a REST client, use the [Management REST API](/rest/api/searchmanagement/) and the [2021-04-01-Preview API version](/rest/api/searchmanagement/management-api-versions) to create the shared private link. Use the [Search REST API](/rest/api/searchservice/) and a [stable API version](/rest/api/searchservice/search-service-api-versions) to create and invoke indexers and data sources.

+ You can use the Import data wizard to create an indexer, data source, and index. However, the generated indexer won't have the correct execution environment setting.

+ You can edit data source and indexer JSON in Azure portal to change properties, including the execution environment and the connection string.

+ You can reset and rerun the indexer in Azure portal. Reset is important for this scenario because it forces a full reprocessing of all documents.

+ You can use Search explorer to check the contents of the index.

## See also

+ [Make outbound connections through a private endpoint](search-indexer-howto-access-private.md)
+ [Indexer connections to Azure SQL Managed Instance through a public endpoint](search-how-to-index-sql-managed-instance.md)
+ [Index data from Azure SQL](search-how-to-index-sql-database.md)
+ [Management REST API](/rest/api/searchmanagement/)
+ [Search REST API](/rest/api/searchservice/)
+ [Quickstart: Full-text search using REST](search-get-started-text.md)
