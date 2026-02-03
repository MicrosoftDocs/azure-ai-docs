---
title: Network isolation and Private Link - custom question answering
description: Users can restrict public access to custom question answering resources.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 12/15/2025
ms.custom: language-service-question-answering
---
#  Network isolation and private endpoints

The following steps describe how to restrict public access to custom question answering resources as well as how to enable Azure Private Link. Protect a Foundry resource from public access by [configuring the virtual network](../../../cognitive-services-virtual-networks.md?tabs=portal).

## Private Endpoints

Azure Private Endpoint is a network interface that connects you privately and securely to a service powered by Azure Private Link. Custom question answering provides you support to create private endpoints to the Azure Search Service.

Private endpoints are provided by [Azure Private Link](/azure/private-link/private-link-overview), as a separate service. For more information about costs, see the [pricing page.](https://azure.microsoft.com/pricing/details/private-link/)

## Steps to enable private endpoint

1. Assign the *contributor* role to your resource in the Azure Search Service instance. This operation requires *Owner* access to the subscription. Go to Identity tab in the service resource to get the identity.

> [!div class="mx-imgBorder"]
> ![Text Analytics Identity](../media/qnamaker-reference-private-endpoints/private-endpoints-identity.png)

2. Add the above identity as *Contributor* by going to the Azure Search Service access control tab.

![Managed service IAM](../media/qnamaker-reference-private-endpoints/private-endpoint-access-control.png)

3. Select on *Add role assignments*, add the identity and select *Save*.

![Managed role assignment](../media/qnamaker-reference-private-endpoints/private-endpoint-role-assignment.png)

4. Now, go to *Networking* tab in the Azure Search Service instance and switch Endpoint connectivity data from *Public* to *Private*. This operation is a long running process and can take up to 30 mins to complete. 

![Managed Azure search networking](../media/qnamaker-reference-private-endpoints/private-endpoint-networking.png)

5. Go to *Networking* tab of language resource and under the *Allow access from*, select the *Selected Networks and private endpoints* option and select *save*.
 
> [!div class="mx-imgBorder"]
> ![Text Analytics networking](../media/qnamaker-reference-private-endpoints/private-endpoint-networking-custom-qna.png)

This will establish a private endpoint connection between language resource and Azure AI Search service instance. You can verify the Private endpoint connection on the *Networking* tab of the Azure AI Search service instance. Once the whole operation is completed, you're good to use your language resource with question answering enabled.

![Managed Networking Service](../media/qnamaker-reference-private-endpoints/private-endpoint-networking-3.png)

## Support details
 * We don't support changes to Azure AI Search service once you enable private access to your language resources. If you change the Azure AI Search service via 'Features' tab after you have enabled private access, the language resource will become unusable.

 * After establishing Private Endpoint Connection, if you switch Azure AI Search Service Networking to 'Public', you won't be able to use the language resource. Azure Search Service Networking needs to be 'Private' for the Private Endpoint Connection to work.

## Restrict access to Azure AI Search resource

Follow these steps to restrict public access to custom question answering language resources. Protect a Foundry resource from public access by [configuring the virtual network](../../../cognitive-services-virtual-networks.md?tabs=portal).

  > [!div class="mx-imgBorder"]
  > [![Screenshot of firewall and virtual networks configuration UI](../media/network-isolation/firewall.png)](../media/network-isolation/firewall.png#lightbox)
