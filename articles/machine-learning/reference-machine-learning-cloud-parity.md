---
title: Feature availability across cloud regions
titleSuffix: Azure Machine Learning
description: This article lists feature availability differences between public cloud and the Azure Government, Azure Germany, and Azure operated by 21Vianet regions.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: concept-article 
ms.reviewer: None
ms.author: scottpolly
author: s-polly
ms.date: 02/28/2025
ms.custom:
  - references_regions
  - ignite-2023
---

# Azure Machine Learning feature availability across clouds regions

Learn what Azure Machine Learning features are available in the Azure Government, Azure Germany, and Microsoft Azure operated by 21Vianet regions. 

In the list of global Azure regions, there are several regions that serve specific markets in addition to the public cloud regions. For example, the Azure Government and the Azure operated by 21Vianet regions. Azure Machine Learning is deployed into the following regions, in addition to public cloud regions:

* Azure Government regions **US-Arizona** and **US-Virginia**.
* Azure operated by 21Vianet region **China-East-2**.

Azure Machine Learning is still in development in air-gap Regions. 

For the Italy North Region, Application Insights isn't available until 12/12/2023 without allowlist. This will affect the following service until then - Job schedule  - Feature store  - Model monitor - Data import



The information in the rest of this document provides information on what features of Azure Machine Learning are available in these regions, along with region-specific information on using these features.
## Azure Government    

