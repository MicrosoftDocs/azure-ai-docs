---
title: Indexer connection to SQL Server on Azure VMs
titleSuffix: Azure AI Search
description: Enable encrypted connections and configure the firewall to allow connections to SQL Server on an Azure virtual machine (VM) from an indexer on Azure AI Search.
author: gmndrg
ms.author: gimondra
manager: nitinme

ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 12/10/2024
---

# Indexer connections to a SQL Server instance on an Azure virtual machine

When configuring an [Azure SQL indexer](search-how-to-index-sql-database.md) to extract content from a database on an Azure virtual machine, extra steps are required for secure connections. 

A connection from Azure AI Search to SQL Server instance on a virtual machine is a public internet connection. In order for secure connections to succeed, perform the following steps:

+ Obtain a certificate from a [Certificate Authority provider](https://en.wikipedia.org/wiki/Certificate_authority#Providers) for the fully qualified domain name of the SQL Server instance on the virtual machine.

+ Install the certificate on the virtual machine.

After you install the certificate on your VM, you're ready to complete the following steps in this article.

> [!NOTE]
> [Always Encrypted](/sql/relational-databases/security/encryption/always-encrypted-database-engine) columns are not currently supported by Azure AI Search indexers.

## Enable encrypted connections

Azure AI Search requires an encrypted channel for all indexer requests over a public internet connection. This section lists the steps to make this work.

1. Check the properties of the certificate to verify the subject name is the fully qualified domain name (FQDN) of the Azure VM. 

   You can use a tool like CertUtils or the Certificates snap-in to view the properties. You can get the FQDN from the VM service page Essentials section, in the **Public IP address/DNS name label** field, in the [Azure portal](https://portal.azure.com/).
  
   The FQDN is typically formatted as `<your-VM-name>.<region>.cloudapp.azure.com`

1. Configure SQL Server to use the certificate using the Registry Editor (regedit). 

   Although SQL Server Configuration Manager is often used for this task, you can't use it for this scenario. It won't find the imported certificate because the FQDN of the VM on Azure doesn't match the FQDN as determined by the VM (it identifies the domain as either the local computer or the network domain to which it's joined). When names don't match, use regedit to specify the certificate.

   1. In regedit, browse to this registry key: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server\[MSSQL13.MSSQLSERVER]\MSSQLServer\SuperSocketNetLib\Certificate`. 

      The `[MSSQL13.MSSQLSERVER]` part varies based on version and instance name. 

   1. Set the value of the **Certificate** key to the **thumbprint** (without spaces) of the TLS/SSL certificate you imported to the VM.

     There are several ways to get the thumbprint, some better than others. If you copy it from the **Certificates** snap-in in MMC, you might pick up an invisible leading character [as described in this support article](https://support.microsoft.com/kb/2023869/), which results in an error when you attempt a connection. Several workarounds exist for correcting this problem. The easiest is to backspace over and then retype the first character of the thumbprint to remove the leading character in the key value field in regedit. Alternatively, you can use a different tool to copy the thumbprint.

1. Grant permissions to the service account. 

   Make sure the SQL Server service account is granted appropriate permission on the private key of the TLS/SSL certificate. If you overlook this step, SQL Server doesn't start. You can use the **Certificates** snap-in or **CertUtils** for this task.

1. Restart the SQL Server service.

## Connect to SQL Server

After you set up the encrypted connection required by Azure AI Search, connect to the instance through its public endpoint. The following article explains the connection requirements and syntax:

+ [Connect to SQL Server over the internet](/azure/azure-sql/virtual-machines/windows/ways-to-connect-to-sql#connect-to-sql-server-over-the-internet)

## Configure the network security group

It's a best practice to configure the [network security group (NSG)](/azure/virtual-network/network-security-groups-overview) and corresponding Azure endpoint or Access Control List (ACL) to make your Azure VM accessible to other parties. Chances are you've done this before to allow your own application logic to connect to your SQL Azure VM. It's no different for an Azure AI Search connection to your SQL Azure VM. 

The following steps and links provide instructions on NSG configuration for VM deployments. Use these instructions to ACL a search service endpoint based on its IP address.

1. Obtain the IP address of your search service. See the [following section](#restrict-network-access-to-azure-ai-search) for instructions.

1. Add the search IP address to the IP filter list of the security group. Either one of following articles explains the steps:

  + [Tutorial: Filter network traffic with a network security group using the Azure portal](/azure/virtual-network/tutorial-filter-network-traffic)

  + [Create, change, or delete a network security group](/azure/virtual-network/manage-network-security-group)

IP addressing can pose a few challenges that are easily overcome if you're aware of the issue and potential workarounds. The remaining sections provide recommendations for handling issues related to IP addresses in the ACL.

### Restrict network access to Azure AI Search

We strongly recommend that you restrict the access to the IP address of your search service and the IP address range of `AzureCognitiveSearch` [service tag](/azure/virtual-network/service-tags-overview#available-service-tags) in the ACL instead of making your SQL Azure VMs open to all connection requests.

You can find out the IP address by pinging the FQDN (for example, `<your-search-service-name>.search.windows.net`) of your search service. Although it's possible for the search service IP address to change, it's unlikely that it will change. The IP address tends to be static for the lifetime of the service.

You can find out the IP address range of `AzureCognitiveSearch` [service tag](/azure/virtual-network/service-tags-overview#available-service-tags) by either using [Downloadable JSON files](/azure/virtual-network/service-tags-overview#discover-service-tags-by-using-downloadable-json-files) or via the [Service Tag Discovery API](/azure/virtual-network/service-tags-overview#use-the-service-tag-discovery-api). The IP address range is updated weekly.

### Include the Azure portal IP addresses

If you're using the Azure portal to create an indexer, you must grant the Azure portal inbound access to your SQL Azure virtual machine. An inbound rule in the firewall requires that you provide the IP address of the Azure portal.

To get the Azure portal IP address, ping `stamp2.ext.search.windows.net`, which is the domain of the traffic manager. The request times out, but the IP address is visible in the status message. For example, in the message "Pinging azsyrie.northcentralus.cloudapp.azure.com [52.252.175.48]", the IP address is "52.252.175.48".

Clusters in different regions connect to different traffic managers. Regardless of the domain name, the IP address returned from the ping is the correct one to use when defining an inbound firewall rule for the Azure portal in your region.

## Supplement network security with token authentication

Firewalls and network security are a first step in preventing unauthorized access to data and operations. Authorization should be your next step. 

We recommend role-based access, where Microsoft Entra ID users and groups are assigned to roles that determine read and write access to your service. See [Connect to Azure AI Search using role-based access controls](search-security-rbac.md) for a description of built-in roles and instructions for creating custom roles.

If you don't need key-based authentication, we recommend that you disable API keys and use role assignments exclusively.

## Next steps

With configuration out of the way, you can now specify a SQL Server on Azure VM as the data source for an Azure AI Search indexer. For more information, see [Index data from Azure SQL](search-how-to-index-sql-database.md).
