---
title: "Face liveness detection - Face"
titleSuffix: Azure AI services
description: This article explains the concept of Face liveness detection, its input and output schema, and related concepts. 
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.custom:
ms.topic: conceptual
ms.date: 02/19/2025
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Face liveness detection

This article explains the concept of Face liveness detection, its input and output schema, and related concepts. 

## How it works

TBD

The Face Liveness Check is conformant to ISO/IEC 30107-3 PAD (Presentation Attack Detection) standards as validated by iBeta level 1 and level 2 conformance testing; the report is [here](https://www.ibeta.com/wp-content/uploads/2023/11/230622-Microsoft-PAD-Level-2-Confirmation-Letter.pdf).


## Liveness detection modes

Azure Face liveness detection API includes the options for both passive and passive-active detection modes.

The **Passive mode** requires a non-bright lighting environment to succeed and will fail in bright lighting environments with an "Environment not supported" error. This mode can be chosen if you prefer minimal end-user interaction and expect end-users to primarily be in non-bright environments.  This mode utilizes a passive liveness technique that requires no additional actions from the user. It also requires high screen brightness for optimal performance which is configured automatically in the Mobile (iOS and Android) solutions.

The **Passive-Active mode** will still behave the same as the Passive mode in non-bright lighting environments and only trigger the Active mode in bright lighting environments. This mode can be chosen if you want the liveness-check to work in any lighting environment. This mode is preferable on Web browser solutions due to the lack of automatic screen brightness control available on browsers which hinders the Passive mode's operational envelope.

This setting can be set during the Session-Creation step (see step 2 of [Perform liveness detection](#perform-liveness-detection)).


## Input requirements

Use the following tips to ensure that your input images give the most accurate recognition results:

[!INCLUDE [identity-input-id-verification-composition](includes/identity-input-id-verification-composition.md)]

### Data privacy

We do not store any images or videos from the Face Liveness Check. No image/video data is stored in the liveness service after the liveness session has been concluded. Moreover, the image/video uploaded during the liveness check is only used to perform the liveness classification to determine if the user is real or a spoof (and optionally to perform a match against a reference image in the liveness-with-verify-scenario), and it cannot be viewed by any human and will not be used for any AI model improvements.

## Output format

The liveness detection API returns a JSON object with the following information:
- A Real or a Spoof Face Liveness Decision. We handle the underlying accuracy and thresholding, so you don’t have to worry about interpreting “confidence scores” or making inferences yourself. This makes integration easier and more seamless for developers.
- Optionally a Face Verification result can be obtained if the liveness check is performed with verification (see [Perform liveness detection with face verification](#perform-liveness-detection-with-face-verification)).
- A quality filtered "session-image" that can be used to store for auditing purposes or for human review or to perform further analysis using the Face service APIs.


## Next steps

Now that you're familiar with liveness detection concepts, implement liveness detection in your app.

* [Face liveness detection](./tutorials/liveness.md)
