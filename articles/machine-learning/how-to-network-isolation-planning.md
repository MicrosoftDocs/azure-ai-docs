---
title: Plan for network isolation
titleSuffix: Azure Machine Learning
description: "Learn about the network isolation options available in Azure Machine Learning and which one is right for your scenario."
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
ms.service: azure-machine-learning
ms.topic: concept-article #Don't change.
ms.date: 01/08/2026

#customer intent: As an admin, I want to understand the network isolation options available to me so that I can architect our solution to meet my business requirements.

---

# Plan for network isolation in Azure Machine Learning

In this article, you learn how to plan your network isolation for Azure Machine Learning and our recommendations. This article is for IT administrators who want to design network architecture. Azure Machine Learning supports IPv6. 

## What is network isolation?

Network isolation is a security strategy that involves dividing a network into separate segments or subnets, each functioning as its own small network. This approach helps to improve security and performance within a larger network structure. Major enterprises require network isolation to secure their resources from unauthorized access, tampering, or leakage of data and models. They also need to adhere to the regulations and standards that apply to their industry and domain.

## Inbound and outbound access

Consider network isolation in three areas within Azure Machine Learning: 
- Inbound access to the Azure Machine Learning workspace. For example, for your data scientists to securely access the workspace.
- Outbound access from the Azure Machine Learning workspace. For example, to access other Azure services.
- Outbound access from the Azure Machine Learning compute resources. For example, to access data sources, Python package repositories, or other resources.

The following diagram breaks down the inbound and outbound communication.  

:::image type="content" source="./media/how-to-network-isolation-planning/inbound-and-outbound.png" alt-text="Diagram showing inbound and outbound communication for Azure Machine Learning.":::

### Inbound access to Azure Machine Learning

