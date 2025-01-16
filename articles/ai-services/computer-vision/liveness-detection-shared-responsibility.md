---
title: Shared Responsibility For Face Liveness Detection 
titleSuffix: Azure AI services
description: Azure and customers share responsibility for liveness detection solutions, covering connections, client apps, devices, and abuse monitoring
author: JinyuID
ms.author: lijiny
manager: nitinme
ms.service: azure-ai-vision
ms.date: 01/15/2025
ms.topic: security
---

# Shared Responsibility for Face Liveness Detection

It's the shared responsibility between Azure and the customer to build a secure and compliance solution. You can learn more about Azure shared responsibility model at here: [Shared responsibility in the cloud - Microsoft Azure](/azure/security/fundamentals/shared-responsibility). Understanding the shared responsibility model is especially important for liveness detection solutions, this document covers three aspects about how to secure the solution and monitor the solution.

## Secure the Connections

The following diagram shows how customers work with Azure to secure the connections end to end. :::image type="content" source="media/secure-connection.png" alt-text="Azure liveness solution connection diagram":::
  
- Ensure the customer’s backend service acts as the orchestrator in liveness detection applications, using Azure's security infrastructure to initiate liveness detection sessions and examine the results. The customer is responsible for securing their backend service.
- Implement proper authentication and authorization for the client application in the customer backend. Ensure the communication between the client application and backend service is protected from manipulation.
- Authenticate the end user's real-world identity and link their account information to the liveness session.
- Sign the application and distribute it only through official stores.
Azure liveness detection secures the connection in following ways:
- Validate all transactions using the session authorization token acquired via the session creation API.
- Allow only HTTPS calls to the backend service.
- Support the setup of Identity Access Management(IAM) roles for customers to authenticate and perform actions.

## Secure the Client Application

A sophisticated attacker could alter or tamper the client application, which could render the liveness result not trustworthy. There are different approaches depending on which platform the application use:

### Mobile Applications

