---
title: Data and privacy for Speaker Recognition
titleSuffix: Azure AI services
description: This document details issues for data, privacy, and security for the Speaker Recognition feature.
author: HeidiHanZhang 
ms.author: heidizh
manager: nitinme
ms.service: azure-ai-speech
ms.topic: article
ms.date: 10/08/2021
---

# Data and privacy for Speaker Recognition

> [!NOTE]
> This article is provided for informational purposes only and not for the purpose of providing legal advice. We strongly recommend seeking specialist legal advice when implementing Speaker Recognition.

While the Speaker Recognition feature was designed with compliance, privacy, and security in mind, you're responsible for its use and the implementation of this technology. Be aware that the laws governing biometric recognition technologies often vary internationally and domestically, including at the federal, state, and local levels. In addition to regulating allowed use cases, some jurisdictions impose special legal requirements for the permissions governing collection, transfer, online processing, and storage of biometric data, particularly when used for identification or verification. Before using Speaker Recognition and Azure for the collect, transfer, processing, and storage of any data subject's biometric data, you must ensure compliance with the relevant legal requirements that apply to your service application.

> [!NOTE]
> For our customer’s convenience, please consider utilizing the following disclosure regarding Microsoft’s role when you use Azure AI services Speaker Recognition with your end users:
>
> [Company] uses Microsoft Speaker Recognition technology to process [Company’s] users’ biometric data as its service provider (“Processor”). Microsoft may process and store your enrollment audio and voice signatures for the purposes of providing speaker verification and/or identification services on [Company]’s behalf, and only as instructed by [Company]. Microsoft will store this data as long as [Company] requests, which shall be no longer than a limited grace period after the date when (i) [Company] ceases to have a relationship with Microsoft or (ii) when [Company] requests deletion.

## What data does Speaker Recognition process?

Speaker Recognition processes the following types of data:

**Enrollment audio:** Before enrollment, customers request a random GUID from the service. During the enrollment phase, customers send a speaker’s audio input and the GUID to generate a voice signature and a passphrase signature match.

**Enrolled voice signature:** This is the numeric vector that represents an individual speaker’s voice characteristics, extracted from audio recordings. 

**Passphrase signature:** This is a pre-defined phrase, for example, ‘My voice is my profile’.  During enrollment of a speaker, enrollment audio will be processed through Azure AI Speech service in order to confirm that the text from that audio matches the passphrase required. 


**Recognition audio:** After the enrollment of the customer’s speaker(s), the customer sends audio input along with the relevant GUIDs to be processed to the Speaker Recognition feature and voice signatures are processed to determine if the audio matches the enrolled speaker’(s) voice signatures. If using text-dependent speaker verification, the passphrase signature is also transcribed by speech recognition to determine if there is a passphrase match.

## How Does Speaker Recognition process this data?

* **Text-dependent speaker verification system:**
  * **Enrollment Phase:** The speaker’s voice is enrolled by saying a passphrase from a set of predefined phrases. Speaker Recognition extracts voice features from these audio recordings to form a unique voice signature, and the text of the chosen passphrase is verified through speech recognition. Both the voice signature and the passphrase are stored for the recognition phase. 
  * **Recognition Phase:** The speaker needs to speak the same passphrase from the enrollment phase. During the recognition phase, Speaker Recognition extracts the voice features from the audio and recognizes the passphrase in the audio. Then the service compares both the voice features and the passphrase against the voice signature and the passphrase signature in the record. Only when both the voice and passphrase match the enrolled voice signature and passphrase signature by achieving the match threshold, the response returns *Accept* and provides a similarity score.

* **Text-independent speaker verification or identification system:**
  * **Activation and Enrollment Phase:** Speaker Recognition extracts the voice features from a speaker’s enrollment audio to form a unique voice signature. There are two steps in the enrollment:
    1. In the activation step when active enrollment is enabled, the speaker's voice is recorded saying an activation phrase defined by Microsoft. The text of the activation phrase is transcribed using speech recognition technology provided by Azure AI Speech, and then compared with the predefined activation phrase. If a match is found, the audio of the activation phrase is stored as the voice signature. Unlike the passphrase in the text-dependent system, the text of the activation phrase won't be stored.

    2. The speaker can continue enrolling by speaking in everyday language to improve the performance of future verification or identification. This step is optional but recommended. After the activation step, there's no restriction on what the speaker says in the audio. The speech content will not be processed, only the voice signature will be extracted and stored for the recognition phase.
  * **Recognition Phase:** After the activation and enrollment phase, the customer may send audio to the Speaker Recognition feature. Speaker Recognition will extract the voice features from the audio. For speaker identification system, Speaker Recognition compares these voice features against a list of voice signatures associated with the specified GUIDs, one by one. The service then ranks the list of GUIDs based on their similarity scores and returns up to five GUIDs and their similarity scores. For speaker verification system, Speaker Recognition compares these voice features against the voice signature in the record. When the voice matches the enrolled voice signature by achieving the match threshold, the response returns *Accept* and provides a similarity score.

## How is data retained, and what customer controls are available?

Enrollment audio, voice signatures, and passphrases are all securely stored in the customer’s Azure tenancy. This data is associated with random GUIDs only and Microsoft is not able to connect any customer names, IDs (other than the random GUID), or other personal information to the enrollment audio, voice signatures, or passphrase signatures. Developers can create, update, and delete enrollment data (both the voice signature and related enrollment audio) for individual speaker through API calls. When the subscription is deleted, all the speaker enrollment data associated with the subscription is also deleted. The following table summarizes Speaker Recognition data retention and controls.

| **Data type** | **Retention** | **Customer controls** |
|---------------|---------------|-----------------------|
|Enrollment audio|Microsoft assigns randomly generated GUIDs (globally unique identifiers) to the enrollment audio for each individual. This GUID is also associated with the voice signature.|You can manage and delete all data that is stored associated with any individual GUID or all GUIDs.|
|Enrolled voice signature|Microsoft assigns a randomly generated unique identifier to every enrolled voice signature.|You can manage and delete all data that is stored associated with any individual GUID or all GUIDs.|
|Passphrase signature|For text-dependent enrollment, the passphrase signature is stored as text, and it's stored with the voice signature.|You can manage and delete all data that is stored associated with any individual GUID or all GUIDs.|
|Recognition audio|Audio sent to the service aren't stored after they're analyzed against the voice signature.|There are no customer controls for this data type.|

To learn more about privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/trust-center).

## Next steps

* [Speaker Recognition overview](/azure/ai-services/speech-service/speaker-recognition-overview)
* [Limited access for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/limited-access-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
* [Transparency Note for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/transparency-note-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
