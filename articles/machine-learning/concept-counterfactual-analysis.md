---
title: Counterfactuals analysis and what-if
titleSuffix: Azure Machine Learning
description: Generate diverse counterfactual examples with feature perturbations to see minimal changes required to achieve desired prediction with the Responsible AI dashboard's integration of DiCE machine learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.topic:  concept-article
ms.author: lagayhar
author: lgayhardt
ms.reviewer: mesameki
ms.date: 03/18/2026
ms.custom: responsible-ml, dev-focus
ai-usage: ai-assisted
---

# Counterfactuals analysis and what-if

What-if counterfactuals address the question of what the model would predict if you changed the action input. They help you understand and debug a machine learning model by showing how it reacts to input (feature) changes. 

Standard interpretability techniques approximate a machine learning model or rank features by their predictive importance. By contrast, counterfactual analysis "interrogates" a model to determine what changes to a particular data point would flip the model decision. 

This analysis helps you disentangle the impact of correlated features in isolation. It also helps you get a more nuanced understanding of how much of a feature change is needed to see a model decision flip for classification models and a decision change for regression models.

The *counterfactual analysis and what-if* component of the [Responsible AI dashboard](concept-responsible-ai-dashboard.md) has two functions:

- Generate a set of examples with minimal changes to a particular point such that they change the model's prediction (showing the closest data points with opposite model predictions).
- Enable users to generate their own what-if perturbations to understand how the model reacts to feature changes.

One of the top differentiators of the Responsible AI dashboard's counterfactual analysis component is that you can identify which features to vary and their permissible ranges for valid and logical counterfactual examples.

The capabilities of this component come from the [DiCE](https://github.com/interpretml/DiCE) package. 

Use what-if counterfactuals when you need to:

- Examine fairness and reliability criteria as a decision evaluator by perturbing sensitive attributes such as gender and ethnicity, and then observing whether model predictions change.
- Debug specific input instances in depth.
- Provide solutions to users and determine what they can do to get a desirable outcome from the model.

## How are counterfactual examples generated?

To generate counterfactuals, DiCE uses model-agnostic techniques. These methods work with any opaque-box classifier or regressor. They sample points near an input point while optimizing a loss function based on proximity. The loss function can also include terms for sparsity, diversity, and feasibility. Currently supported methods are:

- [Randomized search](https://interpretml.github.io/DiCE/notebooks/DiCE_model_agnostic_CFs.html#1.-Independent-random-sampling-of-features): This method randomly samples points near a query point and returns counterfactuals as points whose predicted label is the desired class.
- [Genetic search](https://interpretml.github.io/DiCE/notebooks/DiCE_model_agnostic_CFs.html#2.-Genetic-Algorithm): This method uses a genetic algorithm to sample points. It optimizes proximity to the query point, changes as few features as possible, and seeks diversity among the generated counterfactuals.
- [KD tree search](https://interpretml.github.io/DiCE/notebooks/DiCE_model_agnostic_CFs.html#3.-Querying-a-KD-Tree): This algorithm returns counterfactuals from the training dataset. It builds a KD tree over the training data points based on a distance function. Then, it returns the closest points to a query point that have the desired predicted label.

## Next steps

- Learn how to generate the Responsible AI dashboard via [YAML and Python](how-to-responsible-ai-insights-sdk-cli.md) or [studio UI](how-to-responsible-ai-insights-ui.md).
- Explore the [supported counterfactual analysis and what-if perturbation visualizations](how-to-responsible-ai-dashboard.md#counterfactual-what-if) of the Responsible AI dashboard.
- Learn how to generate a [Responsible AI scorecard](how-to-responsible-ai-scorecard.md) based on the insights observed in the Responsible AI dashboard.
