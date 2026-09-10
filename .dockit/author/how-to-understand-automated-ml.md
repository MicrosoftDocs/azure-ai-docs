**Document:** articles/machine-learning/how-to-understand-automated-ml.md
**Stage:** author
**Date:** 2026-09-10T10:09:57.3203124-05:00

## Git diff --stat
```
.../how-to-understand-automated-ml.md              | 557 ++++++++++++---------
 1 file changed, 328 insertions(+), 229 deletions(-)
```

## Author response

node.exe : Warning: Custom agent "Doc-Kit Author" specifies model 
"claude-opus-4.6-1m" which is not available; using "gpt-5.6-sol" instead
At C:\Users\scottpolly\AppData\Roaming\npm\copilot.ps1:24 char:5
+     & "node$exe"  "$basedir/node_modules/@github/copilot/npm-loader.j ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Warning: Custom....6-sol" instead 
   :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
IΓÇÖll load the task prompt, then execute its instructions end to end.

The prompt requires a source-grounded rewrite of the AutoML evaluation article, including structural, technical, accessibility, metadata, and link fixes. IΓÇÖm loading the mandatory content-discovery workflow before editing.

The repository skill loader is unavailable, so IΓÇÖm applying the persisted plan directly. IΓÇÖll verify the cited technical claims in parallel with reading the article and its governing instructions.

The article has no protected or monikered sections. Before rewriting, IΓÇÖm checking current local destinations and loading the code-convention gate because the revision includes SDK properties and hyperparameter identifiers.

The rewrite will remove unsupported and unverifiable implementation details rather than replace them with guesses. IΓÇÖm confirming the maintained local monitoring and Responsible AI links before applying the full structural edit.

IΓÇÖve resolved the maintained local destinations and the authoritative image-hyperparameter definitions. IΓÇÖm now replacing the opening and navigation flow, including current metadata, decision support, and SDK v2/MLflow access.

The opening is updated. To keep the remaining restructuring coherent and avoid leaving duplicated legacy sections, IΓÇÖm replacing the article body as one complete, source-linked document while preserving all relevant chart assets.

The full rewrite is in place with the requested technical corrections, chart interpretation pattern, accessible alt text, and maintained related links. IΓÇÖm moving to the mandatory metadata and prepublication validation gates.

The configured validation skills are unavailable in this runtime, so IΓÇÖm running equivalent repository checks directly: diff integrity, stale-content scans, link and anchor resolution, heading hierarchy, and alt-text constraints.

The structural and diff checks pass; the stale-content scan needs a PowerShell-native rerun because `rg` isnΓÇÖt installed. IΓÇÖm also loading the repositoryΓÇÖs local validation procedures so the unavailable skill wrapper doesnΓÇÖt block the quality gates.

The direct quality gates now pass for diff integrity, structure, local files, alt-text length, required metadata, and stale guidance. IΓÇÖm tightening the remaining style checks, including anchor resolution and external source availability.

All relative anchors and external sources resolve, metadata lengths are valid, and the only HTTP source is the official Pascal VOC site, which doesnΓÇÖt accept HTTPS. IΓÇÖm now running the requested independent quality evaluation against the rewritten article.

The evaluation clears every numeric target but identifies unsupported image lifecycle and logging claims. IΓÇÖm removing those claims and their dependent screenshots instead of inventing replacements; the requested concept title remains unchanged because it is explicitly specified by the improvement plan.

Updated `articles/machine-learning/how-to-understand-automated-ml.md` in place. The article now separates evaluation by result type, corrects metric definitions, removes SDK v1 and unsupported claims, distinguishes Responsible AI workflows, improves chart accessibility, and adds AI-assisted metadata.

**Attribution log**

- `.dockit/orchestrate/how-to-understand-automated-ml/prompt.author.txt` ΓåÆ Adapted the requested hierarchy, metric-selection table, chart explanation pattern, compact metric tables, Related content section, and evidence-oriented headings.
- [scikit-learn ROC metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics) and [`roc_auc_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html) ΓåÆ Paraphrased ROC AUC as a threshold-independent ranking measure and distinguished it from accuracy.
- [scikit-learn precision, recall, and F-measure guidance](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics) ΓåÆ Adapted recall and precision formulas and macro, micro, and weighted averaging explanations.
- [Azure Machine Learning AutoML metrics](https://learn.microsoft.com/azure/machine-learning/how-to-understand-automated-ml#classification-metrics) ΓåÆ Adapted normalized macro recall, cumulative-gain, and lift definitions.
- [scikit-learn MAPE](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html) and [mean squared logarithmic error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_log_error.html) ΓåÆ Paraphrased formulas, zero-value cautions, and nonnegative RMSLE constraints.
- [SciPy `spearmanr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) ΓåÆ Replaced the version-pinned Spearman reference with the stable API reference.
- [SDK v2 `MLClient`](https://learn.microsoft.com/python/api/azure-ai-ml/azure.ai.ml.mlclient), [MLflow metrics guidance](articles/machine-learning/how-to-log-view-metrics.md), and [SDK v1 migration guidance](https://learn.microsoft.com/azure/machine-learning/how-to-migrate-from-v1) ΓåÆ Removed the unsupported `RunDetails` widget and linked current job-access workflows.
- [SDK v2 `ClassificationJob`](https://learn.microsoft.com/python/api/azure-ai-ml/azure.ai.ml.automl.classificationjob) ΓåÆ Replaced ΓÇ£true classΓÇ¥ with **Positive class label** and documented `positive_label`.
- [AutoML image hyperparameters](https://learn.microsoft.com/azure/machine-learning/reference-automl-images-hyperparameters), [COCO evaluation](https://cocodataset.org/#detection-eval), and [Pascal VOC evaluation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/) ΓåÆ Separated `box_score_threshold` inference filtering from `validation_metric_type` and `validation_iou_threshold`.
- [AutoML studio workflow](https://learn.microsoft.com/azure/machine-learning/how-to-use-automated-ml-for-ml-models) and [Responsible AI SDK/CLI workflow](https://learn.microsoft.com/azure/machine-learning/how-to-responsible-ai-insights-sdk-cli) ΓåÆ Paraphrased the integrated workflow prerequisites, non-retroactive behavior, and distinction from the generic pipeline.
- Existing article media ΓåÆ Retained supported evaluation charts, rewrote all remaining alt text, and removed image lifecycle and metric-logging claims that lacked authoritative confirmation.

All relative links and anchors resolve, external citations returned successfully, alt text meets length and punctuation requirements, stale SDK/link terminology is absent, and `git diff --check` passes. Independent evaluation scored technical accuracy `0.92`, completeness `0.88`, developer experience `0.90`, and overall `0.90`; its two remaining unsupported image claims were subsequently removed.
