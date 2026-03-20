---
title: How to use private endpoints with Speech service
titleSuffix: Foundry Tools
description: Learn how to use Speech service with private endpoints provided by Azure Private Link.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 03/20/2026
ms.reviewer: pafarley
ms.custom: devx-track-azurepowershell, devx-track-azurecli
#Customer intent: As a developer, I want to learn how to use Speech service with private endpoints provided by Azure Private Link.
---

# Use Speech service through a private endpoint

[Azure Private Link](/azure/private-link/private-link-overview) lets you connect to services in Azure by using a [private endpoint](/azure/private-link/private-endpoint-overview). A private endpoint is a private IP address that's accessible only within a specific [virtual network](/azure/virtual-network/virtual-networks-overview) and subnet.

This article explains how to set up and use Private Link and private endpoints with the Speech service. It then describes how to remove private endpoints later but still use the Speech resource.

## Overview steps

| Task | CLI command | Time estimate |
|------|------------|---------------|
| Create custom domain | `az cognitiveservices account update --custom-domain <name>` | 1 min |
| Check domain availability | `az rest --method post --url ".../checkDomainAvailability"` | 30 sec |
| Create private endpoint | `az network private-endpoint create ...` | 2-3 min |
| Configure private DNS | `az network private-dns zone create ...` | 2-3 min |
| Verify DNS resolution | `nslookup <custom-name>.cognitiveservices.azure.com` | 30 sec |

## Prerequisites

Before you proceed, review [how to use virtual networks with Foundry Tools](../cognitive-services-virtual-networks.md).

