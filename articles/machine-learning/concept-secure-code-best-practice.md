---
title: Secure code best practices
titleSuffix: Azure Machine Learning
description: Learn about potential security threats that exist when developing for Azure Machine Learning, mitigations, and best practices.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: concept-article
ms.author: scottpolly
author:  s-polly
ms.reviewer: shshubhe
ms.date: 03/23/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Best practices for secure code

In Azure Machine Learning, you can upload files and content from any source into Azure. Content within Jupyter notebooks or scripts that you load can potentially read data from your sessions, access sensitive data within your organization in Azure, or run malicious processes on your behalf.

> [!IMPORTANT]
> Only run notebooks or scripts from trusted sources. For example, where you or your security team reviewed the notebook or script.

## Potential threats

Development with Azure Machine Learning often involves web-based development environments, such as notebooks or the Azure Machine Learning studio. When you use web-based development environments, the potential threats are:

* [Cross-site scripting (XSS)](https://owasp.org/www-community/attacks/xss/)

    * **DOM injection**: This type of attack can modify the UI displayed in the browser. For example, by changing how the run button behaves in a Jupyter Notebook.
    * **Access token or cookies**: XSS attacks can also access local storage and browser cookies. Your Microsoft Entra authentication token is stored in local storage. An XSS attack could use this token to make API calls on your behalf, and then send the data to an external system or API.

* [Cross-site request forgery (CSRF)](https://owasp.org/www-community/attacks/csrf): This attack could replace the URL of an image or link with the URL of a malicious script or API. When the image is loaded or link clicked, a call is made to the URL.

## Azure Machine Learning studio notebooks

Azure Machine Learning studio provides a hosted notebook experience in your browser. Cells in a notebook can output HTML documents or fragments that contain malicious code. When you render the output, the code can run.

**Possible threats**:
* Cross-site scripting (XSS)
* Cross-site request forgery (CSRF)

**Mitigations provided by Azure Machine Learning**:
* **Code cell output** is sandboxed in an iframe. The iframe prevents the script from accessing the parent DOM, cookies, or session storage.
* **Markdown cell** contents are cleaned by using the dompurify library. This cleaning blocks malicious scripts from executing when markdown cells are rendered.
* **Image URL** and **markdown links** are sent to a Microsoft-owned endpoint, which checks for malicious values. If the endpoint detects a malicious value, it rejects the request.

**Recommended actions**:
* Verify that you trust the contents of files before uploading them to the studio. You must acknowledge that you're uploading trusted files.
* When you select a link to open an external application, you're prompted to trust the application.

## Azure Machine Learning compute instance

Azure Machine Learning compute instance hosts Jupyter and JupyterLab. When you use either, code inside notebook cells can output HTML documents or fragments that contain malicious code. When the output is rendered, the code can run. The same threats apply when you use RStudio or Posit Workbench (formerly RStudio Workbench) hosted on a compute instance.

**Possible threats**:
* Cross-site scripting (XSS)
* Cross-site request forgery (CSRF)

**Mitigations provided by Azure Machine Learning**:
* None. Jupyter and JupyterLab are open-source applications hosted on the Azure Machine Learning compute instance.

**Recommended actions**:
* Verify that you trust the contents of files before uploading. You must acknowledge that you're uploading trusted files.

## Report security problems or concerns

Azure Machine Learning is eligible under the Microsoft Azure Bounty Program. For more information, visit the [Microsoft Azure Bounty Program](https://www.microsoft.com/msrc/bounty-microsoft-azure).

## Related content

* [Enterprise security and governance for Azure Machine Learning](concept-enterprise-security.md)
