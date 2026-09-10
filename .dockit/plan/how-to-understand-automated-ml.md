node.exe : Warning: Custom agent "Doc-Kit Plan" specifies model 
"claude-opus-4.6-1m" which is not available; using "gpt-5.6-sol" instead
At C:\Users\scottpolly\AppData\Roaming\npm\copilot.ps1:24 char:5
+     & "node$exe"  "$basedir/node_modules/@github/copilot/npm-loader.j ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Warning: Custom....6-sol" instead 
   :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
IΓÇÖm loading the task prompt now and will execute its instructions as the complete scope.

IΓÇÖve identified this as an improvement-planning task. IΓÇÖm loading the required content-discovery workflow before reviewing the evaluation evidence.

The required skill isnΓÇÖt available to the runtime, so IΓÇÖm proceeding with the repositoryΓÇÖs persisted evaluation and review artifacts as the authoritative evidence.

IΓÇÖm now correlating the scored evaluation, verification record, review summary, and the articleΓÇÖs remaining metric sections so the plan can rank exact fixes rather than restating generic recommendations.

The artifact paths differ from the promptΓÇÖs legacy examples, so IΓÇÖm resolving the actual persisted layout before synthesizing priorities.

The core evidence confirms the 0.68 failure and adds a verified cumulative-gain/lift defect not called out in the expert table. IΓÇÖm checking the execution-review summary and exact regression passages before final prioritization.

# Improvement Plan: Evaluate automated machine learning experiment results

## Overview

**Document:** `articles/machine-learning/how-to-understand-automated-ml.md`  
**Current type:** Concept article  
**`ms.topic`:** `concept-article`  
**Target audience:** Data scientists and machine learning practitioners who need to interpret Azure Machine Learning automated ML results  
**Current score:** 0.68 ΓÇö FAIL  
**Technical accuracy:** 0.64  
**Completeness:** 0.72  
**Developer experience:** 0.68  
**Feature impact:** Major remediation ΓÇö the article contains mathematical errors, unsupported SDK v1 guidance, misleading workflow claims, stale resources, and accessibility weaknesses across several major sections.  
**Estimated authoring effort:** 1.5ΓÇô2 working days, plus product-owner verification for unresolved implementation details.

The articleΓÇÖs primary purpose remains appropriate: help readers evaluate automated ML models by using metrics, charts, and related analysis tools. Retain the current concept-article classification, but make the content easier to scan and ensure every metric definition is mathematically correct.

The execution review scored the original article 66/100 and found no task-blocking defect. However, its proposed rewrite reintroduced the unsupported SDK v1 `RunDetails` widget and treated the metric tables as verified. The later evaluation, source-backed verification, and DataSci guidance supersede those recommendations.

## Goals

1. Correct all mathematically inaccurate metric definitions.
1. Remove unsupported SDK v1 guidance and stale resources.
1. Accurately distinguish integrated AutoML Responsible AI behavior from the generic Responsible AI pipeline.
1. Separate image inference filtering from validation metric configuration.
1. Restructure the article around result types and common evaluation decisions.
1. Improve chart accessibility and interpretation guidance.
1. Avoid publishing unverified Azure Machine Learning implementation details.

## Phase 1: Critical technical corrections

Complete this phase before structural or stylistic work.

### 1. Correct ROC AUC interpretation

**Location:** `## ROC curve` and the classification metric table  
**Priority:** High  
**Problem:** The article says AUC is the proportion of correctly classified samples. That describes accuracy, not ROC AUC.

**Required changes:**

- Define ROC AUC as the area under the receiver operating characteristic curve, which plots true-positive rate against false-positive rate across decision thresholds.
- State that ROC AUC is the probability that a classifier ranks a randomly selected positive sample higher than a randomly selected negative sample.
- Explain that `1.0` represents perfect ranking and `0.5` represents random ranking.
- Explicitly distinguish ROC AUC from accuracy:
  - ROC AUC is a threshold-independent ranking measure.
  - Accuracy is the proportion of correct predictions at a selected operating threshold.
- Note that ROC AUC and PR AUC summarize performance across thresholds, while accuracy, precision, recall, and F1 apply at a selected threshold.

**Sources:**

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html>
- <https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml>

**Acceptance criteria:**

- No sentence equates AUC with the proportion of correctly classified samples.
- The distinction between threshold-independent and threshold-dependent metrics is explicit.

### 2. Correct recall averaging and normalized macro recall

