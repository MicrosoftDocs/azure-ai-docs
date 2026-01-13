---
title: How to access on-premises resources
titleSuffix: Microsoft Foundry
description: Learn how to configure a Microsoft Foundry managed network to securely allow access to your on-premises resources.
manager: mcleans
ms.service: azure-ai-foundry
ms.custom:
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 01/06/2026
ms.reviewer: meerakurup 
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
# Customer intent: As an admin, I want to allow my developers to securely access on-premises resources from Microsoft Foundry.
---

# Access on-premises resources from your Microsoft Foundry managed network

[!INCLUDE [hub-only](../includes/uses-hub-only.md)]

You can configure an Azure Application Gateway to let your managed virtual network in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) reach non-Azure resources in another virtual network or on-premises. The gateway provides a secure, private end-to-end path to those resources.

Azure Application Gateway is a load balancer that makes routing decisions based on the URL of an HTTPS request. For more information, see [What is Azure Application Gateway](/azure/application-gateway/overview).

Set up the application gateway in your Azure virtual network for inbound access to the Foundry hub. After you configure the gateway, create a private endpoint from the hub's managed virtual network to the gateway. The private endpoint keeps the entire end-to-end path private and off the internet.

To learn how Application Gateway secures connections to non-Azure resources, see [How an application gateway works](/azure/application-gateway/how-application-gateway-works).

:::image type="content" source="../media/how-to/network/ai-studio-app-gateway.png" alt-text="Diagram that shows a managed virtual network using Azure Application Gateway and a private endpoint to reach on-premises resources securely." lightbox="../media/how-to/network/ai-studio-app-gateway.png":::

## Prerequisites

- Set up your Foundry hub's managed virtual network and select an isolation mode: Allow Internet Outbound or Allow Only Approved Outbound. For more information, see [Managed virtual network isolation](configure-managed-network.md).
- Get the resource's private HTTP(S) endpoint.
- To use the Azure CLI example in this article, install the [Azure CLI](/cli/azure/install-azure-cli) and the `ml` extension (version 2.15.0 or higher).
- To use the Python example in this article, install the [Azure SDK for Python](/python/api/overview/azure/ai-ml-readme) packages:
  - `pip install azure-ai-ml azure-identity`
- Ensure the hub's managed identity can approve private endpoint connections on the target Application Gateway. Assign the [Azure AI Enterprise Network Connection Approver role](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-enterprise-network-connection-approver) (or a custom role with equivalent permissions) on the Application Gateway resource.
- Ensure the identity you use to create outbound private endpoint rules has permissions to create private endpoint connections, including these Azure RBAC actions:
  - `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/read`
  - `Microsoft.MachineLearningServices/workspaces/privateEndpointConnections/write`

## Create the private endpoint outbound rule (Azure CLI or Python)

After you create an Azure Application Gateway with a private frontend IP configuration named `appGwPrivateFrontendIpIPv4`, add a private endpoint outbound rule from the Foundry hub's managed virtual network to the Application Gateway.

### Azure CLI

The following example adds or updates a private endpoint outbound rule to an Application Gateway. Replace the placeholder values with your own values.

```azurecli
az ml workspace outbound-rule set \
  --resource-group <resource-group> \
  --workspace-name <hub-name> \
  --rule <rule-name> \
  --type private_endpoint \
  --service-resource-id "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Network/applicationGateways/<APP_GW_NAME>" \
  --subresource-target appGwPrivateFrontendIpIPv4 \
  --spark-enabled false \
  --fqdns "contoso.com,contoso2.com"
```

This command creates or updates a managed outbound rule and starts creating the managed private endpoint connection.

### References

* [az ml workspace outbound-rule set](/cli/azure/ml/workspace/outbound-rule?view=azure-cli-latest&preserve-view=true#az-ml-workspace-outbound-rule-set)

### Python

The following example updates an existing hub and configures a private endpoint outbound rule to an Application Gateway. Replace the placeholder values with your own values.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import PrivateEndpointDestination
from azure.identity import DefaultAzureCredential

subscription_id = "<subscription-id>"
resource_group = "<resource-group>"
hub_name = "<hub-name>"

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=hub_name,
)

hub = ml_client.workspaces.get(name=hub_name)

hub.managed_network.outbound_rules = [
    PrivateEndpointDestination(
        name="<rule-name>",
        service_resource_id="/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Network/applicationGateways/<APP_GW_NAME>",
        subresource_target="appGwPrivateFrontendIpIPv4",
        spark_enabled=False,
        fqdns=["contoso.com", "contoso2.com"],
    )
]