In both Android and iOS platforms, there are native support and third party solutions to check application integrity, such as [iOS App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity), and [Android Play Integrity](https://developer.android.com/google/play/integrity). It's the application developer’s responsibility to integrate the integrity check feature and respond promptly to potential hacks.
Azure liveness detection implemented safeguards against untrustworthy runtime environments. Azure Liveness Detection SDK provides the digest of its liveness detection service call, which can be provided to the application integrity APIs.

### Web Applications

Web applications run in the context of browsers in which they're loaded. Modern browsers support robust application integrity checks. Customer is responsible for ensuring and implementing the integrity checks of the web application that gets deployed to the browsers. These responsibilities include, but aren't limited to:

- Ensuring security headers are properly configured. In particular, extra attention should be paid to caching, HTTP Strict Transport Security (HSTS), iframe, and cross-origin policies.
- Configuring the strictest possible Content Security Policy (CSP) for all resources. CSP helps to deny Cross-Site Scripting (XSS) attack, clickjacking, and weaknesses associated with mixed content page.
- Enabling Sub-Resource Integrity (SRI) through CSP and checking to ensure that the SDK loaded is an authentic copy as published by Microsoft.

Azure publishes cryptographic hashes of the Liveness Detection Web SDK alongside each version, which customer can use in their script integrity CSP header. Azure also ensures the Web SDK can run within feature restrictions of Secure Context in modern browsers.

## Secure the Client Device

Different applications have various security needs based on their specific use cases and scenarios. It's essential to tailor security measures to match these requirements, ranging from basic to highly stringent protocols. Here, we discuss the different levels of security necessary for different environments, ensuring comprehensive protection across all platforms.
In both Android and iOS platforms, application integrity solutions (including their respective first-party offerings) already include device integrity and/or reputation. Customers who implement web applications and require their security baseline to include device integrity must take specific responsibilities. They need to ensure that the application is accessed only through a trusted modern browser on a trusted device. Typically, these responsibilities include:

- Enterprise Device Management solution configured to manage the device by accessing the application
- Virtual Network to silo the device communication with Azure, enforced by Device Management.
- Secure Boot to ensure the hardware integrity, enforced by Device Management
- Supply Chain Security for higher security baselines, can ensure that the device is already managed, and all its security policies enforced from the point of manufacture.

These considerations are also applicable to Android and iOS platforms.
Azure Face API supports Virtual Networks and private endpoints. Refer to the guide.
Customer who considers high security baseline could reference Device Management solution such as Microsoft Defender for Endpoints.

## Always Keep Up-to-date

Microsoft regularly upgrades the liveness detection client SDK and service to improve security, reliability, and user convenience. Staying current with these updates is crucial because the liveness detection field faces active and sophisticated attacks. Customer should always use latest Client-side SDK, latest service, latest service model. For more details, please reference [Understanding Client-side SDK versions](/azure/ai-services/computer-vision/sdk/understand-the-liveness-sdk-versions).

## Monitoring Abuse

Facial recognition technology, when used for access authorization, can be a target for adversaries attempting to bypass it or the liveness detection technology. Often, these bypass attempts involve brute forcing different materials like various printed photos in front of the system, which is considered system abuse. To mitigate such brute force attacks, specific actions around retry count and rate limiting should be implemented.

**Create a session with conservative call and time limits**
A session serves as the frontline of defense, ensuring the liveness detection process is secure and consistent, then deterring brute force compromises. A session authorization token is generated for each session and is usable for a preset quota of recognition or liveness detection attempts. If an application user fails to succeed within the attempt limits, a new token is required. Requiring a new token allows for a reassessment of the risk associated with further retries. By setting a conservatively low number of allowed calls per session, you can reevaluate this risk more frequently before issuing a new token.

**Use the appropriate correlation identifier when creating a session**
Device correlation ID guides the automatic abuse monitoring heuristics within Face API to help you deny abusive traffic to your system that implements facial liveness detection. When a particular correlation identifier reaches the threshold of abusive attempts, it can no longer be used to create sessions.

Generate a random GUID string and associate it with sequential attempts from the same individual primary identifier within your system. The choice of identifier or identifier set to map depends on your application needs and other parameters used to assess access risk. To allow for the regeneration of a new random GUID when necessary, avoid using your application’s primary identifier.

**Design the system to support human judgment**
When a device correlation ID is flagged and no more sessions can be created with the identifier, implement a meaningful human review process to ensure that failures aren't due to abusive traffic or brute forcing attempts. If after review you decide to allow more attempts from the same entity because previous failures are deemed legitimate, reset the association by generating a new random GUID mapped to the individual identifier.

### Azure Support for Abuse Monitoring

Azure provides the following mechanism monitoring liveness detection sessions:

- Monitoring traffic across multiple sessions on same correlation ID, take response when suspicious activity monitored.
- API support customers for auditing to download liveness images during the liveness session   lifespan.
- Azure keeps sufficient logs to further prevent repudiation attacks.  

## Report Abuse

If Azure AI Face API doesn't detect a presentation attack instrument that you believe should be detected as spoof, [create an Azure support request](/azure/ai-services/cognitive-services-support-options?context=/azure/ai-services/computer-vision/context/context).
The support request should include:

- Type of spoofing material presented.
- Service information returned from the service as part of the API call. At a minimum the information must include API path, request ID (apim-request-id), session ID (SID), and API model version (model version).
- Specific conditions required to reproduce the attack.
- Step-by-step instructions to reproduce the attack.
- Exploit image or proof-of-concept image (if possible).
- Description of the business impact of attack.

You might attempt to recreate the attack before reporting it to Microsoft. The reproduce steps would be especially useful if you can't provide the exploited image.

## Next steps

[Tutorial: Detect liveness in faces](/azure/ai-services/computer-vision/tutorials/liveness)