### Model Catalog in USGOV Virginia and Arizona 
| Model Name | MaaP Inference  | Batch Enabled | standard deployment (serverless Compute Inferencing)|  Standard deployment (Fine-tuning) | 
|----------------------------------------------------------------------------|:----------------------:|:--------------------:|:-------------:|:-------------:|
|ALLaM-2-7b-instruct    |maap-inference        ||||    
|Aurora    |maap-inference            ||||
|AutoML-Image-Classification|    maap-inference|    batch-enabled        |||
|AutoML-Image-Instance-Segmentation|    maap-inference|    batch-enabled        |||
|AutoML-Image-Object-Detection    |maap-inference    |batch-enabled    |||    
|bert-base-cased    |maap-inference|    batch-enabled    |||    
|bert-base-uncased    |maap-inference    |batch-enabled        |||
|bert-large-cased|    maap-inference|    batch-enabled        |||
|bert-large-uncased|    maap-inference|    batch-enabled|||        
|BiomedCLIP-PubMedBERT_256-vit_base_patch16_224|    maap-inference|    batch-enabled        |||
|bytetrack_yolox_x_crowdhuman_mot17-private-half    |maap-inference|    batch-enabled        |||
|camembert-base    |maap-inference|    batch-enabled        |||
|CodeLlama-13b-hf|    maap-inference    |batch-enabled        |||
|CodeLlama-13b-Instruct-hf|    maap-inference    |batch-enabled        |||
|CodeLlama-13b-Python-hf    |maap-inference|    batch-enabled        |||
|CodeLlama-34b-hf|    maap-inference    |batch-enabled        |||
|CodeLlama-34b-Instruct-hf|    maap-inference|    batch-enabled        |||
|CodeLlama-34b-Python-hf    |maap-inference|    batch-enabled        |||
|CodeLlama-70b-hf|    maap-inference            ||||
|CodeLlama-70b-Instruct-hf |    maap-inference            ||||
|CodeLlama-70b-Python-hf |        maap-inference                ||||
|CodeLlama-7b-hf |        maap-inference |        batch-enabled         |     |     |    
|CodeLlama-7b-Instruct-hf     |    maap-inference    |batch-enabled        |||
|CodeLlama-7b-Python-hf |    maap-inference |    batch-enabled        |||
|compvis-stable-diffusion-v1-4    |maap-inference    |batch-enabled        |||
|CxrReportGen    maap-inference    |batch-enabled        ||||
|databricks-dolly-v2-12b    |maap-inference |    batch-enabled        
|Deci-DeciCoder-1b    |maap-inference    |batch-enabled        
|deci-decidiffusion-v1-0    |maap-inference    |batch-enabled        
|Deci-DeciLM-7B    |maap-inference|    batch-enabled        
|Deci-DeciLM-7B-instruct    |maap-inference|    batch-enabled        
|deepset-minilm-uncased-squad2    |maap-inference    |batch-enabled        
|deepset-roberta-base-squad2|    maap-inference    |batch-enabled        
|distilbert-base-cased    |maap-inference    |batch-enabled        
|distilbert-base-cased-distilled-squad    |maap-inference|    batch-enabled        
|distilbert-base-uncased|    maap-inference|    batch-enabled        
|distilbert-base-uncased-distilled-squad|    maap-inference    |batch-enabled        
|distilbert-base-uncased-finetuned-sst-2-english    |maap-inference|    batch-enabled        
|distilgpt2|    maap-inference    |batch-enabled        
|distilroberta-base    |maap-inference|    batch-enabled        
|facebook-bart-large-cnn|    maap-inference|    batch-enabled        
|facebook-deit-base-patch16-224|    maap-inference|    batch-enabled        
|facebook-dinov2-base-imagenet1k-1-layer|    maap-inference|    batch-enabled        
|Facebook-DinoV2-Image-Embeddings-ViT-Base    |maap-inference|    batch-enabled        
|Facebook-DinoV2-Image-Embeddings-ViT-Giant    |maap-inference|    batch-enabled        
|facebook-sam-vit-base    |maap-inference    |batch-enabled        
|facebook-sam-vit-huge|    maap-inference    |batch-enabled        
|facebook-sam-vit-large    |maap-inference    |batch-enabled        
|financial-reports-analysis    |maap-inference    |batch-enabled        
|finiteautomata-bertweet-base-sentiment-analysis|    maap-inference    |batch-enabled        
|google-vit-base-patch16-224    |maap-inference    |batch-enabled            
|Jean-Baptiste-camembert-ner|    maap-inference|    batch-enabled        
|Llama-2-13b    |maap-inference|    batch-enabled|    maas-inference|    maas-finetuning|
|Llama-2-13b-chat    |maap-inference    || maas-inference        
|Llama-2-70b    |maap-inference    |batch-enabled |    maas-inference|    maas-finetuning|
|Llama-2-70b-chat    |maap-inference||    maas-inference        
|Llama-2-7b    maap-inference|    batch-enabled||    maas-inference|    maas-finetuning|
|Llama-2-7b-chat    |maap-inference    ||maas-inference        |
|Llama-3.2-11B-Vision-Instruct|    maap-inference    || maas-inference        
|Llama-3.2-1B    |maap-inference            
|Llama-3.2-1B-Instruct    | maap-inference            
|Llama-3.2-3B    |maap-inference            
|Llama-3.2-3B-Instruct    |maap-inference            
|Llama-3.2-90B-Vision-Instruct| maap-inference||    maas-inference        
|Llama-Guard-3-11B-Vision    |maap-inference            
|Llama-Guard-3-1B    |maap-inference            
|Llama-Guard-3-8B|    maap-inference            
|MatterSim|    maap-inference            
|MedImageInsight|    maap-inference|    batch-enabled        
|MedImageParse    |maap-inference|    batch-enabled        
|Meta-Llama-3-70B    |maap-inference            
|Meta-Llama-3-70B-Instruct    |maap-inference    ||maas-inference        
|Meta-Llama-3-8B    maap-inference            
|Meta-Llama-3-8B-Instruct    |maap-inference||    maas-inference        
|Meta-Llama-3.1-70B|maap-inference            
|Meta-Llama-3.1-70B-Instruct    |maap-inference||    maas-inference|    maas-finetuning    
|Meta-Llama-3.1-8B|    maap-inference            
|Meta-Llama-3.1-8B-Instruct    |maap-inference||    maas-inference|    maas-finetuning    
|microsoft-beit-base-patch16-224-pt22k-ft22k|    maap-inference    |batch-enabled        
|microsoft-deberta-base    |maap-inference    |batch-enabled        
|microsoft-deberta-base-mnli    |maap-inference|    batch-enabled        
|microsoft-deberta-large    |maap-inference|    batch-enabled        
|microsoft-deberta-large-mnli|    maap-inference    |batch-enabled        
|microsoft-deberta-xlarge    |maap-inference    | batch-enabled        
|microsoft-llava-med-v1.5-mistral-7b    |maap-inference    |batch-enabled        
|microsoft-rad-dino    |maap-inference    |batch-enabled        
|microsoft-swinv2-base-patch4-window12-192-22k|    maap-inference|    batch-enabled        
|mistral-community-Mixtral-8x22B-v0-1    |maap-inference            
|mistralai-Mistral-7B-Instruct-v0-2    |maap-inference            
|mistralai-Mistral-7B-Instruct-v01|    maap-inference            
|mistralai-Mistral-7B-v01    maap-inference|    batch-enabled        
|mistralai-Mixtral-8x22B-Instruct-v0-1|    maap-inference            
|mistralai-Mixtral-8x22B-v0-1|    maap-inference            
|mistralai-Mixtral-8x7B-Instruct-v01    |maap-inference            
|mistralai-Mixtral-8x7B-v01    |maap-inference            
|mmd-3x-deformable-detr_refine_twostage_r50_16xb2-50e_coco    |maap-inference|    batch-enabled        
|mmd-3x-mask-rcnn_swin-t-p4-w7_fpn_1x_coco    |maap-inference    |batch-enabled        
|mmd-3x-sparse-rcnn_r101_fpn_300-proposals_crop-ms-480-800-3x_coco|    maap-inference|    batch-enabled        
|mmd-3x-sparse-rcnn_r50_fpn_300-proposals_crop-ms-480-800-3x_coco|    maap-inference|    batch-enabled        
|mmd-3x-vfnet_r50-mdconv-c3-c5_fpn_ms-2x_coco    |maap-inference|    batch-enabled        
|mmd-3x-vfnet_x101-64x4d-mdconv-c3-c5_fpn_ms-2x_coco    |maap-inference    |batch-enabled        
|mmd-3x-yolof_r50_c5_8x8_1x_coco    |maap-inference|    batch-enabled        
|mmeft|    maap-inference|    batch-enabled        
|Muse|    maap-inference            
|ocsort_yolox_x_crowdhuman_mot17-private-half |    maap-inference|    batch-enabled        
|Phi-3-medium instruct (128k) |    maap-inference||    maas-inference|    maas-finetuning    
|Phi-3-medium instruct (4k)    |maap-inference||    maas-inference    |maas-finetuning    
|Phi-3-mini instruct (128k)    |maap-inference||    maas-inference|    maas-finetuning    
|Phi-3-mini instruct (4k)|    maap-inference||    maas-inference    |maas-finetuning    
|Phi-3-small instruct (128k)|maap-inference    ||maas-inference        
|Phi-3-small instruct (8k)    |maap-inference||    maas-inference        
|Phi-3-vision-128k-instruct|    maap-inference            
|Phi-3.5-mini instruct (128k)|    maap-inference    ||maas-inference|    maas-finetuning    
|Phi-3.5-MoE instruct (128k)    |maap-inference    ||maas-inference|    maas-finetuning    
|Phi-3.5-vision instruct (128k)|    maap-inference||    maas-inference        
|Phi-4    maap-inference    |||maas-inference        
|Prism    maap-inference    ||batch-enabled        
|projecte-aina-aguila-7b|    maap-inference            
|projecte-aina-FLOR-1-3B|    maap-inference            
|projecte-aina-FLOR-1-3B-Instructed    | maap-inference            
|projecte-aina-FLOR-6-3B    |maap-inference            ||||
|projecte-aina-FLOR-6-3B-Instructed    |maap-inference            
|Prompt-Guard-86M|    maap-inference            
|Prov-GigaPath    |maap-inference|    batch-enabled        
|roberta-base    |maap-inference    |batch-enabled        
|roberta-base-openai-detector|    maap-inference    |batch-enabled        
|roberta-large|    maap-inference    |batch-enabled        
|roberta-large-mnli    |maap-inference|    batch-enabled        
|roberta-large-openai-detector|    maap-inference    |batch-enabled        
|runwayml-stable-diffusion-inpainting    |maap-inference|    batch-enabled        
|runwayml-stable-diffusion-v1-5|    maap-inference|    batch-enabled        
|Salesforce-BLIP-2-opt-2-7b-image-to-text|    maap-inference|    batch-enabled        
|Salesforce-BLIP-2-opt-2-7b-vqa    |maap-inference|    batch-enabled        
|Salesforce-BLIP-image-captioning-base    |maap-inference|    batch-enabled        
|Salesforce-BLIP-vqa-base    |maap-inference    |batch-enabled        
|snowflake-arctic-base    |maap-inference            
|snowflake-arctic-instruct    |maap-inference            
|sshleifer-distilbart-cnn-12-6    |maap-inference    |batch-enabled        
|stabilityai-stable-diffusion-2-1    |maap-inference|    batch-enabled        
|stabilityai-stable-diffusion-2-inpainting| maap-inference    |batch-enabled        
|stabilityai-stable-diffusion-xl-base-1-0|    maap-inference    |batch-enabled        
|stabilityai-stable-diffusion-xl-refiner-1-0|    maap-inference|    batch-enabled        
|supply-chain-trade-regulations    |maap-inference|    batch-enabled        
|t5-base    |maap-inference    |batch-enabled        
|t5-large    |maap-inference|    batch-enabled        
|t5-small|    maap-inference|    batch-enabled        
|TamGen    |maap-inference            
|tiiuae-falcon-40b    |maap-inference     |batch-enabled        
|tiiuae-falcon-7b|    maap-inference |    batch-enabled        
|Virchow    |maap-inference |    batch-enabled        
|Virchow2|    maap-inference|    batch-enabled    |||    