ml_client.workspaces.begin_update(hub).result()
```

### References

* [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)
* [PrivateEndpointDestination](/python/api/azure-ai-ml/azure.ai.ml.entities.privateendpointdestination)

## Supported resources

Application Gateway supports any backend resource that uses HTTP or HTTPS. Application Gateway verifies connections from the managed virtual network to the following resources:
- JFrog Artifactory
- Snowflake
- Private APIs

## Configure Azure Application Gateway

Follow the [Quickstart: Direct web traffic using the portal](/azure/application-gateway/quick-create-portal). To correctly set up your Application Gateway for use with Foundry, use the following guidance when creating the Application Gateway:

1. On the __Basics__ tab, review and apply the following settings.

    - Ensure your Application Gateway is in the same region as the selected Azure Virtual Network.
    - Foundry supports only IPv4 for Application Gateway.
    - In your virtual network, select one dedicated subnet for Application Gateway. Don't deploy other resources in this subnet.

1. On the __Frontends__ tab, Application Gateway doesn't support only a private frontend IP address, so select or create a public IP address. Add private IP addresses for backend resources within the subnet range you selected on the Basics tab.

1. On the __Backends__ tab, add backend targets to backend pools for routing. Create different pools as needed (for example, a Snowflake database).

1. On the __Configuration__ tab, configure how frontend IPs receive requests and route them to the backend.

    - In the __Listener__ section:
        - Create a listener with HTTP or HTTPS and specify the listening port. To use two listeners on the same frontend IP that route to different backend pools, use different ports. Incoming requests are distinguished by port.
        - For end-to-end TLS encryption, select an HTTPS listener and upload your certificate so Application Gateway can decrypt the request received by the listener. For more information, see [Enabling end to end TLS on Azure Application Gateway](/azure/application-gateway/ssl-overview#end-to-end-tls-encryption).
        - For a fully private backend target without public network access, don't set up a listener on the public frontend IP address or its routing rule. Application Gateway forwards only requests that listeners receive on the specified port. To avoid adding a public frontend IP listener by mistake, see [Network security rules](/azure/application-gateway/configuration-infrastructure#network-security-groups) to lock down public network access.

    - In the __Backend targets__ section, if you use HTTPS and the backend server's certificate isn't issued by a well known CA, upload the root certificate (.CER) of the backend server. For more information, see [Configure end-to-end TLS encryption using the portal](/azure/application-gateway/end-to-end-ssl-portal).

1. After the Application Gateway resource is created, go to it in the Azure portal. Under __Settings__, select __Private link__ to enable private access through a private endpoint connection. The Private link configuration isn't created by default.

    - Select __+ Add__ to add the Private Link configuration, and then use the following values to create the configuration:
        - Name: Provide a name for your private link configuration
        - Private link subnet: Select a subnet in your virtual network
        - Frontend IP Configuration: `appGwPrivateFrontendIpIPv4`
    - To verify the Private link is set up correctly, go to the __Private endpoint connections__ tab and select __+ Private endpoint__. On the __Resource__ tab, the __Target sub-resource__ should be the name of your private frontend IP configuration, `appGwPrivateFrontendIpIPv4`. If no value appears in the __Target sub-resource__, the Application Gateway listener isn't configured correctly. For more information, see [Configure Azure Application Gateway Private Link](/azure/application-gateway/private-link-configure).

## Configure private link

1. After you create the Application Gateway frontend IP and backend pools, configure the private endpoint from the managed virtual network to the Application Gateway. In the [Azure portal](https://portal.azure.com), go to your Foundry hub, select __Networking__, then select __Workspace managed outbound access__ > __+ Add user-defined outbound rules__. 
1. In the __Workspace Outbound rules__ form, set the following values to create the private endpoint:

    - Rule name: Enter a name for the private endpoint to Application Gateway.
    - Destination Type: Private Endpoint
    - Subscription and Resource Group: Select the subscription and resource group where the Application Gateway is deployed.
    - Resource Type: `Microsoft.Network/applicationGateways`
    - Resource name: The name of your Application Gateway resource.
    - Subresource: `appGwPrivateFrontendIpIPv4`
    - FQDNs: Enter the FQDN aliases to use in the Foundry portal. They're resolved to the managed private endpoint private IP address that targets the Application Gateway. Add multiple FQDNs if you need to reach multiple resources through the Application Gateway.
      - All added FQDNs use the same IP address for the targeted Application Gateway.
      - The IP address is in the managed virtual network range, not the customer's VNet range.

    > [!NOTE]
    > - If you use an HTTPS listener with an uploaded certificate, make sure the FQDN alias matches the certificate CN (Common Name) or SAN (Subject Alternative Name), otherwise the HTTPS call fails because of SNI (Server Name Indication).
    > - Each FQDN must have at least three labels to create the private DNS zone for the private endpoint to the Application Gateway.
    > - You can edit the FQDNs field after you create the private endpoint by using the SDK or CLI. You can't edit it in the Azure portal.
    > - Dynamic subresource naming isn't supported for the private frontend IP configuration. The frontend IP name must be `appGwPrivateFrontendIpIPv4`.

### Configure by using the Python SDK and Azure CLI

To create the private endpoint outbound rule by using the Azure CLI or Python, see [Create the private endpoint outbound rule (Azure CLI or Python)](#create-the-private-endpoint-outbound-rule-azure-cli-or-python).

## Limitations

- Application Gateway supports only HTTP(S) endpoints in the backend pool. It doesn't support non-HTTP(S) network traffic. Ensure resources use the HTTP(S) protocol.
- When connecting to Snowflake through Application Gateway, add FQDN outbound rules to enable package and driver downloads and OCSP validation.
  - The Snowflake JDBC driver uses HTTPS, but other drivers can differ. Verify that your resource uses the HTTP(S) protocol.
- Application Gateway doesn't support Spark scenarios such as Spark compute or serverless Spark compute. DNS resolution (for example, with nslookup) fails when resolving an FQDN from Spark compute.
- For more information, see [Frequently asked questions about Application Gateway](/azure/application-gateway/application-gateway-faq).

## Application Gateway errors

Troubleshoot Application Gateway connection errors to your backend resources:

- [Troubleshoot backend health issues in Application Gateway](/azure/application-gateway/application-gateway-backend-health-troubleshooting)
- [Troubleshooting bad gateway errors in Application Gateway](/azure/application-gateway/application-gateway-troubleshooting-502)
- [HTTP response codes in Application Gateway](/azure/application-gateway/http-response-codes)
- [Understanding disabled listeners](/azure/application-gateway/disabled-listeners)

## Related content

- [Managed virtual network isolation](configure-managed-network.md)
