---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/20/2026
ms.author: pafarley
---
## Use Speech Studio

[Speech Studio](../speech-studio-overview.md) is a web portal with tools for building and integrating Azure Speech in Foundry Tools service in your application. When you work in Speech Studio projects, network connections and API calls to the corresponding Speech resource are made on your behalf. Working with [private endpoints](../speech-services-private-link.md), [virtual network service endpoints](../speech-service-vnet-service-endpoint.md), and other network security options can limit the availability of Speech Studio features. You normally use Speech Studio when working with features, like [custom speech](../custom-speech-overview.md), [custom voice](../professional-voice-create-project.md) and [audio content creation](../how-to-audio-content-creation.md).


### Reach Speech Studio from a virtual network

To use Speech Studio from a virtual machine within an Azure virtual network, allow outgoing connections to the required set of [service tags](/azure/virtual-network/service-tags-overview) for that virtual network. See details in [supported regions and service offerings](../../cognitive-services-virtual-networks.md#supported-regions-and-service-offerings).

Access to the Speech resource endpoint is *not* equal to access to the Speech Studio web portal. Access to Speech Studio through private or VNet service endpoints is not supported.

### Work with Speech Studio projects

This section describes working with the different kinds of Speech Studio projects for the different network security options of the Speech resource. It's expected that the web browser connection to Speech Studio is established. Set Speech resource network security in the Azure portal or by using the CLI:

**Azure CLI**
```azurecli
# View current network settings
az cognitiveservices account show \
  --name <your-speech-resource-name> \
  --resource-group <your-resource-group-name> \
  --query "{publicAccess:properties.publicNetworkAccess, networkRules:properties.networkAcls}" \
  -o json

# Change public network access (options: Enabled, Disabled)
az cognitiveservices account update \
  --name <your-speech-resource-name> \
  --resource-group <your-resource-group-name> \
  --public-network-access Enabled
```

**Azure portal**
1. Go to the [Azure portal](https://portal.azure.com/) and sign in to your Azure account.
1. Select the Speech resource.
1. In the **Resource Management** group in the left pane, select **Networking** > **Firewalls and virtual networks**. 
1. Select one option from **All networks**, **Selected Networks and Private Endpoints**, or **Disabled**. 

#### Custom speech, custom voice, and audio content creation

The following table describes custom speech/custom voice/audio content creation project accessibility per Speech resource **Networking** > **Firewalls and virtual networks** security setting.

> [!NOTE]
> If you allow only private endpoints through the **Networking** > **Private endpoint connections** tab, you can't use Speech Studio with the Speech resource. You can still use the Speech resource outside of Speech Studio.

| Speech resource network security setting | Speech Studio project accessibility |
|------------------------------------------|-------------------------------------|
| All networks | No restrictions |
| Selected Networks and Private Endpoints | Accessible from allowed public IP addresses |
| Disabled | Not accessible |

If you select **Selected Networks and Private Endpoints**, you see a tab with **Virtual networks** and **Firewall** access configuration options. In the **Firewall** section, you must allow at least one public IP address and use this address for the browser connection with Speech Studio.

To use custom speech without relaxing network access restrictions on your production Speech resource, consider one of these workarounds:

- Create another Speech resource for development that can be used on a public network. Prepare your custom model in Speech Studio on the development resource, and then copy the model to your production resource. See the [Models_CopyTo](/rest/api/speechtotext/models/copy-to) REST request with the [Speech to text REST API](../rest-speech-to-text.md).
- You can use the [Speech to text REST API](../rest-speech-to-text.md) for all custom speech operations instead of Speech Studio.

To use custom voice without relaxing network access restrictions on your production Speech resource, consider one of these workarounds:

- Create another Speech resource for development that can be used on a public network. Prepare your custom model in Speech Studio on the development resource, then submit an Azure support ticket to request assistance with copying the model to your production resource.
- Use the [Custom voice REST API](/rest/api/aiservices/speechapi/operation-groups) directly for all custom voice operations with your production resource.
