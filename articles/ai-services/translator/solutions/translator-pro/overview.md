---
title: What is Microsoft Translator Pro?
description: Learn about Microsoft Translator Pro and how it enables speech-to-speech translated conversations within your enterprise ecosystem.
author: laujan
ms.author: lajanuar
ai-usage: ai-assisted
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.topic: overview
ms.date: 09/15/2026
ms.custom: FY25Q1-Linter
---

# What is Microsoft Translator Pro?

> [!IMPORTANT]
> Microsoft Translator Pro begins retirement on September 15, 2026. The following conditions apply:
>
> * Existing customers retain access to Microsoft Translator Pro in maintenance mode through September 15, 2027.
> * Microsoft doesn't onboard new customers to Microsoft Translator Pro during retirement.
> * During the maintenance period, Microsoft provides critical security, compliance, reliability, and service-continuity updates as applicable. Microsoft doesn't introduce new product capabilities.
> * Effective September 15, 2027, Microsoft Translator Pro is fully retired and is no longer available or supported.
> * The retirement applies solely to the Microsoft Translator Pro client application. It doesn't affect [Azure Translator in Foundry Tools](../../overview.md), [Azure Speech in Foundry Tools](../../../speech-service/overview.md), or the Azure resources used by those services.
>
> Existing customers should complete their transition from Microsoft Translator Pro before September 15, 2027. Organizations that require custom enterprise translation experiences can use Translator and Speech services to build applications that align with their security, organizational, and deployment requirements.

Microsoft Translator Pro is an enterprise mobile application that provides real-time speech-to-speech translation. The application integrates with an organization's Azure environment and requires enterprise users to authenticate with their organizational identities and use configured Translator resources.

During retirement, Microsoft Translator Pro remains available in maintenance mode only to existing customers in the Azure public and Azure Government cloud environments. The application doesn't support access across these cloud environments.

## Specifications and service limits

* The Microsoft Translator Pro app can be accessed on iOS devices and requires iOS 15 or newer versions.

* Enterprise users must set up identities and translator resources within Azure public or US Government cloud environments; the app doesn't support hybrid use across these environments. For example, an identity created in the Azure public cloud can't be used to access an Azure resource in the government cloud via this app.

* This app operates as a paid offering, necessitating payment before use.

* Existing customers can download the app in selected regions. For more information, see [Region availability](#region-availability).

* Offline translation is limited to a select number of languages. For more information, *see* [Language support](language-support.md).

## Core features and capabilities

* **Eliminates language barriers**. Real-time speech-to-speech translation allows seamless communication between individuals speaking different languages.

* **Unified efficient experience**. Both transcription and translation can be viewed or heard simultaneously on a single device, ensuring smooth and efficient conversations.

* **Offline usage capability**. The app's speech-to-speech translation capability can be utilized without an internet connection in limited languages, maintaining productivity without interruption.

* **Customized phrasebook**. Administrators can upload a list of commonly used phrases specific to their organization. These phrases can then be quickly accessed and translated during conversations, ensuring communication remains efficient and accurate.

* **International availability**. The app is now accessible in selected regions outside of the United States. For more information, *see* [Region availability](#region-availability).

* **US Government cloud availability**. US Government agencies can now operate the app within selected regions of the US Government cloud. For more information, *see* [Region availability](#region-availability).

* **Expanded language coverage**. The app now offers support for more languages when online, enhancing its usability for a broader range of users. For more information, *see* [Language support](language-support.md).

* **Full administrator control**. Your enterprise IT administrator has extensive control over the app's deployment and usage within your organization. Administrators can fine-tune settings to manage conversation history, audit trails, and diagnostic logs. Additionally, administrators have the ability to disable history or configure the automatic exportation of the history to cloud storage.

* **Enterprise-grade security**. Microsoft Translator Pro ensures exceptional translation quality paired with robust security features. Recognizing that privacy and security are paramount for your organization, administrators can sign in to the app using organizational credentials. Your organization's conversational data remains entirely protected within your Azure tenant. Not Microsoft or any third parties can access your data.

## App store availability

Existing customers can download Microsoft Translator Pro from the iOS App Store in the following regions:

| Country/Region |
| --- |
| Australia |
| Austria |
| Belgium |
| Bulgaria |
| Croatia |
| Czech Republic |
| Denmark |
| Estonia |
| Finland |
| France |
| Germany |
| Greece |
| Hong Kong SAR |
| Hungary |
| India |
| Ireland |
| Italy |
| Japan |
| Latvia |
| Lithuania |
| Luxembourg |
| Malta |
| Netherlands |
| Poland |
| Portugal |
| Republic of Cyprus |
| Romania |
| Slovakia |
| Slovenia |
| Spain |
| Sweden |
| UAE |
| UK |
| Ukraine |

## Region availability

The app is currently available for Azure Translator resources created in the following regions within the respective clouds. Ensure you onboard the app to your resource located in these specified regions.

**Azure Cloud (public)**

|Geography|Region|
|---|---|
| Africa | South Africa North (`southafricanorth`) |
| Asia Pacific | East Asia (`eastasia`) |
| Asia Pacific | Southeast Asia (`southeastasia`) |
| Australia| Australia East (`australiaeast`) |
| Brazil | Brazil South (`brazilsouth`) |
| Canada | Canada Central (`canadacentral`) |
| Canada | Canada East (`canadaeast`) |
| Europe | North Europe (`northeurope`) |
| Europe | West Europe (`westeurope`) |
| France | France Central (`francecentral`) |
| Germany | Germany West Central (`germanywestcentral`) |
| Global | Global (`global`) |
| India | Central India (`centralindia`) |
| Italy | Italy North (`italynorth`) |
| Japan | Japan East (`japaneast`) |
| Japan | Japan West (`japanwest`) |
| Korea | Korea Central (`koreacentral`) |
| Norway | Norway East (`norwayeast`) |
| Qatar | Qatar Central (`qatarcentral`) |
| Sweden | Sweden Central (`swedencentral`) |
| Switzerland | Switzerland North (`switzerlandnorth`) |
| Switzerland | Switzerland West (`switzerlandwest`) |
| United Kingdom | UK South (`uksouth`) |
| United Kingdom | UK West (`ukwest`) |
| United Arab Emirates | UAE North (`uaenorth`) |
| United States| Central US (`centralus`) |
| United States| East US (`eastus`) |
| United States| East US 2 (`eastus2`) |
| United States| North Central US (`northcentralus`) |
| United States| South Central US (`southcentralus`) |
| United States| West Central US (`westcentralus`) |
| United States| West US (`westus`) |
| United States| West US 2 (`westus2`) |
| United States| West US 3 (`westus3`) |

**Azure US Government Cloud**

|Geography|Region|
|---|---|
|United States|US Gov Virginia|
|United States|US Gov Arizona|

## Next steps

* Learn more about Microsoft Translator Pro:
  * [**Language support**](language-support.md)
  * [**Frequently asked questions (FAQ)**](faq.yml)
