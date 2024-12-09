---
title: Multimodal embeddings concepts - Image Analysis 4.0
titleSuffix: Azure AI services
description: Learn about concepts related to image vectorization and search/retrieval using the Image Analysis 4.0 API.
#services: cognitive-services
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: conceptual
ms.date: 09/25/2024
ms.author: pafarley
---

# Multimodal embeddings (version 4.0)

Multimodal embedding is the process of generating a vector representation of an image that captures its features and characteristics. These vectors encode the content and context of an image in a way that is compatible with text search over the same vector space.

Image retrieval systems have traditionally used features extracted from the images, such as content labels, tags, and image descriptors, to compare images and rank them by similarity. However, vector similarity search offers a number of benefits over traditional keyword-based search and is becoming a vital component in popular content search services.

## Differences between vector search and keyword search

Keyword search is the most basic and traditional method of information retrieval. In that approach, the search engine looks for the exact match of the keywords or phrases entered by the user in the search query and compares it with the labels and tags provided for the images. The search engine then returns images that contain those exact keywords as content tags and image labels. Keyword search relies heavily on the user's ability to use relevant and specific search terms.

Vector search searches large collections of vectors in high-dimensional space to find vectors that are similar to a given query. Vector search looks for semantic similarities by capturing the context and meaning of the search query. This approach is often more efficient than traditional image retrieval techniques, as it can reduce search space and improve the accuracy of the results.

## Business applications

Multimodal embedding has a variety of applications in different fields, including: 

- **Digital asset management**: Multimodal embedding can be used to manage large collections of digital images, such as in museums, archives, or online galleries. Users can search for images based on visual features and retrieve the images that match their criteria.
- **Security and surveillance**: Vectorization can be used in security and surveillance systems to search for images based on specific features or patterns, such as in, people & object tracking, or threat detection. 
- **Forensic image retrieval**: Vectorization can be used in forensic investigations to search for images based on their visual content or metadata, such as in cases of cyber-crime.
- **E-commerce**: Vectorization can be used in online shopping applications to search for similar products based on their features or descriptions or provide recommendations based on previous purchases.
- **Fashion and design**: Vectorization can be used in fashion and design to search for images based on their visual features, such as color, pattern, or texture. This can help designers or retailers to identify similar products or trends.

> [!CAUTION]
> Multimodal embedding is not designed analyze medical images for diagnostic features or disease patterns. Please do not use Multimodal embedding for medical purposes.

## What are vector embeddings? 

Vector embeddings are a way of representing content&mdash;text or images&mdash;as vectors of real numbers in a high-dimensional space. Vector embeddings are often learned from large amounts of textual and visual data using machine learning algorithms, such as neural networks. 

Each dimension of the vector corresponds to a different feature or attribute of the content, such as its semantic meaning, syntactic role, or context in which it commonly appears. In Azure AI Vision, image and text vector embeddings have 1024 dimensions.

> [!IMPORTANT]
> Vector embeddings can only be compared and matched if they're from the same model type. Images vectorized by one model won't be searchable through a different model. The latest Image Analysis API offers two models, version `2023-04-15` which supports text search in many languages, and the legacy `2022-04-11` model which supports only English.

## How does it work? 

The following are the main steps of the image retrieval process using Multimodal embeddings.

:::image type="content" source="media/image-retrieval.png" alt-text="Diagram of the multimodal embedding / image retrieval process.":::

1. Vectorize Images and Text: the Multimodal embeddings APIs, **VectorizeImage** and **VectorizeText**, can be used to extract feature vectors out of an image or text respectively. The APIs return a single feature vector representing the entire input.
   > [!NOTE]
   > Multimodal embedding does not do any biometric processing of human faces. For face detection and identification, see the [Azure AI Face service](./overview-identity.md).
1. Measure similarity: Vector search systems typically use distance metrics, such as cosine distance or Euclidean distance, to compare vectors and rank them by similarity. The [Vision studio](https://portal.vision.cognitive.azure.com/) demo uses [cosine distance](./how-to/image-retrieval.md#calculate-vector-similarity) to measure similarity.  
1. Retrieve Images: Use the top _N_ vectors similar to the search query and retrieve images corresponding to those vectors from your photo library to  provide as the final result.

### Relevance score 

The image and video retrieval services return a field called "relevance." The term "relevance" denotes a measure of similarity between a query and image or video frame embeddings. The relevance score is composed of two parts:
1. The cosine similarity (that falls in the range of [0,1]) between the query and image or video frame embeddings.
1. A metadata score, which reflects the similarity between the query and the metadata associated with the image or video frame.

> [!IMPORTANT]
> The relevance score is a good measure to rank results such as images or video frames with respect to a single query. However, the relevance score cannot be accurately compared across queries. Therefore, it's not possible to easily map the relevance score to a confidence level. It's also not possible to trivially create a threshold algorithm to eliminate irrelevant results based solely on the relevance score. 

## Input requirements

**Image input**
- The file size of the image must be less than 20 megabytes (MB)
- The dimensions of the image must be greater than 10 x 10 pixels and less than 16,000 x 16,000 pixels

**Text input**
- The text string must be between (inclusive) one word and 70 words.

## Next steps

Enable Multimodal embeddings for your search service and follow the steps to generate vector embeddings for text and images.  
* [Call the Multimodal embeddings APIs](./how-to/image-retrieval.md)