Set inbound access to a secured Azure Machine Learning workspace by using the public network access (PNA) flag. The PNA flag setting decides if your workspace requires a private endpoint to access the workspace. An extra setting between public and private is **Enabled from selected IP addresses**. This setting allows access to your workspace from the IP addresses you specify. For more information, see [Enable Public Access only from internet IP ranges](how-to-configure-private-link.md#enable-public-access-only-from-internet-ip-ranges).

### Outbound access

Azure Machine Learning's network isolation involves both Platform as a Service (PaaS) and Infrastructure as a Service (IaaS) components. You can isolate PaaS services, such as the Azure Machine Learning workspace, storage, key vault, container registry, and monitor, by using Private Link. You can inject IaaS computing services, such as compute instances and clusters for AI model training, and Azure Kubernetes Service (AKS) or managed online endpoints for AI model scoring, into your virtual network. These IaaS services communicate with PaaS services by using Private Link. The following diagram shows an example of IaaS and PaaS components.

:::image type="content" source="./media/how-to-network-isolation-planning/outbound-detail.png" alt-text="Diagram showing outbound communication from computes to Azure services.":::

#### Outbound from service to other Azure PaaS resources

You secure outbound access from your Azure Machine Learning service to other PaaS services through trusted services. You can grant a subset of trusted Azure services access to Azure Machine Learning while maintaining network rules for other apps. These trusted services use a managed identity to authenticate your Azure Machine Learning service.

#### Outbound from computes to the internet and other Azure PaaS resources

IaaS components are the compute resources, such as compute instances and clusters, and Azure Kubernetes Service (AKS) or managed online endpoints. For these IaaS resources, you secure outbound access to the internet through a firewall. You secure outbound access to other PaaS resources by using Private Link and private endpoints. A managed virtual network makes it easier to set up control for outbound access from computes.

If you aren't using a managed virtual network, you can secure outbound control by using your own virtual network and subnet set. If you have a standalone virtual network, you can straightforwardly configure it by using a network security group. However, you might have a hub-spoke or mesh network architecture, firewall, network virtual appliance, proxy, and user defined routing. In either case, make sure to allow inbound and outbound access by using your network security components. 

:::image type="content" source="media/how-to-network-isolation-planning/hub-spoke-network-diagram.png" alt-text="Diagram of hub-spoke network with outbound through firewall.":::

In this diagram, you have a hub and spoke network architecture. The spoke virtual network has resources for Azure Machine Learning. The hub virtual network has a firewall that controls internet outbound access from your virtual networks. In this case, your firewall must allow outbound access to required resources. Your compute resources in the spoke virtual network must be able to reach your firewall. 

> [!TIP]
> In the diagram, the compute instance and compute cluster are configured with no public IP. If you instead use a compute instance or cluster with public IP, you need to allow inbound access from the Azure Machine Learning service tag by using a Network Security Group (NSG) and user defined routing to skip your firewall. This inbound traffic comes from a Microsoft service (Azure Machine Learning). However, use the no public IP option to remove this inbound requirement.

## Network isolation offerings for outbound access from computes

Now that you understand what access needs to be secured, let's look at how you can secure your machine learning workspace by using network isolation. Azure Machine Learning offers network isolation options for outbound access from computing resources.

### Managed network isolation (recommended)

Using a managed virtual network makes it easier to configure network isolation. It automatically secures your workspace and managed compute resources in a managed virtual network. You can add private endpoint connections for other Azure services that the workspace relies on, such as Azure Storage Accounts. Depending on your needs, you can allow all outbound traffic to the public network or allow only the outbound traffic you approve. Outbound traffic required by the Azure Machine Learning service is automatically enabled for the managed virtual network. Use workspace managed network isolation for a built-in frictionless network isolation method. Two patterns are available: allow internet outbound mode or allow only approved outbound mode. 

> [!NOTE]
> Securing your workspace with a managed virtual network provides network isolation for outbound access from the workspace and managed computes. An Azure Virtual Network that you create and manage provides network isolation for inbound access to the workspace. For example, you create a private endpoint for the workspace in your Azure Virtual Network. Any clients connecting to the virtual network can access the workspace through the private endpoint. When running jobs on managed computes, the managed network restricts what the compute can access. This configuration is different from the custom virtual network offering, which also requires setting a virtual network and setting all computes into that virtual network.

- __Allow internet outbound mode__: Use this option if you want to allow your machine learning engineers to access the internet freely. You can create other private endpoint outbound rules to let them access your private resources on Azure.

    :::image type="content" source="./media/how-to-network-isolation-planning/allow-internet-outbound-mode.png" alt-text="Diagram of a managed network configured as allow internet outbound mode.":::

- __Allow only approved outbound mode__: Use this option if you want to minimize data exfiltration risk and control what your machine learning engineers can access. You can control outbound rules by using private endpoint, service tag, and FQDN.

    :::image type="content" source="./media/how-to-network-isolation-planning/allow-only-approved-outbound-mode.png" alt-text="Diagram of a managed network with allow only approved outbound mode configured.":::

### Custom network isolation

If you have a specific requirement or company policy that prevents you from using a managed virtual network, use an Azure virtual network for network isolation. 

The following diagram is the recommended architecture to make all resources private but allow outbound internet access from your virtual network. This diagram describes the following architecture: 

- Put all resources in the same region.
- A hub virtual network, which contains your firewall and custom DNS set-up.
- A spoke virtual network, which contains the following resources:
    - A training subnet contains compute instances and clusters used for training ML models. These resources are configured for no public IP.
    - A scoring subnet contains an AKS cluster.
    - A 'pe' subnet contains private endpoints that connect to the workspace and private resources used by the workspace (storage, key vault, container registry, and more).
- To secure your managed online endpoints by using a custom virtual network, enable the legacy managed online endpoint managed virtual network. This method isn't recommended.  

This architecture balances your network security and your ML engineers' productivity.

:::image type="content" source="./media/how-to-network-isolation-planning/custom-network-diagram.png" alt-text="Diagram of a custom network isolation configuration.":::

> [!NOTE]
> To remove the firewall requirement, use network security groups and Azure Virtual Network NAT to allow internet outbound from your private compute resources.

#### Data exfiltration prevention

This diagram shows the recommended architecture to make all resources private and control outbound destinations to prevent data exfiltration. Use this architecture when using Azure Machine Learning with your sensitive data in production. This diagram describes the following architecture:

- Put all resources in the same region.
- A hub virtual network, which contains your firewall.
    - In addition to service tags, the firewall uses FQDNs to prevent data exfiltration.
- A spoke virtual network, which contains the following resources:
    - A training subnet contains compute instances and clusters used for training ML models. These resources are configured for no public IP. Additionally, a service endpoint and service endpoint policy are in place to prevent data exfiltration.
    - A scoring subnet contains an AKS cluster.
    - A 'pe' subnet contains private endpoints that connect to the workspace and private resources used by the workspace (storage, key vault, container registry, and more).
- Managed online endpoints use the private endpoint of the workspace to process incoming requests. A private endpoint is also used to allow managed online endpoint deployments to access private storage.

:::image type="content" source="./media/how-to-network-isolation-planning/custom-network-data-exfiltration.png" alt-text="Diagram of a custom network isolation configuration to prevent data exfiltration.":::

## Comparison of network isolation options

Managed network isolation and custom network isolation offer similar features. The following table describes the similarities and differences between the two offerings in terms of their set-up. The key difference in their set-up is where the virtual network for computes is hosted. For custom network isolation, the virtual network for computes is in your tenant. For managed network isolation, the virtual network for computes is in the Microsoft tenant.  

| Similarities | Differences |
| --- | --- |
| - You get a dedicated network that you don't share with other customers. </br>- Data is protected in the virtual network. </br>- You have full control on egress with outbound rules. </br>- Required ServiceTags. | - Where the virtual network is hosted; in your tenant for custom network isolation or in the Microsoft tenant for managed network isolation. |

To decide which networking set-up works best for your scenario, consider what features within Azure Machine Learning you want to use. For more information regarding the differences between the network isolation offerings, see [Compare network isolation configurations](concept-network-isolation-configurations.md).

### Comparison of configurations

| | Managed network (recommended) | Custom network |
| --- | --- | --- |
| __Benefits__ | - Minimize set-up and maintenance overhead. </br>- Supports managed online endpoints. </br>- Supports serverless spark. </br>- Access to HTTPS endpoint resources located on-premises or in your custom virtual network. </br>- Focus for new feature development. | - Customize network to your requirements. </br>- Bring your own non-Azure resources. </br>- Connect to on-premises resources. |
| __Limitations__ | - Extra costs for Azure Firewall and FQDN rules. </br>- Logging of the virtual network firewall and NSG rules isn't supported. </br>- Access to non-HTTPS endpoint resources isn't supported. | - New feature support might be delayed. </br>-Managed online endpoints aren't supported. </br>- Serverless spark isn't supported. </br>- Foundational models aren't supported. </br>- No code MLFlow isn't supported. </br>- Implementation complexity. </br>- Maintenance overhead. |

### Use a public workspace

You can use a public workspace if you're OK with Microsoft Entra ID authentication and authorization with conditional access. A public workspace has some features that allow using data in a private storage account. Use a private workspace if possible.

## Key considerations

### DNS resolution of private link resources and application on compute instance 

If you have your own DNS server hosted in Azure or on-premises, you need to create a conditional forwarder in your DNS server. The conditional forwarder sends DNS requests to the Azure DNS for all private link enabled PaaS services. For more information, see the [Azure Private Endpoint DNS integration scenarios](/azure/private-link/private-endpoint-dns-integration) and [Azure Machine Learning custom DNS configuration](how-to-custom-dns.md) articles. 

### Data exfiltration protection 

We have two types of outbound access: read-only and read/write. Bad actors can't exploit read-only outbound access, but they can exploit read/write outbound access. Azure Storage and Azure Frontdoor (the frontdoor.frontend service tag) are read/write outbound in our case. 

You can mitigate this data exfiltration risk by using our data exfiltration prevention solution. We use a service endpoint policy with an Azure Machine Learning alias to allow outbound access only to Azure Machine Learning managed storage accounts.

:::image type="content" source="./media/how-to-network-isolation-planning/data-exfiltration-protection-diagram.png" alt-text="Diagram of network with exfiltration protection configuration.":::

In this diagram, the compute instance and cluster need to access Azure Machine Learning managed storage accounts to get set-up scripts. When opening the outbound access to storage, you can use a service endpoint policy with the Azure Machine Learning alias to allow the storage access only to Azure Machine Learning storage accounts.

### Managed online endpoints

You configure security for inbound and outbound communication separately for managed online endpoints. 

- __Inbound communication__: Azure Machine Learning uses a private endpoint to secure inbound communication to a managed online endpoint. To prevent public access to an endpoint, set the public_network_access flag for the endpoint to disabled. When this flag is disabled, you can access your endpoint only via the private endpoint of your Azure Machine Learning workspace, and it can't be reached from public networks. 
- __Outbound communication__: To secure outbound communication from a deployment to resources, Azure Machine Learning uses a workspace managed virtual network. You need to create the deployment in the workspace managed virtual network so that it can use the private endpoints of the workspace managed virtual network for outbound communication. 

The following architecture diagram shows how communications flow through private endpoints to the managed online endpoint. Incoming scoring requests from a client's virtual network flow through the workspace's private endpoint to the managed online endpoint. Private endpoints from the workspace's managed virtual network handle outbound communication from deployments to services to those service instances.

:::image type="content" source="./media/concept-secure-online-endpoint/endpoint-network-isolation-with-workspace-managed-vnet.png" alt-text="Diagram showing inbound communication via a workspace private endpoint and outbound communication via private endpoints of a managed virtual network.":::

For more information, see [Network isolation with managed online endpoints](concept-secure-online-endpoint.md).

### Private IP address shortage in your main network

Azure Machine Learning requires private IPs - one IP for each compute instance, compute cluster node, and private endpoint. You also need many IPs if you use AKS. Your hub-spoke network connected with your on-premises network might not have a large enough private IP address space. In this scenario, you can use isolated, non-peered VNets for your Azure Machine Learning resources. 

:::image type="content" source="./media/how-to-network-isolation-planning/isolated-not-peered-network-diagram.png" alt-text="Diagram showing an isolated network configuration.":::

In this diagram, your main virtual network requires the IPs for private endpoints. You can have hub-spoke VNets for multiple Azure Machine Learning workspaces with large address spaces. A downside of this architecture is that it doubles the number of private endpoints.

### Network policy enforcement

To control network isolation parameters for self-service workspace and computing resources creation, use built-in policies or create a custom policy for more fine-grained controls. For more information on policies, see [Azure Policy regulatory compliance controls](security-controls-policy.md).  

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
