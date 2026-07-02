---
title: How to access on-premises resources
titleSuffix: Azure Machine Learning
description: Learn how to configure an Azure Machine Learning's managed network to securely allow access to your on-premises resources.
ms.service: azure-machine-learning
ms.topic: how-to
ms.date: 06/24/2026
ms.reviewer: meerakurup 
ms.author: scottpolly
author: s-polly
ai-usage: ai-assisted
ms.custom: dev-focus
# Customer intent: As an admin, I want to allow my developers to securely access on-premises resources from Azure Machine Learning.
---

# Access on-premises resources from your Azure Machine Learning workspace's managed network

To access your non-Azure resources located in a different virtual network or located entirely on-premises from your Azure Machine Learning workspace's managed virtual network, you must configure an Application Gateway. Through this Application Gateway, you can configure full end-to-end access to your resources.

Azure Application Gateway is a load balancer that makes routing decisions based on the URL of an HTTPS request. Azure Machine Learning supports using an application gateway to securely communicate with non-Azure resources. For more information about Application Gateway, see [What is Azure Application Gateway](/azure/application-gateway/overview).

To access on-premises or custom virtual network resources from the managed virtual network, you configure an Application Gateway on your Azure virtual network. You use the application gateway for inbound access to the workspace. Once configured, you create a private endpoint from the workspace's managed virtual network to the Application Gateway. By using the private endpoint, you secure the full end-to-end path and don't route it through the Internet.

:::image type="content" source="media/how-to-access-on-premises-resources/machine-learning-app-gateway.png" alt-text="Diagram of a managed network using Application Gateway to access on-premises resources." lightbox="media/how-to-access-on-premises-resources/machine-learning-app-gateway.png":::

## Prerequisites

- Read [How an application gateway works](/azure/application-gateway/how-application-gateway-works) to understand how Application Gateway secures the connection to your non-Azure resources.
- Set up your Azure Machine Learning workspace's managed virtual network and select your isolation mode: **Allow Internet Outbound** or **Allow Only Approved Outbound**. For more information, see [Managed virtual network isolation](how-to-managed-network.md).
- Get the private HTTP(S) endpoint of the resource you want to access.
- If you deploy the Application Gateway into a different subscription than your Azure Machine Learning workspace, register the `Microsoft.MachineLearningServices` resource provider on that subscription. Without this registration, you get a "resource was not found" error when you save the outbound rule.
- Assign the [Azure AI Enterprise Network Connection Approver](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-enterprise-network-connection-approver) built-in role (or a custom role with equivalent permissions) to the workspace's managed identity on the Application Gateway resource. After April 30, 2025, you must configure this assignment manually. For more information, see [Managed virtual network isolation](how-to-managed-network.md#prerequisites).

## Supported resources

Application Gateway supports any backend target resource that uses HTTP or HTTPS protocol. Connections to the following resources from the managed virtual network are verified:
- Jfrog Artifactory
- Snowflake Database 
- Private APIs

## Configure Azure Application Gateway

Follow the [Quickstart: Direct web traffic using the portal](/azure/application-gateway/quick-create-portal). To correctly set up your Application Gateway for use with Azure Machine Learning, use the following guidance when creating the Application Gateway:

1. From the __Basics__ tab:

    - Ensure your Application Gateway is in the same region as the selected Azure Virtual Network.
    - Azure Machine Learning only supports IPv4 for Application Gateway.
    - With your Azure Virtual Network, select one dedicated subnet for your Application Gateway. You can't deploy other resources in this subnet.

1. From the __Frontends__ tab, select or create a public IP address. You can add private IP addresses for the resources that the gateway connects to within the range of the subnet you selected on the Basics tab.

    > [!NOTE]
    > Application Gateway v2 now supports a private IP-only frontend configuration as a generally available capability. To use this option, register the `EnableApplicationGatewayNetworkIsolation` feature on your subscription before creating the gateway. See [Private Application Gateway deployment](/azure/application-gateway/application-gateway-private-deployment). If you don't register this feature, a public IP address is required.

1. From the __Backends__ tab, add your backend target to a backend pool. You can manage your backend targets by creating different backend pools. Request routing is based on the pools. You can add backend targets such as a Snowflake database. 

