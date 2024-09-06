---
title: 'RAG Tutorial: Minimize storage and costs'
titleSuffix: Azure AI Search
description: Compress vectors using binary or scalar quantization, remove copies of stored vectors.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Minimize storage and costs using vector compression and narrow data types (RAG tutorial - Azure AI Search)

In this tutorial, learn the techniques for reducing index size, with a focus on vector compression and storage. 

Key points:

- scalar
- stored false, retrievable false
- filterable, sortable false for non-vector
- narrow data types
- hnsw vs eknn, does hnsw product a smaller footprint?

## Next step

> [!div class="nextstepaction"]
> [Deploy and secure an app](tutorial-rag-build-solution-app.md)