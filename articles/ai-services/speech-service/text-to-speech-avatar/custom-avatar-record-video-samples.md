---
title: How to record video samples for custom text to speech avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to prepare high-quality video samples for creating a custom text to speech avatar.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: best-practice
ms.date: 08/07/2025
ms.author: pafarley
keywords: how to record video samples for custom text to speech avatar
---

# Record video samples for custom text to speech avatar

This article shows you how to prepare high-quality video samples for creating a custom text to speech avatar.

Custom text to speech avatar model building requires training on a video recording of a real human speaking. This person is the avatar talent. You must get sufficient consent under all relevant laws and regulations from the avatar talent to create a custom avatar from their talent's image or likeness. To learn about requirements of the consent statement video, see [Get consent file from the avatar talent](./custom-avatar-create.md#step-2-add-avatar-talent-consent).

## Recording environment

Record in a professional video recording studio or well-lit space.

### Background requirements

For commercial, multi-scene avatars, use a clean, smooth, solid-colored background. A green screen works best.

If your avatar will only be used in a single scene, you can record in a specific location like your office, but you can't change the background later.

Follow these best practices when using a solid-colored background like a green screen:
- Position the green screen behind the actor. For full-body shots, place a green screen on the floor under the actor's feet. Connect the back and floor green screens seamlessly.
- Keep the green screen flat with uniform color.
- Maintain 0.5-1 meter distance between the actor and background.
- Light the green screen properly to prevent shadows.
- Keep the actor's full outline within the green screen edges.
- Don't let the actor stand too close to the green screen.
- Keep the actor's head and hands within the green screen when speaking.

### Lighting requirements

- Use even, bright lighting on the actor's face. Avoid shadows on the face or reflections on glasses and clothing.
- Keep ambient lighting consistent. Turn off projectors, close curtains to avoid daylight changes, and use stable artificial light sources.

### Equipment

- Camera: Minimum 1080p resolution and 25 FPS (frames per second). To create a 4K resolution avatar, the video recording should be in 3840x2160 resolution.
- Keep lighting and camera positions fixed throughout recording.
- You can use a teleprompter during recording, but make sure it doesn't affect the actor's gaze toward the camera. Provide seating if the avatar needs to be in a sitting position.
- For half-length or seated avatars, provide seating for the actor. Choose an appropriate chair if you don't want it visible in the video. 

## Appearance of the actor

Custom text to speech avatar doesn't support customization of clothing or appearance. It's essential to carefully design and prepare the avatar's appearance when recording training data. Consider these tips:

| Categories | Dos          | Don'ts         |
|------------|----------------------------|-------------------|
| **Hair**   | - The actor's hair should have a smooth and glossy surface.</br>- Even the actor's bangs or broken hair should have a clear and smooth border.</br>- Choose a hairstyle that is easy to keep consistent during the whole video recording. | - Avoid messy hair or backgrounds showing through the hair.</br>- Don't let hair block the eyes or eyebrows.</br>- Avoid shadows on the face caused by hairstyle.</br>- Avoid hair changes too much during speech and body gesture. For example, the high ponytail of an actor might appear, disappear, and swing during speaking. |
| **Clothing** | - Pay attention to clothing status and make sure no significant changes on the clothing during speaking. | - Avoid wearing clothing and accessories that are too loose, heavy, or complex, as they might affect the consistency of clothing status during speaking and body gesture.</br>- Avoid wearing clothing that is too similar to the background color or reflective materials like white shirts or translucent materials.</br>- Avoid clothing with obvious lines or items with logos and brand names you don't want to highlight.</br>- Avoid reflective elements such as metal belts, shiny leather shoes, and leather pants. |
| **Face**    | - Ensure the actor's face is clearly visible.  | - Avoid face obscured by hair, sunglasses, or accessories. |

## What video clips to record

You need these types of video clips:

**Consent Video (Required)**
The consent video is required for creating a custom avatar. 
   - The consent video must show the same avatar talent speaking and follow the consent statement requirements. Make sure the statement is recorded correctly with each word spoken clearly. You can use any supported language. To learn about consent statement video requirements, see [Get consent file from the avatar talent](./custom-avatar-create.md#step-2-add-avatar-talent-consent).
   - The avatar talent should always face the camera without large movements.
   - Record the video in a quiet environment with clear audio at reasonable volume. Keep the signal-to-noise ratio above 20. For voice recording guidance, see the [Recording custom voice samples](../record-custom-voice-samples.md#recording-your-script) guide.
   - Make sure the actor's head isn't blocked in any frame.
   - Keep other objects out of the camera view, including filming equipment and mobile phones. 

**Status 0 speaking (Required for gestures)**
The status 0 speaking video clip is required for gestures with the avatar.
   - Status 0 represents the posture you can naturally maintain most of the time while speaking. For example, arms crossed in front of the body or hanging naturally at the sides.
   - Maintain a front-facing pose. The actor can move slightly to show a relaxed state, like moving the head or shoulder slightly, but don't move the body too much.
   - Duration: 3-5 minutes of speaking in status 0.
     
**Samples of status 0 speaking**

![Animated graphic depicting Lisa speaking in status 0, representing the posture naturally maintained while speaking.](media/status-0-lisa.gif) 

![Animated graphic depicting Harry speaking in status 0, representing the posture naturally maintained while speaking.](media/status-0-harry.gif)

![Animated graphic depicting Lori speaking in status 0, representing the posture naturally maintained while speaking.](media/status-0-lori.gif)

**Naturally speaking (Required)**
The naturally speaking video clip is required for the avatar to speak naturally.
   - Actor speaks in status 0 but with natural hand gestures from time to time.
   - Hands should start from status 0 and return after making gestures.
   - Use natural and common gestures when speaking. Avoid meaningful gestures like pointing, applause, or thumbs up.
   - Duration: Minimum 5 minutes, maximum 30 minutes total. At least one 5-minute continuous video recording is required. If recording multiple clips, keep each under 10 minutes.
     
**Samples of natural speaking** 

![Animated graphic depicting sample of Lisa speaking in status 0 with natural hand gestures, representing the posture naturally maintained while speaking.](media/natural-lisa.gif)

![Animated graphic depicting sample of Harry speaking in status 0 with natural hand gestures, representing the posture naturally maintained while speaking.](media/natural-harry.gif)

![Animated graphic depicting sample of Lori speaking in status 0 with natural hand gestures, representing the posture naturally maintained while speaking.](media/natural-lori.gif)

**Silent status (Required)**
The silent status video clip is required. It's important if you build a real-time conversation with the custom avatar. The video clip is used as the main template for both speaking and listening status for a chatbot.

  - Maintain status 0, don't speak, but stay relaxed.
  - Even while remaining in status 0, don't stay completely still. You can move slightly but not too much. Act like you're waiting.
  - Maintain a smile as if listening or waiting patiently.
  - Avoid nodding frequently.
  - Duration: 1 minute.
    
**Samples of silent status** 

![Animated graphic depicting sample of Lisa maintaining silent status without speaking but still feeling relaxed.](media/silent-lisa.gif)

![Animated graphic depicting sample of Harry maintaining silent status without speaking but still feeling relaxed.](media/silent-harry.gif)

![Animated graphic depicting sample of Lori maintaining silent status without speaking but still feeling relaxed.](media/silent-lori.gif)

**Gestures (optional)**

Gesture video clips are optional. If you need to insert certain gestures in the avatar speaking, follow this guideline to record gesture videos. Gesture insertion is only available for batch mode avatar; real-time avatar doesn't support gesture insertion. Each custom avatar model can support up to 10 gestures.

**Gesture tips**
- Each gesture clip should be within 10 seconds.
- Gestures should start from status 0 and end with status 0. It's essential that the character maintains the same position as in status 0, which is in the middle of the screen, throughout the gesture. Otherwise, the gesture clip can't be smoothly inserted into the avatar video. 
- The gesture clip only captures the body gestures; the actor doesn't have to speak during making gestures.
- Design a list of gestures before recording. Here are some examples:

**Samples of gesture**

| Gestures                       | Samples                |
|--------------------------------|------------------------|
| Delivering sell link/promotion code | ![An animated graphic depicting sample of delivering sell link.](media/delivering-sell-link.gif)       |
| Praising the product         |  ![An animated graphic depicting sample of praising the product](media/commending-the-product.gif)       |
| Introducing the product          | ![An animated graphic depicting sample of introducing the product.](media/introducing-the-product.gif)       |
| Displaying the price (number from 1 to 10-fist-number with each hand) | Right hand ![An animated graphic depicting sample of displaying the price with right hand.](media/displaying-the-price-with-right-hand.gif) Left hand ![An animated graphic depicting sample of displaying the price with left hand.](media/displaying-the-price-with-left-hand.gif) |

High-quality avatar models are built from high-quality video recordings, including audio quality. Here are more tips for actor's performance and recording video clips:

| **Dos** | **Don'ts**   |
|---------|--------------|
| - Ensure all video clips are taken in the same conditions.</br>- During the recording process, design the size and display area of the character you need so that the character can be displayed on the screen appropriately.</br> - Actor should be steady during the recording. </br> - Mind facial expressions, which should be suitable for the avatar's use case. For example, look positive and smile if the custom text to speech avatar is used as customer service. Look professionally if the avatar is used for news reporting.</br> - Maintain eye gaze towards the camera, even when using a teleprompter.</br> - Return your body to status 0 when pausing speaking.</br> - Speak on a self-chosen topic, and minor speech mistakes like miss a word or mispronounced are acceptable. If the actor misses a word or mispronounces something, just go back to status 0, pause for 3 seconds, and then continue speaking.</br> - Consciously pause between sentences and paragraphs. When pausing, go back to the status 0 and close your lips. </br> - The audio should be clear and loud enough; bad audio quality impacts training result.</br> - Keep the shooting environment quiet. | - Don't adjust the camera parameters, focal length, position, angle of view. Don't move the camera; keep the person's position, size, angle, consistent in the camera.</br> - Characters that are too small might lead to a loss of image quality during post-processing. Characters that are too large might cause the screen to overflow during gestures and movements.</br> - Don't make too long gestures or too much movement for one gesture; for example, actor's hands are always making gestures and forget to go back to status 0.</br> - The actor's movements and gestures must not block the face.</br> - Avoid small movements of the actor like licking lips, touching hair, talking sideways, constant head shaking during speech, and not closing up after speaking.</br> - Avoid background noise; staff should avoid walking and talking during video recording.</br> - Avoid other people's voice recorded during the actor speaking. |

### How to prepare an interaction video clip

Creating a high-quality interaction video clip is essential if you're building a real-time conversation with a custom avatar. The clip should consist of a question-and-answer format, where a photographer asks a question, and the actor responds. Loop the question-answer pair until the conversation is complete. If you're filming alone, imagine someone else asking the questions during the asking phase.

Here are some tips for each phase:

**Asking phase**
- Maintain status 0, don't speak, but still feel relaxed.
- Even remaining in status 0, don't keep still. Perform like you're waiting.
- Maintain a smile as if listening or waiting patiently.
- Avoid nodding frequently.
- Length: Each asking slot should last around 3–5 seconds.

**Answering phase**
- Speak naturally with natural hand gestures from time to time.
- Use natural and common gestures when speaking. Avoid meaningful gestures like pointing, applause, or thumbs up.
- Begin gestures after starting to speak, and stop them before you finish.
- Length: Each answering slot should last around 5 seconds.

**Total video length**
- Aim for a total video length of 1–5 minutes.

## Data requirements

Basic video processing helps improve model training efficiency:

- Keep the character centered on screen with consistent size and position throughout recording. Keep all video processing parameters like brightness and contrast consistent. The output avatar's size, position, brightness, and contrast will directly reflect those in the training data. We don't apply alterations during processing or model building.
- Start and end clips in status 0. Actors should close their mouths, smile, and look ahead. The video should be continuous, not abrupt.

**Avatar training video recording file format:** .mp4 or .mov.

**Resolution:** At least 1920x1080. 3840x2160 to train a 4K avatar

**Frame rate per second:** At least 25 FPS.

## Related content

* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
* [What is custom text to speech avatar](what-is-custom-text-to-speech-avatar.md)
