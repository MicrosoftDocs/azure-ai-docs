# Verification: how-to-understand-automated-ml

**Document:** articles/machine-learning/how-to-understand-automated-ml.md  
**Date:** 2026-09-09 17:03  
**Status:** FAIL / web-and-source-backed freshness verification

## Verification summary

| Area | Result | Priority | Verified finding |
|---|---|---:|---|
| SDK v1 job results | FAIL | High | The `JobDetails Jupyter widget` link targets the SDK v1 `RunDetails` API, not `JobDetails`. SDK v1 support has ended, and SDK v2 has no direct widget replacement. |
| Metric reference links | FAIL | Medium | Sixteen metric links pin scikit-learn 0.22, and the Spearman link pins SciPy 1.5.2. The URLs return HTTP 200 but aren't fresh. |
| Classification metrics | FAIL | High | The ROC AUC, micro recall, and normalized macro recall explanations contain mathematical errors. |
| Regression metrics | FAIL | High/Medium | MAPE is inaccurately defined, and the RMSLE domain requirements are omitted. Current metric names remain valid. |
| Cumulative gain and lift | FAIL | Medium | The random-model cumulative gain baseline and lift denominator are described incorrectly. |
| Image validation settings | FAIL | High | `box_score_threshold` is an inference output filter, not the control for selecting predictions used in validation metric calculation. |
| Responsible AI workflow | FAIL | High | The article overstates default dashboard generation and doesn't distinguish the integrated AutoML preview workflow from the general SDK/CLI pipeline. |
| Resources and support | FAIL | High | The next step points to an archived SDK v1 repository, and the listed email address couldn't be verified as a supported contact. |
| Product naming | PASS | — | No product rename drift was confirmed. Capitalization is inconsistent but is an editorial issue. |
| Relative links | PASS | — | All five checked repository-relative links exist. |

> A URL returning HTTP 200 doesn't establish freshness. The old scikit-learn and SciPy pages still resolve, and the archived GitHub repository remains reachable, but these resources aren't current guidance.

## Prioritized recommendations

1. **APPLY TO ARTICLE** — Replace `JobDetails Jupyter widget` with current job-result guidance. The linked type is SDK v1 `RunDetails`; Azure Machine Learning SDK v1 was deprecated on 2025-03-31, and support ended on 2026-06-30. SDK v2 has no direct `RunDetails` widget replacement. Direct readers to Azure Machine Learning studio, `MLClient.jobs.get`, and/or MLflow tracking.
1. **APPLY TO ARTICLE** — Correct the classification metric explanations:
   - Describe ROC AUC only through its ranking-probability interpretation. Don't characterize it as the proportion of examples correctly classified.
   - Remove false positives from both `recall_score_micro` descriptions. Recall uses the denominator TP + FN.
   - Don't claim `norm_macro_recall` is always in [0, 1]. Its normalization can produce a value below 0 when recall is worse than random; random performance maps to 0, and perfect performance maps to 1.
   - Replace configuration wording about manually specifying a “true class” with the current SDK v2 `positive_label` property, which identifies the positive label for binary metrics.
1. **APPLY TO ARTICLE** — Correct the regression metric guidance. Define MAPE as mean absolute relative error and warn that zero or near-zero targets can produce undefined or extreme values. State that RMSLE requires nonnegative targets and predictions. Keep the current metric names; no metric-name deprecation was verified.
1. **APPLY TO ARTICLE** — Correct cumulative gain and lift. A random model's cumulative gain follows `y = x`; it isn't always 1. Describe lift as cumulative gain divided by the random-model cumulative gain at the same sampled-population fraction, producing a random baseline of 1.
1. **APPLY TO ARTICLE** — Reframe `box_score_threshold` as an inference output filter. Explain validation behavior using the current `validation_metric_type` and `validation_iou_threshold` settings.
1. **APPLY TO ARTICLE** — Correct the Responsible AI behavior. In the integrated preview AutoML workflow, the user selects **Explain best model** for a new AutoML job; the dashboard is created only for that job's best recommended model and can't be generated for an existing AutoML model through that integrated workflow. Distinguish this behavior from the general SDK/CLI Responsible AI pipeline, whose `task_type` supports classification, regression, and forecasting. Don't state broadly that all Responsible AI dashboards are limited to classification and regression.
1. **APPLY TO ARTICLE** — Replace the archived `Azure/MachineLearningNotebooks` next step with maintained `Azure/azureml-examples` content and current Learn AutoML/configuration guidance. Remove `askautomatedml@microsoft.com` or replace it with an official Azure support route; the address appears only in this article and couldn't be verified as supported.
1. **APPLY TO ARTICLE** — Replace the 16 scikit-learn 0.22 metric links and the SciPy 1.5.2 Spearman link with stable API URLs. At verification, the current stable releases were scikit-learn 1.9.0 and SciPy 1.18.1. These are documentation-version pins, not runtime dependency pins: the article contains no package installation command or package-version pin.
1. **APPLY TO ARTICLE** — Standardize `automated machine learning`, `Automated ML`, and `AutoML` capitalization according to context. Keep the current product names: Azure Machine Learning, Azure Machine Learning studio, and automated machine learning/Automated ML.

