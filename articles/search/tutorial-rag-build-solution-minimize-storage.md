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

# Tutorial: Minimize storage and costs using vector compression and narrow data types (RAG in Azure AI Search)

In this tutorial, learn the techniques for reducing index size, with a focus on vector compression and storage. 

Key points:

- scalar
- stored false, retrievable false
- filterable, sortable false for non-vector
- narrow data types
- hnsw vs eknn, does hnsw product a smaller footprint?

<!-- ps 1: We have another physical resource limit for our services: vector index size. HNSW requires vector indices to reside entirely in memory. "Vector index size" is our customer-facing resource limit that governs the memory consumed by their vector data. (and this is a big reason why the beefiest VMs have 512 GB of RAM). Increasing partitions also increases the amount of vector quota for customers as well.  -->

## Next step

> [!div class="nextstepaction"]
> [Deploy and secure an app](tutorial-rag-build-solution-app.md)