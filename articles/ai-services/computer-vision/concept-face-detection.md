---
title: "Face detection, attributes, and input data - Face"
titleSuffix: Foundry Tools
description: Learn more about face detection; face detection is the action of locating human faces in an image and optionally returning different kinds of face-related data.
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

# Face detection, attributes, and input data

[!INCLUDE [Gate notice](./includes/identity-gate-notice.md)]

> [!IMPORTANT]
> Face attributes are predicted by statistical algorithms. They might not always be accurate. Use caution when you make decisions based on attribute data. Refrain from using these attributes for anti-spoofing. Instead, we recommend using Face Liveness detection. For more information, see [Tutorial: Detect liveness in faces](/azure/ai-services/computer-vision/tutorials/liveness). 

This article explains the concepts of face detection and face attribute data. Face detection is the process of locating human faces in an image and optionally returning different kinds of face-related data.

You use the [Detect] API to detect faces in an image. To get started using the REST API or a client SDK, follow a [Face service quickstart](./quickstarts-sdk/identity-client-library.md). Or, for a more in-depth guide, see [Call the Detect API](./how-to/identity-detect-faces.md).

## Face rectangle

Each detected face corresponds to a *faceRectangle* field in the response. This is a set of pixel coordinates for the left, top, width, and height of the detected face. Using these coordinates, you can get the location and size of the face. In the API response, faces are listed in size order from largest to smallest.

Try out the capabilities of face detection quickly and easily by using Azure Vision Studio.
> [!div class="nextstepaction"]
> [Try Vision Studio](https://portal.vision.cognitive.azure.com/)

## Face ID

The face ID is a unique identifier string for each detected face in an image. Face ID requires limited access approval, which you can apply for by filling out the [intake form](https://aka.ms/facerecognition). For more information, see the Face API [Limited Access page](/azure/ai-foundry/responsible-ai/computer-vision/limited-access-identity). You can request a face ID in your [Detect] API call.

## Face landmarks

Face landmarks are a set of easy-to-find points on a face, such as the pupils or the tip of the nose. By default, there are 27 predefined landmark points. The following figure shows all 27 points:

:::image type="content" source="media/landmarks.1.jpg" alt-text="Diagram of a face with all 27 landmarks labeled.":::

The coordinates of the points are returned in units of pixels.

The Detection_03 model currently has the most accurate landmark detection. The eye and pupil landmarks that it returns are precise enough to enable gaze tracking of the face.

## Attributes

[!INCLUDE [Sensitive attributes notice](./includes/identity-sensitive-attributes.md)]

Attributes are a set of features that can optionally be detected by the [Detect] API. The following attributes can be detected:

* **Accessories**: Indicates whether the given face has accessories. This attribute returns possible accessories including headwear, glasses, and mask, with a confidence score between zero and one for each accessory.
* **Blur**: Indicates the blurriness of the face in the image. This attribute returns a value between zero and one and an informal rating of low, medium, or high.
* **Exposure**: Indicates the exposure of the face in the image. This attribute returns a value between zero and one and an informal rating of *underExposure*, *goodExposure*, or *overExposure*.
* **Glasses**: Indicates whether the given face has eyeglasses. Possible values are *NoGlasses*, *ReadingGlasses*, *Sunglasses*, and *Swimming Goggles*.
* **Head pose**: Indicates the face's orientation in 3D space. This attribute is described by the roll, yaw, and pitch angles in degrees, which are defined according to the [right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule). The order of three angles is roll-yaw-pitch, and each angle's value range is from -180 degrees to +180 degrees. 3D orientation of the face is estimated by the roll, yaw, and pitch angles in order. See the following diagram for angle mappings:

    :::image type="content" source="media/headpose.1.jpg" alt-text="Diagram of a head with the pitch, roll, and yaw axes labeled.":::

    For more information on how to use these values, see [Use the HeadPose attribute](./how-to/use-headpose.md).

* **Mask**: Indicates whether the face is wearing a mask. This attribute returns a possible mask type, and a Boolean value to indicate whether nose and mouth are covered.
* **Noise**: Indicates the visual noise detected in the face image. This attribute returns a value between zero and one, and an informal rating of low, medium, or high.
* **Occlusion**: Indicates whether there are objects blocking parts of the face. This attribute returns a Boolean value for *eyeOccluded*, *foreheadOccluded*, and *mouthOccluded*.
* **QualityForRecognition**: Indicates the overall image quality to determine whether the image being used in the detection is of sufficient quality to attempt face recognition on. The value is an informal rating of low, medium, or high. Only *high* quality images are recommended for person enrollment, and quality at or better than *medium* is recommended for identification scenarios.

    >[!NOTE]
    > The availability of each attribute depends on the detection model specified. *QualityForRecognition* attribute also depends on the recognition model, as it's currently only available when using a combination of detection model detection_01 or detection_03, and recognition model recognition_03 or recognition_04.

## Input requirements

Use the following tips to make sure that your input images give the most accurate detection results:

[!INCLUDE [identity-input-technical](includes/identity-input-technical.md)]
[!INCLUDE [identity-input-detection](includes/identity-input-detection.md)]

### Input data with orientation information

Some input images with JPEG format might contain orientation information in exchangeable image file format (EXIF) metadata. If EXIF orientation is available, images are automatically rotated to the correct orientation before sending for face detection. The face rectangle, landmarks, and head pose for each detected face are estimated based on the rotated image.

To properly display the face rectangle and landmarks, you need to make sure the image is rotated correctly. Most of the image visualization tools automatically rotate the image according to its EXIF orientation by default. For other tools, you might need to apply the rotation using your own code. The following examples show a face rectangle on a rotated image (left) and a non-rotated image (right).

:::image type="content" source="media/image-rotation.png" alt-text="Screenshot of two face images with and without rotation.":::

### Video input

If you're detecting faces from a video feed, you might be able to improve performance by adjusting certain settings on your video camera:

* **Smoothing**: Many video cameras apply a smoothing effect. You should turn this off if you can because it creates a blur between frames and reduces clarity.
* **Shutter speed**: A faster shutter speed reduces the amount of motion between frames and makes each frame clearer. We recommend shutter speeds of 1/60 second or faster.
* **Shutter angle**: Some cameras specify shutter angle instead of shutter speed. You should use a lower shutter angle, if possible, which results in clearer video frames.

    >[!NOTE]
    > A camera sensor with a lower shutter angle receives less light in each frame, so the image is darker. You need to determine the right level to use.

## Next step

Now that you're familiar with face detection concepts, learn how to write a script that detects faces in a given image.

* [Call the Detect API](./how-to/identity-detect-faces.md)

[Detect]: /rest/api/face/face-detection-operations/detect
