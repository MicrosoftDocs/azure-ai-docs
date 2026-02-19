---
title: 'Securing Azure OpenAI inside a virtual network with private endpoints'
titleSuffix: Azure OpenAI
description: How to secure your Azure OpenAI resource inside a virtual network with private endpoints
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 11/26/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Configure Azure OpenAI networking

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, learn how to create and connect to a secure Azure OpenAI resource. The steps in this article use an Azure Virtual Network to create a security boundary for your Azure OpenAI resource.

After completing this article, you'll have the following architecture:

- An Azure Virtual Network, with a subnet where your Azure OpenAI resource will reside.
- An Azure OpenAI resource that uses a private endpoint to communicate using the virtual network.
- Azure Bastion, which allows you to use your browser to securely communicate with the jump box VM inside the virtual network.
- An Azure Virtual Machine that you can remotely connect to and access resources secured inside the virtual network.

## Prerequisites

Familiarity with Azure Virtual Networks and IP networking. If you aren't familiar, try the [Fundamentals of computer networking module](/training/modules/network-fundamentals/).  

For more on networking in Azure OpenAI resource, see [Configure Virtual Networks](/azure/ai-services/cognitive-services-virtual-networks).

## Create a virtual network

To create a virtual network, use the following steps:

1. In the [Azure portal](https://portal.azure.com), select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Virtual Network** in the search field. Select the Virtual Network entry, and then select **Create**.
2. From the **Basics** tab, select the Azure subscription to use for this resource and then select or create a new resource group. Under Instance details, enter a friendly name for your virtual network and select the region to create it in.

    :::image type="content" source="../media/how-to/network/network-basics.png" alt-text="Screenshot of virtual network setup." lightbox="../media/how-to/network/network-basics.png":::

1. Accept the default settings for **Security** and IP **addresses**. A subnet titled "default" will be created for your virtual network. Best practice is to create another subnet to delegate all private endpoints.
1. Select **Review + create**.
1. Verify that the information is correct, and then select **Create**.

## Create an Azure OpenAI resource

1. In the Azure portal, select the portal menu in the upper left corner. From the menu, select **+ Create a resource** and then enter **Azure OpenAI**. Select the Azure OpenAI entry, and then select **Create**.
2. From the Basics tab, select the Azure subscription to use for this resource and then select or create a new resource group. Under Instance details, enter a friendly name for your resource and select the region to create it in. The Azure OpenAI resource does not to be in the same region as your virtual network.
3. Select **Review + create**.

## Create a private endpoint and private DNS zone

1. In the Azure portal, select the Azure OpenAI resource you created. In Resource Management, navigate to the Networking tab.
2. Under Allow access from, select Disabled. Disabled ensures no networks can access this resource. Private endpoint connections will be the exclusive way to access this resource. Select Save to save the settings.

    :::image type="content" source="../media/how-to/network/network-disabled.png" alt-text="Screenshot of resource network disabled UX." lightbox="../media/how-to/network/network-disabled.png":::

1. Navigate to the Private endpoint connections tab and select **+ Private endpoint**. 

    :::image type="content" source="../media/how-to/network/private-endpoint.png" alt-text="Screenshot of private endpoint connections tab." lightbox="../media/how-to/network/private-endpoint.png":::

1. From the Basics tab, select the Azure subscription to use for this resource and then select or create a new resource group. Under Instance details, enter a name for your resource and select the region to create it in. The region you create the private network in must be the same as the region you chose to create your virtual network in. The network interface name will automatically use the name and will add "-nic".

    :::image type="content" source="../media/how-to/network/create-private-endpoint.png" alt-text="Screenshot of create private endpoint." lightbox="../media/how-to/network/create-private-endpoint.png":::

1. From the Resource tab, the Resource type should be `Microsoft.CognitiveServices/accounts`. For Target sub-resource, select **account**.

1. From the Virtual Network tab, use the following values:
   - Virtual network: The virtual network you created earlier.
   - Subnet: default

1. From the DNS tab, use the following values if you would like to use Azure Private DNS instead of custom DNS: 
   - Integrate with private DNS zone: Yes
   - Configurations name: privatelink-openai-azure-com
   - Subscription: The same Azure subscription that contains the previous resources.
   - Resource group: The same Azure resource group that contains the previous resources.

    :::image type="content" source="../media/how-to/network/create-private-link.png" alt-text="Screenshot of create private link DNS tab." lightbox="../media/how-to/network/create-private-link.png":::

1. Select **Review + create**. Verify that the information is correct, and then select **Create**.

1. Once the private endpoint is created, you should see your private endpoint connection name, state, and description. You can select the link to the private endpoint and view further details on its DNS configuration.

    
    :::image type="content" source="../media/how-to/network/deployment-details.png" alt-text="Screenshot of deployment details post private link and endpoint deployment." lightbox="../media/how-to/network/deployment-details.png":::

## Configure gateway and client for local network access

To access the Azure OpenAI in Microsoft Foundry Models from your local or on-premises client machines, there are two approaches. One approach is to configure a virtual machine deployed in the same virtual network. Another approach is to configure Azure VPN Gateway and Azure VPN Client.

For guidelines to set up a virtual network gateway for your virtual network, see [Tutorial – Create & manage a VPN gateway](/azure/vpn-gateway/tutorial-create-gateway-portal#VNetGateway). To add point-to-site configuration, and enable Microsoft Entra ID based authentication, see [Configure a VPN gateway for Microsoft Entra ID](/azure/vpn-gateway/openvpn-azure-ad-tenant#enable-authentication) authentication. Download the Azure VPN Client profile configuration package, unzip, and import the AzureVPN/azurevpnconfig.xml file to your Azure VPN client.

Configure your local machine hosts file to point your resources host names to the private IPs in your virtual network. The hosts file is located at C:\Windows\System32\drivers\etc for Windows, and at /etc/hosts on Linux. Example: 10.0.0.5 contoso.openai.azure.com

## Configure access through another hub and spoke architecture

A common networking architecture adopted by enterprises is the Hub-spoke network topology. In this networking topology, the hub virtual network is the central network zone to control all ingress and egress traffic to the Internet while the spoke virtual network are host different types of workloads. Then, the hub and spoke virtual networks are peered. Peering is a networking feature that allows seamless connectivity between two Azure Virtual Networks in the same region or across different regions. Peering facilitates the sharing of resources, data, and services between virtual networks, enhancing application deployment flexibility and streamlining network architecture.

To set up a basic hub and spoke architecture:

1. Create a second virtual network in your Azure Subscription, your spoke virtual network. This virtual network does not need to be in the same region.
2. In Settings, navigate to the **Peerings** tab. Select **+ Add**.
3. Under Remote virtual network summary, provide a Peering Link Name and select the virtual network you will peer, in this case the Hub virtual network. Ensure `"Allow <hub virtual network name> to access <spoke virtual network name>"` is selected.
4. Under Local virtual network summary, provide a Peering Link Name and ensure `"Allow <hub virtual network name> to access <spoke virtual network name>"` is selected. Then select Add. 

## Configure your Network Security Group (NSG)

Network Security Groups are used to control inbound and outbound traffic to network interfaces (NIC), VMs and subnets. You will need to configure NSG to allow traffic to and from Azure OpenAI. For more on configuring NSGs, see [Azure network security groups overview](/azure/virtual-network/network-security-groups-overview).

## Testing your configuration

You can test the network connection to Azure OpenAI using the Test-NetConnection cmdlet in PowerShell. This cmdlet allows you to test the network connection between your machine and another machine. It's a useful tool for network troubleshooting and debugging.

1. Resolve the IP Address: Use the nslookup command to resolve the IP address of your Azure OpenAI endpoint. For example:

   ```cmd
   nslookup my-openai-instance.openai.azure.com
   ```

   This will return both public and private IP addresses associated with your Azure OpenAI instance. Your private IP address should be the same as the private IP seen in the DNS configuration of your private endpoint. 

2. Test Private Endpoint: Next, test the network connection to the private IP address on port 443. For example:

   ```powershell
   Test-NetConnection 10.0.0.4 -Port 443
   ```

This command should succeed only from a machine that is on the same private network as your Azure OpenAI instance. If this command fails, it means there is a networking issue. Here are some possible causes:

- DNS Issue: The Domain Name System (DNS) is responsible for translating domain names into IP addresses. If there's an issue with the DNS, it might not be able to correctly resolve the domain name of your Azure OpenAI instance to its IP address.

- Machine Not on Private Network: If the machine you're running the command on is not on the same private network as your Azure OpenAI instance, the command will fail because it won't be able to reach the private IP address. Make sure that the machine is connected to the correct private network.

- Customer Firewall Blocking: If there's a custom firewall set up between the machine and the Azure OpenAI instance, it might be blocking the connection. Firewalls are security measures that control incoming and outgoing network traffic based on predetermined security rules. You will need to check your firewall settings and make sure that traffic on port 443 is allowed.

## Next steps

- Explore the [Azure security baseline for Azure OpenAI](/security/benchmark/azure/baselines/azure-openai-security-baseline#virtual-network-integration)
- Learn how to [Configure Virtual Networks for Azure OpenAI](/azure/ai-services/cognitive-services-virtual-networks?tabs=portal)
- [Azure OpenAI Private Endpoints: Connecting Across VNETs | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/azurearchitectureblog/azure-openai-private-endpoints-connecting-across-vnet%E2%80%99s/3913325)