1. From the __Configuration__ tab, configure how requests are received with the frontend IPs and routed to the backend. 

    - In the __Listener__ section:
        - Create a listener by using either HTTP or HTTPS protocol and specify the port you want it to listen to. If you want two listeners listening on the same front-end IP address and routing to different backend pools, choose different ports. Incoming requests are differentiated based on ports.
        - If you want end-to-end TLS encryption, select HTTPS listener and upload your own certificate for Application Gateway to decrypt request received by listener. For more information, see [Enabling end to end TLS on Azure Application Gateway](/azure/application-gateway/ssl-overview#end-to-end-tls-encryption).
        - If you want a fully private backend target without any public network access, don't set up a listener on the public frontend IP address and its associated routing rule. Application Gateway only forwards requests that listeners receive at the specific port. If you want to avoid adding public frontend IP listener by mistake, see [Network security rules](/azure/application-gateway/configuration-infrastructure#network-security-groups) to fully lock down public network access.

    - In the __Backend targets__ section, if you want to use HTTPS and Backend server's certificate isn't issued by a well-known CA, you must upload the Root certificate (.CER) of the backend server. For more on configuring with a root certificate, see [Configure end-to-end TLS encryption using the portal](/azure/application-gateway/end-to-end-ssl-portal).

1. After you create the Application Gateway resource, go to the new Application Gateway resource in the Azure portal. Under __Settings__, select __Private link__ to enable a virtual network to privately access the Application Gateway through a private endpoint connection. The Private link configuration isn't created by default. 

    - Before adding the Private Link configuration, disable Private Link Service Network Policies on the dedicated Private Link subnet:

        ```azurecli
        az network vnet subnet update --name <subnet-name> --vnet-name <vnet-name> --resource-group <resource-group> --disable-private-link-service-network-policies yes
        ```

    - Select __+ Add__ to add the Private Link configuration, and then use the following values to create the configuration:
        - Name: Provide a name for your private link configuration. The combined length of the Application Gateway name and this configuration name must not exceed 70 characters.
        - Private link subnet: Select the dedicated subnet where you disabled network policies.
        - Frontend IP Configuration: `appGwPrivateFrontendIpIPv4`
    - To verify the Private link is set up correctly, go to the __Private endpoint connections__ tab and select __+ Private endpoint__. On the __Resource__ tab, the __Target sub-resource__ should be the name of your private Frontend IP configuration, `appGwPrivateFrontendIpIPv4`. If no value appears in the Target sub-resource,__ then the Application Gateway listener wasn't configured correctly. 

## Configure private link

1. After you create your Application Gateway's front-end IP and backend pools, configure the private endpoint from the managed virtual network to your Application Gateway. In the [Azure portal](https://portal.azure.com), go to your workspace's __Networking__ tab. Select __Workspace managed outbound access__, and then select __+ Add user-defined outbound rules__. 
1. In the __Workspace Outbound rules__ form, select the following options to create your private endpoint:

    - Rule name: Enter a name for your private endpoint to Application Gateway.
    - Destination Type: Private Endpoint
    - Subscription and Resource Group: Select the subscription and resource group where your Application Gateway is deployed.
    - Resource Type: `Microsoft.Network/applicationGateways`
    - Resource name: Enter the name of your Application Gateway resource.
    - Sub resource: `appGwPrivateFrontendIpIPv4`.
    - FQDNs: These FQDNs are the aliases that you want to use inside the Azure Machine Learning workspace. They're resolved to the managed private endpoint's private IP address targeting Application Gateway. You might include multiple FQDNs depending on how many resources you want to connect to with the Application Gateway.
      - All added FQDNs have the same IP address for the targeted Application Gateway.
      - The IP address is within the managed VNET range, not the customer's VNET range.

    > [!NOTE]
    > - If you use an HTTPS listener with a certificate you uploaded, make sure the FQDN alias matches the certificate's CN (Common Name) or SAN (Subject Alternative Name). Otherwise, the HTTPS call fails with SNI (Server Name Indication).
    > - The provided FQDNs must have at least three labels in the name to properly create the private DNS zone of the private endpoint for Application Gateway.
    > - You can edit the FQDNs field after the private endpoint creation through SDK or CLI. You can't edit the field in the Azure portal.
    > - The sub-resource name for the private endpoint must match the name of the private Frontend IP configuration you created on the Application Gateway. This article uses `appGwPrivateFrontendIpIPv4` as the example name. If you choose a different name when configuring the Application Gateway, use that name as the sub-resource value throughout.

### Configure using Python SDK and Azure CLI

To create a private endpoint to Application Gateway by using SDK, see [Azure SDK for Python](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination).

To create a private endpoint to Application Gateway by using the Azure CLI, use the `az ml workspace outbound-rule set` command. Set properties as needed for your configuration. For more information, see [Configure a managed network](how-to-managed-network.md?tabs=azure-cli).

## Limitations

- Application Gateway supports only HTTP(s) endpoints in the backend pool. It doesn't support non-HTTP(s) network traffic. Ensure your resources support the HTTP(S) protocol.
- To connect to Snowflake by using Application Gateway, add your own FQDN outbound rules to enable package or driver download and OCSP validation.
  - The Snowflake JDBC driver uses HTTPS calls, but different drivers might have different implementations. Check if your resource uses HTTP(S) protocol or not.
- Application Gateway isn't supported for Spark scenarios, such as Spark compute or serverless Spark compute. DNS resolution (for example, nslookup) fails when trying to resolve an FQDN from the Spark compute.
- For more information on limitations, see [Frequently asked questions about Application Gateway](/azure/application-gateway/application-gateway-faq).

## Application Gateway errors

For errors related to the Application Gateway connection to your backend resources, follow the existing Application Gateway documentation based on the errors you receive:

- [Troubleshoot backend health issues in Application Gateway](/azure/application-gateway/application-gateway-backend-health-troubleshooting)
- [Troubleshooting bad gateway errors in Application Gateway](/azure/application-gateway/application-gateway-troubleshooting-502)
- [HTTP response codes in Application Gateway](/azure/application-gateway/http-response-codes)
- [Understanding disabled listeners](/azure/application-gateway/disabled-listeners)

## Related content

- [Managed virtual network isolation](how-to-managed-network.md).
- [Managed computes in a managed virtual network](how-to-managed-network-compute.md).
