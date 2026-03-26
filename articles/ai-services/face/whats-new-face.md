---
title: What's new in Azure Face in Foundry Tools?
titleSuffix: Foundry Tools
description: Stay up to date on recent releases and updates to Azure Face in Foundry Tools.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: whats-new
ms.date: 03/26/2026
ms.author: pafarley
---


# What's new in Azure Face in Foundry Tools

Learn what's new in Azure Face. Check this page to stay up to date with new features, enhancements, fixes, and documentation updates.

## March 2026

### Face liveness service reliability updates

The Face liveness detection service received reliability and performance improvements.

### Face liveness client-side SDK 1.4.7 and 1.4.8 releases

Versions **1.4.7** and **1.4.8** of the Liveness SDK introduce several improvements:

- **Government region support** – Added support for the client to route to government region endpoints.
- Improved UI responsiveness to provide smoother active user instructions.
- Optimized client logic to improve the user experience and reduce the need for retries during active checks.
- Upgraded Gradle version on Android SDK to address compatibility issues (1.4.8).

For platform-specific details, samples, and migration guidance, see the full [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases).

## November 2025

### Face liveness client-side SDK 1.4.6 release

Version **1.4.6** is a refresh of the Liveness Web SDK with a few improvements:

- Stability fixes for the Web SDK to reduce errors during initialization.
- New loading animation that displays when network speeds are slow during initialization.
- Fixed several low-memory-related issues.

For more information, see the [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.4.6).

## October 2025

### Face liveness client-side SDK 1.4.5 release

Version **1.4.5** of the Liveness SDK adds a new capability along with continued stability improvements across versions 1.4.2 through 1.4.5:

- **Custom branding** – Developers can now customize the branding and logo displayed in the Web SDK liveness check experience.
- Improved face tracking stability in edge cases.
- Stability fixes across both Web and Mobile SDKs.

For more information, see the [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.4.5).

## August 2025


### Face liveness service v1.3-preview.1 API release

The **v1.3-preview.1** public preview introduces a new security enhancement:  

- **Abuse detection** – Adds built-in risk assessments, including IP-based checks, to help identify and flag liveness sessions that may be fraudulent. This enables earlier intervention in high-risk scenarios such as identity verification or account onboarding. [Learn more](./concept-liveness-abuse-monitoring.md).  

See the [API Reference](/rest/api/face/liveness-session-operations?view=rest-face-v1.3-preview&preserve-view=true) for full details.  

### Network isolation support for Liveness Detection APIs

Liveness Detection APIs now support disabling public network access for calls from client applications, ensuring requests are only processed within your trusted network boundaries. This feature is available across supported API versions and is particularly valuable for regulated or high-security environments. [Learn more](./how-to/liveness-use-network-isolation.md).  

### Face liveness client-side SDK 1.4.1 release

Version **1.4.1** improves distribution and CI/CD integration for the Liveness SDK.  

- **Public wrapper SDKs** are now available in npm (JavaScript/Web), Maven Central (Android), and a GitHub repo (iOS xcframework), enabling easier integration and automated dependency monitoring with tools such as GitHub Dependabot or Renovate.  
- **Simplified gated asset access** – Instead of running a local script, developers can now call a dedicated API to obtain an access token using their Azure Face resource endpoint and API key, making automated builds simpler to set up.  

For platform-specific details, samples, and migration guidance, see the full [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases).

## February 2025

### Face liveness client-side SDK 1.1.0 release

Liveness client-side SDK released [1.1.0](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.1.0)

This update includes a few improvements:

* Increased timeout for the head-turn scenario to provide end-users more time to complete the flow.
* Fixes to iOS and Android SDKs to resolve compatibility issues with Microsoft Intune Mobile Application Management SDKs.
* Security related fixes/improvements.

For more information, see the [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.1.0).

## January 2025

### Face liveness detection GA

The Face liveness detection feature is now generally available (GA).

