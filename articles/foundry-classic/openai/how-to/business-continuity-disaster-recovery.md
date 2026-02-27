---
title: 'Business Continuity and Disaster Recovery (BCDR) with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Considerations for implementing Business Continuity and Disaster Recovery (BCDR) with Azure OpenAI 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle    
ms.author: mbullwin
recommendations: false

---

# Business Continuity and Disaster Recovery (BCDR) considerations with Azure OpenAI in Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI is available in multiple regions. When you create an Azure OpenAI resource, you specify a region. From then on, your resource and all its operations stay associated with that Azure server region.  

It's rare, but not impossible, to encounter a network issue that hits an entire region. If your service needs to always be available, then you should design it to either failover into another region or split the workload between two or more regions. Both approaches require at least two Azure OpenAI resources in different regions. This article provides general recommendations for how to implement Business Continuity and Disaster Recovery (BCDR) for your Azure OpenAI applications.

By default, the Azure OpenAI provides a [default service level agreement](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1). While the default reliability may be sufficient for many applications, applications requiring high degrees of business continuity should take extra steps to further strengthen their model infrastructure.

## Standard Deployments

> [!NOTE]
> If you can use Global Standard deployments, you should use those instead. Data Zone deployments are the next best option for organizations requiring data processing to happen entirely within a geographic boundary.

1. For Standard Deployments default to Data Zone deployment (US/EU options).

1. You should deploy two Azure OpenAI resources in the Azure Subscription. One resource should be deployed in your preferred region and the other should be deployed in your secondary/failover region. The Azure OpenAI allocates quota at the subscription + region level, so they can live in the same subscription with no impact on quota.
1. You should have one deployment for each model you plan to use deployed to the Azure OpenAI resource in your preferred Azure region and you should duplicate these model deployments in the secondary/failover region. Allocate the full quota available in your Standard deployment to each of these endpoints. This provides the highest throughput rate when compared to splitting quota across multiple deployments.
1. Select the deployment region based on your network topology. You can deploy an Azure OpenAI resource to any supported region and then create a Private Endpoint for that resource in your preferred region.
    - Once within the Azure OpenAI boundary, the Azure OpenAI optimizes routing and processing across available compute in the data zone. 
    - Using data zones is more efficient and simpler than self-managed load balancing across multiple regional deployments.
1. If there's a regional outage where the deployment is in an unusable state, you can use the other deployment in the secondary/passive region within the same subscription.
    - Because both the primary and secondary deployments are Zone deployments, they draw from the same Zone capacity pool that draws from all available regions in the Zone. The secondary deployment is protecting against the primary Azure OpenAI endpoint being unreachable.     
    - Use a Generative AI Gateway that supports load balancing and circuit breaker pattern such as API Management in front of the Azure OpenAI endpoints so disruption during a regional outage is minimized to consuming applications.
    - If the quota within a given subscription is exhausted, a new subscription can be deployed in the same manner as above and its endpoint deployed behind the Generative AI Gateway.

## Provisioned Deployments

### Create an Enterprise PTU Pool

1. For provisioned deployments, we recommend having a single Data Zone PTU deployment (available December 4, 2024) that serves as an enterprise pool of PTU. You can use API Management to manage traffic from multiple applications to set throughput limits, logging, priority, and failover logic.     
    - Think of this Enterprise PTU Pool as a "Private standard deployment" resource that protects against the noisy-neighbors problem that can occur on Standard deployments when service demand is high. Your organization will have guaranteed, dedicated access to a pool of capacity that is only available to you and therefore independent of demand spikes from other customers. 
    - This gives you control over which applications experience increases in latency first, allowing you to prioritize traffic to your mission critical applications.
    - Provisioned Deployments are backed by latency SLAs that make them preferable to standard deployments for latency sensitive workloads.
    - Enterprise PTU Deployment also enables higher utilization rates as traffic is smoothed out across application workloads, whereas individual workloads tend to be more prone to spikes.
1. Your primary Enterprise PTU  deployment should be in a different region than your primary Standard Zone deployment. This is so that if there's a regional outage, you don't lose access to both your PTU deployment and Standard Zone deployment at the same time.

### Workload Dedicated PTU Deployment

1. Certain workloads might need to have their own dedicated provisioned deployment. If so, you can create a dedicated PTU deployment for that application.
1. The workload and enterprise PTU pool deployments should protect against regional failures. You could do this by placing the workload PTU pool in Region A and the enterprise PTU pool in Region B.    
1. This deployment should fail over first to the Enterprise PTU Pool and then to the Standard deployment. This implies that when utilization of the workload PTU deployment exceeds 100%, requests would still be serviced by PTU endpoints, enabling a higher latency SLA for that application.

