---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: varundua
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Explore the sample application

When you view the GitHub repository for your sample, check the README for more instructions and information on how to deploy your own version of the application.

Instructions vary by sample, but most include how to:

* Open the solution in the location of your choice:
  * GitHub Codespaces
  * VS Code Dev Containers
  * Your local IDE
* Deploy the application to Azure
* Test the application

The README also includes information about the application, such as the use case, architecture, and pricing information.

## Deploy and customize templates

Most templates support quick-deploy options that launch in minutes. These architectures and implementations are customizable while staying [Well-Architected Framework](/azure/well-architected/) aligned by using [Azure Verified Modules](/azure/azure-resource-manager/bicep/azure-verified-modules). Use tools such as [PSRule](https://aka.ms/ps-rule) and [TFLint](https://github.com/terraform-linters/tflint) to test that your modified implementation is production-ready.

After you deploy, verify that the application is running:

1. Open the deployment URL shown in the terminal output.
1. Confirm the application loads and responds to your input.

## Benefits of AI solution templates

AI templates in Microsoft Foundry provide:

* **Faster time-to-value**: Skip boilerplate code and infrastructure setup to move from concept to production quickly.
* **Reduced engineering overhead**: Preintegrated Azure services eliminate deployment friction.
* **Trusted infrastructure**: Build with confidence on Microsoft's secure, scalable AI platform.
* **Modular and interoperable foundation**: Scale solutions efficiently across your organization.
* **Best practices built-in**: Use proven patterns and frameworks for production-ready solutions.

## Related content

- [Quickstart: Get started with Foundry](../quickstarts/get-started-code.md)
- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
- [What is Microsoft Foundry?](../what-is-foundry.md)
