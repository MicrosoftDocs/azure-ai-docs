---
title: Translate behind firewalls - Azure Translator
titleSuffix: Foundry Tools
description: How to enable Azure Translator to translate behind firewalls using either domain-name or IP filtering.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---

# Use Azure Translator behind firewalls

Azure Translator in Foundry Tools can translate behind firewalls by using either [domain-name](/azure/firewall/dns-settings#dns-proxy-configuration) or [IP filtering](#configure-firewall). Domain-name filtering is the recommended approach.

If you still require IP filtering, you can obtain the [IP addresses details using service tag](/azure/virtual-network/service-tags-overview#discover-service-tags-by-using-downloadable-json-files). Translator is included under the **CognitiveServicesManagement** service tag.

## Configure firewall

 Navigate to your Azure Translator resource in the Azure portal.

1. Select **Networking** from the **Resource Management** section.
1. Under the **Firewalls and virtual networks** tab, choose **Selected Networks and Private Endpoints**.

   :::image type="content" source="../media/firewall-setting-azure-portal.png" alt-text="Screenshot of the firewall setting in the Azure portal.":::

   > [!NOTE]
   >
   > * Once you enable **Selected Networks and Private Endpoints**, you must use the **Virtual Network** endpoint to call the Translator. You can't use the standard translator endpoint (`api.cognitive.microsofttranslator.com`) and you can't authenticate with an access token.
   > * For more information, *see* [**Virtual Network Support**](../text-translation/reference/authentication.md#virtual-network-support).
   > * You can also use a regional endpoint. Regional endpoints follow this format: `https://{region}.api.cognitive.microsoft.com`. Replace {region} with the Azure region where your Translator resource is deployed.

1. To grant access to an internet IP range, enter the IP address or address range (in [`CIDR` notation](https://tools.ietf.org/html/rfc4632)) under **Firewall** > **Address Range**. Only valid public IP (`non-reserved`) addresses are accepted.

Running Azure Translator from behind a specific IP filtered firewall is **not recommended**. The setup is likely to break in the future without notice.

The IP addresses for Translator geographical endpoints as of September 21, 2021 are:

|Geography|Base URL (geographical endpoint)|IP Addresses|
|:--|:--|:--|
|United States|api-nam.cognitive.microsofttranslator.com|20.42.6.144, 20.49.96.128, 40.80.190.224, 40.64.128.192|
|Europe|api-eur.cognitive.microsofttranslator.com|20.50.1.16, 20.38.87.129|
|Asia Pacific|api-apc.cognitive.microsofttranslator.com|40.80.170.160, 20.43.132.96, 20.37.196.160, 20.43.66.16|

## Next steps

[**Azure Translator virtual network support**](../text-translation/reference/authentication.md#virtual-network-support)

[**Configure virtual networks**](../../cognitive-services-virtual-networks.md#grant-access-from-an-internet-ip-range)
