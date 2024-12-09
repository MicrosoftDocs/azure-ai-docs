---
title: Machine learning and data science tools
titleSuffix: Azure Data Science Virtual Machine 
description: Learn about the machine-learning tools and frameworks that are preinstalled on the Data Science Virtual Machine.
keywords: data science tools, data science virtual machine, tools for data science, linux data science
services: machine-learning
ms.service: azure-data-science-virtual-machines
ms.custom: devx-track-python

author: fbsolo-ms1 
ms.author: franksolomon 
ms.topic: conceptual
ms.reviewer: tklimmer
ms.date: 04/17/2024
---

# Machine learning and data science tools on Azure Data Science Virtual Machines
Azure Data Science Virtual Machines (DSVMs) have a rich set of tools and libraries for machine learning. These resources are available in popular languages, such as Python, R, and Julia.

The DSVM supports these machine-learning tools and libraries:

## Azure Machine Learning SDK for Python

For a full reference, visit [Azure Machine Learning SDK for Python](../overview-what-is-azure-machine-learning.md).

| Category | Value |
| ------------- | ------------- |
| What is it?   |   You can use the Azure Machine Learning cloud service to develop and deploy machine-learning models. You can use the Python SDK to track your models as you build, train, scale, and manage them. Deploy models as containers, and run them in the cloud, on-premises, or on Azure IoT Edge.   |
| Supported editions     | Windows (conda environment: AzureML), Linux (conda environment: py36)    |
| Typical uses      | General machine-learning platform      |
| How is it configured or installed?      |  Installed with GPU support   |
| How to use or run it      | As a Python SDK and in the Azure CLI. Activate to the conda environment `AzureML` on the Windows edition *or* activate to `py36` on the Linux edition.      |
| Link to samples      | Find sample Jupyter notebooks in the `AzureML` directory, under notebooks.  |

## H2O

| Category | Value |
| ------------- | ------------- |
| What is it?   | An open-source AI platform that supports distributed, fast, in-memory, scalable machine learning.  |
| Supported versions      | Linux   |
| Typical uses      | General-purpose distributed, scalable machine learning   |
| How is it configured or installed?      | H2O is installed in `/dsvm/tools/h2o`.      |
| How to use or run it      | Connect to the VM with X2Go. Start a new terminal, and run `java -jar /dsvm/tools/h2o/current/h2o.jar`. Then, start a web browser and connect to `http://localhost:54321`.      |
| Link to samples      | Find samples on the VM in Jupyter, under the `h2o` directory.      |

There are several other machine-learning libraries on DSVMs - for example, the popular `scikit-learn` package that's part of the Anaconda Python distribution for DSVMs. For a list of packages available in Python, R, and Julia, run the respective package managers.

## LightGBM

| Category | Value |
| ------------- | ------------- |
| What is it?   | A fast, distributed, high-performance gradient-boosting (GBDT, GBRT, GBM, or MART) framework based on decision tree algorithms. Machine-learning tasks - ranking, classification, etc. - use it.    |
| Supported versions      | Windows, Linux    |
| Typical uses      | General-purpose gradient-boosting framework      |
| How is it configured or installed?      | LightGBM is installed as a Python package on Windows. On Linux, the command-line executable is located in `/opt/LightGBM/lightgbm`. The R package is installed, and Python packages are installed.     |
| Link to samples      | [LightGBM guide](https://github.com/Microsoft/LightGBM/tree/master/examples/python-guide)   |

## Rattle
| Category | Value |
| ------------- | ------------- |
| What is it?   |   A graphical user interface for data mining that uses R.   |
| Supported editions     | Windows, Linux     |
| Typical uses      | General UI data-mining tool for R    |
| How to use or run it      | As a UI tool. On Windows, start a command prompt, run R, and then inside R, run `rattle()`. On Linux, connect with X2Go, start a terminal, run R, and then inside R, run `rattle()`. |
| Link to samples      | [Rattle](https://togaware.com/onepager/) |

## Vowpal Wabbit
| Category | Value |
| ------------- | ------------- |
| What is it?   |   A fast, open-source, out-of-core learning system library    |
| Supported editions     | Windows, Linux     |
| Typical uses      | General machine-learning library      |
| How is it configured or installed?      |  Windows: msi installer<br/>Linux: apt-get |
| How to use or run it      | As an on-path command-line tool (`C:\Program Files\VowpalWabbit\vw.exe` on Windows, `/usr/bin/vw` on Linux)    |
| Link to samples      | [VowPal Wabbit samples](https://github.com/JohnLangford/vowpal_wabbit/wiki/Examples) |

## Weka
| Category | Value |
| ------------- | ------------- |
| What is it?   |  A collection of machine-learning algorithms for data-mining tasks. You can either apply the algorithms directly, or call them from your own Java code. Weka contains tools for data pre-processing, classification, regression, clustering, association rules, and visualization. |
| Supported editions     | Windows, Linux     |
| Typical uses      | General machine-learning tool     |
| How to use or run it      | On Windows, search for Weka on the **Start** menu. On Linux, sign in with X2Go, and then go to **Applications** > **Development** > **Weka**. |
| Link to samples      | [Weka samples](https://docs.weka.io/) |

## XGBoost 
| Category | Value |
| ------------- | ------------- |
| What is it?   |   A fast, portable, and distributed gradient-boosting (GBDT, GBRT, or GBM) library for Python, R, Java, Scala, C++, and more. It runs on a single machine, and on Apache Hadoop and Spark.    |
| Supported editions     | Windows, Linux     |
| Typical uses      | General machine-learning library      |
| How is it configured or installed?      |  Installed with GPU support   |
| How to use or run it      | As a Python library (2.7 and 3.6+), R package, and on-path command-line tool (`C:\dsvm\tools\xgboost\bin\xgboost.exe` for Windows and `/dsvm/tools/xgboost/xgboost` for Linux)    |
| Links to samples      | Samples are included on the VM, in `/dsvm/tools/xgboost/demo` on Linux, and `C:\dsvm\tools\xgboost\demo` on Windows.   |