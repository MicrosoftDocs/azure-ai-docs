---
title: Shared responsibility for Face liveness detection 
titleSuffix: Foundry Tools
description: Azure and customers share responsibility for liveness detection solutions, covering connections, client apps, devices, and abuse monitoring.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.date: 01/30/2026
ms.topic: concept-article
---

# Shared responsibility for Face liveness detection

It's the shared responsibility between Azure and its customers to build a secure and compliant face liveness solution. You can learn more about Azure's shared responsibility at [Shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility). Understanding the shared responsibility model is especially important for liveness detection solutions. This document covers various aspects of how to secure and monitor your solution.

> [!IMPORTANT]
> It is important for developers to be aware of the security implications when choosing the right solution — either Web or Mobile. While both the Web and Mobile solutions conform to iBeta Level 1 and Level 2 ISO/IEC 30107-3 PAD standards, the Mobile solution includes additional Runtime Application Self-Protections (RASP) provided by [GuardSquare](https://www.guardsquare.com/blog/why-guardsquare), which are not available in the Web solution.<br><br>
> Notably, the Web solution has limitations inherent to running in browser environments and may be more vulnerable to certain types of attacks. So we recommend using the Mobile solution whenever possible.<br><br>
> If you do choose the Web solution, it is critical that you closely follow the guidance in this document, ensure that the camera in use is a trusted physical device, and consider implementing additional safeguards and monitoring to mitigate potential runtime attacks.<br>

## Secure the connections

The following diagram shows how customers work with Azure to secure the connections end-to-end. 

:::image type="content" source="media/secure-connection.png" alt-text="Diagram that shows connections in an azure liveness solution." border="false":::

Follow these guidelines to secure the connections:
- Ensure your backend service acts as the orchestrator in liveness detection applications, using Azure's security infrastructure to initiate liveness detection sessions and examine the results. The customer is responsible for securing their backend service.
- Implement proper authentication and authorization for the client application in the backend. Ensure the communication between the client application and backend service is protected from manipulation.
- Authenticate the end user's real-world identity and link their account information to the liveness session.
- Sign the application and distribute it only through official stores.

Azure liveness detection secures the connection in following ways:
- Validate all transactions using the session authorization token acquired via the session creation API.
- Allow only HTTPS calls to the backend service.
- Support the setup of Identity Access Management (IAM) roles for customers to authenticate and perform actions.

## Secure the client application

A sophisticated attacker could alter or tamper with the client application, which could render the liveness result untrustworthy. Use different approaches depending on which platform your application uses:

### Mobile applications

In both Android and iOS platforms, there are native and third-party solutions to check application integrity, such as [iOS App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity), and [Android Play Integrity](https://developer.android.com/google/play/integrity). It's the application developer’s responsibility to incorporate the integrity check feature and respond promptly to potential hacks.

Azure liveness detection implements safeguards against untrustworthy runtime environments. The liveness detection SDK provides a digest of its liveness detection service calls, which can be passed to the application integrity APIs.

### Web applications

Web applications run in the context of the browsers in which they're loaded. Modern browsers support robust application integrity checks. You are responsible for implementing the integrity checks of the web application that gets deployed to browsers. These responsibilities include, but aren't limited to:

- Ensuring security headers are properly configured. In particular, extra attention should be paid to caching, HTTP Strict Transport Security (HSTS), iframe, and cross-origin policies.
- Configuring the strictest possible Content Security Policy (CSP) for all resources. CSP helps to deny Cross-Site Scripting (XSS) attacks, clickjacking, and weaknesses associated with mixed-content pages.
- Enabling Sub-Resource Integrity (SRI) through CSP and checking to ensure that the loaded SDK is an authentic copy as published by Microsoft.

Azure publishes cryptographic hashes of the liveness detection Web SDK alongside each version, which customers can use in their script integrity CSP header. Azure also ensures the Web SDK can run within the feature restrictions of Secure Context in modern browsers.

## Secure the client device

Different applications have different security needs based on their specific use cases and scenarios, ranging from basic to highly stringent protocols. You should tailor security measures to match these requirements. Here, we highlight the different levels of security necessary for different environments.

In both Android and iOS platforms, application integrity solutions (including their respective first-party offerings) already include device integrity and/or reputation. Customers who implement web applications and require their security baseline to include device integrity need to ensure that the application is accessed only through a trusted modern browser on a trusted device. Typically, this process involves:

- Enterprise Device Management solution configured to manage the device by accessing the application.
- Virtual Network to silo the device communication with Azure, enforced by Device Management.
- Secure Boot to ensure the hardware integrity, enforced by Device Management
- Supply Chain Security for higher security baselines, which can ensure that the device is already managed and all its security policies are enforced from the point of manufacture.

These considerations are also applicable to Android and iOS platforms.

Azure Face API supports Virtual Networks and private endpoints. Refer to the [guide](../cognitive-services-virtual-networks.md).

Customer who use a high security baseline can reference a Device Management solution such as [Microsoft Defender for Endpoints](/defender-endpoint/).

## Keep your solution up to date

Microsoft regularly upgrades the liveness detection client SDK and service to improve security, reliability, and user convenience. Staying current with these updates is crucial because the liveness detection field faces active and sophisticated attacks. Customer should always use the latest client-side SDK, latest service, and latest model. For more details, see [Understanding client-side SDK versions](/azure/ai-services/computer-vision/sdk/understand-the-liveness-sdk-versions).

## Monitor abuse

Facial recognition technology, when used for access authorization, can be a target for attackers attempting to bypass it or the liveness detection technology built on top of it. Often, these attempts involve brute-forcing different materials, like various printed photos, in front of the system, which is considered system abuse. To mitigate such brute force attacks, you can take specific actions around retry count and rate limiting.

- **Create a session with conservative call and time limits**: A session serves as the first line of defense of the liveness detection process by deterring brute force compromises. A session authorization token is generated for each session and is usable for a preset quota of recognition or liveness detection attempts. If an application user doesn't succeed within the attempt limits, a new token is required. Requiring a new token allows for a reassessment of the risk associated with further retries. By setting a conservatively low number of allowed calls per session, you can reevaluate this risk more frequently before issuing a new token.
- **Use the appropriate correlation identifier when creating a session**: Device correlation ID enables the automatic abuse monitoring heuristic within Face API to help you deny abusive traffic to your system. When a particular correlation identifier reaches the threshold of abusive attempts, it can no longer be used to create sessions.
    Generate a random GUID string and associate it with sequential attempts from the same individual primary identifier within your system. The choice of identifier or identifier set to map depends on your application needs and other parameters used to assess access risk. To allow for the regeneration of a new random GUID when necessary, avoid using your application’s primary identifier.
- **Design the system to support human judgment**: When a device correlation ID is flagged and no more sessions can be created with the identifier, implement a meaningful human review process to ensure that failures aren't due to abusive traffic or brute forcing attempts. If after review you decide to allow more attempts from the same entity because previous failures are deemed legitimate, reset the association by generating a new random GUID mapped to the individual identifier.

### Azure Support for abuse monitoring

Azure provides several mechanisms to monitor liveness detection sessions and mitigate abuse:
- Traffic Monitoring: Observes activity across multiple sessions when labeled by the developer with different correlation IDs, and triggers alerts when suspicious patterns are detected.
- Auditing via API: Offers API capabilities to audit and download liveness images when the session is active.
- Comprehensive Logging: Maintains detailed logs to help prevent [repudiation attacks](/azure/security/develop/threat-modeling-tool-threats).

## Report abuse

If Azure AI Face API doesn't detect a presentation attack instrument that you believe should be detected as spoof, [create an Azure support request](/azure/ai-services/cognitive-services-support-options?context=/azure/ai-services/computer-vision/context/context).

The support request should include:
- Type of spoofing material presented.
- Service information returned from the service as part of the API call. At a minimum the information must include API path, request ID (`apim-request-id`), session ID (SID), and API model version (`model-version`).
- Specific conditions required to reproduce the attack.
- Step-by-step instructions to reproduce the attack.
- Exploit image or proof-of-concept image (if possible).
- Description of the business impact of attack.

You might attempt to recreate the attack before reporting it to Microsoft. The reproduction steps would be especially useful if you can't provide the exploited image.

## Next step

[Tutorial: Detect liveness in faces](/azure/ai-services/computer-vision/tutorials/liveness)
