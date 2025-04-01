---
title: Share Responsible AI insights and make data-driven decisions with Azure Machine Learning Responsible AI scorecard
titleSuffix: Azure Machine Learning
description: Learn about how to use the Responsible AI scorecard to share responsible AI insights from your machine learning models and make data-driven decisions with non-technical and technical stakeholders.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.topic:  conceptual
ms.author: lagayhar
author: lgayhardt
ms.reviewer: mesameki
ms.date: 03/31/2025
ms.custom: responsible-ml, build-2023, build-2023-dataai
---

# Share Responsible AI insights using the Responsible AI scorecard (preview)

Our Responsible AI dashboard is designed for machine learning professionals and data scientists to explore and evaluate model insights and inform their data-driven decisions. While it can help you implement Responsible AI practically in your machine learning lifecycle, there are some needs left unaddressed:

- Bridging the gap between the technical Responsible AI tools (designed for machine learning professionals) and the ethical, regulatory, and business requirements that define the production environment.
- Facilitating effective multi-stakeholder alignment in an end-to-end machine learning lifecycle, ensuring technical experts receive timely feedback and direction from nontechnical stakeholders.
- Ensuring the ability to share model and data insights with auditors and risk officers for auditability purposes, as required by AI regulations.

One of the biggest benefits of using the Azure Machine Learning ecosystem is the ability to archive model and data insights in the Azure Machine Learning Run History for quick reference in the future. As part of this infrastructure, and to complement machine learning models and their corresponding Responsible AI dashboards, we introduce the Responsible AI scorecard. This scorecard empowers machine learning professionals to easily generate and share their data and model health records.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Who should use a Responsible AI scorecard?

- If you're a data scientist or a machine learning professional, after training your model and generating its corresponding Responsible AI dashboard for assessment and decision-making purposes, you can extract those learnings via our PDF scorecard and share the report easily with your technical and non-technical stakeholders to build trust and gain their approval for deployment.  

- If you're a product manager, business leader, or an accountable stakeholder on an AI product, you can pass your desired model performance and fairness target values such as your target accuracy, target error rate, etc., to your data science team, asking them to generate this scorecard with respect to your identified target values and whether your model meets them. That can provide guidance into whether the model should be deployed or further improved.

## Next steps

- Learn how to generate the Responsible AI dashboard and scorecard via [CLI and SDK](how-to-responsible-ai-insights-sdk-cli.md) or [Azure Machine Learning studio UI](how-to-responsible-ai-insights-ui.md).
- Learn more about how the Responsible AI dashboard and scorecard in this [tech community blog post](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/responsible-ai-dashboard-and-scorecard-in-azure-machine-learning/ba-p/3391068).
