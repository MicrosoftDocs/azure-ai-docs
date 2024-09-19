---
title: Compare network isolation configurations
title-suffix: Azure Machine Learning
description: "Azure Machine Learning can use both managed and custom virtual networks for network isolation. Learn about the differences between the two configurations."
author: Blackmist
ms.author: larryfr
ms.reviewer: meerakurup
ms.service: azure-machine-learning
ms.topic: concept-article #Don't change.
ms.date: 09/19/2024

#customer intent: As an administrator, I want to understand the network isolation options so that I can plan my infrastructure.

---

# Compare network isolation configurations in Azure Machine Learning

For your workspaces, Azure Machine Learning offers two types of outbound network isolation configurations: managed network isolation and custom network isolation. Both offer full network isolation support with its benefits and limitations. This document covers feature support and limitations on both network isolation configurations for you to decide what is best for your needs.

Managed network isolation relies on managed virtual networks, which is a fully managed feature of Azure Machine Learning. Managed network isolation is ideal for users who want to use Azure Machine Learning with minimal configuration and management overhead. Custom network isolation relies on you creating and managing an Azure Virtual Network, which is ideal for customers looking for maximal control over their network configuration.

## Enterprise security needs

Cloud computing enables enterprises to scale up their data and machine learning capabilities, but it also poses new challenges and risks for security and compliance. Enterprises need to ensure that their cloud infrastructure is protected from unauthorized access, tampering, or leakage of data and models. They also need to adhere to the regulations and standards that apply to their industry and domain.  

Typical Enterprise requirements include:  

- Use network isolation boundary with virtual network to have inbound and outbound control and to have private connection to private azure resources.
- Avoid exposure to the internet with no public IP solutions and private endpoints.
- Use virtual network appliances to have better network security capabilities such as firewalling, intrusion detection, vulnerability management, web filtering.
- Network architecture for AzureML can be integrated with existing network architecture.

## What is a managed or custom virtual network

[Describe a main idea.]

## When to use managed or custom virtual networks

[Describe a main idea.]

<!-- Required: Main ideas - H2

Use one or more H2 sections to describe the main ideas
of the concept.

Follow each H2 heading with a sentence about how
the section contributes to the whole. Then, describe 
the concept's critical features as you define what it is.

-->

## Related content

- [Related article title](link.md)
- [Related article title](link.md)
- [Related article title](link.md)

<!-- Optional: Related content - H2

Consider including a "Related content" H2 section that 
lists links to 1 to 3 articles the user might find helpful.

-->

<!--

Remove all comments except the customer intent
before you sign off or merge to the main branch.

-->