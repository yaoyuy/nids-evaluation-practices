# Evaluation practices in deep learning for network intrusion detection (2019-2025)

Supplementary material and analysis code for the systematic review

**Evaluation Practices in Deep Learning for Network Intrusion Detection: A Systematic Audit of Dataset Reuse, Splitting Protocols, and Reproducibility (2019-2025)**

Xiangyu He, School of Artificial Intelligence, Mianyang City College, Mianyang, Sichuan, China

---

## What is in this repository

| Path | What it contains |
|---|---|
| `coding-sheet.csv` | The coding sheet for all 93 coded studies. Columns: `paper_id`, 17 coded items, and a free-text `notes` column. Each note records the page on which the judgement rests and, where the judgement turned on a specific sentence, that sentence verbatim. |
| `coding-rules.md` | The coding instrument: the 18 items, the operational test applied to each, the three meta-rules that governed the whole scheme, the categories of evidence that were explicitly rejected, and the reliability and drift checks. |
| `search-queries.md` | The exact OpenAlex filter strings that were executed, with the date and the document-type, language and date restrictions. |
| `screening-rules.md` | Eligibility criteria, the deterministic screening rules and their outcome counts, the sampling procedure, and the order of preference used for full-text retrieval. |
| `prisma-record.csv` | The PRISMA record of the records excluded by hand, with the reason for each. |
| `download-log.csv` | One row per sampled record: retrieval status, byte count, DOI, venue, year, title and the URL used. |
| `code/` | The scripts that performed retrieval, screening, sampling, coding input, analysis, figure generation, the controlled verification experiment, and the citation-snowballing coverage check. |
| `results/` | Machine-readable output: the controlled experiment (`verification-results.json`), the full cross-tabulation set (`cross-tabulations.md`), the value check (`coding-sheet-check.txt`), Supplementary Table S1 (all pairwise association tests with the sparsity check), and the citation-snowballing summary. |
| `figures/` | The six manuscript figures at 600 dpi. |

## Reproducing the review

The stages run in this order, from `code/`:

1. `s1-retrieval-openalex.py` - executes the two queries and writes the raw candidate set.
2. `s2-screening.py` - applies the deterministic screening rules and writes the include / maybe / exclude split.
3. `s3-sampling.py` - draws the random sample with seed 20261018 and writes the download list.
4. `s4-coding-input.py` - builds the compact per-paper coding input used to read each full text.
5. `analysis-statistics.py` - builds every frequency table, cross-tabulation and test reported in the Results.
6. `figures-main.py` - draws Figures 1-5.
7. `verification-experiment.py` - runs the controlled partitioning experiment on NSL-KDD and UNSW-NB15 (124 fits) and writes `results/verification-results.json`.
8. `figures-verification.py` - draws Figure 6 from that output.
9. `snowball-retrieval.py` and `snowball-screening.py` - the citation-snowballing coverage check of Section 3.9.

The scripts expect a `data/` directory holding the retrieved records and the two benchmark datasets, and write into `output/`. Paths are resolved relative to each script's own location.

## Notes on the data

- The verification experiment downloads or expects two benchmark datasets: NSL-KDD (`KDDTrain+` and `KDDTest+`) and the 175,341-record UNSW-NB15 file. The official 82,332-record UNSW-NB15 test partition could not be retrieved from the provider and is not used; all UNSW-NB15 results are computed within the single distributed file (article, Limitations).
- The coding sheet contains no personal data and no third-party text beyond short verbatim quotations used as coding evidence.
- The scripts were written for Python 3.10 with scikit-learn 1.7.2, PyTorch 2.5.1, pandas 2.3.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9 and python-docx.
- No credentials, tokens or account details are included anywhere in this repository.

## Licence

- Code (`code/`): MIT, see `LICENSE`.
- Data, derived results and figures (`coding-sheet.csv`, `prisma-record.csv`, `download-log.csv`, `results/`, `figures/`): Creative Commons Attribution 4.0 International (CC BY 4.0).

## Citation

Cite the article once published. This repository is archived at Zenodo under DOI 10.5281/zenodo.23491180 (concept DOI 10.5281/zenodo.23491179), which is the permanent identifier given in the article's Data availability statement.