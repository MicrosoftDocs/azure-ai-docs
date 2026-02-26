---
title: Guidance for integration and responsible use with optical character recognition (OCR) - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Guidance for how to deploy OCR responsibly, based on the knowledge and understanding from the team that created this product.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: best-practice
ms.date: 10/15/2025
---

# Guidance for integration and responsible use with OCR technology

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

As Microsoft works to help customers responsibly develop and deploy solutions using Azure Vision in Foundry Tools Read optical character recognition (OCR) capabilities, we're taking a principled approach to upholding personal agency and dignity. Microsoft is considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations are in line with our commitment to developing responsible AI.

This article discusses OCR and the key considerations for making use of this technology responsibly. Consider the following factors when you decide how to use and implement AI-powered products and features:

- Will this product or feature perform well in my scenario? Before you deploy AI into your scenario, test how it performs by using real-life data and make sure it can deliver the accuracy you need.
- Are we equipped to identify and respond to errors? AI-powered products and features won't be 100% accurate, so consider how you will identify and respond to any errors that might occur.

## General guidelines for integration and responsible use

When you prepare to integrate and responsibly use the OCR features, the following activities help to set you up for success.

**Understand what it can do**: Fully vet and review the capabilities of any AI model you're using to understand its capabilities and limitations. Understand how it will perform in your particular scenario by thoroughly testing it with real-life conditions and data. Synthetic data and tests that don't reflect your end-to-end scenario won't be sufficient.

**Respect an individual's right to privacy**: Only collect images and documents from individuals for lawful and justifiable purposes. Only use the images and documents that you have consent to use for this purpose.

**Legal review**: Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and your responsibility to resolve any issues that might come up in the future.

**Human-in-the-loop**: Keep a human-in-the-loop and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of the AI-powered OCR and maintaining the role of humans in decision-making. Ensure you can have real-time human intervention in the solution to prevent harm. Human oversight enables you to manage where the OCR model doesn't perform as required.

**Security**: Ensure your solution is secure and has adequate controls to preserve the integrity of your content and prevent any unauthorized access.

## Recommendations for preserving privacy

A successful privacy approach empowers individuals with information and provides controls and protection to preserve their privacy.

- If the service is part of a solution designed to incorporate personally identifiable information (PII), then think carefully about whether and how to record that data. Follow applicable national and regional regulations concerning privacy.

- Privacy managers should consider the retention policies on the extracted text and the underlying documents or images of those documents. The retention policies will be tied to the intended use of each application.