### Azure OpenAI Models in Model Catalog in USGOV Virginia and Arizona 
| Model Name | Azure OpenAI Deployment | MaaP Inference  | Batch Enabled | MaaS (serverless Compute Inferencing)|
|----------------------------------------------------------------------------|:----------------------:|:--------------------:|:-------------:|:-------------:|
|gpt-35-turbo|    aoai-deployment    
|gpt-4    |aoai-deployment    
|OpenAI GPT-4o mini    |aoai-deployment    
|OpenAI GPT-4o    |aoai-deployment    
|OpenAI Text Embedding 3 (large)    |aoai-deployment    
|OpenAI-CLIP-Image-Text-Embeddings-vit-base-patch32    ||maap-inference    |batch-enabled
|OpenAI-CLIP-Image-Text-Embeddings-ViT-Large-Patch14-336    ||maap-inference    |batch-enabled
|openai-clip-vit-base-patch32|    |maap-inference|    batch-enabled
|openai-clip-vit-large-patch14||    maap-inference| batch-enabled
|openai-whisper-large||    maap-inference|    batch-enabled
|openai-whisper-large-v3    ||maap-inference|    batch-enabled
|text-embedding-ada-002    |aoai-deployment
|gpt2    ||maap-inference    |batch-enabled
|gpt2-large||    maap-inference    |batch-enabled
|gpt2-medium    || maap-inference|    batch-enabled