- An Azure subscription. [Create a free account](https://azure.microsoft.com/free/) if you don't have one. Verify with `az account show`.
- Azure CLI (latest version). Install or update with `az upgrade`. Verify with `az --version`.
- A Speech resource (S0 tier). Create with `az cognitiveservices account create --kind SpeechServices --sku S0 ...`. Verify with `az cognitiveservices account show --name <name> --resource-group <rg>`.
- A virtual network with a subnet. Create with `az network vnet create ...`. Verify with `az network vnet show --name <vnet> --resource-group <rg>`.

> [!NOTE]
> If you use PowerShell instead of Azure CLI, you need PowerShell 7.x or later with the Azure PowerShell module 5.1.0 or later. Verify with `$PSVersionTable` and `Get-Module -ListAvailable Az`.

Setting up a Speech resource for private endpoint scenarios requires these tasks:

1. [Create a custom domain name](#create-a-custom-domain-name)
1. [Turn on private endpoints](#turn-on-private-endpoints)
1. [Adjust existing applications and solutions](#adjust-an-application-to-use-a-speech-resource-with-a-private-endpoint)

[!INCLUDE [](includes/speech-vnet-service-enpoints-private-endpoints.md)]

This article describes the usage of private endpoints with the Speech service. Usage of VNet service endpoints is described in [Use Speech service through a VNet service endpoint](speech-service-vnet-service-endpoint.md).

## Create a custom domain name

> [!CAUTION]
> A Speech resource with a custom domain name enabled uses a different way to interact with the Speech service. You might have to adjust your application code for both of these scenarios: [with private endpoint](#adjust-an-application-to-use-a-speech-resource-with-a-private-endpoint) and [*without* private endpoint](#adjust-an-application-to-use-a-speech-resource-without-private-endpoints).

[!INCLUDE [Custom Domain include](includes/how-to/custom-domain.md)]

## Turn on private endpoints

We recommend using the [private DNS zone](/azure/dns/private-dns-overview) attached to the virtual network with the necessary updates for the private endpoints. You can create a private DNS zone during the provisioning process. If you use your own DNS server, you might also need to change your DNS configuration.

Decide on a DNS strategy before you provision private endpoints for a production Speech resource. Test your DNS changes, especially if you use your own DNS server.

### Create a private endpoint

Use the following steps to create a private endpoint for your Speech resource. Replace placeholder values with your actual values:

**Step 1:** Ensure your subnet has private endpoint network policies disabled:

```azurecli
az network vnet subnet update \
  --name <your-subnet-name> \
  --resource-group <your-resource-group-name> \
  --vnet-name <your-vnet-name> \
  --private-endpoint-network-policies Disabled
```

**Step 2:** Create the private endpoint. Use `account` as the target sub-resource for Foundry Tools:

```azurecli
az network private-endpoint create \
  --name <your-private-endpoint-name> \
  --resource-group <your-resource-group-name> \
  --vnet-name <your-vnet-name> \
  --subnet <your-subnet-name> \
  --private-connection-resource-id $(az cognitiveservices account show \
    --name <your-speech-resource-name> \
    --resource-group <your-resource-group-name> \
    --query "id" -o tsv) \
  --group-id account \
  --connection-name <your-connection-name> \
  --location <your-location>
```

| Parameter | Value |
|-----------|-------|
| Resource type | `Microsoft.CognitiveServices/accounts` |
| Resource | `<your-speech-resource-name>` |
| Target sub-resource | `account` |

**Verification:** Confirm the private endpoint was created:

```azurecli
az network private-endpoint show \
  --name <your-private-endpoint-name> \
  --resource-group <your-resource-group-name> \
  --query "{state:provisioningState, status:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o json
```

Expected output: `provisioningState` is `Succeeded` and `status` is `Approved`.

**Step 3:** Create a private DNS zone and link it to your virtual network:

```azurecli
# Create the private DNS zone
az network private-dns zone create \
  --resource-group <your-resource-group-name> \
  --name privatelink.cognitiveservices.azure.com

# Link the DNS zone to your virtual network
az network private-dns link vnet create \
  --resource-group <your-resource-group-name> \
  --zone-name privatelink.cognitiveservices.azure.com \
  --name <your-dns-link-name> \
  --virtual-network <your-vnet-name> \
  --registration-enabled false

# Create DNS zone group for automatic DNS record management
az network private-endpoint dns-zone-group create \
  --resource-group <your-resource-group-name> \
  --endpoint-name <your-private-endpoint-name> \
  --name default \
  --private-dns-zone privatelink.cognitiveservices.azure.com \
  --zone-name cognitiveservices
```

**Verification:** Confirm the DNS A record was created:

```azurecli
az network private-dns record-set a list \
  --resource-group <your-resource-group-name> \
  --zone-name privatelink.cognitiveservices.azure.com \
  --query "[].{name:name, ip:aRecords[0].ipv4Address}" \
  -o table
```

Expected output: A record for your custom domain name resolving to the private endpoint IP (for example, `10.0.0.4`).

**DNS for private endpoints:** Review the general principles of [DNS for private endpoints in Microsoft Foundry resources](../cognitive-services-virtual-networks.md#apply-dns-changes-for-private-endpoints). Then confirm that your DNS configuration is working correctly by performing the checks described in the following sections.

### Resolve DNS from the virtual network

This check is *required*.

Follow these steps to test the custom DNS entry from your virtual network:

1. Sign in to a virtual machine located in the virtual network to which you attached your private endpoint.
1. Open a Windows command prompt or a Bash shell, run `nslookup`, and confirm that it successfully resolves your resource's custom domain name.

    ```
    C:\>nslookup my-private-link-speech.cognitiveservices.azure.com
    Server:  UnKnown
    Address:  168.63.129.16

    Non-authoritative answer:
    Name:    my-private-link-speech.privatelink.cognitiveservices.azure.com
    Address:  172.28.0.10
    Aliases:  my-private-link-speech.cognitiveservices.azure.com
    ```

1. Confirm that the IP address matches the IP address of your private endpoint.

**Verification:** The resolved IP address (for example, `172.28.0.10`) matches the private endpoint IP assigned in the previous step. The `Name` field includes `privatelink` in the domain.

### Resolve DNS from other networks

Perform this check only if you turned on either the **All networks** option or the **Selected Networks and Private Endpoints** access option in the **Networking** section of your resource.

If you plan to access the resource by using only a private endpoint, you can skip this section.

1. Sign in to a computer attached to a network allowed to access the resource.
2. Open a Windows command prompt or Bash shell, run `nslookup`, and confirm that it successfully resolves your resource's custom domain name.

    ```
    C:\>nslookup my-private-link-speech.cognitiveservices.azure.com
    Server:  UnKnown
    Address:  fe80::1

    Non-authoritative answer:
    Name:    vnetproxyv1-weu-prod.westeurope.cloudapp.azure.com
    Address:  13.69.67.71
    Aliases:  my-private-link-speech.cognitiveservices.azure.com
              my-private-link-speech.privatelink.cognitiveservices.azure.com
              westeurope.prod.vnet.cog.trafficmanager.net
    ```

> [!NOTE]
> The resolved IP address points to a virtual network proxy endpoint, which dispatches network traffic to the private endpoint for the Speech resource. The behavior is different for a resource with a custom domain name but *without* private endpoints. See the [DNS configuration section](#dns-configuration) for details.

## Adjust an application to use a Foundry resource for Speech with a private endpoint

A Foundry resource for Speech with a custom domain interacts with the Speech service in a different way. This is true for a custom-domain-enabled Speech resource both with and without private endpoints. Information in this section applies to both scenarios.

Follow instructions in this section to adjust existing applications and solutions to use a Speech resource with a custom domain name and a private endpoint turned on.

> [!NOTE]
> A Foundry resource for Speech without private endpoints that uses a custom domain name also has a special way of interacting with the Speech service.
> This way differs from the scenario of a Foundry resource for Speech that uses a private endpoint.
> This is important to consider because you may decide to remove private endpoints later. See [Adjust an application to use a Speech resource without private endpoints](#adjust-an-application-to-use-a-speech-resource-without-private-endpoints) later in this article.

### Usage with the REST APIs

Speech service has REST APIs for [Speech to text](rest-speech-to-text.md) and [Text to speech](rest-text-to-speech.md). Consider the following information for the private-endpoint-enabled scenario.

Speech to text has two REST APIs. Each API serves a different purpose, uses different endpoints, and requires a different approach when you use it in the private-endpoint-enabled scenario.

The Speech to text REST APIs are:
- [Speech to text REST API](rest-speech-to-text.md), which is used for [Batch transcription](batch-transcription.md) and [custom speech](custom-speech-overview.md). 
- [Speech to text REST API for short audio](rest-speech-to-text-short.md), which is used for real-time speech to text.

Usage of the Speech to text REST API for short audio and the Text to speech REST API in the private endpoint scenario is the same. It's equivalent to the [Speech SDK case](#usage-with-the-speech-sdk) described later in this article.

Speech to text REST API uses a different set of endpoints, so it requires a different approach for the private-endpoint-enabled scenario.

#### Speech to text REST API

Usually, Speech resources use [Foundry Tools regional endpoints](../cognitive-services-custom-subdomains.md#is-there-a-list-of-regional-endpoints) for communicating with the [Speech to text REST API](rest-speech-to-text.md). These resources have the following naming format:

`{region}.api.cognitive.microsoft.com`

This is a sample request URL:

```
https://westeurope.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions
```

> [!NOTE]
> See [this article](sovereign-clouds.md) for Azure Government and Microsoft Azure operated by 21Vianet endpoints.

After you turn on a custom domain for a Foundry resource for Speech (which is necessary for private endpoints), that resource uses the following DNS name pattern for the basic REST API endpoint:

`{your-custom-name}.cognitiveservices.azure.com`

In the earlier example, the REST API endpoint name becomes:

`my-private-link-speech.cognitiveservices.azure.com`

And the sample request URL converts to:

```
https://my-private-link-speech.cognitiveservices.azure.com/speechtotext/v3.1/transcriptions
```

This URL should be reachable from the virtual network with the private endpoint attached (provided the [correct DNS resolution](#resolve-dns-from-the-virtual-network)).

After you turn on a custom domain name for a Foundry resource for Speech, you typically replace the host name in all request URLs with the new custom domain host name. All other parts of the request (like the path `/speechtotext/v3.1/transcriptions` in the earlier example) remain the same.

**Verification:** Test the endpoint by running:

```bash
curl -s -H "Ocp-Apim-Subscription-Key: <your-speech-key>" \
  "https://<your-custom-name>.cognitiveservices.azure.com/speechtotext/v3.1/transcriptions" | head -c 200
```

Expected output: A JSON response containing a `values` array (which may be empty for a new resource).

> [!TIP]
> Some customers develop applications that use the region part of the regional endpoint's DNS name (for example, to send the request to the Speech resource deployed in a particular Azure region). A custom domain for a Speech resource contains *no* information about the region where the resource is deployed. So the application logic described earlier doesn't work and needs to be altered.

#### Speech to text REST API for short audio and Text to speech REST API

The [Speech to text REST API for short audio](rest-speech-to-text-short.md) and the [Text to speech REST API](rest-text-to-speech.md) use two types of endpoints:
- [Foundry Tools regional endpoints](../cognitive-services-custom-subdomains.md#is-there-a-list-of-regional-endpoints) for communicating with the Foundry Tools REST API to obtain an authorization token
- Special endpoints for all other operations

> [!NOTE]
> See [this article](sovereign-clouds.md) for Azure Government and Azure operated by 21Vianet endpoints.

The detailed description of the special endpoints and how their URL should be transformed for a private-endpoint-enabled Speech resource is provided in the [Construct endpoint URL](#construct-endpoint-url) subsection about usage with the Speech SDK. The same principle described for the SDK applies for the Speech to text REST API for short audio and the Text to speech REST API.
Get familiar with the material in the subsection mentioned in the previous paragraph and see the following example. The example describes the Text to speech REST API. Usage of the Speech to text REST API for short audio is fully equivalent.

**Text to speech REST API usage example**

In this example, West Europe is the Azure region and `my-private-link-speech.cognitiveservices.azure.com` is the Speech resource DNS name (custom domain). The custom domain `my-private-link-speech.cognitiveservices.azure.com` belongs to the Speech resource created in the West Europe region.

To get the list of the voices supported in the region, run:

```
https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list
```

For the private-endpoint-enabled Speech resource, the endpoint URL for the same operation changes. The same request looks like:

```
https://my-private-link-speech.cognitiveservices.azure.com/tts/cognitiveservices/voices/list
```

**Verification:** Test the TTS voices endpoint:

```bash
curl -s -H "Ocp-Apim-Subscription-Key: <your-speech-key>" \
  "https://<your-custom-name>.cognitiveservices.azure.com/tts/cognitiveservices/voices/list" | head -c 200
```

Expected output: A JSON array of voice objects. A non-empty response confirms the endpoint works.

See a detailed explanation in the [Construct endpoint URL](#construct-endpoint-url) subsection for the Speech SDK.

> [!NOTE]
> When you use the Speech to text REST API for short audio and Text to speech REST API in private endpoint scenarios, use a resource key passed through the `Ocp-Apim-Subscription-Key` header. (See details for [Speech to text REST API for short audio](rest-speech-to-text-short.md#request-headers) and [Text to speech REST API](rest-text-to-speech.md#request-headers))
>
> Using an authorization token and passing it to the special endpoint through the `Authorization` header works *only* if you turned on the **All networks** access option in the **Networking** section of your Speech resource. In other cases you get either a `Forbidden` or `BadRequest` error when trying to obtain an authorization token.

### Usage with the Speech SDK

Using the Speech SDK with a custom domain name and private-endpoint-enabled Speech resources requires you to review and likely change your application code.

We use `my-private-link-speech.cognitiveservices.azure.com` as a sample Speech resource DNS name (custom domain) for this section.

#### Construct endpoint URL

Usually in SDK scenarios (and in the Speech to text REST API for short audio and Text to speech REST API scenarios), Speech resources use the dedicated regional endpoints for different service offerings. The DNS name format for these endpoints is:

`{region}.{speech-service-offering}.speech.microsoft.com`

An example DNS name is:

`westeurope.stt.speech.microsoft.com`

All possible values for the region (first element of the DNS name) are listed in [Speech service supported regions](regions.md). (See [this article](sovereign-clouds.md) for Azure Government and Azure operated by 21Vianet endpoints.) The following table presents the possible values for the Speech service offering (second element of the DNS name):

| DNS name value | Speech service offering |
|----------------|------------------------|
| `s2s` | [Speech Translation](speech-translation.md) |
| `stt` | [Speech to text](speech-to-text.md) |
| `tts` | [Text to speech](text-to-speech.md) |
| `voice` | [Custom voice](professional-voice-create-project.md) |

So the earlier example (`westeurope.stt.speech.microsoft.com`) stands for a Speech to text endpoint in West Europe.

Private-endpoint-enabled endpoints communicate with the Speech service through a special proxy. Because of that, *you must change the endpoint connection URLs*.

A "standard" endpoint URL looks like:

`{region}.{speech-service-offering}.speech.microsoft.com/{URL-path}`

A private endpoint URL looks like:

`{your-custom-name}.cognitiveservices.azure.com/{URL-path}`

The Speech SDK automatically configures the `/{URL-path}` depending on the service used. You only need to configure the base URL.

#### Modify applications

Follow these steps to modify your code:

1. Determine the application endpoint URL. Go to the [Azure portal](https://portal.azure.com/), open your Speech resource, and select **Keys and Endpoint** in the **Resource Management** group. Alternatively, use the CLI:

    ```azurecli
    az cognitiveservices account show \
      --name <your-speech-resource-name> \
      --resource-group <your-resource-group-name> \
      --query "properties.endpoint" -o tsv
    ```

    The endpoint looks like: `https://my-private-link-speech.cognitiveservices.azure.com/`

2. Create a `SpeechConfig` instance by using an endpoint URL. Your existing code probably uses something like:

    ```csharp
    var config = SpeechConfig.FromSubscription(speechKey, azureRegion);
    ```

    This doesn't work for a private-endpoint-enabled Speech resource because of the host name and URL changes. If you try to run your existing application without any modifications by using the key of a private-endpoint-enabled resource, you get an authentication error (401).

    To fix this, modify how you instantiate the `SpeechConfig` class to use endpoint-based initialization. Define these two variables:

    - `speechKey` contains the key of the private-endpoint-enabled Speech resource.
    - `endPoint` contains the full modified endpoint URL:

      ```
      wss://my-private-link-speech.cognitiveservices.azure.com
      ```

    Then create a `SpeechConfig` instance:

    **C#:**
    ```csharp
    var config = SpeechConfig.FromEndpoint(endPoint, speechKey);
    ```

    **C++:**
    ```cpp
    auto config = SpeechConfig::FromEndpoint(endPoint, speechKey);
    ```

    **Java:**
    ```java
    SpeechConfig config = SpeechConfig.fromEndpoint(endPoint, speechKey);
    ```

    **Python:**
    ```python
    import azure.cognitiveservices.speech as speechsdk
    config = speechsdk.SpeechConfig(endpoint=endPoint, subscription=speechKey)
    ```

    **Objective-C:**
    ```objectivec
    SPXSpeechConfiguration *config = [[SPXSpeechConfiguration alloc] initWithEndpoint:endPoint subscription:speechKey];
    ```

    **JavaScript:**
    ```javascript
    import * as sdk from "microsoft-cognitiveservices-speech-sdk";
    const config = sdk.SpeechConfig.fromEndpoint(new URL(endPoint), speechKey);
    ```

After this modification, your application should work with the private-endpoint-enabled Speech resources.

### Usage without private endpoints

Using the Speech SDK with custom-domain-enabled Speech resources *without* private endpoints is equivalent to the configuration described *with* private endpoints in this document.

[!INCLUDE [](includes/speech-studio-vnet.md)]


## Adjust an application to use a Foundry resource for Speech without private endpoints

In this article, we noted several times that enabling a custom domain for a Foundry resource for Speech is irreversible. Such a resource uses a different way of communicating with Speech service, compared to the ones that are using [regional endpoint names](../cognitive-services-custom-subdomains.md#is-there-a-list-of-regional-endpoints).

This section explains how to use a Foundry resource with a custom domain name but without any private endpoints with the Speech service REST APIs and [Speech SDK](speech-sdk.md). This might be a resource that was once used in a private endpoint scenario but then had its private endpoints deleted.

### DNS configuration

Remember how a custom domain DNS name of the private-endpoint-enabled Speech resource is [resolved from public networks](#resolve-dns-from-other-networks). In that case, the IP address resolved points to a proxy endpoint for a virtual network. That endpoint is used for dispatching network traffic to the private-endpoint-enabled Microsoft Foundry resource.

However, when *all* resource private endpoints are removed (or right after the enabling of the custom domain name), the CNAME record of the Speech resource is reprovisioned. It now points to the IP address of the corresponding [Foundry Tools regional endpoint](../cognitive-services-custom-subdomains.md#is-there-a-list-of-regional-endpoints).

So the output of the `nslookup` command looks like this:

```
C:\>nslookup my-private-link-speech.cognitiveservices.azure.com
Server:  UnKnown
Address:  fe80::1

Non-authoritative answer:
Name:    apimgmthskquihpkz6d90kmhvnabrx3ms3pdubscpdfk1tsx3a.cloudapp.net
Address:  13.93.122.1
Aliases:  my-private-link-speech.cognitiveservices.azure.com
          westeurope.api.cognitive.microsoft.com
          cognitiveweprod.trafficmanager.net
          cognitiveweprod.azure-api.net
          apimgmttmdjylckcx6clmh2isu2wr38uqzm63s8n4ub2y3e6xs.trafficmanager.net
          cognitiveweprod-westeurope-01.regional.azure-api.net
```

Compare it with the output from the [Resolve DNS from other networks](#resolve-dns-from-other-networks) section.

### Usage with the REST APIs (without private endpoints)

#### Speech to text REST API

Speech to text REST API usage is fully equivalent to the case of [private-endpoint-enabled Speech resources](#speech-to-text-rest-api).

#### Speech to text REST API for short audio and Text to speech REST API

In this case, usage of the Speech to text REST API for short audio and usage of the Text to speech REST API have no differences from the general case, with one exception. (See the following note.) Use both APIs as described in the [Speech to text REST API for short audio](rest-speech-to-text-short.md) and [Text to speech REST API](rest-text-to-speech.md) documentation.

> [!NOTE]
> When you use the Speech to text REST API for short audio and Text to speech REST API in custom domain scenarios, use an API key passed through the `Ocp-Apim-Subscription-Key` header. (See details for [Speech to text REST API for short audio](rest-speech-to-text-short.md#request-headers) and [Text to speech REST API](rest-text-to-speech.md#request-headers))
>
> Using an authorization token and passing it to the special endpoint through the `Authorization` header works *only* if you turned on the **All networks** access option in the **Networking** section of your Speech resource. In other cases you get either a `Forbidden` or `BadRequest` error when trying to obtain an authorization token.

[!INCLUDE [](includes/speech-vnet-service-enpoints-private-endpoints-simultaneously.md)]



**Verification:** Confirm the networking setting via CLI:

```azurecli
az cognitiveservices account show \
  --name <your-speech-resource-name> \
  --resource-group <your-resource-group-name> \
  --query "properties.publicNetworkAccess" -o tsv
```

Other options aren't supported for this scenario.

## Cleanup

To remove the resources created during this configuration, delete them in reverse order:

```azurecli
# Delete private endpoint
az network private-endpoint delete \
  --name <your-private-endpoint-name> \
  --resource-group <your-resource-group-name>

# Delete DNS zone group, link, and zone
az network private-dns link vnet delete \
  --resource-group <your-resource-group-name> \
  --zone-name privatelink.cognitiveservices.azure.com \
  --name <your-dns-link-name> --yes

az network private-dns zone delete \
  --resource-group <your-resource-group-name> \
  --name privatelink.cognitiveservices.azure.com --yes
```

> [!NOTE]
> Deleting private endpoints does not remove the custom domain name. The custom domain remains active, and the Speech resource uses a different DNS resolution pattern. See the [DNS configuration](#dns-configuration) section.

## Troubleshooting

### Authentication error (401) after enabling custom domain

If you get a 401 error after enabling a custom domain, your application is probably still using the region-based `SpeechConfig.FromSubscription()` initialization. Switch to endpoint-based initialization using `SpeechConfig.FromEndpoint()` as described in the [Modify applications](#modify-applications) section.

### DNS resolution returns public IP instead of private IP

If `nslookup` returns a public IP instead of your private endpoint IP:

1. Verify the private DNS zone exists: `az network private-dns zone show --resource-group <rg> --name privatelink.cognitiveservices.azure.com`
2. Verify the VNet link exists: `az network private-dns link vnet list --resource-group <rg> --zone-name privatelink.cognitiveservices.azure.com -o table`
3. Verify the A record exists: `az network private-dns record-set a list --resource-group <rg> --zone-name privatelink.cognitiveservices.azure.com -o table`
4. If you use a custom DNS server, ensure it forwards to the Azure private DNS zone.

### Forbidden or BadRequest when using authorization tokens

When using the `Authorization` header with a bearer token in a private endpoint scenario, the Speech service may return `Forbidden` or `BadRequest`. This happens when the **Networking** setting is not set to **All networks**. Use the `Ocp-Apim-Subscription-Key` header with your resource key instead.

### Speech Studio not accessible

If Speech Studio doesn't work with your network-restricted Speech resource, check that your public IP address is in the **Firewall** allowlist. If you only allow VNet access, Speech Studio doesn't work — use the REST API instead.

## Pricing

For pricing details, see [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link).

## Learn more

- [Use Speech service through a VNet service endpoint](speech-service-vnet-service-endpoint.md)
- [Azure Private Link](/azure/private-link/private-link-overview)
- [Azure VNet service endpoint](/azure/virtual-network/virtual-network-service-endpoints-overview)
- [Speech SDK](speech-sdk.md)
- [Speech to text REST API](rest-speech-to-text.md)
- [Text to speech REST API](rest-text-to-speech.md)
