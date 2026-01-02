---
title: Guidance for integration and responsible use with optical character recognition (OCR) - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Guidance for how to deploy OCR responsibly, based on the knowledge and understanding from the team that created this product.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: article
ms.date: 10/15/2025
---

# Guidance for integration and responsible use with OCR technology

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

As Microsoft works to help customers responsibly develop and deploy solutions using Azure Vision in Foundry Tools Read optical character recognition (OCR) capabilities, we're taking a principled approach to upholding personal agency and dignity. Microsoft is considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations are in line with our commitment to developing responsible AI.

This article discusses OCR and the key considerations for making use of this technology responsibly. Consider the following factors when you decide how to use and implement AI-powered products and features:

- Will this product or feature perform well in my scenario? Before deployment, test OCR performance using representative, real‑world samples (for example, hundreds to thousands of documents matching your production formats) and verify that accuracy metrics such as character or word recognition rates meet your defined acceptance thresholds.
<!-- Comment: Updated to provide concrete testing guidance, including sample size and measurable accuracy thresholds, per agent feedback. -->
- Are we equipped to identify and respond to errors? Because OCR outputs are probabilistic, define explicit error‑handling workflows (for example, confidence‑score thresholds that trigger human review, logging of misrecognitions, and user correction paths).
<!-- Comment: Revised to make error-handling expectations actionable with specific workflow examples, per agent feedback. -->

## General guidelines for integration and responsible use

When you prepare to integrate and responsibly use the OCR features, the following activities help to set you up for success.

**Understand what it can do**: Fully vet and review the capabilities of any AI model you're using to understand its capabilities and limitations. Understand how it will perform in your particular scenario by testing with production‑like images and documents (for example, scanned forms, mobile photos, or low‑resolution images) and by measuring accuracy across relevant languages, fonts, and layouts. Synthetic data and tests that don't reflect your end-to-end scenario won't be sufficient.
<!-- Comment: Tightened guidance with concrete testing criteria, including data types and accuracy dimensions, per agent feedback. -->

**Respect an individual's right to privacy**: Only collect images and documents from individuals for lawful and justifiable purposes. Only use the images and documents that you have consent to use for this purpose.

**Legal review**: Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and your responsibility to resolve any issues that might come up in the future.

**Human-in-the-loop**: Keep a human-in-the-loop and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of the AI-powered OCR and maintaining the role of humans in decision-making. Ensure you can have real-time human intervention in the solution to prevent harm. Human oversight enables you to manage where the OCR model doesn't perform as required.

**Security**: Ensure your solution is secure and has adequate controls to preserve the integrity of your content and prevent any unauthorized access.

## Recommendations for preserving privacy

A successful privacy approach empowers individuals with information and provides controls and protection to preserve their privacy.

- If the service is part of a solution designed to incorporate personally identifiable information (PII), then think carefully about whether and how to record that data. Follow applicable national and regional regulations concerning privacy.

- Privacy managers should define explicit retention policies for extracted text and source images (for example, delete transient OCR outputs after processing or retain them only for a fixed business period such as 30–90 days), aligned to the intended use of each application.
<!-- Comment: Added specific, actionable retention examples to clarify privacy and data lifecycle expectations, per agent feedback. -->