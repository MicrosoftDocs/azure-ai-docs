---
title: 'Fine-tuning cost management'
titleSuffix: Azure OpenAI
description: Learn about cost management
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 07/08/2025
author: mrbullwinkle
ms.author: mbullwin
show_latex: true
---

# Cost Management for Fine Tuning

Fine tuning can be intimidating: unlike base models, where you're just paying for input and output tokens for inferencing, fine tuning requires training your custom models and dealing with hosting. This guide is intended to help you better understand the costs of fine tuning and how to manage them.

## Upfront investment - training your model

This is the one-time, fixed cost associated with teaching a base model your specific requirements using your training data.

### The calculation formula

**Supervised Fine Tuning (SFT) & Preference Fine Tuning (DPO)**

It's straightforward to estimate the costs for SFT & DPO: you are charged based on the number of tokens in your training file, and the number of epochs for your training job.

$$
\text{price} = \text{\# training tokens} \times \text{\# epochs} \times \text{price per token}
$$

In general, smaller models and more recent models have lower prices per token than larger, older models. To estimate the number of tokens in your file, you can use the tiktoken library – or, for a less precise estimate, one word is roughly equivalent to four tokens.

We offer both regional and global training for SFT; if you don't need data residency, global training allows you to train at a discounted rate.

We do not charge you for time spent in queue, failed or cancelled jobs, or data safety checks.

#### Worked example: Supervised Fine Tuning

Projecting the costs to fine tune a model for natural language to code.

- Prepare the training data file: 500 prompt / response pairs, with a total of 1M tokens, and a validation file with 20 examples and 40K tokens
- Configure training run:
  - select base model (GPT-4.1)
  - specify global training
  - set hyperparameters to "default". Algorithmically, training is set to 2 epochs.
- Training runs for 2 hours, 15 minutes
**Total cost**:  
`$2/1M tokens * 1M training tokens * 2 epochs = $4`

### Reinforcement Fine Tuning (RFT)

The cost is determined by the time spent on training the model for Reinforcement fine tuning technique.

#### The formula is:

```
price = Time taken for training ⋅ Hourly training price + Grader inferencing per token if model grader is used
```

- **Time**: Total time in hours rounded to two decimal places (e.g., 1.25 hours)
- **Hourly Training cost**: $100 per hour of core training time for o4-mini-2025-04-16
- **Model grading**: Tokens used to grade outputs during training are billed separately at datazone rates once training is complete.

#### Worked Example: Training model with graders (without Model grader – Score_model)

Let's project the cost to train a customer service chatbot.

- Submit fine tuning job: Time when FT job has submitted: 02:00 hrs
- Data pre-processing completed: It took 30mins for data pre-processing to be completed which includes data safety checks. This time is not used for billing.
- Training started: Training starts at 02:30 hours
- Training completed: Training is completed at 06:30 hours
- Model creation: A deployable model checkpoint is created after training completion which included post-training model safety steps. This time is not used for billing.

**Final Calculation**:  
`Total time taken for training * Hourly training cost = 4 * 100 = $200`

Your one-time investment to create this o4-mini custom fine tuned model would be **$400.00**.

---

#### Worked Example: Training model with Model ‘Score_model’ grader (o3-mini being used as grader)

Let's project the cost to train a customer service chatbot.

- Submit fine tuning job: Time when FT job has started say 02:00 hrs
- Data pre-processing completed: It took 30mins for data pre-processing to be completed which includes data safety checks. This time is not used for billing.
- Training started: Training starts at 02:30 hours
- Training completed: Training is completed at 06:30 hours
- Model grader pricing:
  - Total Input tokens used for grading – 5 M tokens
  - Total Output tokens used for grading – 4.9 M tokens
- Model creation: A deployable model checkpoint is created after training completion which included post-training model safety steps. This time is not used for billing.

**Final Calculation**:  

```
Total time taken for training * Hourly training cost = 4 * 100 = $400  
Grading costs = # Input tokens * Price per i/p token + Output tokens * price per o/p token  
= (5 * 1.1) + (4.9 * 4.4) = 5.5 + 21.56 = $27.06  
Total training costs = $427.06
```

Your one-time investment to create this o4-mini custom fine tuned model would be **$427.06**

### Managing costs and spend limits when using RFT

To control your spend we recommend:

- Start with shorter runs to understand how your configuration affects time – Use configuration ‘reasoning effort’ – Low, smaller validation data sets
- Use a reasonable number of validation examples and ‘eval_samples’. Avoid validating more often than you need.
- Choose the smallest grader model that meets your quality requirements.
- Adjust ‘compute_multiplier’ to balance convergence speed and cost.
- Monitor your run in the Foundry portal or via the API. You can pause or cancel at any time.

As RFT job can lead to high training costs, we are capping the pricing for per training job billing to **$5000** which means this will be the maximum amount that a job can cost before we end the job. The training will be paused and a deployable checkpoint will be created. Users can validate the training job, metrics, logs and then decide to resume the job to complete further. If the user decides to resume the job, billing will continue for the job and subsequently no further price limits would be placed on the training job.

### Job failures and cancellations

You are not billed for work lost due to our error. If you cancel a run, you'll be charged for the work completed up to that point.  
Example: the run trains for 2 hours, writes a checkpoint, trains for 1 more hour, but then fails. Only the 2 hours of training up to the checkpoint are billable.

### Waiting on resources

If job is queued

### Part 2: Ongoing Operational Costs – Using Your Model

After your model is trained, you can deploy it any number of times using the following deployment types:

We have three options for hosting:

- **Standard**: pay per-token at the same rate as base model Standard deployments with an additional $1.70/hour hosting fee. Offers a 99.9% availability SLA and regional data residency guarantees.
- **Global Standard**: pay per-token at the same rate as base model Global Standard deployments with an additional $1.70/hour hosting fee. Offers a 99.9% availability SLA but does not offer data residency guarantees. Offers higher throughputs than Standard deployments.
- **Regional Provisioned Throughput**: offers latency guarantees in addition to the availability SLA, designed for latency-sensitive workloads. Instead of paying per-token or an hourly hosting fee, deployments accrue PTU-hours based on the number of provisioned throughput units (PTU) assigned to the deployment, and billed at a rate determined by your agreements or reservations with Microsoft Azure.
- **Developer Tier (Public Preview)**: pay per-token and without an hourly hosting fee but offers neither data residency nor availability SLAs. Designed for model candidate evaluation and proof of concepts, deployments are removed automatically after 24 hours regardless of usage but may be redeployed as needed.

The right deployment type for your use case depends on weighing your AI requirements and where you are on your fine-tuning journey.

| Deployment Type             | Availability SLA | Latency SLA | Token Rate         | Hourly Rate     |
|----------------------------|------------------|-------------|--------------------|-----------------|
| Standard                   | 99.9%            | None        | Same as base model | $1.70/hour      |
| Global Standard            | 99.9%            | None        | Same as base model | $1.70/hour      |
| Regional Provisioned Throughput | 99.9%      | Same as base model | None         | PTU/hour        |
| Developer Tier             | None             | None        | Same as Global Standard | None      |

Pricing Structure for all models are called out in the Pricing page - Azure OpenAI Service - Pricing  
Microsoft Azure

### Example for o4-mini

- Hosting charges: $1.70 per hour
- Input Cost: $1.10 per 1M tokens
- Output Cost: $4.40 per 1M tokens

#### Worked Example: Monthly Usage of a Fine-Tuned Chatbot

Let's assume your chatbot handles 10,000 customer conversations in its first month:

- Hosting charges: $1.70 per hour
- Total Input: The user queries sent to the model total 20 million tokens.
- Total Output: The model's responses to users total 40 million tokens.

**Input Cost Calculation**:  
`20 × $1.10 = $22.00`

**Output Cost Calculation**:  
`40 × $4.40 = $176.00`

**Your total operational cost for the month would be**:  
`= Hosting charges + Token usage cost`  
`= ($1.70 * 30 days * 24 hours) + ($22 (Input) + $176 (Output))`  
`= $1422.00`
