---
title: Add an Azure OpenAI network security perimeter
description: Use this article to learn about adding Azure OpenAI to your network security perimeter.
ms.date: 11/20/2025
ms.topic: how-to
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
---

# Add an Azure OpenAI service to a network security perimeter (preview)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

> [!IMPORTANT]
> * Azure OpenAI service support for network security perimeter is in public preview under supplemental terms of use. It's available in regions providing the feature. This preview version is provided without a service level agreement, and it's not recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> * Review the [limitations and considerations](#limitations-and-considerations) section before you start.

## Overview
This article explains how to join an Azure OpenAI service to a network security perimeter to control network access to your Azure OpenAI account. By joining a network security perimeter, you can:
- Log all access to your account in context with other Azure resources in the same perimeter.
- Block any data exfiltration from the account to other services outside the perimeter.
- Allow access to your account using inbound and outbound access capabilities of the network security perimeter.

You can add an Azure OpenAI service to a network security perimeter in the Azure portal, as described in this article. Alternatively, you can use the Azure Virtual Network Manager REST API to join a service, and use the Management REST APIs to view and synchronize the configuration settings.

## Limitations and considerations
* Azure OpenAI customer-managed keys might not behave as expected. The Azure OpenAI resources in the Azure subscription might not be able to use the fine-tune API or assistants API.

* Network security perimeter controls only data plane operations within Azure OpenAI, not control plane operations. For example, users can deploy a model within their Azure OpenAI resource secured by the perimeter, but cannot use fine-tuned models, upload files, or start a session in the Chat Playground. In these data plane scenarios, an error message will show that access is blocked by the Network Security Perimeter, as expected.

* For an Azure OpenAI service within a network security perimeter, the resource must use a system or user-assigned managed identity and have a role assignment that permits read-access to data sources.

* Consider securing with a network security perimeter when configuring Azure Blob Storage for Azure OpenAI. Azure OpenAI now supports using Azure Blob Storage for Azure OpenAI Batch input and output files. Secure communications with Blob Storage and Azure OpenAI by placing both resources in the same perimeter. For more on the Azure OpenAI Batch and Blob Storage scenario, see [Configuring Azure Blob Storage for Azure OpenAI](batch-blob-storage.md).


## Prerequisites

> [!CAUTION] 
> Make sure you fully understand the limitations and impact to your Azure Subscription listed in the previous section before registering the preview feature.

Register the network security perimeter feature from the Azure portal preview features. The feature names are the following:
* `OpenAI.NspPreview`
* `AllowNSPInPublicPreview`

Or use the following CLI commands to register the two Preview features
* `az feature registration create  --name OpenAI.NspPreview --namespace Microsoft.CognitiveServices`
* `az feature registration create  --name AllowNSPInPublicPreview --namespace Microsoft.Network`

Ensure the `Microsoft.CognitiveServices` and `Microsoft.Network` providers are registered. To check if the feature flags are allowlisted, use command `az feature registration list`.

### Configure managed identity on your Azure OpenAI account
To allow your Storage account to recognize your Azure OpenAI service via Microsoft Entra ID authentication, you need to enable the managed identity for your Azure OpenAI service. The easiest way is to toggle on system assigned managed identity on Azure portal. The required role for your Storage account is “Storage Blob Data Contributor.” Ensure the role is assigned to your Storage account from your Azure OpenAI account.

## Assign an Azure OpenAI account to a network security perimeter
Azure Network Security Perimeter allows administrators to define a logical network isolation boundary for PaaS resources (for example, Azure Storage and Azure SQL Database) that are deployed outside virtual networks. It restricts communication to resources within the perimeter, and it allows non-perimeter public traffic through inbound and outbound access rules.

You can add Azure OpenAI to a network security perimeter so that all requests occur within the security boundary.

1. In the Azure portal, find the network security perimeter service for your subscription.
2. Select **Associated Resources** from the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/associated-resources-selection.png" alt-text="A screenshot showing the associated resources selection in the left navigation menu." lightbox="../media/network-security-perimeter/associated-resources-selection.png":::

3. Select **Add** > **Associate resources with an existing profile**.


    :::image type="content" source="../media/network-security-perimeter/add-associated-resources.png" alt-text="A screenshot showing the button to add associated resources." lightbox="../media/network-security-perimeter/add-associated-resources.png":::

4. Select the profile you created when you created the network security perimeter for a profile.
5. Select **Associate**, and then select the Azure OpenAI service you created.

    :::image type="content" source="../media/network-security-perimeter/associate-with-profile.png" alt-text="A screenshot showing the screen for associating resources with a profile." lightbox="../media/network-security-perimeter/associate-with-profile.png":::



6. Select Associate in the bottom left-hand section of the screen to create the association.

### Network security perimeter access modes
Network security perimeter supports two different access modes for associated resources:


|Mode |Description  |
|---------|---------|
|Learning mode     | This is the default access mode. In learning mode, network security perimeter logs all traffic to the Azure OpenAI service that would have been denied if the perimeter was in enforced mode. This allows network administrators to understand the existing access patterns of the Azure OpenAI service before implementing enforcement of access rules. |
|Enforced mode   | In Enforced mode, network security perimeter logs and denies all traffic that isn't explicitly allowed by access rules.        |

### Network security perimeter and Azure OpenAI service networking settings
The `publicNetworkAccess` setting determines the Azure OpenAI services association with a network security perimeter.
- In Learning mode, the `publicNetworkAccess` setting controls public access to the resource.
- In Enforced mode, the `publicNetworkAccess` setting is overridden by the network security perimeter rules. For example, if an Azure OpenAI service with a `publicNetworkAccess` setting of `enabled` is associated with a network security perimeter in Enforced mode, access to the Azure OpenAI service is still controlled by network security perimeter access rules.

### Change the network security perimeter access mode
1. Navigate to your network security perimeter resource in the Azure portal.
2. Select **Resources** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/associated-resources-selection.png" alt-text="A screenshot showing the associated resources selection in the left navigation menu." lightbox="../media/network-security-perimeter/associated-resources-selection.png":::

3. Find your Azure OpenAI service in the table.
4. Select the three dots in the far right of the Azure OpenAI service row. Select **Change access mode** in the popup.

    :::image type="content" source="../media/network-security-perimeter/change-access-mode.png" alt-text="A screenshot showing the button to change the access mode." lightbox="../media/network-security-perimeter/change-access-mode.png":::


5. Select the desired access mode and select Apply.

    :::image type="content" source="../media/network-security-perimeter/apply-access-mode.png" alt-text="A screenshot showing the button to apply the access mode." lightbox="../media/network-security-perimeter/apply-access-mode.png":::

## Enable logging network access
1. Navigate to your network security perimeter resource in the Azure portal.
2. Select **Diagnostic settings** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/diagnostic-settings.png" alt-text="A screenshot showing the button for navigating to the diagnostic settings." lightbox="../media/network-security-perimeter/diagnostic-settings.png":::


3. Select **Add diagnostic setting**.
4. Enter any name such as "diagnostic" for Diagnostic setting name.
5. Under Logs, select `allLogs`. `allLogs` ensures all inbound and outbound network access to resources in your network security perimeter is logged.
6. Under Destination details, select Archive to a storage account or Send to Log Analytics workspace. The storage account must be in the same region as the network security perimeter. You can either use an existing storage account or create a new one. A Log Analytics workspace can be in a different region than the one used by the network security perimeter. You can also select any of the other applicable destinations.

    :::image type="content" source="../media/network-security-perimeter/log-categories.png" alt-text="A screenshot showing the available log categories." lightbox="../media/network-security-perimeter/log-categories.png":::

7. Select Save to create the diagnostic setting and start logging network access.

### Reading network access logs
#### Log Analytics workspace
The `network-security-perimeterAccessLogs` table contains all the logs for every log category (for example `network-security-perimeterPublicInboundResourceRulesAllowed`). Every log contains a record of the network security perimeter network access that matches the log category.

Here's an example of the `network-security-perimeterPublicInboundResourceRulesAllowed` log format:

| **Column Name**       | **Meaning**                                                                 | **Example Value**                              |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------|
| Profile                | Which network security perimeter the Azure OpenAI service was associated with | `defaultProfile`                                 |
| Matched Rule           | JSON description of the rule that was matched by the log                  | `{ "accessRule": "IP firewall" }`               |
| SourceIPAddress        | Source IP of the inbound network access, if applicable                    | `1.1.1.1`                                       |
| AccessRuleVersion      | Version of the network-security-perimeter access rules used to enforce the network access rules | 0                                              |

## Add an access rule for your Azure OpenAI service

A network security perimeter profile specifies rules that allow or deny access through the perimeter.

Within the perimeter, all resources have mutual access at the network level. You must still set up authentication and authorization, but at the network level, connection requests from inside the perimeter are accepted.

For resources outside of the network security perimeter, you must specify inbound and outbound access rules. Inbound rules specify which connections to allow in, and outbound rules specify which requests are allowed out.

> [!NOTE] 
> Any service associated with a network security perimeter implicitly allows inbound and outbound access to any other service associated with the same network security perimeter when that access is authenticated using managed identities and role assignments. Access rules only need to be created when allowing access outside of the network security perimeter, or for authenticated access using API keys.

### Add an inbound access rule

Inbound access rules can allow the internet and resources outside the perimeter to connect with resources inside the perimeter. Network security perimeter supports two types of inbound access rules:

- IP address ranges. IP addresses or ranges must be in the Classless Inter-Domain Routing (CIDR) format. An example of CIDR notation is `192.0.2.0/24`, which represents the IPs that range from `192.0.2.0` to `192.0.2.255`. This type of rule allows inbound requests from any IP address within the range.
- Subscriptions. This type of rule allows inbound access authenticated using any managed identity from the subscription.

To add an inbound access rule in the Azure portal:

1. Navigate to your network security perimeter resource in the Azure portal.
2. Select **Profiles** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/profiles-selector.png" alt-text="A screenshot showing the button to navigate to the profiles screen." lightbox="../media/network-security-perimeter/profiles-selector.png":::


3. Select the profile you're using with your network security perimeter.

    :::image type="content" source="../media/network-security-perimeter/selected-profile.png" alt-text="A screenshot showing a selected profile." lightbox="../media/network-security-perimeter/selected-profile.png":::

4. Select **Inbound access rules** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/inbound-network-navigation.png" alt-text="A screenshot showing the button to navigate to the inbound access rules." lightbox="../media/network-security-perimeter/inbound-network-navigation.png":::

5. Select **Add**.

    :::image type="content" source="../media/network-security-perimeter/add-rule.png" alt-text="A screenshot showing the rule button." lightbox="../media/network-security-perimeter/add-rule.png":::

6. Enter or select the following values:
    
    | Setting | Value |
    |---------|-------|
    | Rule name | The name for the inbound access rule (for example, `MyInboundAccessRule`). |
    | Source Type | Valid values are IP address ranges or subscriptions. |
    | Allowed Sources | If you selected IP address ranges, enter the IP address range in a CIDR format that you want to allow inbound access from. Azure IP ranges are available at this link. If you selected **Subscriptions**, use the subscription you want to allow inbound access from. |
    
7. Select **Add** to create the inbound access rule.

    :::image type="content" source="../media/network-security-perimeter/add-rule-2.png" alt-text="A screenshot showing the add button." lightbox="../media/network-security-perimeter/add-rule-2.png":::


### Add an outbound access rule

Recall that in public preview, Azure OpenAI can only connect to Azure Storage or Azure Cosmos DB within the security perimeter. If you want to use other data sources, you need an outbound access rule to support that connection.

Network security perimeter supports outbound access rules based on the Fully Qualified Domain Name (FQDN) of the destination. For example, you can allow outbound access from any service associated with your network security perimeter to an FQDN such as `mystorageaccount.blob.core.windows.net`.

To add an outbound access rule in the Azure portal:

1. Navigate to your network security perimeter resource in the Azure portal.
2. Select **Profiles** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/profiles-selector.png" alt-text="A screenshot showing the profile navigation button." lightbox="../media/network-security-perimeter/profiles-selector.png":::


3. Select the profile you're using with your network security perimeter.

    :::image type="content" source="../media/network-security-perimeter/selected-profile.png" alt-text="A screenshot showing the profile selector." lightbox="../media/network-security-perimeter/selected-profile.png":::

4. Select **Outbound access rules** in the left-hand menu.

    :::image type="content" source="../media/network-security-perimeter/outbound-network-navigation.png" alt-text="A screenshot showing the button to navigate to outbound access rules." lightbox="../media/network-security-perimeter/outbound-network-navigation.png":::

5. Select **Add**.

    :::image type="content" source="../media/network-security-perimeter/add-outbound.png" alt-text="A screenshot showing the button to add outbound access rules." lightbox="../media/network-security-perimeter/add-outbound.png":::

6. Enter or select the following values:
    
    | Setting | Value |
    |---------|-------|
    | Rule name | The name for the outbound access rule (for example, "MyOutboundAccessRule") |
    | Destination Type | Leave as FQDN |
    | Allowed Destinations | Enter a comma-separated list of FQDNs you want to allow outbound access to |
    
7. Select **Add** to create the outbound access rule.

    :::image type="content" source="../media/network-security-perimeter/add-outbound-2.png" alt-text="A screenshot showing the screen to add an outbound access rule." lightbox="../media/network-security-perimeter/add-outbound-2.png":::

## Test your connection through network security perimeter

To test your connection through network security perimeter, you need access to a web browser, either on a local computer with an internet connection or an Azure VM.

1. Change your network security perimeter association to __enforced mode__ to start enforcing network security perimeter requirements for network access to your Azure OpenAI service.

2. Decide if you want to use a local computer or an Azure VM.

    - If you're using a local computer, you need to know your public IP address.

    - If you're using an Azure virtual machine, you can either use a [private link](/azure/private-link/private-link-overview) or [check the IP address using the Azure portal](/azure/virtual-network/ip-services/virtual-network-network-interface-addresses).

3. Using the IP address, you can create an __inbound access rule__ for that IP address to allow access. You can skip this step if you're using private link.

4. Finally, try navigating to the Azure OpenAI service in the Azure portal. Open Azure OpenAI service in Microsoft Foundry. Deploy a model and chat with the model in the Chat Playground. If you receive a response, then the network security perimeter is configured correctly.

## View and manage network security perimeter configuration

You can use the Network Security Perimeter Configuration REST APIs to review and reconcile perimeter configurations. **Be sure to use preview API version** `2024-10-01`.

## See also

- [Role-based access control for Azure OpenAI](./role-based-access-control.md)