* Server-side API: [Face API v1.2](/rest/api/face/operation-groups?view=rest-face-v1.2&preserve-view=true)
* Client-side SDK: [Azure Vision in Foundry Tools SDK 1.0.0](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.0.0)

This SDK allows developers to utilize face liveness checks on both native-mobile applications and web-browsers applications for identity-verification scenarios.

The new SDK supports both Passive and Passive-Active modes. The hybrid Passive-Active mode is designed to require Active motion only in poor lighting conditions, while using the speed and efficiency of Passive liveness checks in optimal lighting. 

For more information, see the [SDK release notes](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases/tag/1.0.0).

## August 2024

### New detectable Face attributes

The glasses, occlusion, blur, and exposure attributes are available with the latest Detection 03 model. See [Specify a face detection model](./how-to/specify-detection-model.md) for more details.

## May 2024

### New Face SDK 1.0.0-beta.1 (breaking changes)

The Face SDK was rewritten in version 1.0.0-beta.1 to better meet the guidelines and design principles of Azure SDKs. C#, Python, Java, and JavaScript are the supported languages. Follow the [QuickStart](./quickstarts-sdk/identity-client-library.md) to get started.

## November 2023

### Face client-side SDK for liveness detection

The Face Liveness SDK supports liveness detection on your users' mobile or edge devices. It's available in Java/Kotlin for Android and Swift/Objective-C for iOS.

