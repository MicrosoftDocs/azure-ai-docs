---
title: Content provenance
titleSuffix: Azure AI services
description: Content provenance 
author: ssalgadodev
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 07/30/2026
ms.author: ssalgado
ai-usage: ai-assisted
---

# Content provenance for Foundry models

Provenance is information that helps identify where content came from and whether it was modified.

For example, provenance information can indicate:

- Which application generated a piece of content.
- Which AI model was used.
- When the content was created.
- Whether the content was edited after creation.
- Whether the content contains supported authenticity signals.

Provenance information doesn't determine whether content is true, accurate, harmful, or trustworthy. Instead, it provides origin signals that applications can use as part of their own content evaluation and transparency experiences.

Microsoft systems use two complementary signals to indicate provenance:

- [C2PA manifests](#c2pa-manifests).
- [Invisible watermarks](#invisible-watermarks).

## C2PA manifests

The [Coalition for Content Provenance and Authenticity](https://c2pa.org) (C2PA) standard defines a cryptographically signed metadata format that you embed into files. Microsoft applications create and sign C2PA manifests, which can contain information about:

Microsoft systems create and sign C2PA manifests, which can contain

- The content creator.
- Generation tools.
- Creation timestamps.

## Invisible watermarks

Microsoft embeds invisible watermarking signals into generated content from supported systems. These signals aren't detectable visually or audibly, but you can verify them by using [Microsoft's provenance detection capabilities](https://ai.azure.com/nextgen/validate).

## Multimodal model support

Microsoft Foundry is expanding content provenance disclosures across supported generative models. For the model listed in the following table, generated output can include an invisible watermark and cryptographically signed C2PA Content Credentials, which help customers identify AI-generated content.

| Modality | Model family | Models |
| --- | --- | --- |
| Image | Azure OpenAI GPT Image | gpt-image-1-mini<br>gpt-image-1.5<br>gpt-image-2 |
| Image | Microsoft AI Image | MAI-Image-2.5<br>MAI-Image-2.5-Flash<br>MAI-Image-2e<br>MAI-Image-2.5-Pro |
| Image | Black Forest Labs Flux| Flux-1.1-Pro<br>Flux.1-Kontext-pro<br>Flux.2-flex<br>Flux.2-Pro |
