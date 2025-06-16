---
title: "Use liveness detection with network isolation - Face"
titleSuffix: Azure AI services
description: Learn how to use face liveness detection feature with resources that disables public network access which normally blocks traffic from end users who are in the public network.
author: dipidoo
manager: 
#customer intent: As a developer, I want to use Face API Liveness Detection but also want to disable public network access to satisfy network isolation requirements of my organization or industry.

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.topic: how-to
ms.date: 06/10/2025
ms.author: pradiphe
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Use liveness detection with network isolation (preview)

Disabling public network access to internal resources is often part of your network security posture design. By routing liveness detection requests through a verified reverse proxy under your control, you can maintain a private network setup and still allow end-user devices to complete liveness checks. The proxy will forward the necessary liveness detection API calls from the client to your Face or Azure AI service. With this setup, you gain strict network control but also take on more responsibility. You must deploy and secure the proxy endpoint, and ensure it remains available – a trade-off for meeting stringent security requirements.

## About network isolation

If a Face or Azure AI services resource’s public access is disabled, any direct call from a public client (like a mobile app on the internet) will be blocked. The face liveness detection feature, which normally relies on direct client-to-service calls, won’t work by default in this configuration.

## Prerequisites

Before proceeding, make sure you have the following prerequisites in place:

* __Face API resource with Limited Access enabled__ – You need a Face or Azure AI services resource within a subscription that has been approved for the Face Liveness Detection Limited Access feature. For more information, see the [Face limited access](/legal/cognitive-services/computer-vision/limited-access-identity?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext) page.
* __Private network configuration__ – The Face or Azure AI services resource should be configured so that __Public network access__ is __Disabled__. Ensure that your networking setup is complete and tested (for example, your app server or proxy can communicate with the Face or Azure AI services resource over the [private link](../cognitive-services-virtual-networks.md#use-private-endpoints)).
* __Reverse proxy with a custom domain__ – Deploy a reverse proxy service that will act as the bridge between public clients and your Face or Azure AI services resource. This proxy should be hosted in a network that can access your Face resource (e.g. in the same VNet or via private endpoint) and exposed via a publicly reachable domain name that you control (for example, liveness.contoso.com). Importantly, configure the proxy to forward the Face liveness routes without modifying headers or payload. Ensure your proxy passes these through directly to your Face or Azure AI services resource’s private endpoint, including all authorization headers, query parameters, and body content unchanged. These correspond to creating a session, ending a session attempt, performing a liveness check, and performing a liveness check with face verification, respectively. In particular, it must handle the following REST paths used by the liveness feature:

  * `/face/[version]/session/start`
  * `/face/[version]/session/attempt/end`
  * `/face/[version]/detectLiveness/singleModal`
  * `/face/[version]/detectLivenessWithVerify/singleModal`

* DNS administration access – Because you will need to prove ownership of the proxy’s domain, you should have the ability to create DNS records (specifically, TXT records) for that domain.
* Azure support plan – The process for enabling a reverse proxy with a private Face or Azure AI services resource currently involves coordination with Microsoft support. Make sure you have the appropriate support access to create an Azure support request.

With these prerequisites satisfied, you’re ready to proceed with configuring liveness detection in a network-isolated setup.

## Solution overview

Using the Face Liveness Detection feature with Face or Azure AI services resource within isolated network involves a few key steps. At a high level, you will register your proxy’s information with Microsoft via a support request, verify domain ownership, update your client application to use the new proxy endpoint, and then test the end-to-end functionality. The timeline below outlines this process:

1. Submit Reverse Proxy Registration – Request Open an Azure support request to register your custom proxy domain for Face Liveness Detection. Include details of your Face or Azure AI services resource and proxy hostname.
1. Verify Domain Ownership – Azure support will provide a verification code. You prove ownership by adding a DNS TXT record on a specific subdomain of your proxy’s domain.
1. Azure Enables Proxy Access – Azure verifies the DNS record and configure your Face or Azure AI services resource to recognize the proxy. Once completed, the service is aware of your proxy domain for liveness detection traffic.
1. Test the Liveness Detection Workflow – Run a liveness detection session from a client device to ensure the setup works. Verify that the client’s requests go through the proxy and that you receive a successful liveness result.

Now we’ll walk through each of these steps in detail.

## Step 1: Submit a support request to register your reverse proxy

The first step is to inform Microsoft that you intend to use a reverse proxy with your Face or Azure AI services resource. Currently, this is done via an Azure support request (also known as a support ticket).

Open a new support request in Azure Portal. Navigate to your Face or Azure AI services resource in the Azure portal, and in the left-hand menu, find __Support + Troubleshooting__ (this may appear as a help icon).

1. In the textbox to briefly describe the issue, fill in a clear summary such as __"Register reverse proxy domain for Face API Liveness Detection with private network access"__.
1. In the choice of service, choose: __Cognitive Services (Cognitive Services-Face API)__.
1. In the choice of resource, choose the subscription and resource you would like to set reverse proxy on.
1. In the choice of issue, choose:
    * __None of the above__
    * Problem type: __Security__
    * Problem subtype: __Virtual Network__
1. Scroll to the very bottom and find __Need more help?__ section. Click __Create a support request__.

In the __New support request__ page:

1. Problem description – This is auto-filled from your previous responses.
1. Recommended solution – This step should be skipped.
1. Additional details – Please fill in as appropriate, for example:
    * When did the problem start? – Fill in an appropriate time, or __Not sure, use current time__
    * Description – Fill in the details, such as:
      * Reverse proxy hostname that you set up (for example, `liveness.contoso.com`)
      * Confirmation of prerequisites outlined above
      * Justification or context, and if you have a specific compliance standard or policy document, you might reference it here to help us evaluate if this preview program is appropriate for you
    * Preferred contact method – __Email__ is more suitable for this purpose given the expected turnaround time and the complexity of spelling long randomized string over the phone
    * There are other required and optional fields that you should fill in as appropriate
1. Review + create – Double-check that all necessary details are included, then create the ticket.

Microsoft support engineers should respond and guide you through the next steps shortly after. However, before we can proceed, we need to verify that you actually own the domain you want to use. This prevents unauthorized parties from hijacking or misusing the proxy configuration. You will receive instructions to perform a domain verification in the next step.

## Step 2: Verify ownership of your domain

After initiating the request, Azure support engineer will reach out with a domain verification step. This is a crucial security measure: Azure needs proof that the domain you specified for the proxy truly belongs to your organization. The support team will provide a unique code and ask you to place it in a DNS record.

### Await verification string

Azure support engineer will update your ticket and email you with a randomly generated verification string. They will specify that you need to create a DNS TXT record under a particular subdomain to confirm domain ownership. Typically, the subdomain used is a dedicated one like `azaiverify` on your domain. For example, if your proxy domain is `liveness.contoso.com`, you will be asked to create a TXT record for the name `azaiverify.liveness.contoso.com` (the exact subdomain will be provided to you). The TXT record’s value should be the provided verification string.

### Create the DNS TXT record

Using your DNS provider’s management portal or CLI, add the new TXT record as instructed. Paste the verification string exactly as given. Do not alter the string, and ensure it’s under the correct subdomain. After publishing the TXT record, respond to the support engineer to let them know the record is in place. Azure will then verify it. This needs to be done within a certain time window (usually within 48 hours) because the verification string may expire.

> [!NOTE]
>
> Domain Verification Window is __48 hours__.
> Complete the DNS TXT record setup within the recommended timeframe to avoid having to request a new verification code.

The support engineer will confirm once they have successfully verified the DNS record.

## Step 3: Microsoft configures your Face or Azure AI services resource for the proxy

Once your ownership of the domain is confirmed, Microsoft will proceed to enable the reverse proxy setting on your Face or Azure AI services resource. The support engineer will update your support request when the configuration is complete. You will then be able to proceed to use the liveness feature via your proxy.

At this point, the Face or Azure AI services resource continues to deny all direct public network access, but your proxy will handle those calls externally and then connect privately to the Face service. This design ensures that you maintain a locked-down resource, meeting your security requirements.

## Step 4: Test the end-to-end liveness detection flow

After configuration, thoroughly test your setup to ensure users can complete liveness checks through your proxy.

1. Perform a Liveness Check
    * Use your client app (e.g., mobile app with Face liveness SDK) to initiate a liveness session as an end user.
    * Confirm that all requests are routed through your proxy domain (check network logs or debugger).
1. Observe Proxy Behavior
    * Monitor your proxy’s access logs to verify it receives and forwards requests to the Face resource’s private endpoint.
    * Ensure the expected API paths (e.g., `/face/[version]/session/start`) are being accessed.
    * Check for successful responses (HTTP 200) from the Face service.
1. Verify Liveness Results
    * Complete the liveness challenge on the client.
    * Confirm that the client or app server receives a valid liveness result (e.g., success boolean or score).
    * A successful result confirms the full pipeline (client → proxy → Face service → proxy → client) is operational.
1. Troubleshooting
    * __Connection issues__: If the client cannot connect or times out, verify the proxy domain, DNS resolution, and proxy availability.
    * __HTTP 403 errors__: Ensure the proxy is registered with Azure, requests are routed through the proxy, and valid session tokens are used.
    * __Partial failures__: Check proxy logs for failed API calls; all API routes must succeed.

    If issues persist, contact Azure support for assistance.
1. Real-World Testing
    * Test with actual client apps and real users to assess latency and user experience.
    * Monitor proxy performance, request rates, response times, and errors.

## Security considerations and shared responsibility

By using a custom reverse proxy for Face API, you are effectively taking on more responsibility in exchange for greater network control. It is important to review the implications with your network security experts.

* __Network isolation__: Public network access remains disabled; only your proxy can access the Face resource.
* __Proxy as gatekeeper__: Secure your proxy with HTTPS, firewalls, rate limiting, and minimal exposed routes.
* __Shared responsibility__: You manage proxy availability, scaling, and security. Microsoft secures the Face service within Azure.
* __End-to-end encryption__: Use TLS for client-to-proxy communication and secure connections from proxy to Face service.
* __Compliance and logging__: Use your proxy for audit logging if required.
* __Domain control__: Only verified domains can be used as proxies. Update Azure if you change domains or proxy infrastructure.

## Related content

* For guidance on how to secure Azure AI service resources (like Face API) using network isolation, see [Use private endpoints section of Configure Azure AI services virtual networks](../cognitive-services-virtual-networks.md#use-private-endpoints) page.

* For details on Limited Access Features of Azure Face API, see [Face limited access](/legal/cognitive-services/computer-vision/limited-access-identity?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext) page.

* [NS-2: Secure cloud native services with network controls](/security/benchmark/azure/mcsb-network-security#ns-2-secure-cloud-native-services-with-network-controls)
