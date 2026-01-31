---
title: Abuse monitoring in Face liveness detection - Face
titleSuffix: Foundry Tools
description: Learn about abuse-monitoring methods in Azure Face service.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: concept-article
ms.date: 01/30/2026
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Abuse monitoring in Face liveness detection

Azure AI Face liveness detection lets you detect and mitigate instances of recurring content and/or behaviors that indicate a violation of the [Code of Conduct](/legal/ai-code-of-conduct?context=/azure/ai-services/computer-vision/context/context) or other applicable product terms. This guide shows you how to work with these features to ensure your application is compliant with Azure policy.

Details on how data is handled can be found on the [Data, Privacy, and Security](/azure/ai-foundry/responsible-ai/face/data-privacy-security) page.

[!INCLUDE [liveness-sdk-gate](./includes/liveness-sdk-gate.md)]

## Components of abuse monitoring in Face API v1.2 and earlier

There are several components to Face liveness abuse monitoring:
- **Session management**: Your backend application system creates liveness detection sessions on behalf of your end-users. The Face service issues authorization tokens for a particular session, and each is valid for a limited number of API calls. When the end-user encounters a failure during liveness detection, a new token is requested. This allows the backend application to assess the risk of allowing more liveness retries. An excessive number of retries may indicate a brute force adversarial attempt to bypass the liveness detection system.
- **Temporary correlation identifier**: The session creation process prompts you to assign a temporary 128-bit correlation GUID (globally unique identifier) for each end-user of your application system. This lets you associate each session with an individual. Classifier models on the service backend can detect presentation attack cues and observe failure patterns across the usage of a particular GUID. This GUID must be resettable on demand to support the manual override of the automated abuse mitigation system.
- **Abuse pattern capture**: Azure AI Face liveness detection service looks at customer usage patterns and employs algorithms and heuristics to detect indicators of potential abuse. Detected patterns consider, for example, the frequency and severity at which presentation attack content is detected in a customer's image capture.
- **Human review and decision**: When the correlation identifiers are flagged through abuse pattern capture as described above, no further sessions can be created for those identifiers. You should allow authorized employees to assess the traffic patterns and either confirm or override the determination based on predefined guidelines and policies. If human review concludes that an override is needed, you should generate a new temporary correlation GUID for the individual in order to generate more sessions.
- **Notification and action**: When a threshold of abusive behavior has been confirmed based on the preceding steps, the customer should be informed of the determination by email. Except in cases of severe or recurring abuse, customers typically are given an opportunity to explain or remediate&mdash;and implement mechanisms to prevent the recurrence of&mdash;the abusive behavior. Failure to address the behavior, or recurring or severe abuse, may result in the suspension or termination of your Limited Access eligibility for Azure AI Face resources and/or capabilities.

## Additional components of abuse monitoring in v1.3 

-	Version 1.3 liveness detection introduces an extra component to improve abuse monitoring. This feature monitors matching facial templates across temporary correlation identifiers and will flag potential abuse in liveness detection results when similar facial templates are repeatedly used with different temporary correlation identifiers. Incorrectly setting up a temporary correlation identifier may also cause this feature to flag abuse. You can turn off this feature if you think it is not applicable to your use case by calling [liveness setting API](/rest/api/face/liveness-session-operations/patch-settings?view=rest-face-v1.3-preview&preserve-view=true).

## Related content

- [Learn more about understanding and mitigating risks associated with identity management](/azure/security/fundamentals/identity-management-overview)
- [Learn more about how data is processed for abuse monitoring](/azure/ai-foundry/responsible-ai/face/data-privacy-security)
- [Learn more about supporting human judgment in your application system](/azure/ai-foundry/responsible-ai/face/characteristics-and-limitations#design-the-system-to-support-human-judgment)
