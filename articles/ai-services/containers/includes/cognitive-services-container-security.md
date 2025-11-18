---
title: Container security
titleSuffix: Foundry Tools
description: Learn how to secure your container
author: aahill
manager: nitinme
ms.service: azure-ai-services
ms.topic: include
ms.date: 12/17/2020
ms.author: aahi
---

## Foundry Tools container security

Security should be a primary focus whenever you're developing applications. The importance of security is a metric for success. When you're architecting a software solution that includes Azure AI containers, it's vital to understand the limitations and capabilities available to you. For more information about network security, see [Configure Foundry Tools virtual networks][az-security].

> [!IMPORTANT]
> By default there is *no security* on the Foundry Tools container API. The reason for this is that most often the container will run as part of a pod which is protected from the outside by a network bridge. However, it is possible for users to construct their own authentication infrastructure to approximate the authentication methods used when accessing the [cloud-based Foundry Tools][request-authentication].

The following diagram illustrates the default and **non-secure** approach:

![Container security](../media/container-security.svg)

As an example of an alternative and *secure* approach, consumers of Azure AI containers could augment a container with a front-facing component, keeping the container endpoint private. Let's consider a scenario where we use [Istio][istio] as an ingress gateway. Istio supports HTTPS/TLS and client-certificate authentication. In this scenario, the Istio frontend exposes the container access, presenting the client certificate that is approved beforehand with Istio.

[Nginx][nginx] is another popular choice in the same category. Both Istio and Nginx act as a service mesh and offer additional features including things like load-balancing, routing, and rate-control.

### Container networking

The Azure AI containers are required to submit metering information for billing purposes. Failure to allowlist various network channels that the Azure AI containers rely on will prevent the container from working.

#### Allowlist Foundry Tools domains and ports

The host should allowlist **port 443** and the following domains:

* `*.cognitive.microsoft.com`
* `*.cognitiveservices.azure.com`

If you are using the Azure Translator in Foundry Tools on-premise, you need to additionally allow the following URLs to download files

* `translatoronprem.blob.core.windows.net`

#### Disable deep packet inspection

[Deep packet inspection (DPI)](https://en.wikipedia.org/wiki/Deep_packet_inspection) is a type of data processing that inspects in detail the data sent over a computer network, and usually takes action by blocking, rerouting, or logging it accordingly.

Disable DPI on the secure channels that the Azure AI containers create to Microsoft servers. Failure to do so will prevent the container from functioning correctly.

[istio]: https://istio.io/
[nginx]: https://www.nginx.com
[request-authentication]: ../../authentication.md
[az-security]: ../../cognitive-services-virtual-networks.md
