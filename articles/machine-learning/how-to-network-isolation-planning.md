---
title: Plan for network isolation
titleSuffix: Azure Machine Learning
description: "Learn about the network isolation options available in Azure Machine Learning and which one is right for your scenario."
author: Blackmist
ms.author: larryfr
ms.service: azure-machine-learning
ms.topic: concept-article #Don't change.
ms.date: 01/13/2025

#customer intent: As an admin, I want to understand the network isolation options available to me so that I can architect our solution to meet my business requirements.

---

# Plan for network isolation in Azure Machine Learning

In this article, you learn how to plan your network isolation for Azure Machine Learning and our recommendations. This article is for IT administrators who want to design network architecture. 

## What is network isolation?

Network isolation is a security strategy that involves dividing a network into separate segments or subnets, each functioning as its own small network. This approach helps to improve security and performance within a larger network structure. Major enterprises require network isolation to secure their resources from unauthorized access, tampering, or leakage of data and models. They also need to adhere to the regulations and standards that apply to their industry and domain.

## Inbound and outbound access

Network isolation must be considered in three areas within Azure Machine Learning: 
- Inbound access to the Azure Machine Learning workspace. For example, for your Data Scientists to securely access the workspace.
- Outbound access from the Azure Machine Learning workspace. For example, to access other Azure services.
- Outbound access from the Azure Machine Learning compute resources. For example, to access data sources, Python package repositories, or other resources.

The following diagram breaks down the inbound and outbound.  

:::image type="content" source="./media/how-to-network-isolation-planning/inbound-and-outbound.png" alt-text="Diagram showing inbound and outbound communication for Azure Machine Learning.":::

### Inbound access to Azure Machine Learning

Inbound access to a secured Azure Machine Learning workspace is set using the public network access (PNA) flag. The PNA flag setting decides if your workspace requires a private endpoint or not to access the workspace. There's an extra setting between public and private: Enabled from selected IP addresses. This setting allows access to your workspace from the IP addresses you specify. For more on this feature, see [Enable Public Access only from internet IP ranges](how-to-configure-private-link.md#enable-public-access-only-from-internet-ip-ranges).

### Outbound access

Azure Machine Learning's network isolation involves both Platform as a Service (PaaS) and Infrastructure as a Service (IaaS) components. PaaS services, such as the Azure Machine Learning workspace, storage, key vault, container registry, and monitor, can be isolated using Private Link. IaaS computing services, such as compute instances/clusters for AI model training, and Azure Kubernetes Service (AKS) or managed online endpoints for AI model scoring, can be injected into your virtual network and communicate with PaaS services using Private Link. The following diagram is an example of IaaS and PaaS components.

:::image type="content" source="./media/how-to-network-isolation-planning/outbound-detail.png" alt-text="Diagram showing outbound communication from computes to Azure services.":::

#### Outbound from service to other Azure PaaS resources

Securing outbound access from your Azure Machine Learning service to other PaaS services is completed through trusted services. You can grant a subset of trusted Azure services access to Azure Machine Learning, while maintaining network rules for other apps. These trusted services use a managed identity to authenticate your Azure Machine Learning service.

#### Outbound from computes to the internet and other Azure PaaS resources

IaaS components are the compute resources such as compute instances/clusters and Azure Kubernetes Service (AKS) or managed online endpoints. For these IaaS resources, outbound access to the Internet is secured through a Firewall and outbound access to other PaaS resources is secured with Private Link and private endpoints. A managed virtual network allows for easier set-up of controlling outbound from computes.

If you aren't using a managed virtual network, outbound control can be secured with your own virtual network and subnet set. If you have a standalone virtual network, the configuration is straightforward using network security group. However, you might have a hub-spoke or mesh network architecture, firewall, network virtual appliance, proxy, and user defined routing. In either case, make sure to allow inbound and outbound with your network security components. 

:::image type="content" source="media/how-to-network-isolation-planning/hub-spoke-network-diagram.png" alt-text="Diagram of hub-spoke network with outbound through firewall.":::

In this diagram, you have a hub and spoke network architecture. The spoke virtual network has resources for Azure Machine Learning. The hub virtual network has a firewall that control internet outbound from your virtual networks. In this case, your firewall must allow outbound to required resources and your compute resources in spoke virtual network must be able to reach your firewall. 

> [!TIP]
> In the diagram, the compute instance and compute cluster are configured for no public IP. If you instead use a compute instance or cluster with public IP, you need to allow inbound from the Azure Machine Learning service tag using a Network Security Group (NSG) and user defined routing to skip your firewall. This inbound traffic would be from a Microsoft service (Azure Machine Learning). However, we recommend using the no public IP option to remove this inbound requirement.

## Network isolation offerings for outbound access from computes

Now that we understand what access needs to be secured, let's look at how we can secure our machine learning workspace with network isolation. Azure Machine Learning offers network isolation options for outbound access from computing resources.

### Managed Network isolation (recommended)

