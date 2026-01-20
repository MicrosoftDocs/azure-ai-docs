---
title: Compare network isolation configurations
title-suffix: Azure Machine Learning
description: "Azure Machine Learning can use both managed and custom virtual networks for network isolation. Learn about the differences between the two configurations."
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
ms.service: azure-machine-learning
ms.topic: concept-article #Don't change.
ms.date: 11/14/2025

#customer intent: As an administrator, I want to understand the network isolation options so that I can plan my infrastructure.

---

# Compare network isolation configurations in Azure Machine Learning

For your workspaces, Azure Machine Learning offers two types of outbound network isolation configurations: managed network isolation and custom network isolation. Both types offer full network isolation support with benefits and limitations. This article covers feature support and limitations for both network isolation configurations to help you decide what works best for your needs.

## Enterprise security needs

Cloud computing enables you to scale up your data and machine learning capabilities, but it also poses new challenges and risks for security and compliance. You need to ensure that your cloud infrastructure is protected from unauthorized access, tampering, or leakage of data and models. You might also need to adhere to the regulations and standards that apply to your industry and domain.  

Typical enterprise requirements include:  

- Use a network isolation boundary with a virtual network to have inbound and outbound control and to have a private connection to private Azure resources.
- Avoid exposure to the internet with no public IP solutions and private endpoints.
- Use virtual network appliances to have better network security capabilities such as firewalling, intrusion detection, vulnerability management, and web filtering.
- Integrate network architecture for Azure Machine Learning with existing network architecture.

## What are managed and custom network isolation configurations?

__Managed network isolation__ relies on managed virtual networks, which is a fully managed feature of Azure Machine Learning. Managed network isolation is ideal if you want to use Azure Machine Learning with minimal configuration and management overhead. 

__Custom network isolation__ relies on you creating and managing an Azure Virtual Network. This configuration is ideal if you want maximal control over your network configuration.

## When to use managed or custom virtual networks

Use managed virtual network when… 
- You're new user to Azure Machine Learning with standard network isolation requirements
- You're a company with standard network isolation requirements
- You require on-premises access to resources with HTTP/S endpoints
- You don't have many non-Azure dependencies set up yet
- You require using Azure Machine Learning managed online endpoints and serverless spark computes
- You have fewer management requirements for networking in your organization

Use custom virtual network when… 
- You're a company with heavy network isolation requirements
- You have many non-Azure dependencies previously set-up and need to access Azure Machine Learning
- You have on-premises databases with no HTTP/S endpoints
- You require using your own Firewall and virtual network logging and monitoring of outbound network traffic
- You want to use Azure Kubernetes Services (AKS) for inference workloads

The following table provides a comparison of the benefits and limitations of managed and custom virtual networks:

| | Custom virtual network | Managed virtual network |
| --- | --- | --- |
| __Benefits__ | - You can tailor networking to your existing set-up</br>- Bring your own non-Azure resources with Azure Machine Learning</br>- Connect to on-premises resources | - Minimize set-up and maintenance overhead</br>- Supports managed online endpoints</br>- Supports serverless spark</br>- Gets new features first |
| __Limitations__ | - New feature support might be delayed</br>- Managed online endpoints NOT supported</br>- Serverless spark NOT supported</br>- Foundational models NOT supported</br>- No code MLFlow NOT supported</br>- Implementation complexity</br>- Maintenance overhead | - Cost implications of the Azure Firewall and fully qualified domain name (FQDN) rules</br>- Logging of the virtual network, firewall, and NSG rules NOT supported</br>- Access to non-HTTP/S endpoint resources NOT supported |

### Custom virtual network limitations

- __New features support might be delayed__: Efforts for improving our network isolation offerings focus on managed virtual networks instead of custom virtual networks. Therefore, we prioritize new feature requests for managed virtual networks over custom virtual networks.
- __Managed online endpoints aren't supported__: Managed online endpoints don't support custom virtual networks. You must enable workspace managed virtual network to secure your managed online endpoints. You can secure managed online endpoints with the legacy network isolation method. But, we strongly recommend that you use workspace managed network isolation. For more information, see [Managed online endpoints](concept-endpoints-online.md).
- __Serverless Spark compute isn't supported__: Serverless Spark computes aren't supported in a custom virtual network. Workspace managed virtual network supports Serverless Spark because Azure Synapse only uses managed virtual network set-up. For more information, see [Configured Serverless Spark](apache-spark-azure-ml-concepts.md#serverless-spark-compute).
- __Implementation complexity and maintenance overhead__: With custom virtual network set-up, you handle all the complexity of setting up a virtual network, subnet, private endpoints, and more. You also maintain the network and computes.

### Managed virtual network limitations

- __Cost implications with Azure Firewall and FQDN rules__: An Azure Firewall is provisioned on your behalf only when you create a user-defined FQDN outbound rule. The Azure Firewall is the Standard SKU Firewall and incurs costs that are added to your billing. For more information, see [Azure Firewall pricing](https://azure.microsoft.com/pricing/details/azure-firewall). 
- __Logging and monitoring of managed virtual network NOT supported__: The managed virtual network doesn't support virtual network flow, NSG flow, or Firewall logs. This limitation exists because the managed virtual network is deployed in a Microsoft tenant and can't send logs to your subscription. 
- __Access to non-Azure, non-HTTP/S resources isn't supported__: The managed virtual network doesn't allow access to non-Azure, non-HTTP/S resources.

## Related content

- [Plan for network isolation](how-to-network-isolation-planning.md)
- [Use a managed virtual network](how-to-managed-network.md)
- [Use a custom virtual network](how-to-network-security-overview.md)