:::image type="content" source="../how-to/media/disaster-recovery/disaster-recovery-diagram.jpg" alt-text="Disaster recovery architectural diagram." lightbox="../how-to/media/disaster-recovery/disaster-recovery-diagram.jpg":::

The other benefit of this architecture is that it allows you to stack Standard deployments with Provisioned Deployments so that you can dial in your preferred level of performance and resiliency. This allows you to use PTU for your baseline demand across workloads and use standard deployment for spikes in traffic.

:::image type="content" source="../how-to/media/disaster-recovery/scaling.jpg" alt-text="Provisioned scaling diagram." lightbox="../how-to/media/disaster-recovery/scaling.jpg":::

## BCDR for agents

To support service reliability, the Agents service relies on customer-provisioned Cosmos DB accounts. This ensures that your agent state can be preserved and recovered if there is a regional outage.

1. As an Azure Standard customer, you provision and manage your own single-tenant Cosmos DB account.
1. All of the agent state is stored in your Cosmos DB. Backup and recovery rely on Cosmos DB's native capabilities, which you control.
1. If the primary region becomes unavailable, the agent will automatically become available in the secondary region by connecting to the same Cosmos DB account.
    Since all history is preserved in Cosmos DB, the agent can continue operation with minimal disruption.

We recommend customers provision and maintain their Cosmos DB account and ensure appropriate backup and recovery policies are configured. This ensures seamless continuity if the primary region becomes unavailable.


## Supporting Infrastructure

The infrastructure that supports the Azure OpenAI architecture needs to be considered in designs. The infrastructure components involved in the architecture vary depending on if the applications consume the Azure OpenAI over the Internet or over a private network. The architecture discussed in this article assumes the organization has implemented a [Generative AI Gateway](/ai/playbook/technology-guidance/generative-ai/dev-starters/genai-gateway/). Organizations with a mature Azure footprint and hybrid connectivity should consume the service through a private network while organizations without hybrid connectivity, or with applications in another cloud such as GCP or AWS, will consume the service through the Microsoft public backbone.

### Designing for consumption through the Microsoft public backbone

Organizations consuming the service through the Microsoft public backbone should consider the following design elements:

1. The Generative AI Gateway should be deployed in manner that ensures it's available if there's an Azure regional outage. If you're using APIM (Azure API Management), you can do this by deploying separate APIM instances in multiple regions or using the [multi-region gateway feature of APIM](/azure/api-management/api-management-howto-deploy-multi-region).

1. A public global server load balancer should be used to load balance across the multiple Generative AI Gateway instances in either an active/active or active/passive manner. [Azure FrontDoor](/azure/traffic-manager/traffic-manager-routing-methods) can be used to fulfill this role depending on the organization’s requirements.

:::image type="content" source="../how-to/media/disaster-recovery/recovery.png" alt-text="Failover architectural diagram." lightbox="../how-to/media/disaster-recovery/recovery.png":::


### Designing for consumption through the private networking

Organizations consuming the service through a private network should consider the following design elements:

1. Hybrid connectivity should be deployed in a way that it protects against the failure of an Azure region. The underlining components supporting hybrid connectivity consist of the organization’s on-premises network infrastructure and [Microsoft ExpressRoute](/azure/expressroute/designing-for-high-availability-with-expressroute) or [VPN](/azure/vpn-gateway/vpn-gateway-highlyavailable). 
1. The Generative AI Gateway should be deployed in manner that ensures it's available in the event of an Azure regional outage. If using APIM (Azure API Management), this can be done by deploying separate APIM instances in multiple regions or using the [multi-region gateway feature of APIM](/azure/api-management/api-management-howto-deploy-multi-region).
1. Azure Private Link Private Endpoints should be deployed for each Azure OpenAI instance in each Azure region. For Azure Private DNS, a split-brain DNS approach can be used if all application access to the Azure OpenAI is done through the Generative AI Gateway to provide for extra protection against a regional failure. If not, Private DNS records need to be manually modified in the event of a loss of an Azure region. 
1. A private global server load balancer should be used to load balance across the multiple Generative AI Gateway instances in either an active/active or active/passive manner. Azure doesn't have a native service for global server load balancer for workloads that require private DNS resolution. For more background on this topic you can refer to this unofficial guide: https://github.com/adstuart/azure-crossregion-private-lb. In lieu of a global server load balancer, organizations can achieve an active/passive pattern through toggling the DNS record for the Generative AI Gateway.
