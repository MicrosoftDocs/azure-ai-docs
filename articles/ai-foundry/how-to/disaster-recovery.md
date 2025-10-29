---
title: Customer enabled disaster recovery for AI hub projects
titleSuffix: Azure AI Foundry
description: Learn how to plan for disaster recovery for Azure AI Foundry hub projects.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
ms.topic: how-to
ms.author: jburchel 
author: jonburchel 
ms.reviewer: andyaviles
ms.date: 08/27/2025
ai.usage: ai-assisted
---

# Customer-enabled disaster recovery

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Plan ahead to maintain business continuity and prepare for disaster recovery with [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). Because Azure AI Foundry builds on the [Azure Machine Learning architecture](/azure/machine-learning/concept-workspace), review the foundational architecture.

Microsoft strives to ensure that Azure services are always available. However, unplanned service outages might occur. Create a disaster recovery plan to handle regional service outages. In this article, you learn how to:

* Plan a multi-region deployment of Azure AI Foundry and associated resources.
* Maximize your chances to recover logs, notebooks, Docker images, and other metadata.
* Design your solution for high availability.
* Fail over to another region.

> [!IMPORTANT]
> Azure AI Foundry itself doesn't provide automatic failover or disaster recovery.

> [!NOTE]
> The information in this article only applies to a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. A **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** isn't supported. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

## Understand Azure services for Azure AI Foundry

Azure AI Foundry depends on multiple Azure services. Some of these services are set up in your subscription. You're responsible for the high availability configuration of these services. Microsoft manages some services that are created in a Microsoft subscription. 

Azure services include:

* **Azure AI Foundry infrastructure**: A Microsoft managed environment for the Azure AI Foundry hub and project. Azure Machine Learning provides the [underlying architecture](../concepts/architecture.md).

* **Required associated resources**: Resources set up in your subscription when you create an Azure AI Foundry hub or project. These resources include Azure Storage and Azure Key Vault.
  * The default storage has models, training logs, and references to data assets.
  * Azure Key Vault stores credentials for Azure Storage and connections.

* **Optional associated resources**: Resources you attach to your Azure AI Foundry hub. These resources include Azure Container Registry and Application Insights.
  * Azure Container Registry stores Docker images for training and inference environments.
  * Application Insights monitors Azure AI Foundry.

* **Compute instance**: A resource you create after you deploy the hub. It provides a Microsoft managed model development environment.

* **Connections**: Azure AI Foundry connects to other services. You're responsible for configuring their high availability settings.

The following table shows the Azure services that Microsoft manages and the ones you manage. It also indicates the services that are highly available by default.

| Service | Managed by | High availability by default |
| ----- | ----- | ----- |
| **Azure AI Foundry infrastructure** | Microsoft | |
| **Associated resources** |  |  |
| Azure Storage | You | |
| Azure Key Vault | You | ✓ |
| Azure Container Registry | You | |
| Application Insights | You | Not applicable |
| **Compute resources** |  |  |
| Compute instance | Microsoft |  |
| **Connections to external services** like Azure AI Services | You | |

The rest of this article explains how to make each service highly available.

## Plan for multiregional deployment

A multiregional deployment relies on the creation of Azure AI Foundry resources and other infrastructure in two Azure regions. If a regional outage occurs, switch to the other region. When you plan where to deploy your resources, consider:

* Regional availability: If possible, use a region in the same geographic area, not necessarily the closest one. To check regional availability for Azure AI Foundry, see [Azure products by region](https://azure.microsoft.com/global-infrastructure/services/).
* Azure paired regions: Paired regions coordinate platform updates and prioritize recovery efforts where needed. But not all regions are paired. For more information, see [Azure paired regions](/azure/reliability/cross-region-replication-azure).
* Service availability: Decide whether to use hot/hot, hot/warm, or hot/cold for your solution's resources.
    
    * Hot/hot: Both regions are active at the same time, and either region is ready to use immediately.
    * Hot/warm: The primary region is active. The secondary region has critical resources (for example, deployed models) ready to start. Deploy noncritical resources manually in the secondary region.
    * Hot/cold: The primary region is active. The secondary region has Azure AI Foundry and other resources deployed, along with the required data. Deploy resources such as models, model deployments, and pipelines manually.

> [!TIP]
> Depending on your business requirements, you might treat Azure AI Foundry services differently.

Azure AI Foundry builds on other services. Some services can replicate to other regions. You must manually create other services in multiple regions. The following table lists the services, who is responsible for replication, and an overview of the configuration:

| Azure service | Geo-replicated by | Configuration |
| ----- | ----- | ----- |
| Azure AI Foundry hub and projects | You | Create a hub and projects in the selected regions. |
| Azure AI Foundry compute | You | Create the compute resources in the selected regions. For compute resources that can dynamically scale, make sure that both regions provide sufficient compute quota for your needs. |
| Key Vault | Microsoft | Use the same Azure Key Vault instance with the Azure AI Foundry hub and resources in both regions. Azure Key Vault automatically fails over to a secondary region. For more information, see [Azure Key Vault availability and redundancy](/azure/key-vault/general/disaster-recovery-guidance).|
| Storage account | You | Azure Machine Learning doesn't support default storage account failover using geo-redundant storage (GRS), geo-zone-redundant storage (GZRS), read-access geo-redundant storage (RA-GRS), or read-access geo-zone-redundant storage (RA-GZRS). Configure a storage account according to your needs and use it for your hub. All subsequent projects use the hub's storage account. For more information, see [Azure Storage redundancy](/azure/storage/common/storage-redundancy). |
| Azure Container Registry | Microsoft | Configure the Azure Container Registry instance to geo-replicate to the paired region for Azure AI Foundry. Use the same instance for both hubs. For more information, see [Geo-replication in Azure Container Registry](/azure/container-registry/container-registry-geo-replication). |
| Application Insights | You | Create Application Insights for the hub in both regions. To adjust the data retention period and details, see [Data collection, retention, and storage in Application Insights](/azure/azure-monitor/logs/data-retention-archive). |

Use these development practices to enable fast recovery and restart in the secondary region:

* Use Azure Resource Manager templates. Templates are infrastructure as code and let you quickly deploy services in both regions.
* To avoid drift between the two regions, update your continuous integration and deployment pipelines to deploy to both regions.
* Create role assignments for users in both regions.
* Create network resources such as Azure virtual networks and private endpoints for both regions. Ensure users can access both network environments. For example, configure VPN and DNS for both virtual networks.

## Design for high availability

### Availability zones

Some Azure services support availability zones. In regions that support availability zones, if a zone goes down, projects pause, and you should save your data. You can't refresh data until the zone is back online.

For more information, see [Availability zone service support](/azure/reliability/availability-zones-service-support).

### Deploy critical components to multiple regions

Decide the level of business continuity you need. The level can differ between components of your solution. For example, you might use a hot/hot configuration for production pipelines or model deployments, and hot/cold for development.

Azure AI Foundry is a regional service and stores data both on the service side and in a storage account in your subscription. If a regional disaster occurs, service data can't be recovered. However, you can recover data that the service stores in the storage account in your subscription if storage redundancy is enabled. Service-side data is mostly metadata (tags, asset names, descriptions). Data in your storage account is typically not metadata, like uploaded data.

For connections, create two separate resources in two distinct regions, and then create two connections for the hub. For example, if AI Services is critical for business continuity, create two AI Services resources and two hub connections. With this configuration, if one region goes down, the other region stays operational.

For any hubs that are essential to business continuity, deploy resources in two regions.

### Isolated storage

If you connect data to customize your AI application, you can use those datasets in Azure AI and outside Azure AI. Dataset volume can be large, so it might be good practice to keep this data in a separate storage account. Evaluate the data replication strategy that makes the most sense for your use case.

In the Azure AI Foundry portal, create a connection to your data. If you have multiple Azure AI Foundry instances in different regions, you can point to the same storage account because connections work across regions.
 

## Initiate a failover

### Continue work in the failover hub

When the primary hub is unavailable, switch to the secondary hub to continue development. Azure AI Foundry doesn't automatically submit jobs to the secondary hub during an outage. Update your configuration to point to the secondary hub or project resources. Avoid hard-coded hub or project references.

Azure AI Foundry can't sync or recover artifacts or metadata between hubs. Depending on your deployment strategy, you might need to move or recreate artifacts in the failover hub to continue. If you configure the primary and secondary hubs to share associated resources with geo-replication enabled, some objects can be available in the failover hub. For example, both hubs can share the same Docker images, configured datastores, and Azure Key Vault resources.

> [!NOTE]
> Jobs that run during a service outage don't automatically transition to the secondary hub. They're also unlikely to resume and finish successfully in the primary hub after the outage. Resubmit these jobs in the secondary hub or in the primary hub after the outage.

## Recovery options

### Resource deletion

If you delete a hub and its resources, some resources support soft delete and can be recovered. Hubs and projects don't support soft delete—if you delete them, you can't recover them. The following table shows which services support soft delete.

| Service | Soft delete enabled |
| ------- | ------------------- |
| Azure AI Foundry hub | Unsupported | 
| Azure AI Foundry project | Unsupported | 
| Azure AI Services resource | Yes |
| Azure Storage | See [Recover a deleted storage account](/azure/storage/common/storage-account-recover#recover-a-deleted-account-from-the-azure-portal). |
| Azure Key Vault | Yes |

## Next steps

* See [Create a secure hub](create-secure-ai-hub.md) to learn about secure infrastructure deployments in Azure AI Foundry.
* Review the [Azure service-level agreements](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1).
