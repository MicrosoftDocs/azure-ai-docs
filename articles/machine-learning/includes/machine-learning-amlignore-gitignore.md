---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 02/10/2025
ms.author: scottpolly
---

To prevent unnecessary files from being included in the snapshot, make an ignore file (`.gitignore` or `.amlignore`) in the directory. Add the files and directories to exclude to this file. For more information on the syntax to use inside this file, see [syntax and patterns](https://git-scm.com/docs/gitignore) for `.gitignore`. The `.amlignore` file uses the same syntax. _If both files exist, the `.amlignore` file is used and the `.gitignore` file is unused._
