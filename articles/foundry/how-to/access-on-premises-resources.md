---
title: "Access on-premises resources from a Foundry managed network"
description: "Configure Azure Application Gateway to route traffic from a Microsoft Foundry managed virtual network to on-premises or non-Azure resources through a private endpoint."
manager: mcleans
ms.service: microsoft-foundry
ms.custom:
  - dev-focus
ms.topic: how-to
ms.date: 05/07/2026
ms.reviewer: meerakurup
ms.author: jburchel
author: jonburchel
ai-usage: ai-assisted
# Customer intent: As an admin, I want to let my Foundry managed network securely reach on-premises resources through Azure Application Gateway.
---

# Access on-premises resources from your Microsoft Foundry managed network

You can configure an Azure Application Gateway to let your managed virtual network in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) reach non-Azure resources in another virtual network or on-premises. The gateway provides a secure, private end-to-end path to those resources.

Azure Application Gateway is a load balancer that makes routing decisions based on the URL of an HTTPS request. For more information, see [What is Azure Application Gateway](/azure/application-gateway/overview).

Set up the application gateway in your Azure virtual network for inbound access to the Foundry resource. After you configure the gateway, create a private endpoint from the Foundry resource's managed virtual network to the gateway. The private endpoint keeps the entire end-to-end path private and off the internet.

To learn how Application Gateway secures connections to non-Azure resources, see [How an application gateway works](/azure/application-gateway/how-application-gateway-works).


## Prerequisites

- Set up your Foundry resource's managed virtual network and select an isolation mode: Allow Internet Outbound or Allow Only Approved Outbound. For more information, see [Managed virtual network isolation](managed-virtual-network.md).
- Get the resource's private HTTP(S) endpoint.
- Install the [Azure CLI](/cli/azure/install-azure-cli).
- Ensure the Foundry resource's managed identity can approve private endpoint connections on the target Application Gateway. Assign the [Azure AI Enterprise Network Connection Approver role](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-enterprise-network-connection-approver) (role ID: `b556d68e-0be0-4f35-a333-ad7ee1ce17ea`) on the Application Gateway resource.

## Create the private endpoint outbound rule

After you create an Azure Application Gateway with a private frontend IP configuration named `appGwPrivateFrontendIpIPv4`, add a private endpoint outbound rule from the Foundry resource's managed virtual network to the Application Gateway.

# [Azure CLI](#tab/azure-cli)

The following example adds or updates a private endpoint outbound rule to an Application Gateway. Replace the placeholder values with your own values.

```azurecli
az cognitiveservices account managed-network \
  outbound-rule set \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name} \
  --type privateendpoint \
  --destination '{
    "serviceResourceId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Network/applicationGateways/{app-gw-name}",
    "subresourceTarget": "appGwPrivateFrontendIpIPv4",
    "sparkEnabled": false
  }'
```

This command creates or updates a managed outbound rule and starts creating the managed private endpoint connection.

### References

- [az cognitiveservices account managed-network outbound-rule set](/cli/azure/cognitiveservices/account/managed-network/outbound-rule#az-cognitiveservices-account-managed-network-outbound-rule-set)

# [REST API](#tab/rest-api)

The following example creates or updates a private endpoint outbound rule to an Application Gateway by using the ARM REST API. Replace the placeholder values with your own values.

```azurecli
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/managedNetworks/default/outboundRules/{rule-name}?api-version=2025-10-01-preview" \
  --body '{
    "properties": {
      "type": "PrivateEndpoint",
      "destination": {
        "serviceResourceId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Network/applicationGateways/{app-gw-name}",
        "subresourceTarget": "appGwPrivateFrontendIpIPv4",
        "sparkEnabled": false
      }
    }
  }'
```

### References

- [Microsoft.CognitiveServices/accounts/managedNetworks/outboundRules](/azure/templates/microsoft.cognitiveservices/accounts/managednetworks/outboundrules)

---

After the rule is created, verify the private endpoint connection status:

```azurecli
az cognitiveservices account managed-network outbound-rule show \
  --resource-group {resource-group} \
  --name {account-name} \
  --rule {rule-name}
```

The connection status should show as **Approved**. If it shows **Pending**, verify that the Foundry resource's managed identity has the **Azure AI Enterprise Network Connection Approver** role on the Application Gateway.

## Add FQDN aliases for the private endpoint

After you create the private endpoint outbound rule, add FQDN aliases so the managed virtual network resolves them to the private endpoint IP address that targets the Application Gateway. FQDN aliases are required so your Foundry project can reach backend resources through the gateway by domain name.



> [!NOTE]
> - If you use an HTTPS listener with an uploaded certificate, make sure the FQDN alias matches the certificate CN (Common Name) or SAN (Subject Alternative Name), otherwise the HTTPS call fails because of SNI (Server Name Indication).
> - Each FQDN must have at least three labels to create the private DNS zone for the private endpoint to the Application Gateway.
> - Dynamic subresource naming isn't supported for the private frontend IP configuration. The frontend IP name must be `appGwPrivateFrontendIpIPv4`.

## Supported resources

Application Gateway supports any backend resource that uses HTTP or HTTPS. Application Gateway verifies connections from the managed virtual network to the following resources:

- JFrog Artifactory
- Snowflake
- Private APIs

Both L4 and L7 traffic are supported with Application Gateway.

> [!NOTE]
> There's no Azure portal UI support for creating managed network outbound rules yet. Use the Azure CLI or REST API to create the private endpoint outbound rule.

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

## Limitations

- Application Gateway supports only HTTP(S) endpoints in the backend pool. It doesn't support non-HTTP(S) network traffic. Ensure resources use the HTTP(S) protocol.
- When connecting to Snowflake through Application Gateway, add FQDN outbound rules to enable package and driver downloads and OCSP validation.
  - The Snowflake JDBC driver uses HTTPS, but other drivers can differ. Verify that your resource uses the HTTP(S) protocol.
- For more information, see [Frequently asked questions about Application Gateway](/azure/application-gateway/application-gateway-faq).

## Application Gateway errors

Troubleshoot Application Gateway connection errors to your backend resources:

- [Troubleshoot backend health issues in Application Gateway](/azure/application-gateway/application-gateway-backend-health-troubleshooting)
- [Troubleshooting bad gateway errors in Application Gateway](/azure/application-gateway/application-gateway-troubleshooting-502)
- [HTTP response codes in Application Gateway](/azure/application-gateway/http-response-codes)
- [Understanding disabled listeners](/azure/application-gateway/disabled-listeners)

## Related content

- [Managed virtual network isolation](managed-virtual-network.md)
- [Configure network isolation](configure-private-link.md)
