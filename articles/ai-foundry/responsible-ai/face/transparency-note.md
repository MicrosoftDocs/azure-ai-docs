---
title: Use cases for Face
titleSuffix: Foundry Tools
description: Face Responsible AI Basics, use cases, terms
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 06/21/2022
---

# Use cases for Azure AI Face service

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. 

Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system. 

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai). 

This Transparency Note is part of our effort at Microsoft to implement our [Facial Recognition Principles](https://blogs.microsoft.com/on-the-issues/2018/12/17/six-principles-to-guide-microsofts-facial-recognition-work/), which set out how we approach the development and deployment of facial recognition technology. We encourage you to use the principles to guide your development efforts as you use this technology. 

## The basics of Azure Vision in Foundry Tools Face API

Depending on the specific capability, Vision Face API (“Face API”) detects, recognizes, and/or analyzes human faces in images and videos using pre-trained machine learning models that have been developed by Microsoft. Developers can integrate Face API functions into their systems without creating their own models. 

When used responsibly, Face API is an important and useful building block technology that can improve efficiency, security, and customer experiences when used to create systems that analyze the face. 

Certain Face API features, such as facial recognition, generate unique identifying numerical (or other) representations of the face known as facial templates. Learn more about the process, including data retention periods, at the [Data and privacy for Vision Face API](/azure/ai-foundry/responsible-ai/face/data-privacy-security) documentation page. 

> [!WARNING]
> On June 11, 2020, Microsoft announced that it will not sell facial recognition technology to police departments in the United States until strong regulation, grounded in human rights, has been enacted. As such, customers may not use facial recognition features or functionality included in Azure Services, such as Face or Video Indexer, if a customer is, or is allowing use of such services by or for, a police department in the United States. When you create a new Face resource, you must acknowledge and agree in the Azure portal that you will not use the service by or for a police department in the United States and that you have reviewed the Responsible AI documentation and will use this service in accordance with it.

> [!CAUTION]
> Face service access is limited based on eligibility and usage criteria in order to support our Responsible AI principles. Face service is only available to Microsoft managed customers and partners. Use the [Face Recognition intake form](https://aka.ms/facerecognition) to apply for access. For more information, see the [Face limited access](/azure/ai-foundry/responsible-ai/computer-vision/limited-access-identity) page.

> [!IMPORTANT]
> If you are using Microsoft products or services to process Biometric Data, you are responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate and required under applicable Data Protection Requirements. "Biometric Data" will have the meaning set forth in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and Privacy for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security).


### Key terms

| Term | Definition |
| --- | --- |
|**Image**| An image is a single frame captured live via a camera, a stored photo, or a single frame from a stored video. Face API does not provide the underlying storage for photos or videos. It is up to system developers to provide the underlying storage. |
|**Probe image**| A probe image is an image submitted to a facial recognition system where it is converted to a facial template in order to be compared to the facial templates of enrolled individuals. All images are immediately deleted after they are converted to facial templates. |
|Facial template| A unique identifying numerical or other representation of an individual’s face that is generated from an image. The images themselves – whether enrollment or probe images – are not stored by Microsoft, and the original images cannot be reconstructed based on a facial template. |
|**Bounding box**| A box drawn around the location of a face in the photo in response to Face detection calls. |
|**Facial detection**| Finds human faces in an image and returns bounding boxes indicating their locations. Facial detection can also be configured to return a numerical label per face detected for the purpose of [insert purpose], as well as face attributes. Facial detection models are incapable of verifying or identifying individuals and they do not find, extract, or create facial templates. |
|**Facial recognition**| A term that captures both facial identification and facial verification uses (see below). |
|**Facial liveness detection**| Determines the authenticity of a face in an image and returns a liveness classification. Facial liveness detection models are incapable of verifying or identifying individuals however they may find, extract, or create facial templates to ensure the same person is present for the duration of the liveness test. An example is a banking app that uses facial liveness detection to ensure that the true account holder is physically present while performing a transaction, providing an additional layer of security. |
|**Facial verification**| A "one-to-one" matching of facial templates between two separate images to verify they are of the same individual. An example is a banking app that verifies the identity of users who wish to open a bank account remotely by comparing the facial template from a selfie taken by the user with the facial template from a photo ID of the account holder stored in the bank’s database. |
|**Facial identification**| A "one-to-many" matching of facial templates between an image and a set of facial templates. An example is a touchless access control system in a building, that replaces or augments physical cards and badges, in which a camera captures the face of one person entering a secured door and attempts to find a match from a set of facial templates for faces of individuals who are approved to access the building. |
|**Facial attributes**| Detection of specified facial attributes such as pose and landmarks like eyes or nose position. Facial attributes functionality is completely separate from facial verification and facial identification. The full list of supported attributes is described in the [Face – Detect API](/rest/api/face/face-detection-operations/detect) reference documentation. Facial attribute models are incapable of verifying or identifying individuals and they do not find, extract, or create facial templates. |
|**Facial redaction**| Redaction enables blurring or blocking human faces in images . Facial redaction models are incapable of verifying or identifying individuals and they do not find, extract, or create facial templates. |
|**Enrollment**| Enrollment is the process of collecting images of individuals and creating facial templates from them for recognition purposes. Higher quality photos or videos yield higher quality facial templates. |
|**Person ID**| When a person is enrolled in a verification system used for authentication, their facial template is also associated with a primary, randomly generated identifier called the Person ID that will be used to determine which facial template to compare with the probe image. |
|**Recognition confidence score**| When a probe image is queried with facial verification or facial identification, a recognition confidence score is returned for whether two faces match in the range of [0, 1], such as 0.6. This is not the same as the percentage likelihood that two faces match (i.e., a 0.9 recognition confidence score does not mean there is a 90% chance that the two faces match). |
|**Recognition confidence threshold**| The minimum confidence score required to determine whether two faces belong to the same person based on the recognition confidence score. For example, if the confidence threshold is 0.5 and the recognition confidence score returned from a probe image query is 0.6, then the two faces are considered a match. |
|**Candidate list**| For facial identification scenarios, a candidate list is the list of faces with scores above the recognition confidence threshold. Face API does not store primary identifiers, such as customer IDs, alongside facial templates. Instead, Face API associates stored facial templates with random GUIDs or globally unique identifiers. System developers can associate the GUID generated by Face API with an individual’s primary identifier to support verification of that individual.  |
|**Device correlation ID**| For facial liveness detection scenarios, a unique per device string is created at the start of liveness detection to assist with abuse detection. This is used by Face API to detect and block clients that are attempting to abuse liveness detection. Device correlation IDs cannot be used in verifying or identifying individuals and Face API does not persist it or any other session data longer than 48 hours. |

### Face API functions

**Facial detection** answers the question, “Are there one or more human faces in this image?” Facial detection finds human faces in an image and returns bounding boxes indicating their locations. Facial detection models are incapable of verifying or identifying individuals and they do not find, extract, or create facial templates. All other Face API functions are dependent on facial detection: before Face API can identify or verify a person (see below), it must know the locations of the faces to be recognized in input images. For more information, see the [Face - Detect API](/rest/api/face/face-detection-operations/detect) reference documentation. 

**Facial detection with facial attributes**: The facial detection feature can also optionally be used to detect facial attributes using additional AI models, such as pose and facial landmarks like eye or nose position. The facial attributes functionality is completely separate from the facial verification and facial identification functionalities of Face API. The values returned by the facial detection feature for each attribute are predictions of the perceived attributes. Facial attributes models are incapable of verifying or identifying individuals and they do not find, extract, or create facial templates.

**Facial verification** builds on the facial detection feature and addresses the question, "Are these two images of the same person?" Facial verification is also called "one-to-one" matching because the facial template for the probe image is compared to only one enrolled template. Facial verification can be used in identity verification or access control scenarios to verify a probe image matches a previously captured image (such as from a photo from a government issued ID card). For more information, see the [Face - Verify API](/rest/api/face/face-recognition-operations/verify-face-to-face) reference documentation. 

**Facial identification** also starts with the facial detection feature and answers the question, "Can this detected face be matched to any enrolled face in a database?" For this reason, facial identification is also called "one-to-many" matching. Candidate matches are returned based on how closely the facial template for the probe image matches each of the enrolled templates. For more information about facial identification, see the [Face - Identify API](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group) reference documentation. 

**Find similar face** also builds on the facial detection feature and searches for similar looking faces from all enrollment templates. For more information, see the Face - [Find Similar API](/rest/api/face/face-recognition-operations/find-similar) reference documentation. 

**Face group** also builds on the facial detection feature and creates small groups of faces that look similar to each other from all enrollment templates. For more information, see the [Face - Group ](/rest/api/face/face-recognition-operations/group) API reference documentation. 

**Facial liveness detection** answers the question, “Is the detected human face in this scene real and present?” Facial liveness detection determines the authenticity of a human face in a scene and returns a classification of live or spoof. Facial liveness detection models are incapable of verifying or identifying individuals however they may find, extract, or create facial templates to ensure the same person is present for the duration of the liveness test. For more information, see the Face - Detect Liveness API reference documentation ([iOS](https://aka.ms/liveness-sdk-ios), [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/vision/azure-ai-vision-imageanalysis/src/samples/README.md)). 

For more information on functions of Azure AI Face service, see the [Face documentation](/azure/ai-services/computer-vision/overview-identity). 

### Limited Access to Vision Face API 

Vision Face API (“Face API”) is a Limited Access service and registration is required for access to some features. For more information, see the [Microsoft’s Limited Access Policy](https://aka.ms/limitedaccesscogservices). Certain features are only available to Microsoft managed customers and approved partners, and only for certain use cases selected at the time of registration. Note that facial detection, facial attributes, and facial redaction use cases do not require registration. 

### Commercial use cases

The following use cases are approved for commercial contexts:

**Facial liveness detection** to prove that a real human is using the application. Liveness detection can be used standalone as an alternative to a CAPTCHA system or may be combined with an existing facial verification or identification operation to improve security. 

**Facial verification (1:1 matching) with optional facial liveness detection for identity verification** to grant access to digital or physical services or spaces. Such verification may be used for opening a new account, verifying a worker, or authenticating to participate in an online assessment. Identity verification can be done once during onboarding, and repeatedly as someone accesses a digital or physical service or space. 

**Facial identification (1:N or 1:1 matching) with optional facial liveness detection for touchless access control** to enable an enhanced experience using facial recognition, as opposed to methods like cards and tickets. This can reduce hygiene and security risks from card/ticket sharing/handling, loss, or theft. Facial recognition can assist the check-in process for accessing sites and buildings, such as airports, stadiums, offices, and hospitals. 

**Facial identification (1:N or 1:1 matching) with optional facial liveness detection for personalization** to enable ambient environment personalization with consent-based facial recognition that enriches experiences on shared devices. For example, hot desk screens and kiosks in the workplace and home can recognize you as you approach to provide directions to your destination or jump-start hands-free interaction with smart meetings devices. 

**Facial identification (1:N or 1:1 matching) with optional facial liveness detection to find duplicate or blocked users** to control or prevent unauthorized access to digital or physical services or spaces. For example, such identification may be used at account creation or sign-in or at access to a work site. 

**Facial identification (1:N or 1:1 matching) to search for a face in a media or entertainment video archive** to find a face within a video and generate metadata for media or entertainment use cases only. 

### Government and International Organization Use Cases 

The following use cases are approved for the public sector:

**Facial liveness detection** to prove that a real human is using the application. Such a detection can be used standalone as an alternative to a CAPTCHA system or may be combined with an existing facial verification or identification operation to improve security. 

**Facial verification (1:1 matching) with optional facial liveness detection for identity-verification** to grant access to digital or physical services or spaces. Such verification may be used for opening a new account, verifying a worker, or authenticating to participate in an online assessment. Identity verification can be done once during onboarding, and repeatedly as someone accesses a digital or physical service or space. 

**Facial identification (1:N or 1:1 matching) with optional facial liveness detection for touchless access control** to enable an enhanced experience using facial recognition, as opposed to methods like cards and tickets. This can help reduce hygiene and security risks from card/ticket sharing/handling, loss, or theft. Facial recognition can assist the check-in process for accessing sites and buildings, such as airports, stadiums, offices, and hospitals. 

**Facial identification (1:N or 1:1 matching) with optional facial liveness detection for personalization** to enable ambient environment personalization with consent-based facial recognition that enriches experiences on shared devices. For example, hot desk screens and kiosks in the workplace and home can recognize you as you approach to provide directions to your destination or jump-start hands-free interaction with smart meetings devices. 

**Facial identification (1:N or 1:1 matching) to assist law enforcement or court officials** in prosecution or defense of a criminal suspect who has already been apprehended, to the extent specifically authorized by a duly empowered government authority in a jurisdiction that maintains a fair and independent judiciary and provided that the person sought to be identified or verified is not a minor, OR to assist officials of duly empowered international organizations in the prosecution of abuses of international criminal law, international human rights law, or international humanitarian law, provided that the person sought to be identified or verified is not a minor. 

**Facial identification (1:N or 1:1 matching) for preservation and enrichment of public media archives** to identify individuals in public media or entertainment video archives for the purposes of preserving and enriching public media only. Examples of public media enrichment include identifying historical figures in video archives or generating descriptive metadata. 

**Facial identification (1:N or 1:1 matching) to respond to an emergency** involving imminent danger or risk of death or serious physical injury to an individual. 

**Facial identification (1:N or 1:1 matching) for purposes of providing humanitarian aid**, conducting search and rescue of individuals, or identifying missing persons, deceased persons or victims of crimes. 


### Considerations when using Azure AI Face Service

**The use of Face API by or for state or local police in the U.S. is prohibited by Microsoft policy.**

**The use of real-time facial recognition technology on mobile cameras used by law enforcement to attempt to identify individuals in uncontrolled, "in the wild" environments is prohibited by Microsoft policy.** This includes where police officers on patrol use body-worn or dash-mounted cameras using facial recognition technology to attempt to identify individuals present in a database of suspects or prior inmates. This policy applies globally. 

**Avoid use of facial recognition or facial detection technology to attempt to infer emotional states, gender identity, or age**. Microsoft has retired general-purpose facial recognition and facial detection capabilities that were used to classify emotion, gender, age, smile, hair, facial hair, and makeup. General-purpose use of these capabilities poses a risk of misuse that could subject people to stereotyping, discrimination, or unfair denial of services. These capabilities will be carefully restricted to select accessibility scenarios such as those provided by [Seeing AI](https://www.microsoft.com/ai/seeing-ai). 

**Avoid use for ongoing surveillance of real-time or near real-time identification or persistent tracking of an individual**. Ongoing surveillance is defined as the tracking of movements of an identified individual on a persistent basis. Persistent tracking is defined as the tracking of movements of an individual on a persistent basis without identification or verification of that individual. Face API was not designed for ongoing surveillance or persistent tracking of an individual and does not work on large-scale real-time camera streams. In accordance with our [Six Principles for Developing and Deploying Facial Recognition Technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf), the use of facial recognition technology for the ongoing surveillance of individuals by law enforcement should be prohibited except in narrow circumstances and only with adequate protections for individual civil liberties and human rights. 

**Avoid use for task-monitoring systems that can interfere with privacy**. Face API's probabilistic AI models were not designed to monitor individual patterns to infer intimate personal information, such as an individual's sexual or political orientation. 

**Avoid use in protected spaces**. Protect individuals' privacy by evaluating camera locations and positions, adjusting angles and regions of interest so they do not take images of protected areas such as restrooms. 

**Avoid use in environments where enrollment in identification or verification is not optional**. Protect individuals' autonomy by not planning enrollment in situations where there's pressure to consent. 

**Avoid use where a human in the loop or secondary verification method is not available**. Fail-safe mechanisms (e.g., a secondary method being available to the end user if the technology fails) help prevent denial of essential services or other harms due to false negatives. 

**Carefully consider use in schools or facilities for older adults**. Face API has not been heavily tested with data containing minors under the age of 18 or adults over age 65. We recommend that users thoroughly evaluate error rates for any scenario in environments where there is a predominance of these age groups. 

**Carefully consider use for healthcare-related decisions**. Face API provides probabilistic results like face detections, attributes, and recognitions. The data may not be suitable for making healthcare-related decisions. 

**Carefully consider use in public spaces**. Evaluate camera locations and positions, adjusting angles and regions of interest to minimize collection from public spaces. Lighting and weather in public spaces such as streets and parks will significantly impact the performance of the facial systems, and it is extremely difficult to provide effective disclosure that facial systems are being used in public spaces. 

[!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]


## Next steps

* [Characteristics and limitations](/azure/ai-foundry/responsible-ai/face/characteristics-and-limitations)
* [Responsible deployment of Face](/azure/ai-foundry/responsible-ai/face/guidance-integration-responsible-use)
* [Data, privacy, and security for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security)
* [Quickstart your Face use case development](/azure/ai-services/computer-vision/quickstarts-sdk/identity-client-library)
