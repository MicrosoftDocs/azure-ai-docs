---
title: "Use liveness detection with network isolation - Face"
titleSuffix: Foundry Tools
description: Learn how to use the face liveness detection feature when your resource has public network access disabled. This guide shows how you can support end users on public networks while keeping your Foundry Tools private.
author: PatrickFarley
manager: 
#customer intent: As a developer, I want to use Face API Liveness Detection but also want to disable public network access to satisfy network isolation requirements of my organization or industry.

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: how-to
ms.date: 01/30/2026
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Use liveness detection with network isolation (preview)

Disabling public network access to internal resources is often part of your network security posture design. By routing liveness detection requests through a verified reverse proxy under your control, you can maintain a private network setup and still allow end-user devices to complete liveness checks. The proxy forwards the necessary liveness detection API calls from the client to your Face or Foundry Tool. With this setup, you gain strict network control but also take on more responsibility. You must deploy and secure the proxy endpoint, and ensure it remains available – a trade-off for meeting stringent security requirements.

## About network isolation

If a Face or Foundry Tools resource's public access is disabled, any direct call from a public client (like a mobile app on the internet) is blocked. The face liveness detection feature, which normally relies on direct client-to-service calls, doesn't work by default in this configuration.

## Prerequisites

Before proceeding, make sure you have the following prerequisites in place:

* __Face API resource with Limited Access enabled__ – You need a Face or Foundry Tools resource within a subscription approved for the Face Liveness Detection Limited Access feature. For more information, see the [Face limited access](/legal/cognitive-services/computer-vision/limited-access-identity?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext) page.
* __Private network configuration__ – The Face or Foundry Tools resource should be configured so that __Public network access__ is __Disabled__. Ensure that your networking setup is complete and tested (for example, your app server or proxy can communicate with the Face or Foundry Tools resource over the [private link](../../cognitive-services-virtual-networks.md#use-private-endpoints)).
* __Reverse proxy with a custom domain__ – Deploy a reverse proxy service that acts as a bridge between public clients and your Face or Foundry Tools resource. Host this proxy in a network that can access your Face resource, such as the same virtual network or through a private endpoint. Expose the proxy using a public domain name that you control.

    Configure your proxy to forward Face liveness routes without changing existing headers or payloads. Make sure the proxy passes requests directly to your Face or Foundry Tools resource's private endpoint. All authorization headers, query parameters, and body content must remain unchanged.

    The proxy must support the following REST paths used by the liveness feature. These paths are for creating a session, ending a session attempt, performing a liveness check, and performing a liveness check with face verification:

    * `/face/[version]/session/start`
    * `/face/[version]/session/attempt/end`
    * `/face/[version]/detectLiveness/singleModal`
    * `/face/[version]/detectLivenessWithVerify/singleModal`

* Domain Name System (DNS) administration access – Because you need to prove ownership of the proxy's domain, you should have the ability to create DNS records (specifically, TXT records) for that domain.
* Azure support plan – The process for enabling a reverse proxy with a private Face or Foundry Tools resource currently involves coordination with Microsoft support. Make sure you have the appropriate support access for creating an Azure support request.

With these prerequisites satisfied, you're ready to proceed with configuring liveness detection in a network-isolated setup.

## Solution overview

Using the Face Liveness Detection feature with Face or Foundry Tools resource within isolated network involves a few key steps. At a high level, you register your proxy's information with Microsoft via a support request, verify domain ownership, update your client application to use the new proxy endpoint, and then test the end-to-end functionality.

1. Submit Reverse Proxy Registration – Begin registration of your custom proxy domain for Face Liveness Detection by opening an Azure support request. Include details of your Face or Foundry Tools resource and proxy hostname.
1. Verify Domain Ownership – Azure support provides a verification code. You prove ownership by adding a DNS TXT record on a specific subdomain of your proxy's domain.
1. Wait for Azure to Enable Proxy Access – Azure verifies the DNS record and configure your Face or Foundry Tools resource to recognize the proxy. Once completed, the service is aware of your proxy domain for liveness detection traffic.
1. Test the Liveness Detection Workflow – Ensure the setup works by running a liveness detection session from a client device. Verify that the client's requests go through the proxy and that you receive a successful liveness result.

The following sections provide detailed instructions for each step.

## Step 1: Register your reverse proxy by submitting a support request

To begin the process of enabling liveness detection with network isolation, your goal is to register your reverse proxy domain with Microsoft. Open an Azure support request to initiate this registration for your Face or Foundry Tools resource. Navigate to your Face or Foundry Tools resource in the Azure portal, and in the left-hand menu, find __Support + Troubleshooting__ (which may appear as a help icon).

1. In the textbox for a brief issue description, enter a clear summary such as: __"Request to register a reverse proxy domain for Face API Liveness Detection with public network access disabled."__
1. In the choice of service, choose: __Cognitive Services (Cognitive Services-Face API)__.
1. In the choice of resource, choose the subscription and resource you would like to set reverse proxy on.
1. In the choice of issue, choose:
    * __None of the above__
    * Problem type: __Security__
    * Problem subtype: __Virtual Network__
1. Scroll to the very bottom and find __Need more help?__ section. Click __Create a support request__.

In the __New support request__ page:

1. Problem description – This description is autofilled from your previous responses.
1. Recommended solution – This step should be skipped.
1. Additional details – Fill in as appropriate, for example:
    * When did the problem start? – Fill in an appropriate time, or __Not sure, use current time__
    * Description – Fill in the details, such as:
      * Reverse proxy hostname that you set up (for example, `liveness.contoso.com`)
      * Confirmation of prerequisites
      * Justification or context, and if you have a specific compliance standard or policy document, you might reference it here to help us evaluate if this preview program is appropriate for you
    * Preferred contact method – __Email__ is more suitable for this purpose given the expected turnaround time and the complexity of spelling long randomized string over the phone
    * Fill in other fields as appropriate
1. Review + create – Double-check that all necessary details are included, then create the ticket.

Azure support engineers should respond and guide you through the next steps shortly after. However, before we can proceed, we need to verify that you actually own the domain you want to use. This verification step prevents unauthorized parties from hijacking or misusing the proxy configuration. You'll receive instructions to perform a domain verification in the next step.

## Step 2: Verify ownership of your domain

After you initiate the request, Azure support engineer will reach out with a domain verification step. Azure needs proof that the domain you specified for the proxy truly belongs to your organization. The support team provides a unique code and ask you to place it in a DNS record.

### Await verification string

Azure support engineer updates your ticket and email you a randomly generated verification string. Confirm your domain ownership by creating a DNS TXT record under a particular subdomain. Typically, the subdomain used is a dedicated one like `azaiverify` on your domain. For example, if your proxy domain is `liveness.contoso.com`, create a TXT record for the name `azaiverify.liveness.contoso.com` (the emailed instructions contain the exact subdomain for this step). The TXT record's value should be the provided verification string.

### Create the DNS TXT record

Using your DNS provider's management portal or CLI, add the new TXT record as instructed. Paste the verification string exactly as given. Don't alter the string, and ensure it's under the correct subdomain. After publishing the TXT record, respond to the support engineer to let them know the record is in place. This step needs to be done within a certain time window (usually within 48 hours) because the verification string may expire.

> [!NOTE]
>
> Domain Verification Window is __48 hours__.
> Avoid having to request a new verification code by completing the DNS TXT record setup within the recommended timeframe.

The support engineer confirms DNS record verification after successful validation.

## Step 3: Microsoft configures your Face or Foundry Tools resource for the proxy

After Microsoft confirms your domain ownership, the support engineer enables the reverse proxy setting on your Face or Foundry Tools resource. The support request is updated once configuration is complete. You can then use the liveness detection feature through your proxy.

At this point, the Face or Foundry Tools resource continues to deny all direct public network access, but your proxy handles those calls and then connect privately to the Face service. This design ensures that you maintain a locked-down resource, meeting your security requirements.

## Step 4: Test the end-to-end liveness detection flow

After configuration, thoroughly test your setup to ensure users can complete liveness checks through your proxy.

1. Perform a Liveness Check
    * Initiate a liveness session as an end user using your client app (for example, mobile app with Face liveness SDK).
    * Confirm that all requests are routed through your proxy domain (check network logs or debugger).
1. Observe Proxy Behavior
    * Monitor your proxy's access logs to verify it receives and forwards requests to the Face resource's private endpoint.
    * Ensure the expected API paths (for example, `/face/[version]/session/start`) are being accessed.
    * Check for successful responses (HTTP 200) from the Face service.
1. Verify Liveness Results
    * Complete the liveness challenge on the client.
    * Confirm that the client or app server receives a valid liveness result (for example, success boolean or score).
    * A successful result confirms the full pipeline (client → proxy → Face service → proxy → client) is operational.
1. Troubleshooting
    * __Connection issues__: If the client can't connect or times out, verify the proxy domain, DNS resolution, and proxy availability.
    * __HTTP 403 errors__: Ensure the proxy is registered with Azure, requests are routed through the proxy, and valid session tokens are used.
    * __Partial failures__: Check proxy logs for failed API calls; all API routes must succeed.

    If issues persist, contact Azure support for assistance.
1. Real-World Testing
    * Test with actual client apps and real users to assess latency and user experience.
    * Monitor proxy performance, request rates, response times, and errors.

## Security considerations and shared responsibility

By using a custom reverse proxy for Face API, you're effectively taking on more responsibility in exchange for greater network control. It's important to review the implications with your network security experts.

* __Network isolation__: Public network access remains disabled; only your proxy can access the Face resource.
* __Proxy as gatekeeper__: Secure your proxy with HTTPS, firewalls, rate limiting, and minimal exposed routes.
* __Shared responsibility__: You manage proxy availability, scaling, and security. Microsoft secures the Face service within Azure.
* __End-to-end encryption__: Use Transport Layer Security (TLS) for client-to-proxy communication and secure connections from proxy to Face service.
* __Compliance and logging__: Use your proxy for audit logging if necessary.
* __Domain control__: Only verified domains can be used as proxies. Update Azure if you change domains or proxy infrastructure.

## Related content

* For guidance on how to secure Foundry Tools resources (like Face API) using network isolation, see [Use private endpoints section of Configure Foundry Tools virtual networks](../../cognitive-services-virtual-networks.md#use-private-endpoints) page.

* For details on Limited Access Features of Azure Face API, see [Face limited access](/legal/cognitive-services/computer-vision/limited-access-identity?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext) page.

* For related security control by Microsoft, see [NS-2: Secure cloud native services with network controls](/security/benchmark/azure/mcsb-network-security#ns-2-secure-cloud-native-services-with-network-controls) page.
