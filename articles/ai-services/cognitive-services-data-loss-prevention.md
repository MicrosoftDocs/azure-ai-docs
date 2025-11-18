---
title: Data loss prevention
description: Foundry Tools data loss prevention capabilities allow customers to configure the list of outbound URLs their Foundry Tools resources are allowed to access. This configuration creates another level of control for customers to prevent data loss.
author: gclarkmt
ms.author: gregc
ms.date: 10/02/2025
ms.service: azure-ai-services
ms.topic: how-to
ms.custom:
  - template-concept
  - build-2025
---

# Configure data loss prevention for Foundry Tools

Foundry Tools data loss prevention capabilities allow customers to configure the list of outbound URLs their Foundry Tools resources are allowed to access. This creates another level of control for customers to prevent data loss. In this article, we'll cover the steps required to enable the data loss prevention feature for Foundry Tools resources.

## Prerequisites

Before you make a request, you need an Azure account and a Foundry Tools subscription. If you already have an account, go ahead and skip to the next section. If you don't have an account, we have a guide to get you set up in minutes: [Create a Foundry resource](multi-service-resource.md?pivots=azportal).

## Access control guidance for Foundry Tools

* You can limit inbound and outbound access to Azure OpenAI by implementing a [network security perimeter](/azure/private-link/network-security-perimeter-concepts). For additional information on how to implement a network security perimeter for Foundry Tools, see [Add network security perimeter (preview) to Azure OpenAI](../ai-foundry/openai/how-to/network-security-perimeter.md). For additional information on how to implement a network security perimeter for Microsoft Foundry-based projects, see [Add Foundry to a network security perimeter (preview)](../ai-foundry/how-to/add-foundry-to-network-security-perimeter.md).

* Define the permitted FQDNs for outbound connections from the AI services resource and apply egress controls accordingly using the information in this guide.

## Enabling data loss prevention

There are two parts to enable data loss prevention. First, the resource property `restrictOutboundNetworkAccess` must be set to `true`. When this is set to true, you also need to provide the list of approved URLs. The list of URLs is added to the `allowedFqdnList` property. The `allowedFqdnList` property contains an array of comma-separated URLs.

>[!NOTE]
>
> * The `allowedFqdnList`  property value supports a maximum of 1000 URLs.
> * The property supports fully qualified domain names (for example `www.contoso.com`) as values.
> * It can take up to 15 minutes for the updated list to take effect. 

# [Azure CLI](#tab/azure-cli)

1. Install the [Azure CLI](/cli/azure/install-azure-cli) and [sign in](/cli/azure/authenticate-azure-cli), or select **Try it**.

1. View the details of the Foundry Tools resource.

    ```azurecli-interactive
    az cognitiveservices account show \
        -g "myresourcegroup" -n "myaccount" \
    ```

1. View the current properties of the Foundry Tools resource.

    ```azurecli-interactive
    az rest -m get \
        -u /subscriptions/{subscription ID}/resourceGroups/{resource group}/providers/Microsoft.CognitiveServices/accounts/{account name}?api-version=2024-10-01 \
    ```

1. Configure the restrictOutboundNetworkAccess property and update the allowed FqdnList with the approved URLs

    ```azurecli-interactive
    az rest -m patch \
        -u /subscriptions/{subscription ID}/resourceGroups/{resource group}/providers/Microsoft.CognitiveServices/accounts/{account name}?api-version=2024-10-01 \
        -b '{"properties": { "restrictOutboundNetworkAccess": true, "allowedFqdnList": [ "contoso.com" ] }}'
    ```

# [PowerShell](#tab/powershell)

1. Install the [Azure PowerShell](/powershell/azure/install-azure-powershell) and [sign in](/powershell/azure/authenticate-azureps), or select **Try it**.

1. Display the current properties for Foundry Tools resource.

    ```azurepowershell-interactive
    $getParams = @{
        ResourceGroupName = 'myresourcegroup'
        ResourceProviderName = 'Microsoft.CognitiveServices'
        ResourceType = 'accounts'
        Name = 'myaccount'
        ApiVersion = '2024-10-01'
        Method = 'GET'
    }
    Invoke-AzRestMethod @getParams
    ```

1. Configure the restrictOutboundNetworkAccess property and update the allowed FqdnList with the approved URLs

    ```azurepowershell-interactive
    $patchParams = @{
        ResourceGroupName = 'myresourcegroup'
        ResourceProviderName = 'Microsoft.CognitiveServices'
        ResourceType = 'accounts'
        Name = 'myaccount'
        ApiVersion = '2024-10-01'
        Payload = '{"properties": { "restrictOutboundNetworkAccess": true, "allowedFqdnList": [ "contoso.com" ] }}'
        Method = 'PATCH'
    }
    Invoke-AzRestMethod @patchParams
    ```

---

## Supported services

The following services support data loss prevention configuration:

* Azure OpenAI
* Foundry (Foundry-based projects)
* Azure Vision
* Content Moderator
* Custom Vision
* Face
* Document Intelligence
* Speech
* QnA Maker


## Next steps

* [Configure Virtual Networks](cognitive-services-virtual-networks.md)
