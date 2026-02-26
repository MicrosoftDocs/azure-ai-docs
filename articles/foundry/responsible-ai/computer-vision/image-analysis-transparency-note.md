---
title: Transparency Note and use cases for Image Analysis
titleSuffix: Foundry Tools
description: This article explains Image Analysis Responsible AI basics, use cases, and terms.
ai-usage: ai-assisted
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 10/15/2025
---

# Transparency note: Image Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who use it, the people who will be affected by it, and the environment in which it's deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see the [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Image Analysis

### Introduction

Organizations are building solutions to process media assets such as digital files and images and extract actionable insights. These insights include visual features from images such as objects, people, and image descriptions that can be used to power knowledge mining, business process automation, and accessibility of content for everyone.

Accessible through Foundry Tools, Image Analysis APIs offer pretrained machine learning models to assign labels to images and classify them into thousands of predefined categories. The APIs extract many visual features from images, including objects, people, adult content, and auto-generated image captions. Using the Customization feature, customers can quickly train vision models using their own data and defining their own categories.

### Key terms

| **Term** | **Definition** |
| --- | --- |
| **prebuilt models** | Models powering features that Image Analysis offers to customers. These models do not require additional training. |
| **Base model** | Base models are a combination of model architecture and training data used to tune that architecture for a specific type of task (for example, image classification or object detection). Base models are built by Microsoft and are used as a starting point for the transfer learning process for various domains such as General, Food, Landmarks, Retail, Logos, and Products on Shelves. |
| **Model training** | This refers to the process of training a model based on customer provided labeled images when using the model customization feature. |
| **Few-shot learning** | In contrast to traditional methods of training machine learning models, where large amounts of training data are typically used, few shot learning uses a small amount of training data to train a model to learn the underlying pattern in order to recognize and classify new data provided by the customer when using the customization feature. |
| **Transfer learning** | The use of customer provided training data in the model customization feature to retrain a base model to address the specific problem the customer is trying to solve. The training data might be a combination of the classes they want to recognize or detect, and the type of images. |
| **Class** | A trained model has a set of classes it will assign when analyzing an input image. When you're building a custom image classification model through model customization, you define the set of classes you want the model to output and provide labeled training data for each of the classes. |
| **Class accuracy pair** | The class accuracy pair is a set of two values consisting of the name of the class and a float value for the confidence score associated with the class detection. For example, a class might be a type of fruit like a pineapple or pear represented in the image set. The class-accuracy pair is the specific class and the confidence score that the class is present in the image (for example, Pineapple: 93.53%). |
| **Image classification** | This feature takes an image as an input, and outputs a set of class accuracy pairs that are image level properties (they don't specify a location within the image). For example, a pair might be fruit versus non-fruit, where most of the image is occupied by the respective class. |
| **Object detection** | This feature takes an image as an input, and outputs a set of class accuracy pairs that also includes the bounding box coordinates for where in the image those classes were detected. For example, the model might detect the bounding box coordinates for where a vehicle is found in the image. |
| **Bounding box** | A set of four numerical values representing the x,y pixel coordinates of the top left corner of the detected object relative to the top left corner of the image, the width of the detected object. |
| **Confidence** | An Image Analysis operation returns confidence values in the range of 0 to 1 for all extracted output. The confidence value represents the estimate of the likelihood of a tag.|
| **Florence** | Florence is the name of a new foundation AI model, part of an Azure Vision in Foundry Tools initiative, trained with billions of text-image pairs that powers many of the quality improvements in the v4.0 release of the Vision service. It has the ability to recognize millions of object categories out of the box, and enables faster, lower-cost customization to recognize specific patterns with fewer training images in the model customization service. |
| **Planogram** | A planogram is a document or diagram that describes the placement of products on shelves or displays in a retail store. It's used to help retailers and manufacturers optimize the placement of products to increase sales. In product recognition scenarios, the planogram is represented as a JSON document.|

## Capabilities

### Features

> [!IMPORTANT]
> Except for celebrity recognition, none of the following Image Analysis capabilities can identify or verify individual people. They don't predict or classify facial attributes, and they don't create facial templates (unique set of numbers that are generated from an image that represents the distinctive features of a face) when faces are detected. Any recognition of an individual is the result of your labeling and not from our facial recognition capabilities or from the creation of a facial template. Celebrity recognition is a limited access feature only available to approved customers. When celebrity recognition is in use, Image Analysis calls Face API, generates facial templates for detected faces, and compares them to the stored templates for celebrities (see Celebrity, landmark, and brand recognition, below).

You can use Image Analysis to process images:

- [**Tag visual features**](/azure/ai-services/computer-vision/concept-tagging-images): From a set of thousands of recognizable objects, living things, scenery, and actions, you can identify and tag visual features in an image. When the tags are ambiguous or the identity of the contents aren't common knowledge, the API response provides hints to clarify the context of the tag. Tagging isn't limited to the main subject of the image, such as a person in the foreground. Tagging can also include the setting (indoors or outdoors), furniture, tools, plants, animals, accessories, and gadgets.
- [**Detect objects**](/azure/ai-services/computer-vision/concept-object-detection): Object detection is similar to tagging, but the API returns the bounding box coordinates for each tag applied. For example, if an image contains a dog, a cat, and a person, the operation lists each object and its coordinates in the image. You can use this functionality to process relationships between the objects in an image. Object detection also lets you know when there are multiple instances of the same tag in an image.
- **[Generate descriptive captions](/azure/ai-services/computer-vision/concept-describing-images):** The image captioning algorithm uses celebrity recognition and landmark recognition models to generate more descriptive captions when celebrities or landmarks are present in the image. Celebrity recognition is only available to approved customers, apply [here](https://aka.ms/facerecognition) if you would like to use celebrity recognition.

   > [!NOTE]
   > "Caption" replaces "Describe" in V4.0 as the improved image captioning feature rich with details and semantic understanding. Dense Captions provides more detail by generating one sentence descriptions of up to 10 regions of the image in addition to describing the whole image. Dense Captions also returns bounding box coordinates of the described image regions.

- [**Moderate content in images**](/azure/ai-services/computer-vision/concept-detecting-adult-content): You can use Image Analysis to detect adult, racy, and gory content in an image and obtain confidence scores for these classifications. You can set the threshold for flagging content as adult, racy, or gory on a sliding scale to accommodate your preferences.
- [**Obtain an area of interest and smart crops**](/azure/ai-services/computer-vision/concept-generating-thumbnails?tabs=3-2): You can analyze the contents of an image to return the coordinates of the image's most important region or get AI-suggested crops of the image for different aspect ratios. Face detection is used to help determine important regions in the image. The detection doesn't involve distinguishing one face from another face, predicting or classifying facial attributes, or creating a facial template (a unique set of numbers that are generated from an image that represents the distinctive features of a face).
- [**Extract text in images**](/azure/ai-services/computer-vision/concept-ocr): Image Analysis has optical character recognition (OCR) that you can use to detect printed or handwritten text in images and return the text and the text coordinates.
- [**Detect people and faces**](/azure/ai-services/computer-vision/concept-detecting-faces): You can use Azure Vision to detect faces and people in an image. The APIs return the rectangle coordinates for each detected face and person. Face verification and identification are offered by the [Azure AI Face service](/azure/ai-services/computer-vision/overview-identity).
- **[Celebrity, landmark, and brand recognition](/azure/ai-services/computer-vision/concept-detecting-domain-content)**: Use Image Analysis to identify commercial brands, popular landmarks, and celebrities in images or videos from a preset database of thousands of global logos, landmarks, and celebrities (includes around 1 million faces based on commonly requested data sources such as IMDb, Wikipedia, and top LinkedIn influencers). You can use this feature, for example, to discover which brands are most popular on social media or brands that are most prevalent in media product placement. Celebrity recognition is limited to approved customers.
- **[Customization](/azure/ai-services/computer-vision/concept-model-customization)**: Customization is a feature of Azure Vision that lets you build, deploy, and improve your own custom image identification system. An image identifier applies labels to images, according to their visual characteristics. Each label represents a classification or object. Customization allows you to specify your own labels and train custom models to detect them.
- **[Product understanding](/azure/ai-services/computer-vision/how-to/shelf-analyze)**: Use a specialized Image Analysis model to detect the presence of products on retail store shelves. This can be combined with **Customization** to train models to identify specific products on store shelves.
- **[Image stitching](/azure/ai-services/computer-vision/how-to/shelf-modify-images)**: Combine multiple images that partially overlap into a single large image. This is used in the product recognition scenario to get a single image of an entire retail shelf.
- **[Image rectification](/azure/ai-services/computer-vision/how-to/shelf-modify-images)**: Undo the perspective distortion of an image. This is used in the product recognition scenario to ensure shelf images are  easier to analyze.
- **[Planogram matching](/azure/ai-services/computer-vision/how-to/shelf-planogram)**: Compare product recognition results with a planogram document to see which spots are occupied by products and which have gaps.
- [**Background Removal**](/azure/ai-services/computer-vision/concept-background-removal): Lets you remove the background of an image. This operation can either output an image of the detected foreground object with a transparent background, or a grayscale alpha matte image showing the opacity of the detected foreground object.
- [**Image Retrieval**](/azure/ai-services/computer-vision/how-to/image-retrieval): Image Retrieval allows users to search images the way they think: using natural phases, questions, even vague descriptions. It enables the _vectorization_ of images and text queries. This lets you convert images and text to coordinates in a multi-dimensional vector space. Use vector similarity to match images with search terms based on semantic closeness, for example for searching across image content or recommending an image based on a text query or similar image.
- [**Video summary and frame locator**](https://aka.ms/visionstudio): Search and interact with video content in the same intuitive way you think and write. Locate relevant content without the need for additional metadata. Currently available only in Vision Studio

### Use cases

#### Intended uses

Here are some examples of when you might use Image Analysis:

- **Image discoverability**: Images that are uploaded to an organization's internal share space and social media platforms contain rich information and metadata. Usually, though, this information isn't machine readable, and it is unavailable for automated tagging, categorization, and search. Image Analysis makes insights from these images available for analysis, search, and retrieval. E-commerce companies, for example, could make their product library searchable, or a large website with user-generated content could enable powerful search and content recommendations.
- **Content processing automation**: You can use Image Analysis to automate tasks such as detecting visual content in images and building metadata into your media analysis pipeline. Automation can reduce the time, effort, and costs that are associated with creating and producing content.
- **Image content moderation**: E-commerce companies, user-generated content publishers, online gaming communities, and social media platforms need to moderate image content. Image Analysis allows you to automatically flag inappropriate content in images (for example, adult, racy, or gory). You can then use the returned content flags and their respective confidence scores to moderate content in your application as you see fit.
- **Domain-specific identification**: Developers can use Image Analysis to identify domain-specific content in social media and photo apps. For example, you can identify famous landmarks or brand logos in an image to provide appropriate recommendations for your users.
- **Use Azure Vision to build solutions that assist people who are blind and people with low vision by detecting and describing image content in human-readable language. In this context, we have enabled a parameter which will allow users to choose either gender-specific descriptions, for example, "a man and a woman sitting on a bench", or gender-neutral descriptions, for example, "two people sitting on a bench."
- **Image filtering for privacy purposes**: You can use Azure Vision to detect faces and people in images. Use face detection and people detection to determine whether images contain potentially sensitive information for privacy considerations.
- **Retail inventory management**: The product recognition APIs let you analyze photos of retail shelves, detect which products are there, and compare the photos to a planogram document.

#### Considerations when choosing other use cases

- **Apply human oversight for award or denial of benefits**: Using Azure Vision output directly to award or deny benefits might result in errors if outcomes are based on incorrect or incomplete information. To ensure fair and high-quality decisions for users, combine the automation that's available in Azure Vision with human oversight.
- **Not suitable for face identification or verification**: Azure Vision doesn't have facial recognition capabilities. Any recognition of an individual using Azure Vision occurs as a result of your labeling and not from actual facial recognition technology. [Use Azure AI Face.](/azure/ai-services/computer-vision/overview-identity)
- **Not suitable for age or gender classification**: Avoid using Azure Vision for age or gender classification.
- **Account for additional measures for domain-specific recognition**: prebuilt AI capabilities like celebrity recognition, landmark recognition, and brand logos recognition are trained on a finite set of celebrities, landmarks, and brands. The recognition service might not recognize all regionally specific celebrities, landmarks, or brands.
- **Not suitable for biometric identification**: Azure Vision wasn't designed or tested to verify the identity of individuals based on biometric markers such as iris recognition, fingerprint identification, or passports or other forms of ID for the purpose of identification and verification of a person.
- **Do not use Azure Vision for medical diagnosis**: including for use as a medical device, clinical support, diagnostic tool, or other technology intended to be used in the diagnosis, cure, mitigation, treatment, or prevention of disease or other conditions, and no license or right is granted by Microsoft to use this capability for such purposes. This capability isn't designed or intended to be implemented or deployed as a substitute for professional medical advice or healthcare opinion, diagnosis, treatment, or the clinical judgment of a healthcare professional, and shouldn't be used as such. The customer is solely responsible for any use of Azure Vision or Customization for medical diagnosis.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## System performance and Limitations for Image Analysis

### Accuracy for Image Analysis

The accuracy of the Image Analysis feature is a measure of how well AI-generated outputs correspond to actual visual content that's present in images. For example, the Image Tag feature should generate tags of the visual content that's present in the images. To measure accuracy, you might evaluate the image with your ground-truth data and compare the output of the AI model. By comparing the ground truth with AI-generated results, you can classify events into two kinds of correct ("true") results and two kinds of incorrect ("false") results:

| **Term** | **Definition** |
| --- | --- |
| True Positive | The system-generated output correctly corresponds to ground-truth data. For example, the system correctly tags an image of a dog as a dog.|
| True Negative | The system correctly doesn't generate results that aren't present in the ground-truth data. For example, the system correctly doesn't tag an image as a dog when no dog is present in the image.|
| False Positive | The system incorrectly generates an output that's absent in the ground-truth data. For example, the system tags an image of a cat as a dog.|
| False Negative | The system fails to generate results that are present in the ground-truth data. For example, the system fails to tag an image of a dog that was present in the image.|

These event categories are used to calculate precision and recall:

| **Term** | **Definition** |
| --- | --- |
| Precision | A measure of the correctness of the extracted content. From an image that contains multiple objects, you find out how many of those objects were correctly extracted. |
| Recall | A measure of the overall content extracted. From an image that contains multiple objects, you find out how many objects were detected overall, without regard to their correctness. |

The precision and recall definitions imply that, in certain cases, it can be hard to optimize for both precision and recall at the same time. Depending on your scenario, you might need to prioritize one over the other. For example, if you're developing a solution to detect only the most accurate tags or labels in the content, such as to display image search results, you would optimize for higher precision. But if you're trying to tag all possible visual content in the images for indexing or internal cataloging, you would optimize for higher recall.

If you are the owner of an image processing system, we recommend that you collect ground-truth evaluation data, which is data that is collected and tagged by human judges to evaluate a system. The prebuilt AI models provided in the Vision service might not satisfy the requirements of your use case. By using the evaluation dataset that is specific to your use case, you can make an informed decision on whether the prebuilt Image Analysis models are right for your scenario. If the prebuilt Image Analysis models are not right for your scenario, you can build your own models using the Customization feature described below. You can also use the data to determine how the confidence threshold affects the achievement of your goals.

You can compare ground-truth labels to the output of the system to establish overall accuracy and error rates. Error distribution helps you set the right threshold for your scenario. Ground-truth evaluation data should include an adequate sampling of representative images so that you can understand performance differences and take corrective action. Based on the results of your evaluation, you can iteratively adjust the threshold until the trade-off between precision and recall meets your objectives.

### System performance implications based on scenarios

System performance implications can vary according to how you use it. For example, you can use the confidence value to calibrate custom thresholds to handle your content and scenarios. Depending on its confidence value, content might be routed for straight-through processing or it might be forwarded to a human-in-the-loop process. The resulting measurements determine scenario-specific accuracy in terms of the precision and recall metrics, as illustrated in the following examples:

- **Photo-sharing app**: You can use Azure Vision to automatically generate tags for images that are shared and stored by application users. App users rely on this functionality to search for specific photos that are shared by other users. In this use case, the developer might prefer high-precision results because the cost of incorrectly extracting tags would result in incorrect query results for app users.
- **Image processing**: For insurance and claims processing applications, because you do not want to miss any potentially relevant information, you might prefer a high recall to maximize extractions. In this scenario, a human reviewer could flag incorrect or inappropriate tags.

### Additional limitations for Image Retrieval

- **Relevance**: Image Retrieval will always return a result to a user query even if there is no relevant match in the user's image set. For example, if the user searches for "dogs playing in the backyard" in an image set that only contains images of people, the system will return the closest thing to the search query. In this case, it could return images of people. This can also happen when querying abstract concepts that do not correspond to images, such as emotion and gender.

- **Stereotyping**: The model has learned to associate names with the stereotypical gender and ethnicity of people with those names and may associate private citizens' names with celebrity images.

- **Recency**: Our models have been trained on datasets that contain some information about real world events but if you query the models about events that took place after the models were trained, they will not perform well.

- **Deliberate misuse**: If highly disturbing images, paired with highly disturbing text are uploaded into Image Retrieval, it can return harmful and offensive content as part of the results. To mitigate this unintended result, we recommend that you control access to the system, and educate the people who will use it about appropriate use.

- **Understanding Motion**: Video summary and frame locator has a limited ability to accurately understand motion and actions in a video. When queried for actions like "a person taking a picture" or "a person falling," it may give inaccurate results.

- **Complex queries syntax**: Queries containing complex syntax such as prepositions, e.g., "a person _on_ a ladder" or "a person _with_ no ladder" might yield inaccurate results.

### Best practices for improving system performance

The following guidelines can help you understand and improve the performance of Azure Vision APIs:

- Image Analysis supports images that meet the file [requirements](/azure/ai-services/computer-vision/overview-image-analysis?tabs=3-2#image-requirements) for each version.
- Although Azure Vision is robust, factors like resolution, light exposure, contrast, and image quality might affect the accuracy of your results. Refer to the product specifications and test it on your images to validate the fit for your situation.
- Before a large-scale deployment or rollout of any Azure Vision system, system owners should conduct an evaluation phase in the context in which the system will be used and with the people who will interact with the system. Pre-deployment evaluation helps ensure system accuracy, and it will help you take actions to improve system accuracy, if applicable.
- Build a feedback channel for people who make decisions based on the system output. Include satisfaction data from the people who will be relying on your Azure Vision features and feedback from existing customer voice channels. Use feedback to fine-tune the system and improve accuracy.
- The AI provides a confidence score for each predicted output. A confidence score represents the accuracy of a prediction as a percentage. For example, you might set a minimum confidence threshold for a system to automatically caption a photo. If a generated caption's confidence score is below the threshold, it should be forwarded for further review.

## Evaluation of Image Analysis

### Evaluation methods

We use various public, internal, and customer-donated image datasets to evaluate the accuracy of each Azure Vision model. These image datasets contain images of a wide array of visual content and of a wide range of quality to make sure that the models are evaluated for a range of possible cases. We calculate precision, recall, and F1 scores for the different datasets. We compare each model against internal and public benchmarks and against earlier versions of the model.

### Fairness considerations

We have rigorously tested all our Azure Vision AI models for fairness to identify and prioritize demographic groups that might be at risk of experiencing worse quality of services and to identify instances in which our models might produce outputs that perpetuate existing stereotypes, demean, or erase certain groups of people. We have found that our models work well for all people who are depicted in image inputs regardless of their race, gender identity, age, and culture.

In some rare instances, image tagging, and image captioning models have made fairness errors by returning incorrect gender and age labels for people that appear in input images. These instances are very rare, and we continue to improve our models so that newer models are less likely to produce such errors. We recommend that customers don't use Azure Vision models for gender and age classifications.

We ask customers to report any fairness errors and to share their feedback on these issues through the [Azure portal](https://portal.azure.com/?feature.customportal=false#home) so that we can keep identifying areas of improvement as we seek to ensure that our models work well for everyone. Customers who train their own models using the Customization feature will need to perform additional testing to ensure fairness.

## Evaluating and integrating Image Analysis for your use

Microsoft works to help customers responsibly develop and deploy solutions that use Azure Vision in Foundry Tools. We're taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations are in line with our commitment to developing Responsible AI.

### General guidelines for integration and responsible use

This section discusses Azure Vision and key considerations for using this technology responsibly. The following are general recommendations for the responsible deployment and use of Azure Vision. Your context might require you to prioritize and include your own mitigations according to the needs of your specific deployment scenario. But in general, we provide the following best practices as a starting point to assist you.

- **Understand what it can do** : Fully assess the potential of any AI system you are using to understand its capabilities and limitations. Understand how it will perform in your scenario and context by thoroughly testing it with real-life conditions and data.
- **Respect an individual's right to privacy** : Collect data and information from individuals only for lawful and justifiable purposes. Use only the data and information that you have consent to use and use it only for the purposes for which consent was given.
- **Legal review**: Obtain appropriate independent legal advice to review your solution, particularly if you use it in sensitive or high-risk applications. Understand what restrictions you might need to work within, and understand your responsibility to resolve any issues that might come up in the future.
- **Human-in-the-loop**: Keep a human in the loop and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of Azure Vision and maintaining the role of humans in decision-making. Ensure that you can have real-time human intervention in the solution to prevent harm. This way, you can manage situations in which Azure Vision does not perform as expected.
- **Security**: Ensure that your solution is secure and that it has adequate controls to preserve the integrity of your content and prevent unauthorized access.
- **Have a blocklist or an allowlist**: Instead of enabling all tags with Azure Vision tag feature, focus on the specific ones that are most appropriate for your use case.
- **Structure user interactions by limiting specific inputs**: We recommend monitoring user text input for undesired content. This could include hate speech, racial or ethnic slurs, and profane words or phrases. The exact definition of undesired content will depend on your scenario and may change over time.
- **Control user access**: Consider requiring your customers and users to sign in, as this will make it easier for your business to respond to misuse incidents if they occur. If possible, consider placing the product behind a paywall, to make misuse more difficult.
- **Limit societal bias**: We recommend running tests for your specific use cases to limit societal biases.
- **Establish feedback and reporting channel for users**: We recommend creating channels to collect questions and concerns from users and bystanders affected by the system. Invite feedback on the usefulness and accuracy of outputs and give users a clear path to report problematic, offensive, biased, or inappropriate outputs. Possible mechanisms include building feedback features into the UI and publishing an email address for public feedback.

### Responsible AI Content Filtering

[Vision Studio](https://aka.ms/visionstudio) includes a content management system that works alongside core models to filter content for Image Retrieval and Video Summary and Frame Locator demos. This system works by running both the input prompt and media content through an ensemble of classification models aimed at detecting misuse. If the system identifies harmful content, you'll receive an error message that the prompt was deemed inappropriate and filtered by Responsible AI services.

You can report feedback on the content filtering system [through support](/azure/ai-services/cognitive-services-support-options).

To ensure you have properly mitigated risks in your application, you should evaluate all potential harms carefully, follow guidance in the [Transparency Note](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-transparency-note) and add scenario-specific mitigation as needed.

### Recommendations for preserving privacy

A successful privacy approach empowers individuals with information, and it provides controls and protection to preserve their privacy.

- If the service is part of a solution that is designed to incorporate health-related data, think carefully about whether and how to record that data. Follow applicable state and federal privacy and health regulations.
- Privacy managers should carefully consider what retention policies to use for extracted image metadata and insights, as well as for the underlying images. Retention policies should reflect the intended use of the applications.
- Don't share any data without explicit consent from affected stakeholders or data owners, and minimize the quantity of data that is shared.

## Customization in Image Analysis

The Image Analysis Customization feature has additional considerations to be aware of. Customization uses machine learning to analyze images. You submit images that both include and lack the characteristics in question. You label the images yourself. Then, the service trains the model using this data and calculates the model accuracy by testing a set of images from the training dataset. Once you've trained the model, you can test, retrain, and eventually use it in your image recognition application or solution to infer predictions on new images.

**Custom Image classification** applies one or more labels to an image. **Custom Object detection** returns the coordinates in the image where the applied label(s) can be found for detected objects. Both features are delivered through APIs, SDKs and no-code experience at Vision Studio at [https://portal.vision.cognitive.azure.com](https://portal.vision.cognitive.azure.com/).

Customization supports the creation and use of custom vision models through the following high-level functions. They represent the two core activities you will complete to prepare your model for use:

- **Data labeling**: is the process of annotating the training images with the classes of images that the model needs to classify. In the case of object detection, you annotate the training images with bounding boxes that surround the object to be detected in the image. Customers can label data in Azure Machine Labeling Studio or import labeled data in COCO file format. Once the training data is labeled, you can use it for training the model via Vision Studio, API or SDK.
- **Model training**: uses the base model and transfer learning to train a model that's optimized for customer-provided images and corresponding classes. With previous model customization technology, large amounts of training data were needed to achieve high accuracy. With the new model customization, less amount of data is required to train a model to learn to recognize and classify new data with same or higher accuracy/performance. Because these Customization features are using a large foundational model, trained with an extensive dataset, the model can be trained with as little as a single image per label. The model can continue to improve when trained with few images per label. Few-shot learning provides a path for customization without the need for extensive data collection and labeling. Customization provides accuracy metrics, to approximate model performance based on a split of the training data provided. When training few images per label, it is recommended to test the model accuracy with an additional evaluation dataset.

When you're ready to use your model, you can make a model prediction by sending an image for processing. Please note, when running prediction with custom models, you might experience longer than expected latency to receive prediction results. Microsoft is working on making latency improvements in the near future. It is not currently recommended to use custom models for business-critical environments. Please also note, the quality of your classifier or object detector model built with Customization depends on the quality and variety of the labeled data you provide when training the model. The quality also depends on how balanced the overall dataset is between classes. When satisfied with model quality, you can deploy and host the model in Cognitive Service for Vision.

> [!IMPORTANT]
> Please note, Customization is **not suitable for training custom models for large-scale sets of images that contain hundreds of classes and tags, for generating human-readable descriptions of images that can be used as alt text for accessibility purposes.** Image Analysis based models have these capabilities and should be used instead of Customization. Please note, Customization is also **not suitable for facial recognition** as it was not designed or tested to recognize or identify individuals in images.[Use Azure AI Face.](/azure/ai-services/computer-vision/overview-identity) Any recognition of an individual is the result of your labeling and not from our facial recognition capabilities or from the creation of a facial template (a unique set of numbers that are generated from an image that represents the distinctive features of a face).

### Use cases

#### Intended uses

You might use Customization, a feature of Azure Vision for the following scenarios:

- **Automated visual alerts**: The ability to monitor a video stream and have alerts triggered when certain circumstances are detected. For example, you might want an alert when there is steam detected, or foam on a river, or an animal is present.
- **Improved efficiency of manual inspection**: In retail, product recognition enables you to reduce the time you or associates spend counting unique SKUs or identifying whether all SKUs that should be on a shelf are present.
- **Expansion of inspection coverage**: When detecting defects, it's not always possible for a human to review all items coming off a manufacturing line. Instead, you can use Customization to cover the set of items you aren't able to inspect manually, as well as inform which items you do inspect manually.
- **Improve object discoverability**: Labeling your images with metadata can make them easier to find later. For example, you might tag the images based on your product catalog or other visual features that you're interested in filtering on. Customization allows you to label images with metadata at the time of ingestion.

### Customization feature performance

After you've trained your model, you can see the estimate of the project's performance in the Studio [https://portal.vision.cognitive.azure.com](https://portal.vision.cognitive.azure.com/). Customization uses a subset of the images that you submitted for training or user provided evaluation dataset to estimate average precision, mean average precision, accuracy- top 1 and accuracy-top 5. These three measurements of an image classifier and object detector's effectiveness are defined as follows:

_Average Precision_ is the percentage of identified classifications that were correct. For example, if the model identified 100 images as dogs, and 99 of them were actually dogs, then the precision is 99 percent.

_Mean average precision (mAP)_ is the average value of the average precision (AP). AP is the area under the precision/recall curve (precision plotted against recall for each prediction made).

- Mean Average Precision @ 30: Object detector performance across all the tags, when IoU is 30.
- Mean Average Precision @ 50: Object detector performance across all the tags, when IoU is 50.
- Mean Average Precision @ 75: Object detector performance across all the tags, when IoU is 75.

_Accuracy_ is one metric for evaluating classification models. Informally,  **accuracy**  is the fraction of predictions your model got right. Formally, accuracy has the following definition:

- _Accuracy – Top 1_ is the conventional accuracy, model prediction (the one with the highest probability) must be exactly the expected answer. It measures the proportion of examples for which the predicted label matches the single target label.
- _Accuracy – Top 5_ means any of our model's top 5 highest probability answers match the expected answer. It considers a classification correct if any of the five predictions matches the target label.

### Best practices to improve customization model accuracy

The process of building a Customization model is iterative. Each time you train your model, you create a new iteration/evaluation with its own updated performance metrics. You can view all your evaluations in the details of your project in Vision Studio. To improve the performance of the model, expand the variety of the labeled data you provide when training the model. The quality also depends on how balanced the overall dataset is between classes.

A model may learn to make predictions based on arbitrary characteristics that your images have in common. We suggest that you test the model for an evaluation with additional data. After testing the model, you can publish and use the model for inference.

Based on the model's performance, you need to decide if the model is appropriate for your use case and business needs. Here's an approach that you might take. You can deploy a Customization model in an isolated environment, test the performance of the model relative to your use case, and then use the predictions to further train the model until it reaches the level of performance you want.

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)
- [Microsoft Azure Learning courses on responsible AI](/learn/paths/responsible-ai-business-principles/)

## Learn more about Image Analysis

- [Image Analysis overview](/azure/ai-services/computer-vision/overview-image-analysis?tabs=3-2)
- [Image Analysis quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library?tabs=visual-studio%2C3-2&pivots=programming-language-rest-api)
- [Image Analysis on Vision Studio](https://portal.vision.cognitive.azure.com/gallery/imageanalysis)

## Next steps

* [Responsible deployment of Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-guidance-for-integration)
* [Image Analysis Overview](/azure/ai-services/computer-vision/overview-image-analysis)
* [QuickStart your Image Analysis use case development](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library)
* [Data, privacy, and security for Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security)