**Location:** `## Classification metrics`, the recall table entry, and `### Binary vs. multiclass classification metrics`  
**Priority:** High  
**Problem:** The micro recall explanation incorrectly includes false positives. The normalized macro recall range incorrectly excludes negative values.

**Required changes:**

- Define recall as:

  `recall = TP / (TP + FN)`

- Explain that false positives don't appear in recall. Keep precision separate:

  `precision = TP / (TP + FP)`

- Define micro recall as:

  `micro_recall = sum(TP) / (sum(TP) + sum(FN))`

- State that micro recall aggregates counts across classes before calculating the result.
- Explain that micro recall gives each sample equal weight, so majority classes can dominate.
- State that micro recall equals overall accuracy in single-label multiclass classification.
- Define macro recall as the unweighted mean of per-class recall:

  `macro_recall = (1 / K) * sum(recall_k)`

- Explain that macro recall treats every class equally, regardless of class support.
- Define normalized macro recall as:

  `normalized_macro_recall = (macro_recall - baseline) / (1 - baseline)`

  where `baseline = 1 / K` for balanced random guessing.
- Correct its interpretation:
  - `1.0` is perfect performance.
  - `0.0` is the random baseline.
  - Values can be negative when performance is worse than the random baseline.
- Replace the documented `[0, 1]` range with wording that permits negative values.

**Sources:**

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html>
- <https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml#classification-metrics>

**Acceptance criteria:**

- False positives appear only in the precision definition, not recall.
- Normalized macro recall explicitly permits negative values.
- Macro, micro, and weighted averaging remain clearly distinguishable.

### 3. Correct MAPE and RMSLE guidance

**Location:** `## Regression/forecasting metrics`  
**Priority:** High for MAPE; medium for RMSLE  
**Problem:** MAPE isn't described as relative error, and RMSLE omits its input domain.

**Required changes:**

- Define MAPE as:

  `MAPE = mean(abs((y_true - y_pred) / y_true))`

- Describe MAPE as the average per-sample absolute error relative to the actual value. Explain that implementations can present the result as a fraction or multiply it by 100 for a percentage.
- Warn that:
  - MAPE is undefined when an actual value is zero.
  - Actual values near zero can make MAPE unstable or extremely large.
  - MAPE is unreliable for target series that pass through or approach zero.
- Define RMSLE as:

  `RMSLE = sqrt(mean((log(1 + y_true) - log(1 + y_pred))^2))`

- State that target and predicted values must be nonnegative.
- Recommend RMSE or MAE when negative values are possible.
- Explain that RMSLE is scale-relative and penalizes underprediction more than equivalent overprediction.

**Sources:**

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html>
- <https://scikit-learn.org/stable/modules/model_evaluation.html#mean-absolute-percentage-error>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml#regression-and-forecasting-metrics>

**Acceptance criteria:**

- MAPE is identified as relative error and includes zero and near-zero warnings.
- RMSLE includes the nonnegative-input constraint and an alternative for negative targets.

### 4. Correct cumulative gain and lift

**Location:** `## Cumulative gains curve` and `## Lift curve`  
**Priority:** High  
**Problem:** The article implies that the random-model cumulative gain denominator is always `1`.

**Required changes:**

- Retain the explanation that random cumulative gain follows `y = x`.
- Define lift at a sampled-population fraction as cumulative gain divided by the random-model cumulative gain at the same fraction.
- State that this calculation produces a random-model lift baseline of `1`.
- Do not say that cumulative gain for the random model itself is always `1`.
- Check examples and chart captions for consistent terminology.

**Acceptance criteria:**

- The article clearly distinguishes the diagonal cumulative-gain baseline from the horizontal lift baseline.
- No text describes random cumulative gain as a constant value.

### 5. Remove the SDK v1 results widget

**Location:** `## View job results`  
**Priority:** High  
**Problem:** The article labels the linked API as `JobDetails`, but it links to SDK v1 `azureml.widgets.RunDetails`. SDK v1 support ended June 30, 2026, and SDK v2 has no direct widget replacement.

**Required changes:**

- Keep Azure Machine Learning studio as the primary job-monitoring workflow.
- Remove the `JobDetails Jupyter widget` bullet and any `RunDetails` example.
- Don't repair or expand the SDK v1 sample recommended by the execution review.
- For programmatic access, link readers to current SDK v2 job access through `MLClient.jobs` and, where relevant, MLflow tracking.
- Add a migration link for readers maintaining SDK v1 implementations.
- Don't imply that SDK v2 provides a replacement notebook widget.