### Azure Machine Learning Features

| Feature | Public cloud status  | US-Virginia | US-Arizona| 
|----------------------------------------------------------------------------|:----------------------:|:--------------------:|:-------------:|
| **[Automated machine learning](concept-automated-ml.md)** | | | |
| Create and run experiments in notebooks                                    | GA                   | YES                | YES         |
| Create and run experiments in studio web experience                        | Public Preview       | YES                | YES         |
| Industry-leading forecasting capabilities                                  | GA                   | YES                | YES         |
| Support for deep learning and other advanced learners                      | GA                   | YES                | YES         |
| Large data support (up to 100 GB)                                          | Public Preview       | YES                | YES         |
| Azure Databricks integration                                              | GA                   | NO                 | NO          |
| SQL, Azure Cosmos DB, and HDInsight integrations                                   | GA                   | YES                | YES         |
| **[Machine Learning pipelines](concept-ml-pipelines.md)** |   |  | | 
| Create, run, and publish pipelines using the Azure Machine Learning SDK                   | GA                   | YES                | YES         |
| Create pipeline endpoints using the Azure Machine Learning SDK                           | GA                   | YES                | YES         |
| Create, edit, and delete scheduled runs of pipelines using the Azure Machine Learning SDK | GA                   | YES*               | YES*        |
| View pipeline run details in studio                                        | GA                   | YES                | YES         |
| Create, run, visualize, and publish pipelines in Azure Machine Learning designer          | GA      | YES                | YES         |
| Azure Databricks Integration with ML Pipeline                             | GA                   | NO                 | NO          |
| Create pipeline endpoints in Azure Machine Learning designer                             | GA      | YES                | YES         |
| **[Integrated notebooks](how-to-run-jupyter-notebooks.md)** |   |  | | 
| Workspace notebook and file sharing                                        | GA                   | YES                | YES         |
| R and Python support                                                       | GA                   | YES                | YES         |
| Virtual Network support                                                    | GA       | YES                 | YES          |
| **[Compute instance](concept-compute-instance.md)** |   |  | | 
| Managed compute Instances for integrated Notebooks                         | GA                   | YES                | YES         |
| Jupyter, JupyterLab Integration                                            | GA                   | YES                | YES         |
| Virtual Network (VNet) support                                             | GA       | YES                | YES         |
| [Configure Apache Spark pools to perform data wrangling](apache-spark-azure-ml-concepts.md)                                             | Public Preview       | No                | No         |
| **SDK support** |  |  | | 
| [Python SDK support](/python/api/overview/azure/ml/)                                                         | GA                   | YES                | YES         |
| **[Security](concept-enterprise-security.md)** |   | | | 
| Managed virtual network support                                            | Preview                   | Preview                | Preview         |
| Virtual Network (VNet) support for training                                | GA                   | YES                | YES         |
| Virtual Network (VNet) support for inference                               | GA                   | YES                | YES         |
| Scoring endpoint authentication                                            | Public Preview       | YES                | YES         |
| Workplace private endpoint                                                 | GA  |  GA  |  GA |
| ACI behind VNet                                                            | Public Preview       | NO                 | NO          |
| ACR behind VNet                                                            | GA       | YES                 | YES          |
| Private IP of AKS cluster                                                  | Public Preview       | NO                 | NO          |
| Network isolation for managed online endpoints                             | GA       | NO                 | NO          |
| **Compute** |   | | |
| [quota management across workspaces](how-to-manage-quotas.md)                                         | GA                   | YES                | YES         |
| [Kubernetes compute](./how-to-attach-kubernetes-anywhere.md)                                         | GA                   | NO                | NO         |
| **[Data for machine learning](concept-data.md)** |   | | |
| Create, view, or edit datasets and datastores from the SDK                  | GA                   | YES                | YES         |
| Create, view, or edit datasets and datastores from the UI                   | GA                   | YES                | YES         |
| View, edit, or delete dataset drift monitors from the SDK                   | Public Preview       | YES                | YES         |
| View, edit, or delete dataset drift monitors from the UI                    | Public Preview       | YES                | YES         |
| **Machine learning lifecycle** |   | | |
| [Model profiling (SDK/CLI v1)](v1/how-to-deploy-profile-model.md)                                                            | GA                   | YES                | PARTIAL     |
| [The Azure Machine Learning CLI v1](v1/reference-azure-machine-learning-cli.md)     | GA                   | YES                | YES         |
| [Visual Studio Code integration](how-to-setup-vs-code.md)                                             | Public Preview       | NO                 | NO          |
| [Event Grid integration](how-to-use-event-grid.md)                                                     | Public Preview       | NO                 | NO          |
| [Integrate Azure Stream Analytics with Azure Machine Learning](/azure/stream-analytics/machine-learning-udf)               | Public Preview       | NO                 | NO          |
| **Labeling [images](how-to-create-image-labeling-projects.md) and [text](how-to-create-text-labeling-projects.md)** |   | | |
| Labeling Project Management Portal                                        | GA                   | YES                | YES         |
| Labeler Portal                                                            | GA                   | YES                | YES         |
| Labeling using private workforce                                          | GA                   | YES                | YES         |
| ML assisted labeling (Image classification and object detection)           | Public Preview       | YES                | YES         |
| **[Responsible ML](concept-responsible-ml.md)** |   | | |
| Explainability in UI                                                       | Public Preview       | NO                 | NO          |
| Differential privacy SmartNoise toolkit                                    | OSS                  | NO                 | NO          |
| Custom tags in Azure Machine Learning to implement datasheets              | GA                   | NO                 | NO          |
| Fairness Azure Machine Learning Integration                                               | Public Preview       | NO                 | NO          |
| Interpretability  SDK                                                      | GA                   | YES                | YES         |
| **Training** |   | | |
| [Experimentation log streaming](how-to-track-monitor-analyze-runs.md)                                              | GA                   | YES                | YES         |
| [Experimentation UI](how-to-track-monitor-analyze-runs.md)                                                         | Public Preview                   | YES                | YES         |
| [.NET integration ML.NET 1.0](/dotnet/machine-learning/tutorials/object-detection-model-builder)                                                | GA                   | YES                | YES         |
| **Inference** |   | | |
| Managed online endpoints | GA | YES | YES |
| [Batch inferencing](tutorial-pipeline-batch-scoring-classification.md)                                                          | GA                   | YES                | YES         |
| **Other** |   | | |
| [Open Datasets](../open-datasets/samples.md)                                                              | Public Preview       | YES                | YES         |
| [Custom Azure AI Search (SDK v1)](./v1/how-to-deploy-model-cognitive-search.md)                                                    | Public Preview       | YES                | YES         |


