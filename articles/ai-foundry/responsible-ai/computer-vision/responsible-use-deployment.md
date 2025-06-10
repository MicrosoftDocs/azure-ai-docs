---
title: Responsible use deployment for Azure AI Vision spatial analysis
titleSuffix: Azure AI services
description: This document details responsible use recommendations for an Azure AI Vision spatial analysis container deployment.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: article
ms.date: 08/15/2022
---

# Responsible use in AI deployment for Azure AI Vision spatial analysis

As Microsoft works to help customers safely develop and deploy solutions using Azure AI Vision spatial analysis, we are taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability & safety, privacy & security, inclusiveness, transparency, and human accountability.

The following recommendations have been developed together with private preview customers to guide the responsible deployment and use of spatial analysis. While these recommendations may be broadly applicable, they have been validated in the context of public health and safety uses for responding to COVID-19. We are providing these as a useful guide, while recognizing each customer context is different, so the prioritization and application of these recommendations should be based around the specific deployment scenarios and context of spatial analysis use.

## Definitions

Throughout this document, we use the following terms:

- **Customer** - Refers to the entity that is purchasing the technology from Microsoft.
- **Deployer** - Refers to the individual and organization involved in the creation and implementation of software using Azure AI services.
- **Operator** - Refers to the individual that will be using the video insights to manage the public health and safety of buildings and/or businesses.
- **Affected stakeholders** - Refers to the individuals who will be subject to spatial analysis. This could be a tenant in a building, a shopper in a store, or the public at large.

## Key questions