**Sources:**

- <https://learn.microsoft.com/azure/machine-learning/how-to-migrate-from-v1>
- <https://learn.microsoft.com/python/api/azure-ai-ml/azure.ai.ml.mlclient>
- <https://learn.microsoft.com/azure/machine-learning/how-to-track-monitor-analyze-runs>

**Acceptance criteria:**

- No active recommendation uses `azureml.widgets`, `RunDetails`, or the nonexistent `JobDetails` widget.
- The studio path remains complete without requiring SDK access.
- Programmatic guidance points only to current SDK v2 or MLflow documentation.

### 6. Correct Responsible AI dashboard behavior

**Locations:** Introduction and `## Responsible AI dashboard for best recommended AutoML model (preview)`  
**Priority:** High  
**Problem:** The article implies that automated ML generates the dashboard by default and conflates the integrated AutoML experience with the generic Responsible AI SDK/CLI pipeline.

**Required changes:**

- State that the integrated dashboard isn't generated by default.
- Add an important callout that lists the integrated workflow prerequisites:
  - A supported new automated ML classification or regression job.
  - The **Explain best model** option enabled.
  - Suitable compute.
  - The best recommended model from that job.
- Explain that the integrated workflow doesn't retroactively create a dashboard for an existing AutoML model.
- Distinguish this workflow from the generic Responsible AI SDK/CLI pipeline, which users build separately for arbitrary supported models.
- Avoid broadly stating that all Responsible AI dashboards are limited to classification and regression; apply that restriction only to the integrated AutoML workflow.
- Don't claim forecasting support or exclusion beyond what the linked workflow-specific source confirms.

**Sources:**

- <https://learn.microsoft.com/azure/machine-learning/how-to-responsible-ai-dashboard>
- <https://learn.microsoft.com/azure/machine-learning/concept-responsible-ai-dashboard>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml>

**Acceptance criteria:**

- The introduction no longer says or implies that the dashboard appears by default.
- Integrated AutoML behavior and the generic SDK/CLI pipeline are separate concepts.
- The prerequisites are visible in a callout rather than buried in prose.

### 7. Separate image inference filtering from validation metrics

**Location:** `### Object detection and instance segmentation metrics`  
**Priority:** High  
**Problem:** The article treats `box_score_threshold` as if it controls which predictions participate in validation metrics.

**Required changes:**

- Define `box_score_threshold` only as an inference-output filter that removes predicted boxes with confidence below the threshold at prediction time.
- Explain validation behavior using:
  - `validation_metric_type` to select the metric convention, such as COCO or VOC.
  - `validation_iou_threshold` to set the IoU cutoff for counting a detection as correct.
- Keep confidence filtering and validation matching in separate paragraphs or table rows.
- Prefer Microsoft Learn and official COCO or Pascal VOC sources for normative claims.
- Remove Wikipedia and the Medium blog as support for Azure Machine Learning behavior.

**Sources:**

- <https://learn.microsoft.com/azure/machine-learning/reference-automl-images-hyperparameters>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml#object-detection-and-instance-segmentation-metrics>
- <https://cocodataset.org/#detection-eval>

**Acceptance criteria:**

- `box_score_threshold` isn't described as a validation-metric control.
- Validation metric type and validation IoU threshold have distinct, accurate explanations.

### 8. Adopt current positive-label terminology

**Location:** Classification metric table and `### Binary vs. multiclass classification metrics`  
**Priority:** Medium  
**Problem:** The article repeatedly uses ΓÇ£`true` class,ΓÇ¥ which doesn't match current SDK v2 configuration terminology.

**Required changes:**

- Replace ΓÇ£`true` classΓÇ¥ with **positive class label**.
- Name the SDK v2 configuration property `positive_label`.
- Describe all remaining labels as negative for the binary one-vs-rest calculation.
- Explain that selecting a positive class affects binary precision, recall, F1, and related binary metrics.
- Don't use ΓÇ£true classΓÇ¥ to mean the actual ground-truth label elsewhere.

**Sources:**

- <https://learn.microsoft.com/python/api/azure-ai-ml/azure.ai.ml.automl.classificationjob>
- <https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml#binary-vs-multiclass-classification-metrics>

**Acceptance criteria:**