Our liveness detection service achieved a 0% penetration rate in [iBeta Level 1 and Level 2 Presentation Attack Detection (PAD) tests](https://servicetrust.microsoft.com/DocumentPage/ea3fa18f-3940-4c0b-aa96-41cb50898aee), conducted by a NIST/NVLAP-accredited laboratory and conformant to the [ISO/IEC 30107-3 PAD international standard](https://www.iso.org/standard/79520.html).

## April 2023

### Face limited access tokens

Independent software vendors (ISVs) can manage the Face API usage of their clients by issuing access tokens that grant access to Face features that are normally gated. This allows client companies to use the Face API without having to go through the formal approval process. [Use limited access tokens](how-to/identity-access-token.md).

## June 2022

### Vision Studio launch

Vision Studio is UI tool that lets you explore, build, and integrate features from Azure Vision into your applications.

Vision Studio provides you with a platform to try several service features, and see what they return in a visual manner. Using the Studio, you can get started without needing to write code, and then use the available client libraries and REST APIs in your application.

### Responsible AI for Face

#### Face transparency note
* The [transparency note](https://aka.ms/faceraidocs) provides guidance to assist our customers to improve the accuracy and fairness of their systems by incorporating meaningful human review to detect and resolve cases of misidentification or other failures, providing support to people who believe their results were incorrect, and identifying and addressing fluctuations in accuracy due to variations in operational conditions.

#### Retirement of sensitive attributes

* We have retired facial analysis capabilities that purport to infer emotional states and identity attributes, such as gender, age, smile, facial hair, hair, and makeup. 
* Facial detection capabilities, (including detecting blur, exposure, glasses, headpose, landmarks, noise, occlusion, facial bounding box) will remain generally available and don't require an application.

#### Fairlearn package and Microsoft's Fairness Dashboard

* [The open-source Fairlearn package and Microsoft’s Fairness Dashboard](https://github.com/microsoft/responsible-ai-toolbox/tree/main/notebooks/cognitive-services-examples/face-verification) aims to support customers to measure the fairness of Microsoft's facial verification algorithms on their own data, allowing them to identify and address potential fairness issues that could affect different demographic groups before they deploy their technology.

#### Limited Access policy

* As a part of aligning Face to the updated Responsible AI Standard, a new [Limited Access policy](https://aka.ms/AAh91ff) has been implemented for the Face API and Azure Vision. Existing customers have one year to apply and receive approval for continued access to the facial recognition services based on their provided use cases. See details on Limited Access for Face [here](/azure/ai-foundry/responsible-ai/computer-vision/limited-access-identity).

## February 2022

### New Quality Attribute in Detection_01 and Detection_03
* To help system builders and their customers capture high quality images, which are necessary for high quality outputs from Face API, we’re introducing a new quality attribute **QualityForRecognition** to help decide whether an image is of sufficient quality to attempt face recognition. The value is an informal rating of low, medium, or high. The new attribute is only available when using any combinations of detection models `detection_01` or `detection_03`, and recognition models `recognition_03` or `recognition_04`. Only "high" quality images are recommended for person enrollment and quality above "medium" is recommended for identification scenarios. To learn more about the new quality attribute, see [Face detection and attributes](concept-face-detection.md) and see how to use it with [QuickStart](./quickstarts-sdk/identity-client-library.md?pivots=programming-language-csharp&tabs=visual-studio).

## April 2021

### PersonDirectory data structure (preview)

* In order to perform face recognition operations such as Identify and Find Similar, Face API customers need to create an assorted list of **Person** objects. The new **PersonDirectory** is a data structure that contains unique IDs, optional name strings, and optional user metadata strings for each **Person** identity added to the directory. Currently, the Face API offers the **LargePersonGroup** structure, which has similar functionality but is limited to 1 million identities. The **PersonDirectory** structure can scale up to 75 million identities.
* Another major difference between **PersonDirectory** and previous data structures is that you'll no longer need to make any Train calls after adding faces to a **Person** object&mdash;the update process happens automatically. For more details, see [Use the PersonDirectory structure](how-to/use-persondirectory.md).

## February 2021

### New Face API detection model
* The new Detection 03 model is the most accurate detection model currently available. If you're a new customer, we recommend using this model. Detection 03 improves both recall and precision on smaller faces found within images (64x64 pixels). Other improvements include an overall reduction in false positives and improved detection on rotated face orientations. Combining Detection 03 with the new Recognition 04 model provides improved recognition accuracy as well. See [Specify a face detection model](./how-to/specify-detection-model.md) for more details.
### New detectable Face attributes
* The `faceMask` attribute is available with the latest Detection 03 model, along with the added attribute `"noseAndMouthCovered"`, which detects whether the face mask is worn as intended, covering both the nose and mouth. To use the latest mask detection capability, users need to specify the detection model in the API request: assign the model version with the _detectionModel_ parameter to `detection_03`. See [Specify a face detection model](./how-to/specify-detection-model.md) for more details.
### New Face API Recognition Model
* The new Recognition 04 model is the most accurate recognition model currently available. If you're a new customer, we recommend using this model for verification and identification. It improves upon the accuracy of Recognition 03, including improved recognition for users wearing face covers (surgical masks, N95 masks, cloth masks). We recommend against enrolling images of users wearing face covers as this will lower recognition quality. Now customers can build safe and seamless user experiences that detect whether a user is wearing a face cover with the latest Detection 03 model, and recognize them with the latest Recognition 04 model. See [Specify a face recognition model](./how-to/specify-recognition-model.md) for more details.

## January 2021

### Mitigate latency
* The Face team published a new article detailing potential causes of latency when using the service and possible mitigation strategies. See [Mitigate latency when using the Face service](./how-to/mitigate-latency.md).

## December 2020
### Customer configuration for Face ID storage
* While the Face Service does not store customer images, the extracted face feature(s) will be stored on server. The Face ID is an identifier of the face feature and will be used in [Face - Identify](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group), [Face - Verify](/rest/api/face/face-recognition-operations/verify-face-to-face), and [Face - Find Similar](/rest/api/face/face-recognition-operations/find-similar). The stored face features will expire and be deleted 24 hours after the original detection call. Customers can now determine the length of time these Face IDs are cached. The maximum value is still up to 24 hours, but a minimum value of 60 seconds can now be set. The new time ranges for Face IDs being cached is any value between 60 seconds and 24 hours. More details can be found in the [Face - Detect](/rest/api/face/face-detection-operations) API reference (the *faceIdTimeToLive* parameter).

## November 2020
### Sample Face enrollment app
* The team published a sample Face enrollment app to demonstrate best practices for establishing meaningful consent and creating high-accuracy face recognition systems through high-quality enrollments. The open-source sample can be found in the [Build an enrollment app](Tutorials/build-enrollment-app.md) guide and on [GitHub](https://github.com/Azure-Samples/cognitive-services-FaceAPIEnrollmentSample), ready for developers to deploy or customize.

## August 2020
### Customer-managed encryption of data at rest
* The Face service automatically encrypts your data when persisting it to the cloud. The Face service encryption protects your data to help you meet your organizational security and compliance commitments. By default, your subscription uses Microsoft-managed encryption keys. There is also a new option to manage your subscription with your own keys called customer-managed keys (CMK). More details can be found at [Customer-managed keys](./identity-encrypt-data-at-rest.md).

## April 2020
### New Face API Recognition Model
* The new recognition 03 model is the most accurate model currently available. If you're a new customer, we recommend using this model. Recognition 03 provides improved accuracy for both similarity comparisons and person-matching comparisons. More details can be found at [Specify a face recognition model](./how-to/specify-recognition-model.md).

## June 2019

### New Face API detection model
* The new Detection 02 model features improved accuracy on small, side-view, occluded, and blurry faces. Use it through [Face - Detect](/rest/api/face/face-detection-operations), [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face), [LargeFaceList - Add Face](/rest/api/face/face-list-operations/add-large-face-list-face), [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face) and [LargePersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-large-person-group-person-face) by specifying the new face detection model name `detection_02` in `detectionModel` parameter. More details in [How to specify a detection model](how-to/specify-detection-model.md).

## April 2019

### Improved attribute accuracy
* Improved overall accuracy of the `age` and `headPose` attributes. The `headPose` attribute is also updated with the `pitch` value enabled now. Use these attributes by specifying them in the `returnFaceAttributes` parameter of [Face - Detect](/rest/api/face/face-detection-operations) `returnFaceAttributes` parameter.
### Improved processing speeds
* Improved speeds of [Face - Detect](/rest/api/face/face-detection-operations), [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face), [LargeFaceList - Add Face](/rest/api/face/face-list-operations/add-large-face-list-face), [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face) and [LargePersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-large-person-group-person-face) operations.

## March 2019

### New Face API recognition model
* The Recognition 02 model has improved accuracy. Use it through [Face - Detect](/rest/api/face/face-detection-operations), [FaceList - Create](/rest/api/face/face-list-operations/create-face-list), [LargeFaceList - Create](/rest/api/face/face-list-operations/create-large-face-list), [PersonGroup - Create](/rest/api/face/person-group-operations/create-person-group) and [LargePersonGroup - Create](/rest/api/face/person-group-operations/create-large-person-group) by specifying the new face recognition model name `recognition_02` in `recognitionModel` parameter. More details in [How to specify a recognition model](how-to/specify-recognition-model.md).

## January 2019

### Face Snapshot feature
* This feature allows the service to support data migration across subscriptions: [Snapshot](/rest/api/face/snapshot).

> [!IMPORTANT]
> As of June 30, 2023, the Face Snapshot API is retired.

## October 2018

### API messages
* Refined description for `status`, `createdDateTime`, `lastActionDateTime`, and `lastSuccessfulTrainingDateTime` in [PersonGroup - Get Training Status](/rest/api/face/person-group-operations/get-person-group-training-status), [LargePersonGroup - Get Training Status](/rest/api/face/person-group-operations/get-large-person-group-training-status), and [LargeFaceList - Get Training Status](/rest/api/face/face-list-operations/get-large-face-list-training-status).

## May 2018

### Improved attribute accuracy
* Improved `gender` attribute significantly and also improved `age`, `glasses`, `facialHair`, `hair`, `makeup` attributes. Use them through [Face - Detect](/rest/api/face/face-detection-operations) `returnFaceAttributes` parameter.
### Increased file size limit
* Increased input image file size limit from 4 MB to 6 MB in [Face - Detect](/rest/api/face/face-detection-operations), [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face), [LargeFaceList - Add Face](/rest/api/face/face-list-operations/add-large-face-list-face), [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face) and [LargePersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-large-person-group-person-face).

## March 2018

### New data structure
* [LargeFaceList](/rest/api/face/face-list-operations/create-large-face-list) and [LargePersonGroup](/rest/api/face/person-group-operations/create-large-person-group). More details in [How to scale to handle more enrolled users](how-to/use-large-scale.md).
* Increased [Face - Identify](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group) `maxNumOfCandidatesReturned` parameter from [1, 5] to [1, 100] and default to 10.

## May 2017

### New detectable Face attributes
* Added `hair`, `makeup`, `accessory`, `occlusion`, `blur`, `exposure`, and `noise` attributes in [Face - Detect](/rest/api/face/face-detection-operations) `returnFaceAttributes` parameter.
* Supported 10K persons in a PersonGroup and [Face - Identify](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group).
* Supported pagination in [PersonGroup Person - List](/rest/api/face/person-group-operations/get-person-group-persons) with optional parameters: `start` and `top`.
* Supported concurrency in adding/deleting faces against different FaceLists and different persons in PersonGroup.

## March 2017

### New detectable Face attribute
* Added `emotion` attribute in [Face - Detect](/rest/api/face/face-detection-operations) `returnFaceAttributes` parameter.
### Fixed issues
* Face could not be re-detected with rectangle returned from [Face - Detect](/rest/api/face/face-detection-operations) as `targetFace` in [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face) and [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face).
* The detectable face size is set to ensure it is strictly between 36x36 to 4096x4096 pixels.

## November 2016
### New subscription tier
* Added Face Storage Standard subscription to store additional persisted faces when using [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face) or [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face) for identification or similarity matching. The stored images are charged at $0.5 per 1000 faces and this rate is prorated on a daily basis. Free tier subscriptions continue to be limited to 1,000 total persons.

## October 2016
### API messages
* Changed the error message of more than one face in the `targetFace` from 'There are more than one face in the image' to 'There is more than one face in the image' in [FaceList - Add Face](/rest/api/face/face-list-operations/add-face-list-face) and [PersonGroup Person - Add Face](/rest/api/face/person-group-operations/add-person-group-person-face).

## July 2016
### New features
* Supported Face to Person object authentication in [Face - Verify](/rest/api/face/face-recognition-operations/verify-face-to-face).
* Added optional `mode` parameter enabling selection of two working modes: `matchPerson` and `matchFace` in [Face - Find Similar](/rest/api/face/face-recognition-operations/find-similar) and default is `matchPerson`.
* Added optional `confidenceThreshold` parameter for user to set the threshold of whether one face belongs to a Person object in [Face - Identify](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group).
* Added optional `start` and `top` parameters in [PersonGroup - List](/rest/api/face/person-group-operations/get-person-groups) to enable user to specify the start point and the total PersonGroups number to list.

## V1.0 changes from V0

* Updated service root endpoint from ```https://westus.api.cognitive.microsoft.com/face/v0/``` to ```https://westus.api.cognitive.microsoft.com/face/v1.0/```. Changes applied to:
 [Face - Detect](/rest/api/face/face-detection-operations), [Face - Identify](/rest/api/face/face-recognition-operations/identify-from-dynamic-person-group), [Face - Find Similar](/rest/api/face/face-recognition-operations/find-similar) and [Face - Group](/rest/api/face/face-recognition-operations/group).
* Updated the minimal detectable face size to 36x36 pixels. Faces smaller than 36x36 pixels will not be detected.
* Deprecated the PersonGroup and Person data in Face V0. Those data cannot be accessed with the Face V1.0 service.
* Deprecated the V0 endpoint of Face API on June 30, 2016.