### Azure Government scenarios

| Scenario                                                    | US-Virginia | US-Arizona| Limitations  |
|----------------------------------------------------------------------------|:----------------------:|:--------------------:|-------------|
| **General security setup** |   | | |
| Disable/control internet access (inbound and outbound) and specific VNet | PARTIAL| PARTIAL    |  | 
| Placement for all associated resources/services  | YES | YES |  |
| Encryption at-rest and in-transit.                                                 | YES | YES |  |
| Root and SSH access to compute resources.                                          | YES | YES |  |
| Maintain the security of deployed systems (instances, endpoints, etc.), including endpoint protection, patching, and logging |  PARTIAL|    PARTIAL    |ACI behind VNet currently not available |                                  
| Control (disable/limit/restrict) the use of ACI/AKS integration                    | PARTIAL|    PARTIAL    |ACI behind VNet currently not available|
| Azure role-based access control (Azure RBAC) - Custom Role Creations                           | YES | YES |  |
| Control access to ACR images used by ML Service (Azure provided/maintained versus custom)  |PARTIAL|    PARTIAL    |  |
| **General Machine Learning Service Usage** |  | | |
| Ability to have a development environment to build a model, train that model, host it as an endpoint, and consume it via a webapp     | YES | YES |  |
| Ability to pull data from ADLS (Data Lake Storage)                                 |YES | YES |  |
| Ability to pull data from Azure Blob Storage                                       |YES | YES |  |