- All binary configuration guidance uses **Positive class label** and `positive_label`.
- Ground truth and positive-label configuration aren't conflated.

## Phase 2: Structure and decision support

### 1. Organize content by result type

**Priority:** High  
**Recommended structure:**

# Evaluate automated machine learning experiment results

## Choose evaluation results

- Compact task-to-result decision table.
- Guidance to use multiple complementary metrics and charts.

## View job results

- Studio procedure.
- Current SDK v2 and MLflow links for programmatic access.

## Evaluate classification results

### Choose classification metrics  
### Classification metric reference  
### Binary and multiclass metrics  
### Confusion matrix  
### Classification curves

- ROC.
- Precision-recall.
- Cumulative gains.
- Lift.
- Calibration.

## Evaluate regression and forecasting results

### Choose regression and forecasting metrics  
### Regression and forecasting metric reference  
### Metric normalization  
### Forecasting aggregation  
### Residuals  
### Predicted versus actual values  
### Forecast horizon

## Evaluate image model results

### Image classification  
### Object detection and instance segmentation

## Use Responsible AI insights

## Related content

This hierarchy groups metrics and charts by user intent while avoiding a flat sequence of unrelated H2 sections.

### 2. Add a compact metric-selection aid

**Priority:** Medium  
**Placement:** After the opening result-type summary

| Scenario | Start with | Complement with | Important caution |
|---|---|---|---|
| Imbalanced classification | Macro recall, balanced accuracy, or PR AUC | Confusion matrix and per-class precision/recall | Accuracy and micro averages can hide minority-class failures. |
| Ranking positive cases | ROC AUC or PR AUC | Threshold-specific precision and recall | AUC doesn't select an operating threshold. |
| Probability quality | Log loss and calibration curve | Accuracy or AUC | A well-calibrated model isn't necessarily accurate. |
| Regression with outliers | MAE or median absolute error | RMSE and residual histogram | RMSE gives large errors more influence. |
| Relative regression error | MAPE only when actual values remain away from zero | MAE or RMSE | Zero and near-zero actual values make MAPE unreliable. |
| Nonnegative, scale-relative targets | RMSLE | RMSE or MAE | RMSLE doesn't support negative targets or predictions. |
| Multiseries forecasting | Macro-normalized metrics | Micro metrics and per-series inspection | High-volume series can dominate micro metrics. |
| Model debugging | Responsible AI insights | Aggregate metrics and charts | The integrated AutoML dashboard has workflow prerequisites. |

Keep the table qualitative. Don't add unverified formulas for Azure Machine Learning aggregation or normalization.

### 3. Simplify metric tables

**Priority:** High

- Use compact columns such as **Metric**, **What it measures**, **When to use it**, **Better value**, and **Reference**.
- Move macro, micro, weighted, and binary variant explanations out of individual table cells into a shared subsection.
- Use descriptive link text, such as ΓÇ£scikit-learn `recall_score` reference,ΓÇ¥ rather than repeated ΓÇ£Calculation.ΓÇ¥
- Preserve exact Azure Machine Learning metric identifiers in code formatting.
- Keep mathematical formulas only where they clarify a known error or decision constraint.

### 4. Standardize chart explanations

**Priority:** Medium

Give each chart the same three-part pattern:

1. **What it shows**
2. **How to read it**
3. **What to watch for**

Move the repeated legend-selection tip to one note before the classification curve subsections. Remove the duplicate tip from each chart.

Replace generic headings such as ΓÇ£good modelΓÇ¥ and ΓÇ£bad modelΓÇ¥ with evidence-oriented headings, for example:

- ΓÇ£ROC curve approaching the upper-left cornerΓÇ¥
- ΓÇ£ROC curve near the random-model baselineΓÇ¥
- ΓÇ£Residual errors concentrated near zeroΓÇ¥
- ΓÇ£Residual errors widely dispersedΓÇ¥
- ΓÇ£Predictions close to the ideal diagonalΓÇ¥
- ΓÇ£Predictions deviating from the ideal diagonalΓÇ¥

## Phase 3: References, accessibility, and maintenance

### 1. Update stale metric links

**Priority:** Medium

- Replace all scikit-learn `0.22` URLs with `/stable/` URLs.
- Replace the SciPy `1.5.2` Spearman URL with its stable API URL.
- Don't replace stale version pins with newer version pins; use stable documentation paths.
- Use descriptive link labels.

Examples:

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html>
- <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html>

### 2. Replace weak image alt text

