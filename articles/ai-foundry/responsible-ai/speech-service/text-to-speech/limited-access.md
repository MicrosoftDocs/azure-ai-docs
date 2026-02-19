---
title: Limited Access
titleSuffix: Foundry Tools
description: This article explains why custom neural voice is available as Limited Access feature and how to request access.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 06/16/2022
---

# Limited Access

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

#### [Custom neural voice](#tab/cnv)

As part of Microsoft’s commitment to responsible AI, custom neural voice is designed with the intention of protecting the rights of individuals and society, fostering transparent human-computer interaction, and counteracting the proliferation of harmful deepfakes and misleading content. For this reason, custom neural voice is a Limited Access feature available by registration only, and only for certain use cases.

> [!NOTE]
> Approved Limited Access registrants for custom neural voice will also get access to deploy and use a custom neural voice lite voice model. Custom neural voice lite is a project type in public preview that allows you to record 20-50 voice samples on Speech Studio and create a lightweight custom voice model for demonstration and evaluation purposes. Both the recording script and the testing script are pre-defined by Microsoft. A synthetic voice model you create using custom neural voice lite may be deployed and used more broadly only if you apply for and receive full access to custom neural voice (subject to applicable terms).
>
> Personal voice, including the try-with-your-own-data demo experience in Speech Studio,* *is a Limited Access feature* *and requires registration and approval. Customers must register to access the demo and/or the API for business use.   

## Registration process 

As a Limited Access feature, access to custom neural voice requires registration. Only customers managed by Microsoft, meaning those who are working directly with Microsoft account teams, are eligible for access. Customers who wish to use this feature are required to register by submitting the [Limited Access registration form](https://aka.ms/customneural). Your use of custom neural voice is limited to the use case(s) that you select and Microsoft approves at the time of registration. Microsoft may require customers to re-verify information submitted for registration. 

Custom neural voice is made available to customers under the terms governing their subscription to Microsoft Azure Services (including the [Service Specific Terms](https://go.microsoft.com/fwlink/?linkid=2018760)). Please review these terms carefully as they contain important conditions and obligations governing your use of custom neural voice. For example, these terms include, but are not limited to, the following obligations:
- **Voice talent and approved use cases**. Customers must warrant that they have obtained explicit written permission from voice talent prior to creating a voice model, and must share the [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent) with the voice talent in advance. Customer may use each custom voice model only for use cases approved during registration. 
- **Implementation requirements**. As outlined in our [Code of conduct](/legal/ai-code-of-conduct?context=/azure/ai-services/speech-service/context/context), in addition to other requirements, customers must not use any custom voice model for prohibited uses and must also agree that when deploying each custom voice model, they will [disclose the synthetic nature](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines) of the service to users and support a feedback channel that allows users of the service to report issues and share details with Microsoft. 
- **Microsoft's additional processing and use of voice talent data**. Before a customer can train a custom voice model, Microsoft will require the customer to upload a recorded audio file to the Speech Studio with a pre-defined statement from the voice talent acknowledging that the customer will use the talent's voice to create a synthetic voice. As a technical safeguard intended to help prevent misuse of this service, Microsoft reserves the right to use Microsoft's speaker recognition biometric identification technology on this recorded acknowledgement statement and verify it against the training audio data to confirm that the voices are from the same speaker. Microsoft will also continue to retain this recorded acknowledgement statement file and the custom voice model to protect the security and integrity of our services. **Customer is responsible for ensuring all necessary permissions are obtained from voice talent for these purposes**.

#### [Custom text to speech avatar](#tab/avatar)

As part of Microsoft's commitment to responsible AI, custom text to speech avatar is designed with the intention of protecting the rights of individuals and society, fostering transparent human-computer interaction, and counteracting the proliferation of harmful deepfakes and misleading content. For this reason, custom text to speech avatar is a Limited Access feature available by registration only, and only for certain use cases.

## Registration process 

As a Limited Access feature, custom text to speech avatar requires registration. Only customers managed by Microsoft, meaning those who are working directly with Microsoft account teams, are eligible for access. Customers who wish to use this feature are required to register by submitting the [Limited Access registration form](https://aka.ms/customneural). Your use of custom text to speech avatar is limited to the use case(s) that you select and Microsoft approves at the time of registration. Microsoft may require customers to re-verify information submitted for registration.  

Custom text to speech avatar is made available to customers under the terms governing their subscription to Microsoft Azure Services (including the [Service Specific Terms](https://go.microsoft.com/fwlink/?linkid=2018760)). Please review these terms carefully as they contain important conditions and obligations governing your use of custom text to speech avatar. For example, these terms include, but are not limited to, the following obligations: 
- **Avatar talent and approved use cases**. Customers must warrant that they have obtained explicit written permission from avatar talent prior to creating an avatar model, and must share the [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent) with the avatar talent in advance. Customer may use each custom avatar model only for use cases approved during registration.  
- **Implementation requirements**. As outlined in our [Code of conduct](/legal/ai-code-of-conduct?context=/azure/ai-services/speech-service/context/context), in addition to other requirements, customer must not use any  custom avatar model for prohibited uses and must also agree that when deploying each custom avatar model, they will [disclose the synthetic nature](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines) of the service to users and support a feedback channel that allows users of the service to report issues and share details with Microsoft. 
- **Microsoft's additional processing and use of avatar talent data**. Before a customer can train a custom avatar model, Microsoft will require the customer to upload a recorded video file with a pre-defined statement from the avatar talent acknowledging that the customer will use the talent’s image and voice to create a text to speech avatar. As a technical safeguard intended to help prevent misuse of this service, Microsoft reserves the right to verify the acknowledgement video statement file against the training audio data to confirm that the videos are from the same person. Microsoft will also continue to retain this acknowledgement statement file and the custom avatar model to protect the security and integrity of our services. **Customer is responsible for ensuring all necessary permissions are obtained from avatar talent for these purposes**. 

Learn more about how we process this data in the [Data, privacy, and security doc](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security). Learn more about the legal terms that apply to this feature [here](https://azure.microsoft.com/support/legal/).

---

## Help and support

FAQ about Limited Access features can be found [here](/azure/ai-services/cognitive-services-limited-access).

If you need help with custom neural voice, find support [here](/azure/ai-services/cognitive-services-support-options).

Report abuse of custom neural voice [here](https://aka.ms/reportabuse).

Learn more about how we process this data in the [Data, privacy, and security doc](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security). Learn more about the legal terms that apply to this feature [here](https://azure.microsoft.com/support/legal/). 

## Next steps

* [Introduction to custom neural voice](/azure/ai-services/speech-service/custom-neural-voice)
* [Transparency note and use cases for custom neural voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
* [Responsible deployment of synthetic speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
* [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent)