### Other Azure Government limitations

* For Azure Machine Learning compute instances, the ability to refresh a token lasting more than 24 hours isn't available in Azure Government.
* Model Profiling doesn't support 4 CPUs in the US-Arizona region.   
* Sample notebooks may not work in Azure Government if it needs access to public data.
* IP addresses: The CLI command used in the [required public internet access](how-to-secure-training-vnet.md#required-public-internet-access-to-train-models) instructions doesn't return IP ranges. Use the [Azure IP ranges and service tags for Azure Government](https://www.microsoft.com/download/details.aspx?id=57063) instead.
* For scheduled pipelines, we also provide a blob-based trigger mechanism. This mechanism isn't supported for CMK workspaces. For enabling a blob-based trigger for CMK workspaces, you have to do extra setup. For more information, see [Trigger a run of a machine learning pipeline from a Logic App (SDK/CLI v1)](v1/how-to-trigger-published-pipeline.md).
* Firewalls: When using an Azure Government region, add the following hosts to your firewall setting:

    * For Arizona use: `usgovarizona.api.ml.azure.us`
    * For Virginia use: `usgovvirginia.api.ml.azure.us`
    * For both: `graph.windows.net` 


## Azure operated by 21Vianet    

| Feature                                       | Public cloud status | CH-East-2 | CH-North-3 |
|----------------------------------------------------------------------------|:------------------:|:--------------------:|:-------------:|
| **Automated machine learning** |    | | |
| Create and run experiments in notebooks                                    | GA               | YES       | N/A        |
| Create and run experiments in studio web experience                        | Preview   | YES       | N/A        |
| Industry-leading forecasting capabilities                                  | GA               | YES       | N/A        |
| Support for deep learning and other advanced learners                      | GA               | YES       | N/A        |
| Large data support (up to 100 GB)                                          |  Preview   | YES       | N/A        |
| Azure Databricks Integration                                              | GA               | YES        | N/A        |
| SQL, Azure Cosmos DB, and HDInsight integrations                                   | GA               | YES       | N/A        |
| **Machine Learning pipelines** |    | | |
| Create, run, and publish pipelines using the Azure Machine Learning SDK                   | GA               | YES       | N/A        |
| Create pipeline endpoints using the Azure Machine Learning SDK                           | GA               | YES       | N/A        |
| Create, edit, and delete scheduled runs of pipelines using the Azure Machine Learning SDK | GA               | YES       | N/A        |
| View pipeline run details in studio                                        | GA               | YES       | N/A        |
| Create, run, visualize, and publish pipelines in Azure Machine Learning designer          | GA  | YES       | N/A        |
| Azure Databricks Integration with ML Pipeline                             | GA               | YES        | N/A        |
| Create pipeline endpoints in Azure Machine Learning designer                             | GA   | YES       | N/A        |
| **Integrated notebooks** |   | | |
| Workspace notebook and file sharing                                        | GA               | YES       | N/A        |
| R and Python support                                                       | GA               | YES       | N/A        |
| Virtual Network support                                                    |  GA   | YES        | N/A        |
| **Compute instance** |    | | |
| Managed compute Instances for integrated Notebooks                         | GA               | YES        | N/A        |
| Jupyter, JupyterLab Integration                                            | GA               | YES       | N/A        |
| Managed virtual network support                                            | Preview               | Preview        | N/A        |
| Virtual Network (VNet) support                                             | GA   | YES       | N/A        |
| **SDK support** |    | | |
| Python SDK support                                                         | GA               | YES       | N/A        |
| **Security** |   | | |
| Virtual Network (VNet) support for training                                | GA               | YES       | N/A        |
| Virtual Network (VNet) support for inference                               | GA               | YES       | N/A        |
| Scoring endpoint authentication                                            |  Preview   | YES       | N/A        |
| Workplace Private Endpoint                                                 | GA               | YES        | N/A        |
| ACI behind VNet                                                            | Preview   | NO        | N/A        |
| ACR behind VNet                                                            | GA   | YES       | N/A        |
| Private IP of AKS cluster                                                  | Preview   | NO        | N/A        |
| Network isolation for managed online endpoints                             | GA     | NO                 | N/A          |
| **Compute** |   | | |
| quota management across workspaces                                         | GA               | YES       | N/A        |
| [Kubernetes compute](./how-to-attach-kubernetes-anywhere.md)                                         | GA                   | NO                | NO         |
| **Data for machine learning** | | | |
| Create, view, or edit datasets and datastores from the SDK                  | GA               | YES       | N/A        |
| Create, view, or edit datasets and datastores from the UI                   | GA               | YES       | N/A        |
| View, edit, or delete dataset drift monitors from the SDK                   |  Preview   | YES       | N/A        |
| View, edit, or delete dataset drift monitors from the UI                    | Preview   | YES       | N/A        |
| **Machine learning lifecycle** |    | | |
| Model profiling                                                            | GA               | YES  | N/A        |
| The Azure DevOps extension for Machine Learning & the Azure Machine Learning CLI         | GA               | YES       | N/A        |
| FPGA-based Hardware Accelerated Models                                     | Deprecating               | Deprecating            | N/A        |
| Visual Studio Code integration                                             | Preview   | NO        | N/A        |
| Event Grid integration                                                     | Preview   | YES       | N/A        |
| Integrate Azure Stream Analytics with Azure Machine Learning               | Preview   | NO        | N/A        |
| **Labeling** |    | | |
| Labeling Project Management Portal                                        | GA               | YES       | N/A        |
| Labeler Portal                                                            | GA               | YES       | N/A        |
| Labeling using private workforce                                          | GA               | YES       | N/A        |
| ML assisted labeling (Image classification and object detection)           | Preview   | YES       | N/A        |
| **Responsible AI** |    | | |
| Explainability in UI                                                       | Preview   | NO        | N/A        |
| Differential privacy SmartNoise toolkit                                    | OSS              | NO        | N/A        |
| custom tags in Azure Machine Learning to implement datasheets              | GA               | YES        | N/A        |
| Fairness Azure Machine Learning Integration                                               | Preview   | NO        | N/A        |
| Interpretability  SDK                                                      | GA               | YES       | N/A        |
| **Training** |    | | |
| Experimentation log streaming                                              | GA               | YES       | N/A        |
| Reinforcement Learning                                                     | Deprecating       | Deprecating            | N/A        |
| Experimentation UI                                                         | GA               | YES       | N/A        |
| .NET integration ML.NET 1.0                                                | GA               | YES       | N/A        |
| **Inference** |   | | |
| Managed online endpoints | GA | YES | N/A |
| Batch inferencing                                                          | GA               | YES       | N/A        |
| Azure Stack Edge with FPGA                                                    | Deprecating       | Deprecating            | N/A        |
| **Other** |    | | |
| Open Datasets                                                              | Preview   | YES       | N/A        |
| Custom Azure AI Search                                                    | Preview   | YES       | N/A        |



### Other Azure operated by 21Vianet limitations

* Azure operated by 21Vianet has limited VM SKU, especially for GPU SKU. It only has NCv3 family (V100).
* REST API Endpoints are different from global Azure. Use the following table to find the REST API endpoint for Azure operated by 21Vianet regions:

    | REST endpoint                 | Global Azure                                 | China-Government                           |
    |------------------|--------------------------------------------|--------------------------------------------|
    | Management plane | `https://management.azure.com/`              | `https://management.chinacloudapi.cn/`       |
    | Data plane       | `https://{location}.experiments.azureml.net` | `https://{location}.experiments.ml.azure.cn` |
    | Microsoft Entra ID              | `https://login.microsoftonline.com`          | `https://login.chinacloudapi.cn`             |

* Sample notebook may not work, if it needs access to public data.
* IP address ranges: The CLI command used in the [required public internet access](how-to-secure-training-vnet.md#required-public-internet-access-to-train-models) instructions doesn't return IP ranges. Use the [Azure IP ranges and service tags for Microsoft Azure operated by 21Vianet](https://www.microsoft.com//download/details.aspx?id=57062) instead.
* Azure Machine Learning compute instances preview isn't supported in a workspace where Private Endpoint is enabled for now, but CI will be supported in the next deployment for the service expansion to all Azure Machine Learning regions.
* Searching for assets in the web UI with Chinese characters won't work correctly.

## Next steps

To learn more about the regions that Azure Machine Learning is available in, see [Products by region](https://azure.microsoft.com/global-infrastructure/services/).