**Priority:** High

Rewrite every chartΓÇÖs alt text to convey the visual evidence needed to understand the surrounding explanation. Don't repeat the heading or use only ΓÇ£goodΓÇ¥ and ΓÇ£bad.ΓÇ¥

Examples:

- ΓÇ£Confusion matrix with most observations concentrated along the diagonal.ΓÇ¥
- ΓÇ£Confusion matrix with many observations outside the diagonal, indicating frequent class confusion.ΓÇ¥
- ΓÇ£ROC curve approaching the upper-left corner, showing high true-positive and low false-positive rates.ΓÇ¥
- ΓÇ£ROC curve close to the diagonal random-model baseline.ΓÇ¥
- ΓÇ£Residual histogram concentrated near zero with few large errors.ΓÇ¥
- ΓÇ£Predicted-versus-actual trend close to the ideal diagonal across most target values.ΓÇ¥

### 3. Replace deprecated next steps

**Priority:** High

- Remove the archived `Azure/MachineLearningNotebooks` link.
- Remove `askautomatedml@microsoft.com`; the address couldn't be verified as a supported contact.
- Prefer maintained, task-oriented local articles:
  - Configure automated ML training.
  - Create and inspect automated ML jobs in studio.
  - Track and monitor jobs.
  - Generate Responsible AI insights.
- If a sample repository link remains necessary, use maintained `Azure/azureml-examples` content only after confirming the exact destination.
- Use `## Related content` because the section contains multiple links.

### 4. Tighten prose and terminology

**Priority:** Low

- Standardize ΓÇ£scikit-learn.ΓÇ¥
- Use ΓÇ£automated machine learningΓÇ¥ on first mention and ΓÇ£AutoMLΓÇ¥ where the surrounding product documentation uses that abbreviation.
- Use active voice and direct UI instructions.
- Break paragraphs longer than three sentences where practical.
- Replace ΓÇ£true valuesΓÇ¥ with ΓÇ£actual valuesΓÇ¥ in explanatory prose when that improves clarity.
- Define ΓÇ£forecast originΓÇ¥ on first use as the point where predictions begin.
- Preserve meaningful explanations; don't shorten metric definitions until they become ambiguous.

## Claims requiring verification before publication

Do not preserve, remove, or rewrite these claims into new specifics without authoritative implementation evidence or product-owner confirmation:

| Claim | Required action |
|---|---|
| Exact `weighted_accuracy` formula | Describe behavior qualitatively and link to the AutoML metric reference. |
| AutoML clipping of R┬▓ at `-1` | Mark `[TO VERIFY]` or remove the clipping assertion until confirmed. |
| Exact regression and forecasting normalization implementation | Avoid asserting a universal formula unless current product evidence confirms it. |
| Complete forecasting macro/micro assignment table | Verify each metric assignment or replace the table with qualitative guidance. |
| Forecast-horizon point limits and fold-display behavior | Mark `[TO VERIFY]` pending studio or product-owner confirmation. |
| Residual sign convention | Confirm whether the product reports `y_pred - y_true` or `y_true - y_pred`. |
| Exact image metric logging and studio UI behavior | Verify against current service behavior before changing details. |
| Image AutoML lifecycle status | Resolve conflicting preview and general-availability sources before changing status. |
| Complete model-explanation exclusion list | Verify against a current support matrix rather than preserving a potentially stale list. |

## Related articles requiring updates

The remediation is primarily local to this article. Validate linked articles for consistency, but don't broaden the change without evidence.

| Existing article | Relationship | Recommended action | Rationale | Confidence |
|---|---|---|---|---|
| `how-to-use-automated-ml-for-ml-models.md` | Studio workflow and integrated Responsible AI prerequisites | Add link or align wording only if its current **Explain best model** instructions conflict | This article should defer procedural details to the studio how-to. | High |
| `how-to-configure-auto-train.md` | SDK v2 AutoML configuration | Add link; no substantive rewrite expected | It is the appropriate destination for current SDK configuration, including `positive_label`. | High |
| `how-to-track-monitor-analyze-runs.md` | Current job monitoring | Add link | Replaces the unsupported SDK v1 widget as programmatic monitoring guidance. | High |
| `how-to-responsible-ai-insights-sdk-cli.md` | Generic Responsible AI pipeline | Add a clearly labeled link | Readers need to understand that this pipeline differs from the integrated AutoML workflow. | High |
| `how-to-responsible-ai-insights-ui.md` | Responsible AI UI workflow | Verify scope and prerequisites | Prevent conflicting classification, regression, or forecasting claims. | Medium |
| `reference-automl-images-hyperparameters.md` | Image metric configuration reference | Add or retain links to the exact settings | It is the authoritative local destination for `validation_metric_type`, `validation_iou_threshold`, and `box_score_threshold`. | High |
| Machine learning TOC | Discoverability | No change expected | The articleΓÇÖs title and placement remain suitable; restructuring is internal. | Medium |

