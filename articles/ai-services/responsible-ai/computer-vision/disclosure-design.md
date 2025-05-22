---
title: Disclosure design guidelines for Azure AI Vision spatial analysis
titleSuffix: Azure AI services
description: This document details disclosure design guidelines for an Azure AI Vision spatial analysis container deployment.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: article
ms.date: 08/15/2022
---

# Disclosure design guidelines for Azure AI Vision spatial analysis

This document outlines helpful tips and guidance to facilitate responsible and ethical use of the Azure AI Vision spatial analysis service.

## Background

When designing experiences that integrate spatial analysis, it is important to disclose information about the system in a way that makes people feel informed and empowered. Considering the diversity of implementation approaches, scenarios, and affected stakeholders, such as employees, visitors, and bystanders, we can't assume that people will automatically understand how the technology functions or what data is being utilized. For example, the presence of video cameras may lead people to question why their personal data is being collected, stored, shared. A successful disclosure experience is one that helps proactively address the needs and concerns of affected stakeholders and puts them in a position to get the most benefit possible from the system, as well as meeting the requirements of regulators. Disclosure is effective under the following conditions: 

- **Awareness** - People have no doubt about when their data is being collected.

- **Understanding** - People are able to accurately describe in their own words how the solution works, what data it requires, and how that data is used for individual and collective benefit.  

## Design considerations

## 1. Determine WHAT information needs to be disclosed

Begin by having the customer and deployer review each use case, documenting the following information on a spreadsheet:

- The data that is collected or processed.
- The method of data collection and processing.
- The purpose of data collection and processing.
- The benefits to affected stakeholders.
- The people or groups that have access to the data.
- The reasons people have access to the data, if applicable.
- The existence of automated decision-making using the data, and meaningful information about the logic involved.
- The retention duration of the data (including if durations are different for distinct purposes or groups).
- Who the stakeholder can complain or give feedback.
- Privacy protection measures.

In addition, gather the following information about affected stakeholders when needed:

- Common concerns and perceptions regarding data privacy.
- Common level of knowledge about how the technology works.
- How concerns, perceptions, and technical knowledge may impact the ability to understand data handling practices.

For each disclosure touchpoint, focus on the comprehension points that are the most relevant to people at the moment of their interaction with the system (e.g. signage near the building entrance should provide an overview of the system, while signage pointing at a camera should specify what data that camera is collecting.) In addition, make sure to always provide an alternate channel for people to learn more (e.g. an FAQ webpage).

- Set up routine audits to make sure the disclosure content is up to date.

## 2. Determine WHEN and HOW to disclose the information

In order to provide affected stakeholders with sufficient disclosure, consider leveraging multiple surface areas to create useful redundancy and accommodate the needs of different groups of people. Proposed ideas: 

**Upfront disclosure:** Explain how data is handled when people first interact with your system. Example touchpoints: rollout emails, onboarding walkthroughs (mobile app), signage at the building's entrance.

:::image type="content" source="media/spatial-analysis/upfront-disclosure.png" alt-text="A screenshot of an example of providing up front disclosure in a mobile app.":::

**On-demand disclosure**: Host all your disclosure content in a centralized information hub that is easy to access for all affected stakeholders. Example touchpoints: FAQ webpage, privacy dashboard (mobile app).

:::image type="content" source="media/spatial-analysis/on-demand-disclosure.png" alt-text="A screenshot of an example of an on-demand disclosure in a mobile app.":::

**Just-in-time disclosure**: Identify moments in the user journey where people might have questions or concerns regarding data privacy. Anticipate the types of questions that affected stakeholders are likely to have and proactively address their concerns. Example touchpoints: data dashboards, data reports, registration form for visitors, signage pointing at a camera or a sensor.  

:::image type="content" source="media/spatial-analysis/just-in-time-disclosure-cellphone.png" alt-text="A screenshot of an example of just-in-time disclosure in a mobile app.":::

:::image type="content" source="media/spatial-analysis/just-in-time-disclosure-dashboard.png" alt-text="A screenshot of an example of just-in-time disclosure in a dashboard app.":::

## 3. How to build trust with affected stakeholders

- Clearly communicate the expected benefits and potential risks to affected stakeholders.

- Help people understand why the data is needed and how the use of the data will lead to their benefit.

- Describe data handling in an understandable way. Be specific and accurate. Avoid generic descriptions, jargon, and technical terminology.

- Demonstrate good data security practices to affected stakeholders.

- Receptionists and other building staff serve as important touchpoint for disclosure. Consider providing regular training to those roles to keep them informed about system updates.  

- Consider establishing feedback channels to collect questions and concerns from affected stakeholders. 

- Consider providing additional venues and support for people who require more assistance to access the disclosure information.
  - When applicable, provide bilingual or multi-lingual disclosures for people with limited official language proficiency.
  - Follow accessibility standards when designing digital disclosure touchpoints to accommodate people with visual impairments.
  - When placing physical signage, consider ways in which people with mobility or visual impairments could also access the same information.

## How to assess effectiveness of disclosure

Evaluate the first and continuous-use experience with a representative sample of the community to validate that the design choices lead to effective disclosure. Conduct user research with 10-20 community members (affected stakeholders) to evaluate their comprehension of the information and to determine if their expectations are met.

- Recruit representative volunteers across diverse characteristics (e.g., age, ethnicity, gender, job role, level of privacy concerns).

- Obtain participation consent and consider providing fair compensation in return.

- Conduct a cognitive walkthrough (or request that they complete a general on-boarding task) using the functional or prototyped experience, asking the volunteers think-aloud as they complete general tasks.

- Following the walkthrough, ask probing questions to determine their level of awareness with key pieces of information, their understanding of specific elements, and general satisfaction with the experience.

- Summarize key challenges and update the experience as applicable.

## Next steps

> [!div class="nextstepaction"]
> [Research insights for spatial analysis](/legal/cognitive-services/computer-vision/research-insights?context=%2fazure%2fcognitive-services%2fComputer-vision%2fcontext%2fcontext)
