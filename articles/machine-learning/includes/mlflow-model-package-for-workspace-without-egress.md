---
author: msakande
ms.service: azure-machine-learning
ms.topic: include
ms.date: 01/24/2025
ms.author: mopeakande
---

> [!TIP]
> In __workspaces without public network access__, before you can deploy MLflow models to online endpoints without egress connectivity, you have to [package the models](../how-to-package-models.md). The model packaging capability is in preview. When you package a model, you can avoid the need for an internet connection, which Azure Machine Learning otherwise requires to dynamically install necessary Python packages for the MLflow models.