Using a Managed virtual network provides an easier configuration for network isolation. It automatically secures your workspace and managed compute resources in a managed virtual network. You can add private endpoint connections for other Azure services that the workspace relies on, such as Azure Storage Accounts. Depending on your needs, you can allow all outbound traffic to the public network or allow only the outbound traffic you approve. Outbound traffic required by the Azure Machine Learning service is automatically enabled for the managed virtual network. We recommend using workspace managed network isolation for a built-in friction less network isolation method. We have two patterns: allow internet outbound mode or allow only approved outbound mode. 

> [!NOTE]
> Securing your workspace with a managed virtual network provides network isolation for outbound access from the workspace and managed computes. An Azure Virtual Network that you create and manage is used to provide network isolation inbound access to the workspace. For example, a private endpoint for the workspace is created in your Azure Virtual Network. Any clients connecting to the virtual network can access the workspace through the private endpoint. When running jobs on managed computes, the managed network restricts what the compute can access. This configuration is different from the custom virtual network offering which also requires setting a virtual network and setting all computes into that virtual network.

- __Allow internet outbound mode__: Use this option if you want to allow your machine learning engineers access the internet freely. You can create other private endpoint outbound rules to let them access your private resources on Azure.

    :::image type="content" source="./media/how-to-network-isolation-planning/allow-internet-outbound-mode.png" alt-text="Diagram of a managed network configured as allow internet outbound mode.":::

- __Allow only approved outbound mode__: Use this option if you want to minimize data exfiltration risk and control what your machine learning engineers can access. You can control outbound rules using private endpoint, service tag, and FQDN.

    :::image type="content" source="./media/how-to-network-isolation-planning/allow-only-approved-outbound-mode.png" alt-text="Diagram of a managed network with allow only approved outbound mode configured.":::

### Custom network isolation

If you have a specific requirement or company policy that prevents you from using a managed virtual network, you can use an Azure virtual network for network isolation. 

The following diagram is our recommended architecture to make all resources private but allow outbound internet access from your virtual network. This diagram describes the following architecture: 

- Put all resources in the same region.
- A hub virtual network, which contains your firewall and custom DNS set-up.
- A spoke virtual network, which contains the following resources:
    - A training subnet contains compute instances and clusters used for training ML models. These resources are configured for no public IP.
    - A scoring subnet contains an AKS cluster.
    - A 'pe' subnet contains private endpoints that connect to the workspace and private resources used by the workspace (storage, key vault, container registry, etc.)
- To secure your managed online endpoints with custom virtual network, enable the legacy managed online endpoint managed virtual network. We do NOT recommend this method.  

This architecture balances your network security and your ML engineers' productivity.

:::image type="content" source="./media/how-to-network-isolation-planning/custom-network-diagram.png" alt-text="Diagram of a custom network isolation configuration.":::

> [!NOTE]
> If you want to remove the firewall requirement, you can use network security groups and Azure Virtual Network NAT to allow internet outbound from your private compute resources.

#### Data exfiltration prevention

This diagram shows the recommended architecture to make all resources private and control outbound destinations to prevent data exfiltration. We recommend this architecture when using Azure Machine Learning with your sensitive data in production. This diagram describes the following architecture:

- Put all resources in the same region.
- A hub virtual network, which contains your firewall.
    - In addition to service tags, the firewall uses FQDNs to prevent data exfiltration.
- A spoke virtual network, which contains the following resources:
    - A training subnet contains compute instances and clusters used for training ML models. These resources are configured for no public IP. Additionally, a service endpoint and service endpoint policy are in place to prevent data exfiltration.
    - A scoring subnet contains an AKS cluster.
    - A 'pe' subnet contains private endpoints that connect to the workspace and private resources used by the workspace (storage, key vault, container registry, etc.)
- Managed online endpoints use the private endpoint of the workspace to process incoming requests. A private endpoint is also used to allow managed online endpoint deployments to access private storage.

:::image type="content" source="./media/how-to-network-isolation-planning/custom-network-data-exfiltration.png" alt-text="Diagram of a custom network isolation configuration to prevent data exfiltration.":::

## Comparison of network isolation options

Both managed network isolation and custom network isolation are similar offerings. The following table describes all the similarities and differences between the two offerings in terms of their set-up. The one key difference in their set-up is where the virtual network for computes itself is hosted. For custom network isolation, the virtual network for computes is in your tenant while for managed network isolation, the virtual network for computes is located in the Microsoft tenant.  

| Similarities | Differences |
| --- | --- |
| - Network is dedicated to you and not shared with any other customers. </br>- Data is protected in the virtual network. </br>- Full control on egress with outbound rules. </br>- Required ServiceTags. | - Where the virtual network is hosted; in your tenant for custom network isolation or in the Microsoft tenant for managed network isolation. |

To make the right decision on which networking set-up works best for your scenario, consider what features within Azure Machine Learning you want to use. For more information regarding the differences between our network isolation offerings, see [Compare network isolation configurations](concept-network-isolation-configurations.md).

### Comparison of configurations