Based on [research insights](#research-insights) and an impact assessment conducted on the social distancing scenarios, Microsoft identified the following key questions that deployers, operators, and affected stakeholders are likely to confront as they aim to harness the spatial analysis for the public health and safety of buildings and businesses.

- **Privacy:** How might we maximize personal privacy while improving building health & safety?
- **Disclosure:** How might we balance transparency and information overload to promote trust and peace of mind for people in a monitored space?
- **Human oversight for operators:** How might we design human-AI collaboration to leverage the insights and ingenuity of people to make the most of spatial analysis core skills?

## Research insights

We conducted research studies, referenced in [Research insights](research-insights.md), to investigate the perception of "intelligence-enabled" cameras in public and commercial spaces. While the application of "intelligence-enabled" cameras is still new, the use of video surveillance in public and commercial spaces has been around for a considerable amount of time. The following are the top insights from those studies regarding public perception of video surveillance cameras.

- **Concerns with workplace employee monitoring** - Recent external research shows that many people care about what organizations and employers are doing to ensure public safety with respect to COVID-19. ([1](https://news.gallup.com/poll/312461/amid-slow-return-workplaces-covid-precautions-abound.aspx), [2](https://www.gallup.com/workplace/313358/covid-continues-employees-feeling-less-prepared.aspx), [3](https://www.webershandwick.com/news/employee-perceptions-on-returning-to-work/)) However, there is also research that shows people have less trust when the technology is used in a workplace environment for monitoring purposes. The recommendations below provide considerations for addressing this tension. ([6](https://www.pewresearch.org/internet/2019/09/05/more-than-half-of-u-s-adults-trust-law-enforcement-to-use-facial-recognition-responsibly/), [7](https://www.adalovelaceinstitute.org/wp-content/uploads/2019/09/Public-attitudes-to-facial-recognition-technology_v.FINAL_.pdf), [8](https://www.pewresearch.org/internet/2014/11/12/public-privacy-perceptions/))
- **Risk-benefit comparison** - For COVID-19 scenarios, it is important to communicate the benefits of public health and safety. ([2](https://www.gallup.com/workplace/313358/covid-continues-employees-feeling-less-prepared.aspx), [3](https://www.webershandwick.com/news/employee-perceptions-on-returning-to-work/)) Public polling shows that many are willing to make economic sacrifices in order to save lives ([9](https://cic.nyu.edu/sites/default/files/public-opinion-trust-and-covid19.pdf)), and place high importance on having safety conditions met before returning to normal activities. ([10](https://news.gallup.com/poll/310247/targeted-quarantines-top-u-s-adults-conditions-normalcy.aspx)) However, trust in surveillance technology depends on perceived benefits. For example, there is generally trust in the use of surveillance technologies for building access as there is a clear perceived benefit.
- **Trust in technology varies across demographic groups** - Careful considerations for marginalized groups should be taken when deploying technology. Some demographic groups have less trust in technology based on societal inequities and cultural norms. For example, systematically marginalized groups often alter their behavior out of fear or intimidation when under surveillance. ([14](https://policyreview.info/articles/analysis/internet-surveillance-regulation-and-chilling-effects-online-comparative-case))

Read more about these and additional insights in the [research insights article](research-insights.md).

## Recommendations for customers and deployers

These recommendations are founded in the research insights and impact assessment conducted with building health and safety scenarios that our customers identified during their initial deployment. The recommendations are organized based around the key risks of harm identified during our impact assessment process including privacy, transparency through disclosure, and accountability through effective human decision-making.

## Application pre-development recommendations

We recommend developers start by conducting an impact assessment to understand the intended use, context, and unintended or high-risk uses to avoid. The impact assessment process will provide customers and deployers with the basis to prioritize the recommendations below.

| **RECOMMENDATIONS** |
|---------------------|
| Evaluate the benefits of short-term versus potential harms of long-term data collection by conducting an impact assessment of the system. One key factor of impact assessments is to understand the potential for harms. One approach for that is [harms modeling](/azure/architecture/guide/responsible-innovation/harms-modeling/) |
| Obtain feedback from a diverse sampling of the community during the development and evaluation process (e.g., historically marginalized groups, people with disabilities, service workers). One approach to obtaining feedback from diverse perspectives is through a [Community Jury](/azure/architecture/guide/responsible-innovation/community-jury/) |
| Establish feedback channels to collect questions and concerns from affected stakeholders. For example, feedback features built into app experiences, an easy-to-remember email address for feedback, anonymous feedback boxes placed in semi-private spaces, knowledgeable representatives in the lobby.|

## Recommendations for preserving privacy

Special consideration is required when using Spatial Analysis for public health and safety amidst a pandemic. In April 2020, [Microsoft outlined 7 principles for preserving privacy](https://blogs.microsoft.com/on-the-issues/2020/04/20/privacy-covid-19-data-collection/) while addressing the challenges of responding to COVID-19. We recommend reviewing the [article explaining these principles](https://blogs.microsoft.com/on-the-issues/2020/04/20/privacy-covid-19-data-collection/) before you review the following recommendations. **A successful privacy approach empowers individuals with information and provides controls and protection to preserve their privacy.** Spatial Analysis collects data about individuals without identifying them. Even so, is  important to follow standard best practices including minimizing data collection, secure and protect data, and empower people with  information that explains how their data will be collected and used.

| **RECOMMENDATIONS** |
|---------------------|
| If the service is part of a solution designed to incorporate health related data, then think carefully about whether and how to record that data and follow applicable privacy and health state and federal regulations. |
| When considering how to minimize data collection be sure to think about protecting individual's privacy by avoiding unintentional collection of identifiable information.<br/><br/>Evaluate camera locations and positions, adjusting angles and region of interests so they do not overlook protected areas such as bathrooms, or public spaces such as external streets or mall concourses.<br/><br/>Spatial analysis is designed to operate by identifying and placing bounding boxes around humans and developing aggregated analytics related to the same. It is not intended for individual identification. However, individuals could potentially be identified if secondary data is collected and associated with spatial analysis insights. For example, location data associated with an individual's office or desk could be overlayed with building occupancy data to unintentionally produce identifiable information.<br/><br/>It is the customers responsibility to follow legal and regulatory requirements regarding notice, disclosure and consent based on the data being collected and processed. |
| When planning your data storage, design automatic data retention plans per your policy requirements, which stores data for the shortest amount of time necessary to derive insights, and consider deleting raw data as soon as possible. |
| Provide appropriate safeguards to secure the data. Design the system to maintain encryption and de-identification end-to-end to protect data from harmful exposure and hacking attempts. |
| Minimize data sharing. If data must be shared, consider potential negative impacts and plan effective strategies to mitigate them. |

## Disclosure recommendations

Our research indicates that people have underlying concerns regarding the person data being collected from existing CCTV cameras, and that people will not automatically understand how AI technology functions or what data is being utilized. **A successful disclosure experience is one that helps proactively address the needs and concerns of affected stakeholders and puts them in a position to get the most benefit possible from the system, as well as meeting the requirements of regulators.** When designing experiences that integrate spatial analysis it is important to disclose information about the system in a way that makes people feel informed and empowered.

| **RECOMMENDATIONS** |
|---------------------|
| Be transparent with affected stakeholders, such as employees, visitors, and bystanders, about how their data is being handled. Review the [disclosure design guidance article](disclosure-design.md) to determine what and how information should be disclosed, which could include:<br/><br/>1.  The data that is collected and processed.<br/><br/>2.  The method of data collection and processing.<br/><br/>3.  The purpose of data collection and processing.<br/><br/>4.  The benefits to affected stakeholders.<br/><br/>5.  The people or groups that have access to the data.<br/><br/>6.  The reasons people have access to the data, if applicable.<br/><br/>7.  The existence of automated decision-making using the data, and meaningful information about the logic involved.<br/><br/>8.  The retention duration of the data (including if durations are different for distinct purposes or groups).<br/><br/>9.  Who the stakeholder can complain or give feedback.<br/><br/>10. Privacy & security protection measures. |
| Disclosures should be easily accessible for all affected stakeholders. See the [disclosure design guidance article](disclosure-design.md) for further recommendations on when and how to disclose information.<br/><br/>Leverage multiple touchpoints - including digital (e.g., emails, websites, mobile apps) and physical (e.g., signage, front-desk receptionists, Q&A sessions) - to reach people where they are most likely to discover and appreciate the information. |
| Evaluate the onboarding and continuous-use experience with a representative sample of the community to validate that the design choices lead to effective disclosure. See the [disclosure design guidance article](disclosure-design.md) for approaches to build trust with affected stakeholders. |

Read more information in the [disclosure design guidance article](disclosure-design.md).

## Effective human decision-making recommendations

When designing in support of human decision-making, systems need to convey multiple types of information to help raise operators' awareness of important details, understand how those details affect the situation, and take appropriate action. In addition, designing experiences with AI can be inherently complex because, by definition, they perform with variable reliability (probabilistic logic). Therefore, **a successful experience is one that guides operators to make more informed decisions while preventing them from over-relying on the outputs of the AI.**

The recommendations outlined below provide general guidance for supporting effective human decision-making.

| **RECOMMENDATIONS** |
|---------------------|
| Help operators (e.g. building operators, store managers) develop an accurate understanding of the probabilistic AI system. Make sure people are clear about what the observational data represents, where it comes from, how reliable the outcome is, and what actions they should and shouldn't take based on these measures. |
| Work backwards from expected jobs-to-be-done (i.e., tasks or goals of the operator) to identify the optimal metrics and the right granularity level of data to display. Only present the minimum viable data to avoid unintentional revelation of personal information. |
| Surface comparative measures to operators to enhance their ability to understand metrics in context (e.g. averages, highs, lows, time periods of measurement). |
| Evaluate common scenarios/tasks with a representative sample of the community to validate that the design choices lead to accurate situational understanding and good decision-making. |
| Implement an easy to access feedback channel for operators and affected stakeholders to raise concerns and report system failures. |
| Conduct regular performance evaluations of the Spatial Analysis core skills in production environments. Additionally, establish system performance thresholds for effective human decision-making which have been validated through user research. |

## Next steps

> [!div class="nextstepaction"]
> [Disclosure design guidelines for spatial analysis](/azure/ai-foundry/responsible-ai/computer-vision/disclosure-design?context=%2fazure%2fcognitive-services%2fComputer-vision%2fcontext%2fcontext)
