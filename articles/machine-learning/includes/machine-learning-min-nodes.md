---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 02/10/2025
ms.author: scottpolly
---

> [!IMPORTANT]
> To avoid charges when no jobs are running, **set the minimum nodes to 0**. This setting allows Azure Machine Learning to de-allocate the nodes when they aren't in use. Any value larger than 0 will keep that number of nodes running, even if they are not in use.