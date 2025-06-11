---
title: Transparency note for Spatial Analysis
titleSuffix: Azure AI services
description: The Transparency note discusses Spatial Analysis and the key considerations for making use of this technology responsibly.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: article
ms.date: 08/12/2022
---

# Transparency note for Spatial Analysis

[!INCLUDE [non-english-translation](/azure/ai-foundry/responsible-ai/includes/non-english-translation.md)]

This Transparency note discusses Spatial Analysis and the key considerations for making use of this technology responsibly.

## What is a Transparency note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use transparency notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Responsible AI principles from Microsoft](https://www.microsoft.com/ai/responsible-ai).

## The basics of Spatial Analysis and Video Retrieval

### Introduction

This Transparency note discusses Spatial Analysis and Video Retrieval and the key considerations for making use of this technology responsibly.

Spatial Analysis is a feature of Azure AI Vision that helps organizations maximize the value of their physical spaces by understanding people's movements and presence within a given area. It allows you to ingest video from CCTV or surveillance cameras, run AI operations to extract insights from the video streams, and generate events to be used by other systems. With input from a camera stream, an AI operation can do things like count the number of people entering a space or measure compliance with face mask and social distancing guidelines.

Video Retrieval enables state-of-the-art natural language video search across thousands of hours of footage within a video index. This is achieved through a vector-based search that operates on both vision and speech transcript modalities. Video Retrieval uses vector similarity to match video frames with search terms based on semantic closeness, for example for searching across video content or recommending similar content based on a text query.

