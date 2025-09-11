---
title: Share Responsible AI insights and make data-driven decisions with Azure Machine Learning Responsible AI scorecard
titleSuffix: Azure Machine Learning
description: Learn about how to use the Responsible AI scorecard to share responsible AI insights from your machine learning models and make data-driven decisions with nontechnical and technical stakeholders.
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

- The gap between the technical Responsible AI tools (designed for machine learning professionals) and the ethical, regulatory, and business requirements that define the production environment.
- The need for effective multi-stakeholder alignment in an end-to-end machine learning lifecycle, ensuring technical experts receive timely feedback and direction from nontechnical stakeholders.
- The ability to share model and data insights with auditors and risk officers for auditability purposes, as required by AI regulations.

One of the biggest benefits of using the Azure Machine Learning ecosystem is the ability to archive model and data insights in the Azure Machine Learning Run History for quick reference in the future. As part of this infrastructure, and to complement machine learning models and their corresponding Responsible AI dashboards, we introduce the Responsible AI scorecard. This scorecard empowers machine learning professionals to easily generate and share their data and model health records.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Who should use a Responsible AI scorecard?

- **Data scientists and machine learning professionals**: After training your model and generating its corresponding Responsible AI dashboard for assessment and decision-making purposes, you can extract those learnings via our PDF scorecard. This allows you to easily share the report with your technical and nontechnical stakeholders, building trust and gaining their approval for deployment.
- **Product managers, business leaders, and accountable stakeholders on an AI product**: You can provide your desired model performance and fairness target values, such as target accuracy and target error rate, to your data science team. They can then generate the scorecard based on these target values to determine whether the model meets them. This helps guide decisions on whether the model should be deployed or further improved.

## Next steps

- Learn how to generate the Responsible AI dashboard and scorecard via [CLI and SDK](how-to-responsible-ai-insights-sdk-cli.md) or [Azure Machine Learning studio UI](how-to-responsible-ai-insights-ui.md).
- Learn more about how the Responsible AI dashboard and scorecard in this [tech community blog post](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/responsible-ai-dashboard-and-scorecard-in-azure-machine-learning/ba-p/3391068).