| | Managed network (recommended) | Custom network |
| --- | --- | --- |
| __Benefits__ | - Minimize set-up and maintenance overhead. </br>- Supports managed online endpoints. </br>- Supports serverless spark. </br>- Access to HTTPS endpoint resources located on-premises or in your custom virtual network. </br>- Focus for new feature development. | - Customize network to your requirements. </br>- Bring your own non-Azure resources. </br>- Connect to on-premises resources. |
| __Limitations__ | - Extra costs for Azure Firewall and FQDN rules. </br>- Logging of the virtual network firewall and NSG rules isn't supported. </br>- Access to non-HTTPS endpoint resources isn't supported. | - New feature support might be delayed. </br>-Managed online endpoints aren't supported. </br>- Serverless spark isn't supported. </br>- Foundational models aren't supported. </br>- No code MLFlow isn't supported. </br>- Implementation complexity. </br>- Maintenance overhead. |

### Use a public workspace

You can use a public workspace if you're OK with Microsoft Entra ID authentication and authorization with conditional access. A public workspace has some features that allow using data in a private storage account. We recommend using a private workspace if possible.

## Key considerations

### DNS resolution of private link resources and application on compute instance 

If you have your own DNS server hosted in Azure or on-premises, you need to create a conditional forwarder in your DNS server. The conditional forwarder sends DNS requests to the Azure DNS for all private link enabled PaaS services. For more information, see the DNS configuration scenarios and Azure Machine Learning specific DNS configuration articles. 

### Data exfiltration protection 

We have two types of outbound; read only and read/write. Malicious actor's can't expoilt read only outbound, but read/write outbound can be. Azure Storage and Azure Frontdoor (the frontdoor.frontend service tag) are read/write outbound in our case. 

You can mitigate this data exfiltration risk using our data exfiltration prevention solution. We use a service endpoint policy with an Azure Machine Learning alias to allow outbound to only Azure Machine Learning managed storage accounts.

:::image type="content" source="./media/how-to-network-isolation-planning/data-exfiltration-protection-diagram.png" alt-text="Diagram of network with exfiltration protection configuration.":::

In this diagram, the compute instance and cluster need to access Azure Machine Learning managed storage accounts to get set-up scripts. When opening the outbound to storage, you can use service endpoint policy with Azure Machine Learning alias to allow the storage access only to Azure Machine Learning storage accounts.

### Managed online endpoints

Security for inbound and outbound communication are configured separately for managed online endpoints. 

- __Inbound communication__: Azure Machine Learning uses a private endpoint to secure inbound communication to a managed online endpoint. To prevent public access to an endpoint, set public_network_access flag for the endpoint to disabled. When this flag is disabled, your endpoint can be accessed only via the private endpoint of your Azure Machine Learning workspace, and it can't be reached from public networks. 
- __Outbound communication__: To secure outbound communication from a deployment to resources, Azure Machine Learning uses a workspace managed virtual network. The deployment needs to be created in the workspace managed virtual network so that it can use the private endpoints of the workspace managed virtual network for outbound communication. 

The following architecture diagram shows how communications flow through private endpoints to the managed online endpoint. Incoming scoring requests from a client's virtual network flow through the workspace's private endpoint to the managed online endpoint. Outbound communication from deployments to services is handled through private endpoints from the workspace's managed virtual network to those service instances.

:::image type="content" source="./media/concept-secure-online-endpoint/endpoint-network-isolation-with-workspace-managed-vnet.png" alt-text="Diagram showing inbound communication via a workspace private endpoint and outbound communication via private endpoints of a managed virtual network.":::

For more information, see [Network isolation with managed online endpoints](concept-secure-online-endpoint.md).

### Private IP address shortage in your main network

Azure Machine Learning requires private IPs; one IP per compute instance, compute cluster node, and private endpoint. You also need many IPs if you use AKS. Your hub-spoke network connected with your on-premises network might not have a large enough private IP address space. In this scenario, you can use isolated, not-peered VNets for your Azure Machine Learning resources. 

:::image type="content" source="./media/how-to-network-isolation-planning/isolated-not-peered-network-diagram.png" alt-text="Diagram showing an isolated network configuration.":::

In this diagram, your main virtual network requires the IPs for private endpoints. You can have hub-spoke VNets for multiple Azure Machine Learning workspaces with large address spaces. A downside of this architecture is to double the number of private endpoints.

### Network policy enforcement

You can use built-in policies if you want to control network isolation parameters with self-service workspace and computing resources creation or create a custom policy for more fine-grained controls. For more on policies, see [Azure Policy regulatory compliance controls](security-controls-policy.md).  

## Related content

For more information on using a __managed virtual network__, see the following articles:

- [Managed network isolation](how-to-managed-network.md)
- [Use private endpoints to access your workspace](how-to-configure-private-link.md)
- [Use custom DNS](how-to-custom-dns.md)

For more information on using a __custom virtual network__, see the following articles:

- [Virtual network overview](how-to-network-security-overview.md)
- [Secure the workspace resources](how-to-secure-workspace-vnet.md)
- [Secure the training environment](how-to-secure-training-vnet.md)
- [Secure the inference environment](how-to-secure-inferencing-vnet.md)
- [Enable studio functionality](how-to-enable-studio-virtual-network.md)
- [Configure inbound and outbound network traffic](how-to-access-azureml-behind-firewall.md)