For more information, see the [Spatial Analysis overview](https://go.microsoft.com/fwlink/?linkid=2154029) and the [Video Retrieval how-to guide](/azure/ai-services/computer-vision/how-to/video-retrieval).

### Key terms

The core operations of Spatial Analysis and Video Retrieval are built on a system that ingests video, detects whether people are in the video, tracks the people as they move around over time, and generates events as people interact with regions of interest. To understand how Spatial Analysis and Video Retrieval work, it's important to define a set of key components that make up this pipeline. Customers have control of which components to use when they configure the services.

| Component | Definition |
|------|------------|
| **People Detection** | This component answers the question, "Where are the people in this image?" It finds people in an image and passes bounding box coordinates indicating the location of each person. These bounding boxes are used as input to the **People Tracking** component.  **People Detection** is incapable of uniquely identifying individuals and it does not create any unique identifying numerical or other representation of an individual’s physical, physiological, or behavioral (including gait) characteristics from the video.  |
| **People Tracking** | This component connects the people detections over time as people move around in front of a camera. It uses temporal logic about how people typically move as well as basic information about the overall appearance of the people, not based on uniquely identifying individuals. It does not track people across multiple cameras. If a person exits the field of view for longer than approximately one minute and then reenters the view, the system will perceive them as a new person. </br></br>For example, the system will track the path of a person as they walk from left to right past a camera, but won’t be able to identify them or even know it’s the same person when they pass 5 minutes later. </br></br>**People Tracking** is incapable of uniquely identifying individuals and it does not create any unique identifying numerical or other representation of an individual’s physical, physiological, or behavioral (including gait) characteristics from the video.|
| **Skeleton Detection** | This component detects the location of key points of a person's body and its parts. For each bounding box output by **People Tracking**, **Skeletal Detection** may be periodically run, depending on whether orientation and calibration are enabled. The model identifies skeletal key points, including key points on the face, and measurements of the body positions and joints representing body parts are used to estimate the location of the camera and the 3D orientation of each person. **Skeletal Detection** is incapable of uniquely identifying individuals and it does not create any unique identifying numerical or other representation of an individual’s physical, physiological, or behavioral (including gait) characteristics from the video. |
| **Face Mask Detection** | This component detects the location of a person's face in the camera's field of view and identifies the presence of a face mask. The AI operation scans images from video and where a face is detected the service provides a bounding box around the face. Using object detection capabilities, it identifies the presence of face masks within the bounding box. **Face Mask Detection** is incapable of uniquely identifying individuals and it does not create any unique identifying numerical or other representation of an individual’s physical, physiological, or behavioral (including gait) characteristics from the video. |
| **Region of Interest** | This component is a user-defined zone or line in the input video frame. When a person interacts with this region on the video, the system generates an event. For example, for the _PersonCrossingLine_ operation, a line is defined in the video frame. When a person crosses that line, an event is generated. |
| **Event** | An event is the primary output of Spatial Analysis. Each operation raises a specific event either periodically (like once per minute) or whenever a specific trigger occurs. The event includes information about what occurred in the input video but does not include any images or video. For example, the Spatial Analysis "People Count" operation can raise an event containing the updated count every time the count of people changes (trigger) or once every minute (periodically). |
| **Vectorization** | This component encodes selected video frames and speech transcripts into vector embeddings by converting these elements into numerical representations that capture the key features in the frames and transcripts. Similarly, when a user submits a search query, the text of the query is also converted into a vector embedding within the same dimensional space as the vector embedding of the video frame and/or speech transcript. This allows the component to compare between embeddings and analyze them to enable effective retrieval. </br></br>This component is not intended or optimized for identifying individuals and retrieval of individuals is not the result of facial recognition or analysis of facial templates. Queries only contain natural language descriptions, so visual querying (e.g., inputting images) is not possible. Rather, the component may use contextual cues or stereotyping, as opposed to a person’s physical characteristics (e.g., the face), to associate the search query with an individual in the search corpus. Alternatively, there may only be a few individuals in the search corpus enhancing the likelihood of a chance match. For example, a query for a popular athlete might retrieve that precise athlete not because of any matching of face embeddings, but because the search corpus contained the athlete wearing their team’s jersey and their specific number, or that athlete was the only person in the dataset. |

## Capabilities

### System behavior

#### Spatial Analysis

Spatial Analysis ingests video and detects people in the video in real-time. It decodes the video, then utilizes a person detection model to identify the bounding boxes for locations of people shown in the video. After people are detected, the system assigns a numbered identifier to each individual as part of the person tracking process. This identifier is crucial for tracking their movements over time but is not intended for personal identification purposes within Spatial Analysis. It simply distinguishes and tracks different people within the video frame. As individuals move, the system tracks these bounding boxes, generating events when they interact with predefined regions of interest. While it may be possible for customers to cross-reference these Spatial Analysis identifiers with other datasets to uniquely identify individuals, Spatial Analysis itself does not provide specific capabilities to facilitate this identification. Additionally, all operations provide insights from a single camera's field of view so tracking is only done in the small region covered by a camera, not an entire building.

#### Video Retrieval

Video Retrieval enables natural language video search across thousands of hours of footage within a video index. This is achieved through a vector-based search that operates on both vision and speech transcripts modalities. By utilizing Azure AI Vision multimodal vector embeddings—a numerical representation that captures the essence of text or imagery—Video Retrieval can find specific content within videos from the index at a granular level.

Video Retrieval enhances search precision through a three-step process:

1. **Vectorization**: Initially, the system vectorizes both the video content and the search queries. It encodes key data from selected video frames and speech transcripts into vector embeddings, translating these elements into a numerical vector format. Similarly, when a user submits a search query, the text is also converted into a vector within the same dimensional space. Alignment for similar concepts between the embeddings for the search query and the video enables effective retrieval.
1. **Measurement**: During this stage, the system conducts a comprehensive vector similarity analysis. It measures the alignment between the vector of the user's query and the vectors representing the video data. The result is a set of search results that most closely correspond to the user’s query for both the spoken words and the visual elements of the video according to the embedding models.
1. **Retrieval**: The last step is the retrieval of relevant content. The system identifies and extracts the specific video segments that match the query, based on the similarity analysis. These identified segments are then presented to the user.

### Use cases

#### Uses for Spatial Analysis

The following are example use cases for which we designed and tested spatial analysis.
- **Shopper analysis** - A grocery store uses cameras pointed at product displays to measure the impact of merchandising changes on store traffic. The system allows the store manager to identify which new products drive the most change to engagement.
- **Queue management** - Cameras pointed at checkout queues provide alerts to managers when wait time gets too long, allowing them to open more lines. Historical data on queue abandonment gives insights into consumer behavior.
- **Building occupancy & analysis** - An office building uses cameras focused on entrances to key spaces to measure footfall and how people use the workplace. Insights allow the building manager to adjust service and layout to better serve occupants.
- **Minimum staff detection** - In a data center, cameras monitor activity around servers. When employees are physically fixing sensitive equipment two people are always required to be present during the repair for security reasons. Cameras are used to verify that this guideline is followed.
- **Workplace optimization** - In a fast casual restaurant, cameras in the kitchen are used to generate aggregate information about employee workflow. This is used by managers to improve processes and training for the team.
- **Social distancing compliance** - An office space has several cameras that use spatial analysis to monitor social distancing compliance by measuring the distance between people. The facilities manager can use heatmaps showing aggregate statistics of social distancing compliance over time to adjust the workspace and make social distancing easier.
- **Face mask compliance** – Retail stores can use cameras pointing at the store fronts to check if customers walking into the store are wearing face masks to maintain safety compliance and analyze aggregate statistics to gain insights on mask usage trends.

#### Uses for Video Retrieval

- **Media & entertainment library search** - A media company can use Video Retrieval to find specific content in a large media library. The system allows the content creators and editors to search for relevant video clips based on keywords, topics, or visual elements. For example, they can search for "scenes with dogs" or "dramatic moments with rain." The system returns the most matching video segments from the library, saving time and effort for the content production team.
- **Safety & security forensic search** - A security company can use Video Retrieval to find specific events in the footage from multiple cameras. The system allows security personnel to search for anomalous activities based on criteria such as time, location, or behavior. For example, they can search for "person with a red jacket" or "person carrying a backpack" to find video related to a specific incident. The system returns the most relevant video segments from the footage, accelerating the review and investigation process.

It's important to note that the Video Retrieval system is not designed to identify or retrieve footage based on specific individuals by their identity. It focuses for generic object and activity retrieval using, visual and transcript elements. 

#### Considerations when choosing other use cases

- Avoid real-time critical safety alerting – Spatial analysis and Video Retrieval were not designed for critical safety real-time alerting. They should not be relied on for scenarios when real-time alerts are needed to trigger intervention to prevent injury, like turning off a piece of heavy machinery when a person is present. They can be used for risk reduction using statistics and intervention to reduce risky behavior, like people entering a restricted/forbidden area.
- Avoid use for employment-related decisions – Spatial analysis provides probabilistic metrics regarding the location and movement of people within a space. While this data may be useful for aggregate process improvement, the data is not a good indicator of individual worker performance and should not be used for making employment-related decisions.
- Avoid use for healthcare-related decisions – Spatial analysis provides probabilistic and partial data related to people’s movements. The data is not suitable for making health-related decisions.
- Carefully consider use in public spaces – Evaluate camera locations and positions, adjusting angles and region of interests to minimize collection from public spaces. Lighting and weather in public spaces such as streets and parks will significantly impact the performance of the spatial analysis system, and it is extremely difficult to provide effective disclosure in public spaces.
- Avoid use in protected spaces – Protect individuals’ privacy by evaluating camera locations and positions, adjusting angles and region of interests so they do not overlook protected areas, such as restrooms.
- Carefully consider use in schools or elderly care facilities – Spatial analysis has not been rigorously tested with data containing minors under the age of 18 or adults over age 65. We would recommend that customers thoroughly evaluate error rates for their scenario in environments where these ages predominate.
- Avoid identification or ID verification – The system is not designed for identification or ID verification of individuals. Its use should explicitly avoid scenarios where identification or verification of individuals is required. 
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Technical limitations, operational factors, and ranges


### Limitations for Spatial Analysis

Spatial analysis should not be relied on for scenarios where real-time alerts are needed to trigger intervention to prevent injury, like turning off a piece of heavy machinery when a person is present. Space analytics is better used to reduce the number of unsafe acts by measuring the aggregate number of people violating rules like entering restricted/forbidden areas.

- Spatial analysis has not rigorously tested with data containing minors under the age of 18 or adults over age 65. We would recommend that customers thoroughly evaluate error rates for their scenario in environments where these ages predominate.
- Spatial analysis face mask detection attribute should not be relied on if a person is wearing a transparent shield or glittery face masks; they make it challenging for the system to function accurately.
- Spatial analysis will work best when configured with a ~15 frames per second input video stream with at least 1080p resolution. A slower frame rate or lower resolution risks losing track of people when they move quickly or are too small in the camera view.
- Camera placement should maximize the chance of a good view of people in the space and reduce the likelihood of occlusion. Follow the instructions in Camera Placement Guidance whenever possible to ensure the system functions optimally.
- Often objects or people will block the view of a camera occluding part a scene. This will impact the accuracy of the system, especially if occlusions occur in a region of interest. Spatial analysis has a limited ability to track a person through an occlusion. Cameras should be setup to minimized occlusions as much as possible.
- Zone and line placement designate a specific region of interest for generating insights. The region should be optimized to cover the largest area possible without including any area that you do not care about. Too small a region can result in unreliable data. For details see Zone and Line Placement Guide.
- Cameras should be setup to yield high quality images, avoiding lighting conditions outside the recommended operating range that result in over or under exposure of images.
- CCTV Cameras are often setup outside or with exterior views, so lighting and weather can influence the quality of video dramatically. This will impact the accuracy of insights derived from such a camera.
- Fisheye or 360 cameras are sometimes used in CCTV deployments. Spatial analysis can consume de-warped video from a 360 camera, but directly consuming a raw 360 stream is not supported. The system will be less accurate in detecting people in the video since it has not been trained with this kind of distortion.
- Spatial analysis is designed to work well with fixed cameras. When cameras move, you may need to adjust regions and rerun autocalibration. Skills that use auto-calibration assume that the floor in the space is relatively flat. If the floor in the space has dramatic changes in slope it may impact accuracy.

### Limitations for Video Retrieval

- **Relevance**: Image Retrieval will always return a result to a user query even if there is no relevant match in the user’s image set. For example, if the user searches for "dogs playing in the backyard" in an image set that only contains images of people, the system will return the closest thing to the search query. In this case, it could return images of people. This feature is not intended for use to query abstract concepts that do not correspond to images, such as emotion and gender.
- **Stereotyping**: The model has learned to associate names inputted with the stereotypical gender and ethnicity of people with those names and may associate private citizens’ names with celebrity images or visa versa.
    > [!NOTE]
    > Video Retrieval is incapable of verifying or identifying individuals, and it does not predict or classify facial attributes or create facial templates (unique identifying numerical or other representation of an individual’s face that is generated from an image) when faces are detected. Any perceived recognition of an individual is the result of stereotyping.
- **Recency**: Our models have been trained on datasets that contain some information about real world events but if you query the models about events that took place after the models were trained, they will not perform well.
- **Deliberate misuse**: If highly disturbing images, paired with highly disturbing text are uploaded into Video Retrieval, it can return harmful and offensive content as part of the results. To mitigate this unintended result, we recommend that you control access to the system, and educate the people who will use it about appropriate use.
- **Understanding motion**: Video summary and frame locator has a limited ability to accurately understand motion and actions in a video. When queried for actions like "a person taking a picture" or "a person falling," it may give inaccurate results. More effective queries would include "a person with a camera" or "a person on the ground." 
- **Complex queries syntax**: Queries containing complex syntax such as prepositions, e.g., "a person on a ladder" or "a person with no ladder" might yield inaccurate results.


## System performance

System accuracy depends on a number of factors, including core model accuracy, camera placement, configuration of regions of interest, how people interact with the system, and how people interpret the system's output. The following sections are designed to help you understand key concepts about accuracy as they apply to using spatial analysis.

### Language of accuracy

The **accuracy** of a Spatial Analysis skill is a measure of how well the system-generated events correspond to real events that happened in the space. For example, the _PersonCrossingLine_ should generate a system event whenever a person crosses a designated line in the cameras field of view. To measure accuracy, one might record a video with people walking across the designated line, count the true number of events based on human judgement, and then compare with the output of the system. Comparing the human judgement with the system generated events would allow you to classify the events into two kinds of correct (or "true") events and two kinds of incorrect (or "false") events.

The **accuracy** of Video Retrieval is assessed by how closely the system's search results align with the actual content of the video. For instance, when a user searches for "scenes with dogs" or "dramatic moments with rain," the Video Retrieval system is expected to return video segments that precisely match these descriptions. To evaluate accuracy, specific test datasets, representative of various real-world scenarios and conditions, are used. These datasets include a wide range of video content types and user interaction scenarios.

Accuracy measurement in Video Retrieval involves comparing the search results against a benchmark set based on human judgment. For example, the system's response to a query about "dramatic moments with rain" is assessed against a manually curated list of video segments that experts agree depict such scenes. The comparison allows classification of the results into categories like correct matches (true positives) and incorrect matches (false positives).

|Term | Definition| Example|
|--|--|--|
|True Positive	|The system-generated event correctly corresponds to a real event.	|The system correctly generates a _PersonLineEvent_ when a person crosses the line.|
|True Negative	|The system correctly does not generate an event when a real event has not occurred.	|The system correctly does not generate a _PersonLineEvent_ during a time when no one has crossed the line.|
|False Positive	|The system incorrectly generates an event when no real event has occurred.|	The system incorrectly generates a _PersonLineEvent_ when no one has actually crossed the line.|
|False Negative	|The system incorrectly fails to generate an event when a real event has occurred.	|The system incorrectly fails to generate a _PersonLineEvent_ when a person has actually crossed the line.|

There are many scenarios in which Spatial Analysis can be used. Accuracy has different implications for the people involved depending on the scenario. Considering each of the defined example use cases:

- **Spatial Analysis: Measuring social distancing compliance** - In this case, a false positive would occur if the system inaccurately flagged an interaction between two people as a social distance violation. A false negative would be if the system missed an instance where two people violated the social distancing guideline.
    A customer who is concerned about safety may be willing to accept more false positives in order to prevent false negatives, where the system misses cases in which the 6-foot social distancing rule is violated. This customer might choose to set a seven-foot threshold instead of six, increasing the number of potential violations flagged by the system, in order to reduce the chance that a violation is missed.
- **Spatial Analysis: Queue management** - In this case, the system could use _PersonCrossingPolygon_ enter and exit events to calculate how many people are in line and the wait time. If several false positive _enter_ events occur, the system would overestimate the wait time resulting in recommending the store manager deploy more associates to checkout than necessary wasting resources. If several false negative _enter_ events occur, the system would underestimate the wait time resulting in recommending too few associates be deployed to checkout, creating a negative customer experience.
    In this case, a customer would likely be equally concerned about false positives and false negatives. To minimize the chances of each, it would be important to have a well-defined fixed space for the queue and following the best practices listed below especially the [Camera Placement Guidance](/azure/ai-services/computer-vision/spatial-analysis-camera-placement), [Zone and Line Placement Guide](/azure/ai-services/computer-vision/spatial-analysis-zone-line-placement), and minimizing occlusion in the queue area.
- **Video Retrieval: Media & Entertainment Library Search** - In this scenario, a media company utilizes Video Retrieval to efficiently navigate their extensive media library. Content creators and editors can search for specific types of video clips using keywords, topics, or visual elements. For instance, they might look for "scenes with dogs" or "dramatic moments with rain."
    Accuracy in this context plays a crucial role. A false positive in this scenario would occur if the system retrieves a video segment that doesn't match the query, such as returning a scene with cats when searching for dogs. This would lead to inefficiency and potentially disrupt the creative process. On the other hand, a false negative would happen if the system fails to identify and retrieve a relevant scene that does exist in the library, like missing a key dramatic rain scene that would have been perfect for the project at hand.

    For media companies, the precision of search results directly impacts the efficiency and effectiveness of their content production process. False positives could lead to wasted time reviewing irrelevant footage, while false negatives might mean missing out on ideal content that's already in their library. Therefore, refining search queries and ensuring the video library is well-indexed with accurate tags and descriptions are essential steps to enhance the accuracy and usefulness of the Video Retrieval system in a media and entertainment setting. This accuracy is key to saving time and effort for the content production team, enabling them to find the exact content they need quickly and efficiently.

Both kinds of errors reduce the accuracy of the system. For deployment recommendations, including providing effective human oversight to reduce the potential risks associated with these errors see the [Responsible Use Deployment documentation](/azure/ai-foundry/responsible-ai/computer-vision/responsible-use-deployment).

### Best practices for improving system performance

#### Best practices for Spatial Analysis

- Spatial Analysis should not be relied on for scenarios where real-time alerts are needed to trigger intervention to prevent injury, like turning off a piece of heavy machinery when a person is present. Spatial Analysis is better used to reduce the number of unsafe acts by measuring the aggregate number of people violating rules like entering restricted/forbidden areas. Use other methods, such as sensors or alarms, to provide real-time alerts and prevent injuries.
- Spatial Analysis will work best when configured with a ~15 frames per second input video stream with at least 1080p resolution. A slower frame rate or lower resolution risks losing track of people when they move quickly or are too small in the camera view. Use high-quality cameras and video streams to ensure the optimal performance of Spatial Analysis.
- Camera placement should maximize the chance of a good view of people in the space and reduce the likelihood of occlusion. Follow the instructions in [Camera Placement Guidance](/azure/ai-services/computer-vision/spatial-analysis-camera-placement) whenever possible to ensure the system functions optimally. Place the cameras at a high and wide angle, avoid direct sunlight or glare, and cover the entire area of interest.
- Often objects or people will block the view of a camera occluding part of a scene. This will impact the accuracy of the system, especially if occlusions occur in a region of interest. Spatial Analysis has a limited ability to track a person through an occlusion. Cameras should be set up to minimize occlusions as much as possible. Use multiple cameras to cover different angles and perspectives, and avoid placing objects or furniture that may obstruct the view.

#### Best practices for Video Retrieval

- **Relevance**: To get the best results from Video Retrieval, make sure that your video index contains content that is relevant to your search queries. For example, if you want to search for "dogs playing in the backyard," make sure that your video index includes dogs and backyards. Avoid querying abstract concepts that do not correspond to still images from the video index, such as emotion and gender, as they may return inaccurate or irrelevant results.
- **Stereotyping**: Be aware that Video Retrieval may associate names inputted with the stereotypical gender and ethnicity of people with those names and may associate celebrity names with private citizens’ images or vice versa. Video Retrieval was not intended, is not capable of and should not be used, for identifying or verifying individuals.  Using Video Retrieval for identification or verification may result in false positives or false negatives. Video Retrieval does not predict or classify facial attributes, and it does not create facial templates when faces are detected. Any perceived recognition of an individual is the result of stereotyping.
- **Understanding Motion**: Video Retrieval has a limited ability to accurately understand motion and actions in a video. When querying for actions like "a person taking a picture" or "a person falling", it may give inaccurate results. To improve the accuracy of Video Retrieval, use clear and specific queries, such as "a person holding a camera" or "a person lying on the ground."
- **Complex queries syntax**: Video Retrieval may not handle queries containing complex syntax, such as prepositions, e.g., "a person on a ladder" or "a person with no ladder", very well. It may yield inaccurate results. To avoid this, use simple and direct queries, such as "a ladder" or "no ladder."

## Evaluation of Spatial Analysis and Video Retrieval

The evaluation of both Spatial Analysis and Video Retrieval models involves detailed testing to ensure their effectiveness and fairness across various scenarios and conditions.

### Evaluation methods

To evaluate these models, specific test datasets are used. These datasets are carefully curated to represent a wide range of scenarios and conditions that the models might encounter in real-world applications.

For Spatial Analysis, the focus is on metrics like Precision & Recall for specific event types, such as "person crossing a line." Additionally, there is a specific emphasis on People Detection Precision & Recall, as this is the primary component the directly makes inferences based on the image.

In Video Retrieval, the evaluation includes regression testing and model performance testing, with key metrics like precision and recall at different ranks or numbers of results (e.g., Precision@1 or Precision with of the top result, Precision@5 or Precision with of the top five results), Normalized Discount Cumulative Gain (nDCG) for the results set, and latency at the 90th percentile.

### Evaluation results

The objective is to ensure that updates to these models do not result in regression. This means that new models should maintain or improve the performance of the current production models. For a model to be considered for deployment, it must demonstrate noticeable improvements in the key metrics compared to the current production model.

The models are trained and evaluated on diverse datasets. For spatial analysis, this includes variations in environment settings, camera angles, lighting conditions, and movement dynamics. For video retrieval, the datasets are designed to include a variety of video content types and user interaction scenarios. Both models are trained to handle diverse demographic representations including age groups, genders, and ethnic backgrounds.

### Fairness considerations

In alignment with our commitment to fair and inclusive technology, both spatial analysis and video retrieval models undergo rigorous fairness evaluations. For Spatial Analysis, the fairness evaluation focuses on the People Detection model's performance across different categories of people. This includes ensuring that the model does not exhibit biases based on race, gender, age, or other demographic factors. Similarly, for Video Retrieval, the system's performance is evaluated to ensure equitable accuracy and no disproportionate favoring or disadvantage for any group based on demographic factors.

### Evaluating Spatial Analysis and Video Retrieval for your use

Real-world performance of Spatial Analysis and Video Retrieval can vary based on specific use cases and conditions. Users are encouraged to conduct their evaluations using datasets that reflect their scenarios. These should include a wide range of content and interactions for Video Retrieval and varied environmental conditions and event types for Spatial Analysis.

### Guidance for integration and responsible use

Responsible use and integration of these AI-powered systems are crucial. Users should:
- **Understand capabilities and limitations**: It is crucial to fully assess the capabilities and limitations of both spatial analysis and video retrieval technologies. Understanding their performance in your specific scenario and context is key. This requires thorough testing with real-life conditions and data to gauge their effectiveness and limitations accurately.
- **Respect privacy**: Data collection and usage should be lawful and justifiable. Only gather and use data for which you have explicit consent and for the intended purposes. Be mindful of privacy concerns and handle data with the utmost care and security.
- **Legal review**: Seek appropriate legal advice to ensure your solution complies with all applicable laws and regulations, particularly if used in sensitive or high-risk applications. Understand the legal framework within which you operate and your responsibilities for any future issues that might arise.
- **Human-in-the-loop**: Maintain a consistent human oversight mechanism. This means ensuring continuous human monitoring of the AI-powered systems and keeping humans integral to decision-making processes. Be prepared for real-time human intervention to mitigate potential harms, ensuring that situations where the model underperforms are appropriately managed.
- **Security**: Secure your solutions to protect the integrity of your content and prevent unauthorized access. Implement robust security measures to ensure the safety and privacy of the data and systems.
- **Build trust with stakeholders**: Transparently communicate with all stakeholders, including users and the public, about the expected benefits and potential risks of the technologies. Explain the need for data and how its usage contributes to those benefits. Make data handling practices clear and understandable.
- **Feedback loop**: Establish a feedback channel for users to report any issues or concerns with the service once deployed. Continuously monitor and improve the AI-powered features based on this feedback. Be ready to act on suggestions and concerns, maintaining an open dialogue with users and stakeholders. See: [Community jury](/azure/architecture/guide/responsible-innovation/community-jury/).
- **Diverse community feedback**: Actively seek feedback from a diverse range of community members during development and evaluation. This includes historically marginalized groups, people with disabilities, and various occupational groups. Such feedback is critical for understanding the broader societal impact and for mitigating biases and stereotypes.
- **User studies for consent and disclosure**: Conduct user studies to evaluate the comprehension and acceptance of the technology among different community members. This helps to ensure that design choices are effective and meet user expectations. Validate these studies with a representative sample to ensure they are inclusive and comprehensive.

The evaluation of Spatial Analysis and Video Retrieval models is essential to ensure their effectiveness and fairness in a diverse range of applications. By thoroughly testing and refining these technologies, we aim to provide powerful tools that respect diversity and fairness, crucial in our increasingly digital and global society.

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)
- [Microsoft Azure Learning courses on responsible AI](/learn/paths/responsible-ai-business-principles/)

## Learn more about Spatial Analysis

- [Spatial Analysis overview](/azure/ai-services/computer-vision/intro-to-spatial-analysis-public-preview)
- [Data, privacy, and security for Spatial Analysis](/azure/ai-foundry/responsible-ai/computer-vision/compliance-privacy-security-2?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext)