## Resource requirements

### Source verification

- Current AutoML metrics documentation.
- Stable scikit-learn metric references.
- Stable SciPy Spearman reference.
- SDK v2 `MLClient.jobs` reference.
- SDK v1-to-v2 migration guidance.
- Current AutoML image hyperparameter reference.
- Integrated AutoML and generic Responsible AI workflow documentation.
- Maintained `Azure/azureml-examples` destination, if retained.

### Visual assets

- Rewrite alt text for every existing chart.
- Don't add navigation screenshots solely because the older execution review recommended them. First verify that screenshots provide durable value and reflect the current studio interface.
- If screenshots are added, capture the **Jobs**, **Models**, and **Metrics** views and provide task-oriented alt text.

### Code samples

No new executable code sample is required for this concept article. Link to current SDK v2 job-access documentation instead of embedding a replacement for the SDK v1 widget. If authoring later adds code, validate it against current SDK v2 signatures and repository code-sample conventions before publication.

## Validation checklist

### Technical accuracy

- [ ] ROC AUC isn't described as accuracy.
- [ ] Recall uses `TP + FN`; precision uses `TP + FP`.
- [ ] Micro recall excludes false positives.
- [ ] Normalized macro recall can be negative.
- [ ] MAPE is relative error and warns about zero and near-zero actual values.
- [ ] RMSLE requires nonnegative actual and predicted values.
- [ ] Cumulative gain and lift baselines are distinct and correct.
- [ ] `box_score_threshold` is described only as an inference filter.
- [ ] Validation behavior uses `validation_metric_type` and `validation_iou_threshold`.
- [ ] Responsible AI dashboard generation isn't described as automatic.
- [ ] Integrated and generic Responsible AI workflows are clearly separated.
- [ ] No unsupported SDK v1 widget remains.
- [ ] No unverified implementation detail is presented as fact.

### Completeness

- [ ] Readers can choose metrics by scenario.
- [ ] Metric limitations accompany definitions.
- [ ] Current studio and programmatic job-access paths are discoverable.
- [ ] Responsible AI prerequisites appear in a visible callout.
- [ ] Related content replaces deprecated samples and support contacts.

### Developer experience and accessibility

- [ ] Result types have distinct H2 sections.
- [ ] Metric tables are compact and scannable.
- [ ] Classification chart guidance isn't repeated.
- [ ] Chart headings describe evidence rather than labeling models ΓÇ£goodΓÇ¥ or ΓÇ£bad.ΓÇ¥
- [ ] Every chart has meaningful alt text.
- [ ] Links use descriptive labels.
- [ ] Stable documentation URLs replace version-pinned references.

## Success metrics

- **Technical accuracy:** Re-evaluation score of at least `0.90`, with no high-priority metric, SDK lifecycle, Responsible AI, or image-validation findings.
- **Completeness:** Score of at least `0.85`, including metric-selection guidance and explicit limitations.
- **Developer experience:** Score of at least `0.85`, with result-type grouping and accessible chart descriptions.
- **Overall:** Score of at least `0.88`.
- **Freshness:** No active SDK v1 guidance, archived notebook links, unverified support mailbox, scikit-learn `0.22` links, or SciPy `1.5.2` links.
- **Verification:** All relative links resolve, every changed mathematical claim matches its cited source, and unresolved implementation-specific claims are removed or marked `[TO VERIFY]`.

## Authoring sequence

1. Apply all Phase 1 correctness fixes without restructuring unrelated content.
1. Resolve or remove unverified implementation-specific claims.
1. Reorganize the corrected content by result type.
1. Add the metric-selection decision aid and simplify tables.
1. Rewrite chart headings, interpretation patterns, and alt text.
1. Refresh links and replace deprecated next steps.
1. Run technical-accuracy, completeness, developer-experience, metadata, link, accessibility, and style validation.
1. Re-evaluate the article and require all high-priority findings to be closed before publication.


