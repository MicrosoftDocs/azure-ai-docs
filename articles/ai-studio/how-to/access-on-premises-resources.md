---
title: How to access on-premises resources
titleSuffix: Azure AI Studio
description: Learn how to configure an Azure AI Studio managed network to securely allow access to your on-premises resources.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/22/2024
ms.reviewer: meerakurup 
ms.author: larryfr
author: Blackmist
# Customer intent: As an admin, I want to allow my developers to securely access on-premises resources from Azure AI Studio.
---

# Access on-premises resources from your Azure AI Studio's managed network (preview)

To access your non-Azure resources located in a different virtual network or located entirely on-premises from your Azure AI Studio's managed virtual network, an Application Gateway must be configured. Through this Application Gateway, full end to end access can be configured to your resources.

Azure Application Gateway is a load balancer that makes routing decisions based on the URL of an HTTPS request. Azure Machine Learning supports using an application gateway to securely communicate with the following resources. For more on Application Gateway, see [What is Azure Application Gateway](/azure/application-gateway/overview).

To access on-premises or custom virtual network resources from the managed virtual network, you configure an Application Gateway on your Azure virtual network. The application gateway is used for inbound access to the AI Studio's hub. Once configured, you then create a private endpoint from the Azure AI Studio hub's managed virtual network to the Application Gateway. With the private endpoint, the full end to end path is secured and not routed through the Internet.

## Prerequisites

- Read the [How an application gateway works](/azure/application-gateway/how-application-gateway-works) article to understand how the Application Gateway can secure the connection to your non-Azure resources. 
- Set up your Azure AI Studio hub's managed virtual network and select your isolation mode, either Allow Internet Outbound or Allow Only Approved Outbound. For more information, see [Managed virtual network isolation](configure-managed-network.md).
- Get the private HTTP(S) endpoint of the resource to access.

## Supported resources

Application Gateway is verified to support a private connection from the managed virtual network to:
- Jfrog Artifactory
- Snowflake Database
- Private APIs

## Configure Azure Application Gateway

Follow the [Quickstart: Direct web traffic using the portal](/azure/application-gateway/quick-create-portal). To correctly set up your Application Gateway for use with Azure Machine Learning, use the following guidance when creating the Application Gateway:

1. From the __Basics__ tab:

    - Ensure your Application Gateway is in the same region as the selected Azure Virtual Network.
    - Azure AI Studio only supports IPv4 for Application Gateway.
    - With your Azure Virtual Network, one subnet can only be associated with one Application Gateway.

1. From the __Frontends__ tab, Application Gateway doesn’t support private Frontend IP address only so Public IP addresses need to be selected or a new one created. Private IP addresses for the resources that the gateway connects to can be added within the range of the subnet you selected on the Basics tab.

1. From the __Backends__ tab, you can add your backend target to a backend pool. You can manage your backend targets by creating different backend pools. Request routing is based on the pools. You can add backend targets such as a Snowflake database. 

1. From the __Configuration__ tab, you configure how requests are received with the frontend IPs and routed to the backend. 

    - In the __Listener__ section:
        - You can create a listener with either HTTP or HTTPS protocol and specify the port you want it to listen to. If you want two listeners listening on the same front-end IP address and routing to different backend pools, you need to choose different ports. Incoming requests are differentiated based on ports.
        - If you want end-to-end TLS encryption, select HTTPS listener and upload your own certificate for Application Gateway to decrypt request received by listener. For more information, see [Enabling end to end TLS on Azure Application Gateway](/azure/application-gateway/ssl-overview#end-to-end-tls-encryption).
        - If you want a fully private backend target without any public network access, DO NOT setup a listener on the public frontend IP address and its associated routing rule. Application Gateway only forwards requests that listeners receive at the specific port. If you want to avoid adding public frontend IP listener by mistake, see [Network security rules](/azure/application-gateway/configuration-infrastructure#network-security-groups) to fully lock down public network access.

    - In the __Backend targets__ section, if you want to use HTTPS and Backend server’s certificate is NOT issued by a well-known CA, you must upload the Root certificate (.CER) of the backend server. For more on configuring with a root certificate, see Configure end-to-end TLS encryption using the portal.

## Configure private link

1. Now that your Application Gateway’s front-end IP and backend pools are created, you can now configure the private endpoint from the managed virtual network to your Application Gateway. in the [Azure portal](https://portal.azure.com), navigate to your Azure AI Studio hub's __Networking__ tab. Select __Workspace managed outbound access__, __+ Add user-defined outbound rules__. 
1. In the __Workspace Outbound rules__ form, select the following to create your private endpoint:

    - Rule name: Provide a name for your private endpoint to Application Gateway.
    - Destination Type: Private Endpoint
    - Subscription and Resource Group: Select the Subscription and Resource Group where your Application Gateway is deployed
    - Resource Type: `Microsoft.Network/applicationGateways`
    - Resource name: `appgateway`
    - Sub resource: `appGwPrivateFrontendIpIPv4` 
    - FQDNs: These FQDNs are the aliases that you want to use inside the Azure AI Studio. They're resolved to the managed private endpoint’s private IP address targeting Application Gateway. You might include multiple FQDNs depending on how many resources you would like to connect to with the Application Gateway.

    > [!NOTE]
    > If you are using HTTPS listener with certificate uploaded, make sure the FQDN alias matches with the certificate's CN (Common Name) or SAN (Subject Alternative Name) otherwise HTTPS call will fail with SNI (Server Name Indication).
    > The Application Gateway subresource name comes from the Application Gateway Listener which can be deleted after creation. ***

### Configure using Python SDK and Azure CLI

To create a private endpoint to Application Gateway with SDK, see [Azure SDK for Python](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination).

To create a private endpoint to Application Gateway with the Azure CLI, see [Configure a managed network](configure-managed-network.md?tabs=azure-cli).

## Limitations

- Application Gateway supports only HTTP(s) endpoints in the Backend pool. There's no support for non-HTTP(s) network traffic. Ensure your resources support HTTP(S) protocol.
- To connect to Snowflake using the Application Gateway, you should add your own FQDN outbound rules to enable package/driver download and OCSP validation.
  - The Snowflake JDBC driver uses HTTPS calls, but different drivers might have different implementations. Check if your resource uses HTTP(S) protocol or not.
- For more information on limitations, see [Frequently asked questions about Application Gateway](/azure/application-gateway/application-gateway-faq).

## Related content

- [Managed virtual network isolation](configure-managed-network.md)