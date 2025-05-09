---

title: Create a secure hub
titleSuffix: Azure AI Foundry
description: Create an Azure AI Foundry hub inside a managed virtual network. The managed virtual network secures access to managed resources such as computes.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 05/09/2025
ms.reviewer: meerakurup 
ms.author: larryfr
author: Blackmist
# Customer intent: As an administrator, I want to create a secure hub and project with a managed virtual network so that I can secure access to the Azure AI Foundry hub and project resources.

---

# How to create a secure Azure AI Foundry hub and project with a managed virtual network

> [!NOTE]
> The information provided in this article is specific to a **[!INCLUDE [hub](../includes/hub-project-name.md)]**, and doesn't apply for a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

You can secure your [Azure AI Foundry](https://ai.azure.com) hub, projects, and managed resources in a managed virtual network. With a managed virtual network, inbound access is only allowed through a private endpoint for your hub. Outbound access can be configured to allow either all outbound access, or only allowed outbound that you specify. For more information, see [Managed virtual network](configure-managed-network.md).

> [!IMPORTANT]
> The managed virtual network doesn't provide inbound connectivity for your clients. For more information, see the [Connect to the hub](#connect-to-the-hub) section. 

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free) before you begin.
- An Azure Virtual Network that you use to securely connect to Azure services. For example, you might use [Azure Bastion](/azure/bastion/bastion-overview), [VPN Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) or [ExpressRoute](/azure/expressroute/expressroute-introduction) to connect to the Azure Virtual Network from your on-premises network. If you don't have an Azure Virtual Network, you can create one by following the instructions in [Create a virtual network](/azure/virtual-network/quick-create-portal).

## Create a hub

1. From the Azure portal, search for `Azure AI Foundry`. From the left menu, select **AI Hubs**, and then select **+ Create** and **Hub**.

    :::image type="content" source="../media/how-to/hubs/create-hub.png" alt-text="Screenshot of the Azure AI Foundry portal." lightbox="../media/how-to/hubs/create-hub.png":::

1. Enter your hub name, subscription, resource group, and location details. For **Azure AI services base models**, select an existing AI services resource or create a new one. Azure AI services include multiple API endpoints for Speech, Content Safety, and Azure OpenAI. 
    
    :::image type="content" source="../media/how-to/network/ai-hub-basics.png" alt-text="Screenshot of the option to set hub basic information." lightbox="../media/how-to/network/ai-hub-basics.png":::

1. Select the **Storage** tab. Select an existing **Storage account** and **Credential store** resource or create new ones. Optionally, choose an existing **Application insights**, and **Container Registry** for logs and docker images.

    :::image type="content" source="../media/how-to/network/ai-hub-storage.png" alt-text="Screenshot of the Create a hub with the option to set storage resource information." lightbox="../media/how-to/network/ai-hub-storage.png"::: 

1. Select the **Inbound access** tab to configure network isolation for inbound traffic to the hub. Set **Public network access** to **Disabled**, and then use **+ Add** to add a private endpoint for the hub to an Azure Virtual Network that your clients connect to. The private endpoint allows your clients to connect to the hub over a private connection. For more information, see [Private endpoints](/azure/private-link/private-endpoint-overview).
 
    :::image type="content" source="../media/how-to/network/inbound-access.png" alt-text="Screenshot of the inbound access tab with public network access disabled." lightbox="../media/how-to/network/inbound-access.png":::

1. Select the **Outbound access** to configure the managed virtual network that Azure AI Foundry uses to secure its hub and projects. Select **Private with Internet Outbound**, which allows compute resources to access the public internet for resources such as Python packages.
    
    > [!TIP]
    > To provision the virtual network during hub creation, select **Provision managed virtual network**. If this option isn't selected, the network isn't provisioned until you create a compute resource. For more information, see [Managed virtual network](configure-managed-network.md#manually-provision-a-managed-vnet).

    :::image type="content" source="../media/how-to/network/outbound-access.png" alt-text="Screenshot of the Create a hub with the option to set network isolation information." lightbox="../media/how-to/network/outbound-access.png":::

1. Select **Review + create**, then **Create** to create the hub. Once the hub is created, any projects or compute instances created from the hub inherit the network configuration.

## Connect to the hub

The managed virtual network doesn't directly provide access to your clients. Instead, your clients connect to an Azure Virtual Network that *you* manage. They can then access the hub using the private endpoint you created in these steps.

There are multiple methods that you might use to connect clients to the Azure Virtual Network. The following table lists the common ways that clients connect to an Azure Virtual Network:

| Method | Description |
| ----- | ----- |
| [Azure VPN gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) | Connects on-premises networks to an Azure Virtual Network over a private connection. Connection is made over the public internet. |
| [ExpressRoute](https://azure.microsoft.com/services/expressroute/) | Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider. |
| [Azure Bastion](/azure/bastion/bastion-overview) | Connects to a virtual machine inside the Azure Virtual Network using your web browser. |

## Next steps

- [Create a project](create-projects.md)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about Azure AI Foundry hubs](../concepts/ai-resources.md)
