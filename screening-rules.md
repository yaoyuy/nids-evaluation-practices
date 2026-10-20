# Eligibility, screening, sampling and retrieval

## 1. Eligibility criteria

A record was eligible if it satisfied **all** of the following:

1. it was an original research article - not a review, survey, editorial, correction or retraction notice;
2. it addressed network intrusion detection on packet- or flow-level traffic;
3. it applied at least one machine learning or deep learning classifier;
4. it evaluated on at least one publicly available benchmark dataset;
5. its full text was retrievable through a legitimate route (section 4).

Records were excluded when they addressed an adjacent but distinct problem - malware classification, phishing detection, spam filtering, ransomware analysis, Android application vetting, or log-based anomaly detection - or when the paper reported no quantitative detection results. Reviews and surveys were excluded because the unit of analysis is the primary study: a review cannot be coded for how its own experiments were partitioned.

## 2. Deterministic screening rules and their order of application

Title-and-abstract screening used machine-readable fields only, in a fixed order, so that the outcome does not depend on the order in which a human happened to read the records. The rules were applied in this order:

| # | Rule | Outcome when it fires | Records |
|---|---|---|---|
| 1 | `E2` non-research item type (editorial, correction, retraction, erratum, book chapter, report) | exclude | 1 |
| 2 | `E1` review vocabulary in the title | exclude | 40 |
| 3 | `E7` off-topic application domain (malware, ransomware, fraud, phishing, spam) | exclude | 58 |
| 4 | `I1-topic` title/abstract is not about intrusion detection | exclude | (part of 113 below) |
| 5 | `I1-method` no machine learning or deep learning method | exclude | 113 |
| 6 | `I3-dataset` no named public benchmark dataset | *maybe* | 438 |
| 7 | `I4-result` no quantitative detection result | *maybe* | 256 |
| - | none of the above fires | include | 1,335 |

**Exclusions total 212** (113 no ML method + 58 off-topic + 40 reviews + 1 non-research item). A record that the rules could not resolve - most often because the abstract named no benchmark dataset or reported no metric - was retained as *maybe* (694 records) rather than excluded, so that no decision depended on a machine judgement in an ambiguous case. *include* plus *maybe* left **2,029** records in the eligible pool.

## 3. Sampling

Coding all 2,029 eligible records was not feasible. Rather than selecting studies by hand, which would invite the objection of selective inclusion, a random sample was drawn with a fixed seed: **180 records from the 2,029 eligible records, using Python 3.10 with seed 20261018**. The sample was drawn larger than the target number of coded studies because full-text availability had to be verified record by record and a substantial fraction was expected to be unretrievable.

## 4. Order of preference for full-text retrieval

1. the publisher's open-access PDF, where the record was flagged as open access;
2. an openly available repository copy deposited by the authors (Unpaywall and Europe PMC were used to locate these);
3. the publisher's landing page, where no direct PDF link was exposed.

No paper was coded from its abstract alone, and no paper was coded from a third-party mirror or an abstract-only record. No shadow-library route was used at any point.

Of the 180 sampled records, full texts were obtained for **91 (50.6%)** and **89 were not retrieved**, predominantly because the publisher blocked automated access or because the record sat behind a subscription without institutional access. Of the 91 retrieved, **6 were excluded on full-text inspection**: 3 proved to be reviews, 2 had been retracted, and 1 reported no experiment on a publicly available benchmark. This left **85 coded studies** from the sample; **8 further studies** had been coded during protocol piloting, giving **93 coded studies** in total.

## 5. Pilot round

Ten studies were coded before the main round, to calibrate the rules and measure the time per study. Eight of them are included in the 93; two were excluded because the institution had no subscription to the publisher and no other lawful route to the full text. The pilot block is not a random draw from the same population, and the article reports the three items on which it differs materially from the sampled block (dataset currency, computational-cost reporting and hyperparameter disclosure) side by side with the pooled figures.