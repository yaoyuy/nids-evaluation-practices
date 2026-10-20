# Coding instrument and decision rules

## 1. What the sheet records

Each study is coded on **18 items in four categories**, plus a free-text `notes` column that records the page on which the judgement rests and, where the judgement turned on a specific sentence, that sentence verbatim.

| Category | Items |
|---|---|
| Bibliographic (4) | study identifier; publication year; venue; dataset identity |
| Dataset practice (4) | dataset version / retrieval date disclosed; dataset currency; partitioning protocol; partitioning reported in reproducible detail |
| Transparency (6) | code availability; hyperparameter disclosure; repeated runs; ablation; computational cost; discussion of leakage risk |
| Reporting (4) | primary metric; accuracy as the only metric; baselines re-run under an identical protocol; class-imbalance handling |

## 2. Three meta-rules that govern the whole scheme

1. **Credit only the authors' own experiment.** A repository link that appears in the reference list, a dataset homepage, or a third-party tool used in preprocessing does not count as code disclosure.
2. **Availability on request is not availability.** Any form of *available upon request* is coded as not available, because the item measures whether a reader can obtain the artefact today, and not whether the authors would comply with a request.
3. **Silence is coded conservatively, and the absence is recorded.** Where the text says nothing, the conservative value is recorded and the absence noted; the likely practice is never inferred from the surrounding literature.

## 3. Operational test for each item

| Item | Value | Operational test |
|---|---|---|
| `dataset_version` | yes / no | yes only if the paper gives a version identifier or a retrieval date for the dataset; a bare dataset name is not enough |
| `dataset_outdated` | yes / no | yes if the **oldest** dataset used was published more than five years before the paper's publication year |
| `split_protocol` | random / temporal / grouped / kfold / unspecified | the protocol the paper documents; `unspecified` when no protocol is documented |
| `split_reported` | yes / no | yes only where a reader could reconstruct the partition: the method, the proportions or fold structure, and - for k-fold cross-validation - whether the folds were random or stratified. A ratio with no method, or a method with no proportions, is coded as not reported. A study that reused an official fixed split file is coded `yes` when it states the composition of those files (file names and record counts), and `unspecified` on `split_protocol`, because the dataset does not document how the files were built |
| `code_public` | yes / no | yes only if the authors provide a clickable link to their **own** code; *available upon request* is no; a dataset homepage or a cited third-party tool is no |
| `hyperparams_public` | yes / partial / no | yes if learning rate, optimiser and network size / architecture are all given; partial if some are given; no if none is. Hyperparameters quoted from a cited paper's own experiment do not count for the citing paper |
| `runs_reported` | yes / no | yes only if dispersion across repeated runs is reported (mean with standard deviation, min-max, or per-seed results). A single number with no dispersion is no; a standard deviation across *different models* is not a repeated run |
| `ablation` | yes / no | yes if a component of the proposed method is added or removed and the effect is measured. Feature-count sweeps, hyperparameter sweeps and comparisons against other published models are **not** ablation |
| `compute_reported` | yes / no | yes if the paper states the hardware used, the training time, or the model size in parameters - any one of the three |
| `leakage_discussed` | yes / no | yes only if the paper raises the risk that records are shared, duplicated or otherwise overlap between training and test data. Mentioning that duplicates were cleaned during preprocessing, without connecting it to the partition, is no |
| `main_metric` | free text | the metric or metrics the main results table reports |
| `only_accuracy` | yes / no | yes if the main results table reports accuracy and no other metric |
| `same_protocol_compare` | yes / no / unclear | yes if the authors themselves re-ran the baselines under the same protocol - either stated explicitly, or evidenced by a table that reports a training time or a per-algorithm evaluation for each competing method; no if the comparison uses numbers cited from other papers; unclear if the comparison is presented without any statement of provenance |
| `imbalance_handled` | yes / no / mentioned | yes if a technique was actually applied (resampling, class weights, cost-sensitive loss); mentioned if class imbalance is acknowledged or recommended as future work but no technique is applied |

## 4. Ambiguities found in the pilot, and how they were resolved

A ratio with no stated partitioning method is coded `unspecified` rather than `random`. A study reusing a dataset's official training and test files is coded `unspecified` on `split_protocol` rather than inheriting the dataset's own protocol. Feature-selection comparisons, hyperparameter sweeps and cross-model comparisons are not coded as ablation.

## 5. Reliability of the coding

The review has a single author, so no inter-coder agreement statistic exists and none is reported. What is reported is **intra-coder consistency**: ten coded studies were re-coded on a second pass within the same coding session and without access to the original sheet, and the second-pass codes were committed to file before the original codes were opened. Agreement was **90.7% (127 of 140 decisions)** over the fourteen items that require reading the full text, with a **mean item-level Cohen's kappa of 0.827**. Eight items reached kappa = 1.000; hyperparameter disclosure reached 0.846 and dataset identity 0.778; the partitioning protocol, its reporting detail and dataset currency each reached 0.615; same-protocol comparison reached 0.103. The values are computed against the sheet as it stood before the thirteen disagreements were adjudicated; adjudication altered one of them.

Because same-protocol comparison was unreliable at the level of single-paper judgement, all 93 studies were subsequently re-examined for that item in a dedicated full-corpus pass, in which the reference list was truncated away before searching so that citations could not be mistaken for the authors' own experiments. That pass changed five codes, all in the direction of under-recognition.

## 6. Drift check

The 93 studies were divided into three consecutive blocks of 31 in coding order and each of the thirteen categorical items was compared between the first and the third block. Nine items did not move by ten percentage points or more on any value; four did (repeated runs, ablation, class-imbalance handling and same-protocol comparison), in every case toward recording the practice more often in the later block. Restricting the comparison to studies published in 2024-2025 removes the shift for ablation but leaves it in place for same-protocol comparison.