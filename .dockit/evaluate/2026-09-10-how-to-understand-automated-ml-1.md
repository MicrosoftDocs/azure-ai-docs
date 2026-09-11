---
ai-usage: ai-assisted
---

# Evaluation: how-to-understand-automated-ml

**Document:** `articles/machine-learning/how-to-understand-automated-ml.md`  
**Date:** 2026-09-10 09:54  
**Status:** FAIL

The rewrite clears the numeric quality targets, but it doesn't clear the
publication gate. The prompt's evidence says that image AutoML lifecycle status
and exact image metric logging or studio behavior remain unverified, while the
article presents both as facts.

## Scores

| Dimension | Score | Status |
|---|---:|---|
| Technical accuracy | 0.92 | Pass |
| Completeness | 0.88 | Pass |
| Developer experience | 0.90 | Pass |
| Metadata | 1.00 | Pass |
| Links | 1.00 | Pass |
| Accessibility | 0.97 | Pass |
| Style | 0.88 | Needs review |
| **Core rubric overall** | **0.90** | **Pass** |
| **Publication gate** | — | **Fail** |

The core rubric overall is the mean of technical accuracy, completeness, and
developer experience. The publication decision also applies the prompt's
acceptance criteria and high-priority evidence gate.

## Blocking and high-priority findings

### High

- **[Technical accuracy / evidence] Unverified image lifecycle status.** Lines
  390–396 definitively label image model evaluation as preview. The permitted
  verification evidence says image AutoML lifecycle sources are conflicting or
  stale and requires authoritative confirmation before publication. Either
  verify the preview status from an allowed authoritative source or remove the
  unsupported lifecycle claim.
- **[Technical accuracy / evidence] Unverified image logging and UI behavior.**
  Lines 398–399, 405–406, 414–415, and 440–441 state that image metrics are
  recorded at each epoch, identify best-epoch summary results, and name
  per-epoch object-detection metrics. The permitted evidence explicitly lists
  exact image metric logging and studio behavior as unverified. Verify each
  detail or replace it with qualitative wording that doesn't assert unsupported
  implementation behavior.
- **[Style / pattern] H1 conflicts with the declared article type.** Line 17
  starts with the imperative verb “Evaluate,” but the local `concept-article`
  pattern requires a concept H1 such as a noun-phrase concept, “What is …?”, or
  an overview. Align the H1 with the concept pattern, or change the article type
  only if the content owner determines that the article is primarily
  procedural.

## Acceptance criteria

### Technical accuracy

- [x] ROC AUC isn't described as accuracy. Lines 81–87, 96, and 162–177.
- [x] Recall uses `TP + FN`; precision uses `TP + FP`. Lines 102–103.
- [x] Micro recall excludes false positives. Lines 114–117.
- [x] Normalized macro recall can be negative. Lines 122–125.
- [x] MAPE is relative error and warns about zero and near-zero actual values.
  Lines 297–302.
- [x] RMSLE requires nonnegative actual and predicted values. Lines 304–310.
- [x] Cumulative gain and lift baselines are distinct and correct. Lines
  210–250.
- [x] `box_score_threshold` is described only as an inference filter. Line 429.
- [x] Validation behavior uses `validation_metric_type` and
  `validation_iou_threshold`. Lines 430–431.
- [x] Responsible AI dashboard generation isn't described as automatic. Lines
  445–448.
- [x] Integrated and generic Responsible AI workflows are clearly separated.
  Lines 460–466.
- [x] No unsupported SDK v1 widget remains. Lines 71–75; stale-content scans
  found no `azureml.widgets`, `RunDetails`, or `JobDetails`.
- [ ] No unverified implementation detail is presented as fact. Fails at lines
  390–396, 398–399, 405–406, 414–415, and 440–441.

### Completeness

- [x] Readers can choose metrics by scenario. Lines 32–57.
- [x] Metric limitations accompany definitions. Lines 45–57, 79–87, 275–310,
  and the chart “What to watch for” passages.
- [x] Current studio and programmatic job-access paths are discoverable. Lines
  59–75.
- [x] Responsible AI prerequisites appear in a visible callout. Lines 450–458.
- [x] Related content replaces deprecated samples and support contacts. Lines
  470–479; stale-content scans found neither the archived notebook repository
  nor the unsupported mailbox.

### Developer experience and accessibility

- [x] Result types have distinct H2 sections. Lines 77, 273, 390, and 445.
- [x] Metric tables are compact and scannable. Lines 93–106 and 286–295.
- [x] Classification chart guidance isn't repeated. The shared legend guidance
  appears once at lines 157–158.
- [x] Chart headings describe evidence rather than labeling models “good” or
  “bad.” Lines 147–269 and 345–370.
- [x] Every chart has meaningful alt text. All 20 images have nonempty,
  evidence-oriented alt text between 76 and 119 characters.
- [x] Links use descriptive labels. No generic “click here” labels appear.
- [x] Stable documentation URLs replace version-pinned references. No
  scikit-learn `0.22` or SciPy `1.5.2` links remain.

## Supplemental validation

- **Metadata:** All required fields are present. The title is 34 characters, the
  description is 136 characters, `ms.date` uses `MM/DD/YYYY`, and
  `ai-usage: ai-assisted` is present.
- **Links:** All repository-relative files, anchors, and image files resolve.
  The persisted author-run evidence reports that all cited external sources
  resolve. The official Pascal VOC source is the only HTTP URL and doesn't
  support HTTPS.
- **Accessibility:** The article has one H1, sequential heading levels, no empty
  alt text, and descriptive link labels. The repeated “Diagram that shows”
  lead-in is a low-priority screen-reader verbosity issue, not a blocker.
- **Style:** Voice, sentence-case headings, UI formatting, paragraph length, and
  terminology are generally strong. Besides the high-priority H1 pattern issue,
  minor issues include undefined abbreviations in the decision table, “checkboxes”
  instead of “check boxes” at line 69, and “70 percent” instead of `70%` at line
  258.

## Missing information

- Current authoritative lifecycle status for AutoML image model evaluation.
- Current service and studio behavior for per-epoch image metrics and best-epoch
  summary artifacts.
- Current forecast-horizon studio behavior for fold selection, series selection,
  and prediction intervals at lines 374–386. This remains unverified, but the
  permitted evidence doesn't classify it as a high-priority blocker.

---
_Generated by Doc-Kit Evaluate_