## Missing or unverified information

The following implementation-specific statements need authoritative implementation evidence or product-owner confirmation before revision:

- The exact `weighted_accuracy` formula.
- Whether AutoML clips R2 at -1.
- The exact regression and forecasting normalization implementation, including a complete macro/micro aggregation table.
- Forecast-horizon limits and fold-display behavior.
- The residual sign convention.
- Exact image logging and studio UI behavior.
- Image AutoML lifecycle status; available information is conflicting or stale.
- The complete model-explanation exclusion list.

## Link and source verification

The following relative links were checked and exist:

- `how-to-responsible-ai-insights-ui.md`
- `how-to-use-automated-ml-for-ml-models.md`
- `how-to-configure-auto-train.md`
- `reference-automl-images-hyperparameters.md`
- `how-to-responsible-ai-insights-sdk-cli.md`

## Authoritative sources

- Azure Machine Learning SDK v1 migration and end-of-support dates: [Migrate from SDK v1 to SDK v2](https://learn.microsoft.com/azure/machine-learning/how-to-migrate-from-v1).
- Current local-run alternatives and MLflow guidance: [Migrate local runs from SDK v1 to SDK v2](https://learn.microsoft.com/azure/machine-learning/migrate-to-v2-local-runs).
- Current SDK v2 classification job contract, including `positive_label`: [Azure SDK for Python `classification_job.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ml/azure-ai-ml/azure/ai/ml/entities/_job/automl/tabular/classification_job.py).
- Stable scikit-learn metric API references: [Metrics and scoring](https://scikit-learn.org/stable/api/sklearn.metrics.html) and [scikit-learn release history](https://scikit-learn.org/stable/whats_new.html).
- Stable SciPy Spearman API reference and release history: [`scipy.stats.spearmanr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) and [SciPy news](https://scipy.org/news/).
- Current image setting definitions: [Azure SDK for Python `image_model_settings.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ml/azure-ai-ml/azure/ai/ml/entities/_job/automl/image/image_model_settings.py) and [AutoML image hyperparameters](https://learn.microsoft.com/azure/machine-learning/reference-automl-images-hyperparameters).
- Integrated AutoML workflow: [Train models with automated machine learning](https://learn.microsoft.com/azure/machine-learning/how-to-use-automated-ml-for-ml-models).
- General Responsible AI SDK/CLI pipeline: [Generate Responsible AI insights with YAML and Python](https://learn.microsoft.com/azure/machine-learning/how-to-responsible-ai-insights-sdk-cli).
- Repository lifecycle evidence: [Archived Azure/MachineLearningNotebooks](https://github.com/Azure/MachineLearningNotebooks) and [maintained Azure/azureml-examples](https://github.com/Azure/azureml-examples).
- Repository-local workflow and configuration evidence: `articles/machine-learning/how-to-use-automated-ml-for-ml-models.md`, `articles/machine-learning/how-to-responsible-ai-insights-sdk-cli.md`, `articles/machine-learning/how-to-configure-auto-train.md`, and `articles/machine-learning/reference-automl-images-hyperparameters.md`.

---
_Generated by Doc-Kit Verify (automation)_
