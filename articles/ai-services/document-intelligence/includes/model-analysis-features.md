---
author: laujan
ms.service: azure-ai-document-intelligence
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
<!-- markdownlint-disable MD041 -->

|Model ID|Content extraction|Query fields|Paragraphs|Paragraph roles|Selection marks|Tables|Key/value pairs|Languages|Barcodes|Document analysis|Formulas*|Style font*|High resolution*|Searchable PDF
|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|
|`prebuilt-read`|✓| |✓| | | | |O|O| |O|O|O|O|
|`prebuilt-layout`|✓|✓|✓|✓|✓|✓|O|O|O| |O|O|O|
|`prebuilt-contract`|✓|✓|✓|✓|✓ | | |O|O|✓|O|O|
|`prebuilt-healthInsuranceCard.us`|✓|✓| | | | | |O|O|✓|O|O|O|
|`prebuilt-idDocument`|✓|✓|| | | | |O|O|✓|O|O|O|
|`prebuilt-invoice`|✓|✓| | |✓|✓|O|O|O|✓|O|O|O|
|`prebuilt-receipt`|✓|✓| | | | | |O|O|✓|O|O|O|
|`prebuilt-marriageCertificate.us` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-creditCard` | ✓|✓ | | | | | | O | O |✓ | O | O | O |
|`prebuilt-check.us` | ✓|✓ | | | | | | O | O |✓ | O | O | O |
|`prebuilt-payStub.us` | ✓|✓ | | | | | | O | O |✓ | O | O | O |
|`prebuilt-bankStatement` | ✓|✓ | | | | | | O | O |✓ | O | O | O |
|`prebuilt-mortgage.us.1003` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-mortgage.us.1004` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-mortgage.us.1005` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-mortgage.us.1008` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-mortgage.us.closingDisclosure` | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-tax.us`|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.w2`|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.w4`|✓|✓| | | | | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1040` (various) | ✓|✓ | | |✓| | | O | O |✓ | O | O | O |
|`prebuilt-tax.us.1095A`|✓|✓| | | | | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1095C`|✓|✓| | | | | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1098`|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1098E`|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1098T`|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1099` (various)|✓|✓| | |✓| | |O|O|✓|O|O|O|
|`prebuilt-tax.us.1099SSA`|✓|✓| | | | | |O|O|✓|O|O|O|
|`{ customModelName }`|✓|✓|✓|✓|✓|✓| |O|O|✓|O|O|O|

✓ - Enabled</br>
O - Optional</br>
\* - Premium features incur extra costs
